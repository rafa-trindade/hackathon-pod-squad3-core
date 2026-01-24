# %%
# PATH SETUP #####################################
##################################################
from pathlib import Path
import sys
import pandas as pd
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

# %% 
# IMPORTS E CONFIGURAÇÃO #########################
##################################################
from config.data_connections import get_duckdb_connection
from scripts.profiling.utils.profiling_utils import init_md_report, print_and_save_md

GOLD_BASE_PATH = "s3://lake/gold/abt_base_prod"

con = get_duckdb_connection(memory_limit="6GB", threads=5)

# Captura a última run_id
latest_run_id = con.execute(f"""
    SELECT MAX(run_id) AS run_id
    FROM read_parquet('{GOLD_BASE_PATH}/run_id=*/**/*.parquet', hive_partitioning=1)
""").fetchone()[0]

path_parquet = f"{GOLD_BASE_PATH}/run_id={latest_run_id}/**/*.parquet"

md_file = init_md_report(
    report_filename="gold-abt_base_prod-profiling.md",
    dataset_name=f"gold/abt_base_prod` - `{latest_run_id}",
    layer="gold"
)

# %% 
# 🛠️ BLOCO 1: SUMÁRIO TÉCNICO DO DATASET ###################
#############################################################
md = "### ⚙️ Sumário Técnico do Dataset: `abt_base_prod`\n\n"

metrics = con.execute(f"""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT num_cpf) as unique_cpfs
    FROM read_parquet('{path_parquet}')
""").df()

total_rows = metrics['total_rows'].iloc[0]
unique_cpfs = metrics['unique_cpfs'].iloc[0]

md += f"- **Volume de Registros (N):** {total_rows:,}\n".replace(",", ".")
md += f"- **Cardinalidade (CPF):** {unique_cpfs:,}\n".replace(",", ".")
md += f"- **Grão Definido:** `num_cpf, safra, prod`"

print_and_save_md(md, md_file)

# %% 
# 🎯 BLOCO 2: ANÁLISE DO TARGET (FPD RATE) ##########
#############################################################
md = "### 🎯 Distribuição da Variável Alvo (Target): `abt_base_prod`\n\n"

df_target = con.execute(f"""
    SELECT 
        fpd,
        COUNT(*) as frequencia,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) || '%' as percentual
    FROM read_parquet('{path_parquet}')
    GROUP BY 1
    ORDER BY 1
""").df()

md += df_target.to_markdown(index=False)


print_and_save_md(md, md_file)

# %% 
# 🔑 VALIDAÇÃO DE UNICIDADE (PRIMARY KEY) ###########
####################################################
chave_tecnica_cols = ["num_cpf", "safra", "prod"]
md = "### 🔑 Verificação de Chave Técnica: `abt_base_prod`\n"

concat_expression = " || '-' || ".join([f"COALESCE({c}::VARCHAR, 'NULL')" for c in chave_tecnica_cols])

df_unicidade = con.execute(f"""
    SELECT
        distintos_reais AS pk_distintos,
        total_linhas - distintos_reais AS duplicatas_reais,
        ROUND((total_linhas - distintos_reais) * 100.0 / total_linhas, 2) || '%' AS pct_duplicidade
    FROM (
        SELECT 
            COUNT(*) AS total_linhas,
            COUNT(DISTINCT ({concat_expression})) AS distintos_reais
        FROM read_parquet('{path_parquet}')
    )
""").df()

md += df_unicidade.to_markdown(index=False)

print_and_save_md(md, md_file)

# %% 
# 🔍 BLOCO 3: PERFIL DE MISSINGS                   ##########
#############################################################
md = "### 🔍 Perfil de Missings por Feature: `abt_base_prod`\n\n"

df_order = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{path_parquet}')").df()[['column_name', 'column_type']]

df_stats_raw = con.execute(f"SUMMARIZE SELECT * FROM read_parquet('{path_parquet}')").df()

df_stats = pd.merge(df_order, df_stats_raw, on='column_name', how='left')

col_nulo = 'null_percentage' if 'null_percentage' in df_stats.columns else 'null_ratio'
df_stats['pct_missing_val'] = df_stats[col_nulo] * (100.0 if col_nulo == 'null_ratio' else 1.0)
df_stats['pct_missing'] = df_stats['pct_missing_val'].round(2).astype(str) + '%'

md += df_stats[['column_name', 'column_type_x', 'pct_missing']].rename(columns={'column_type_x': 'column_type'}).to_markdown(index=False)

print_and_save_md(md, md_file)

# %% 
# 🚩 BLOCO 4: DETECÇÃO DE OUTLIERS (3 SIGMA) ###############
#############################################################
md = "### 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ): `abt_base_prod`\n\n"

outliers_data = []
# Filtro para analisar apenas colunas de comportamento transacional
numeric_summary = df_stats[
    (df_stats['std'].notnull()) & 
    (df_stats['column_name'].str.startswith(('rec_', 'pag_', 'atr_')))
].copy()

for _, row in numeric_summary.iterrows():
    try:
        avg, std, v_max = float(row['avg']), float(row['std']), float(row['max'])
        limite = avg + (3 * std)
        if v_max > limite and v_max > 0:
            outliers_data.append({
                "Feature": row['column_name'],
                "Max Value": f"{v_max:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "Threshold (3σ)": f"{limite:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "Status": "⚠️ Outlier Detected"
            })
    except: continue

if outliers_data:
    md += pd.DataFrame(outliers_data).to_markdown(index=False)
else:
    md += "* ✅ Nenhuma anomalia crítica detectada nas variáveis comportamentais."


print_and_save_md(md, md_file)

# %%
# VOLUMETRIA #####################################
##################################################
md = "### 📦 Volumetria: `abt_base_prod`\n"

try:
    df_files = con.execute(f"""
        WITH meta AS (
            SELECT
                file_name,
                total_compressed_size,
                total_uncompressed_size
            FROM parquet_metadata('{path_parquet}')
        ),
        enriched AS (
            SELECT
                regexp_extract(
                    file_name,
                    'ano_mes=[^/]+'
                ) AS ano_mes_dir,
                file_name,
                total_compressed_size,
                total_uncompressed_size
            FROM meta
        ),
        base AS (
            SELECT
                ano_mes_dir AS diretorio,
                COUNT(DISTINCT file_name) AS qtd_arquivos,
                SUM(total_compressed_size) AS tamanho_comprimido_bytes,
                SUM(total_uncompressed_size) AS tamanho_descomprimido_bytes
            FROM enriched
            GROUP BY ano_mes_dir
        ),
        registros AS (
            SELECT
                ano_mes,
                COUNT(*) AS qtd_registros
            FROM read_parquet(
                '{path_parquet}',
                hive_partitioning=1
            )
            GROUP BY ano_mes
        ),
        colunas AS (
            SELECT COUNT(*) AS qtd_colunas
            FROM (
                DESCRIBE
                SELECT *
                FROM read_parquet('{path_parquet}', hive_partitioning=1)
            )
        ),
        joined AS (
            SELECT
                b.diretorio,
                b.qtd_arquivos,
                r.qtd_registros,
                c.qtd_colunas,
                b.tamanho_comprimido_bytes,
                b.tamanho_descomprimido_bytes,
                0 AS ordem
            FROM base b
            LEFT JOIN registros r
                ON b.diretorio = 'ano_mes=' || CAST(r.ano_mes AS VARCHAR)
            CROSS JOIN colunas c

            UNION ALL

            SELECT
                'TOTAL' AS diretorio,
                SUM(qtd_arquivos),
                SUM(qtd_registros),
                MAX(qtd_colunas),
                SUM(tamanho_comprimido_bytes),
                SUM(tamanho_descomprimido_bytes),
                1 AS ordem
            FROM base b
            LEFT JOIN registros r
                ON b.diretorio = 'ano_mes=' || CAST(r.ano_mes AS VARCHAR)
            CROSS JOIN colunas c
        )
        SELECT
            diretorio,
            qtd_arquivos,
            qtd_registros AS registros,
            qtd_colunas AS colunas,
            ROUND(tamanho_comprimido_bytes / 1024.0 / 1024.0, 2) AS tamanho_comprimido_mib,
            ROUND(tamanho_descomprimido_bytes / 1024.0 / 1024.0, 2) AS tamanho_descomprimido_mib
        FROM joined
        ORDER BY
            ordem,
            diretorio
    """).df()

    df_files["registros"] = (
        df_files["registros"]
        .fillna(0)
        .astype("int64")
        .apply(lambda x: f"{x:,}".replace(",", "."))
    )

    md += df_files.to_markdown(index=False)

except Exception as e:
    md += f"> ⚠️ Erro ao calcular volumetria física: `{e}`"

print_and_save_md(md, md_file)

# %% 
# FINALIZAÇÃO ####################################
##################################################

print(f"✅ Profiling técnico finalizado!")