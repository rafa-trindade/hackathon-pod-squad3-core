# %%
# PATH SETUP #####################################
##################################################
from pathlib import Path
import sys
import pandas as pd
from datetime import datetime

PROJECT_ROOT = Path().resolve()
while PROJECT_ROOT.name != "scripts":
    PROJECT_ROOT = PROJECT_ROOT.parent
PROJECT_ROOT = PROJECT_ROOT.parent 

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
md = "## ⚙️ Sumário Técnico do Dataset\n\n"

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
md += f"- **Grão Definido:** `num_cpf, safra, prod`\n\n"

# %% 
# 🎯 BLOCO 2: ANÁLISE DO TARGET (FPD RATE) ##########
#############################################################
md += "## 🎯 Distribuição da Variável Alvo (Target)\n\n"

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
md += "\n\n"

# %% 
# 🔑 VALIDAÇÃO DE UNICIDADE (PRIMARY KEY) ###########
####################################################
chave_tecnica_cols = ["num_cpf", "safra", "prod"]
md += "### 🔑 Verificação de Chave Técnica\n"

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
md += "\n\n"

# %% 
# 🔍 BLOCO 3: PERFIL DE MISSINGS                   ##########
#############################################################
md += "## 🔍 Perfil de Missings por Feature (Ordem Oficial do Banco)\n\n"

df_order = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{path_parquet}')").df()[['column_name', 'column_type']]

df_stats_raw = con.execute(f"SUMMARIZE SELECT * FROM read_parquet('{path_parquet}')").df()

df_stats = pd.merge(df_order, df_stats_raw, on='column_name', how='left')

col_nulo = 'null_percentage' if 'null_percentage' in df_stats.columns else 'null_ratio'
df_stats['pct_missing_val'] = df_stats[col_nulo] * (100.0 if col_nulo == 'null_ratio' else 1.0)
df_stats['pct_missing'] = df_stats['pct_missing_val'].round(2).astype(str) + '%'

md += df_stats[['column_name', 'column_type_x', 'pct_missing']].rename(columns={'column_type_x': 'column_type'}).to_markdown(index=False)
md += "\n\n"

# %% 
# 🚩 BLOCO 4: DETECÇÃO DE OUTLIERS (3 SIGMA) ###############
#############################################################
md += "## 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ)\n\n"

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

md += "\n\n"

# %% 
# 📦 BLOCO 5: VOLUMETRIA E PARTICIONAMENTO ##################
#############################################################
md += "## 📦 Volumetria de Armazenamento por Partição (Safra)\n\n"

df_vol = con.execute(f"""
    WITH size_meta AS (
        SELECT 
            regexp_extract(file_name, 'ano_mes=([0-9]+)', 1) as am,
            SUM(total_compressed_size) as bytes
        FROM parquet_metadata('{path_parquet}')
        GROUP BY 1
    ),
    row_meta AS (
        SELECT 
            CAST(ano_mes AS VARCHAR) as am,
            COUNT(*) as rows
        FROM read_parquet('{path_parquet}', hive_partitioning=1)
        GROUP BY 1
    )
    SELECT 
        'ano_mes=' || r.am AS partition_dir,
        r.rows AS row_count,
        ROUND(s.bytes / 1024.0 / 1024.0, 2) AS compressed_mib
    FROM row_meta r
    LEFT JOIN size_meta s ON r.am = s.am
    ORDER BY r.am
""").df()

df_vol["row_count"] = df_vol["row_count"].apply(lambda x: f"{x:,}".replace(",", "."))
md += df_vol.to_markdown(index=False)

# %% 
# FINALIZAÇÃO ####################################
##################################################
print_and_save_md(md, md_file)
print(f"✅ Profiling técnico finalizado!")