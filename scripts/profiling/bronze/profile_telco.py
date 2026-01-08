# %%
# PATH SETUP #####################################
##################################################
from pathlib import Path
import sys

PROJECT_ROOT = Path().resolve()
while PROJECT_ROOT.name != "scripts":
    PROJECT_ROOT = PROJECT_ROOT.parent
PROJECT_ROOT = PROJECT_ROOT.parent 

sys.path.insert(0, str(PROJECT_ROOT))


# %% 
# IMPORTS E CONFIGURAÇÃO #########################
##################################################
from config.data_connections import get_duckdb_connection
from scripts.profiling.utils.profiling_utils import init_md_report, print_and_save_md, df_to_md

BRONZE_BASE_PATH = "s3://lake/bronze/telco"

con = get_duckdb_connection(
    memory_limit="6GB",
    threads=5
)

# Captura a última run_id via Hive Partitioning
latest_run_id = con.execute(f"""
    SELECT MAX(run_id) AS run_id
    FROM read_parquet(
        '{BRONZE_BASE_PATH}/run_id=*/**/*.parquet',
        hive_partitioning=1
    )
""").fetchone()[0]

if latest_run_id is None:
    raise RuntimeError("Nenhuma run_id encontrada na camada Bronze para telco")

print(f"📌 Última run_id encontrada: {latest_run_id}")

path_parquet = (
    f"{BRONZE_BASE_PATH}/"
    f"run_id={latest_run_id}/**/*.parquet"
)

md_file = init_md_report(
    report_filename="bronze_telco_profiling.md",
    dataset_name=f"bronze/telco` - `{latest_run_id}",
    layer="bronze"
)


# %%
# VOLUMETRIA #####################################
##################################################
md = "### 📦 Volumetria: `bronze/telco`\n"

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
# SCHEMA #########################################
##################################################
md = "### 🧬 Schema: `bronze/telco`\n"

df_schema = con.execute(f"""
    DESCRIBE
    SELECT *
    FROM read_parquet('{path_parquet}', hive_partitioning=1)
""").df()

md += df_schema.to_markdown(index=False)

print_and_save_md(md, md_file)



# %%  
# CAMPOS DATE/TIME ###############################
##################################################
md = "### 📅 Range de Datas: `bronze/telco`\n"

date_cols = df_schema[
    df_schema["column_type"].str.contains("DATE|TIMESTAMP", case=False, na=False)
]["column_name"].tolist()

if not date_cols:
    md += "> ⚠️ Nenhuma coluna de data real encontrada.\n\n"
else:
    for col in date_cols:
        md += f"#### Coluna: `{col}`\n"
        res = con.execute(f'SELECT MIN("{col}") as min, MAX("{col}") as max FROM read_parquet("{path_parquet}", hive_partitioning=1)').df()
        md += res.to_markdown(index=False) + "\n\n"

print_and_save_md(md, md_file)


# %% 
# ESTATÍSTICA POR COLUNA (OTIMIZADO E CORRIGIDO) ####
####################################################
import pandas as pd

md = "### 📊 Estatísticas por Coluna: `bronze/telco`\n"

cols = df_schema["column_name"].tolist()

total_registros = con.execute(f'SELECT COUNT(*) FROM read_parquet("{path_parquet}")').fetchone()[0]

aggs = []
for col in cols:
    aggs.append(f'APPROX_COUNT_DISTINCT("{col}") AS "dist_{col}"')
    aggs.append(f'COUNT(*) FILTER (WHERE "{col}" IS NULL) AS "null_{col}"')

print("⏳ Iniciando scan único para estatísticas...")
unified_results = con.execute(f'SELECT {", ".join(aggs)} FROM read_parquet("{path_parquet}")').df()

stats_list = []
for col in cols:
    stats_list.append({
        "coluna": col,
        "distintos": unified_results[f"dist_{col}"].iloc[0],
        "nulos": unified_results[f"null_{col}"].iloc[0]
    })

df_column_statistics = pd.DataFrame(stats_list)

df_column_statistics['duplicados'] = total_registros - df_column_statistics['distintos']

if total_registros > 0:
    df_column_statistics['pct_nulos'] = (df_column_statistics['nulos'] * 100.0 / total_registros).round(2).astype(str) + '%'
    df_column_statistics['pct_duplicados'] = (df_column_statistics['duplicados'] * 100.0 / total_registros).round(2).astype(str) + '%'
else:
    df_column_statistics['pct_nulos'] = '0.0%'
    df_column_statistics['pct_duplicados'] = '0.0%'

def get_cardinality(dist):
    if dist <= 0.001 * total_registros: return 'BAIXA'
    if dist <= 0.05 * total_registros: return 'MEDIA'
    return 'ALTA'

df_column_statistics['cardinalidade'] = df_column_statistics['distintos'].apply(get_cardinality)

md += df_column_statistics.to_markdown(index=False)
print_and_save_md(md, md_file)



# %%  
# DISTRIBUIÇÃO POR VALORES (TOP 10) ##############
##################################################
md = "### 🔟 Distribuição de Valores (Top 10): `bronze/telco`\n"

for col in df_column_statistics["coluna"]:
    
    md += f"#### Coluna: `{col}`\n\n"

    try:
        df_top10 = con.execute(f"""
            SELECT
                CAST("{col}" AS VARCHAR) AS valor,
                COUNT(*) AS qtd
            FROM read_parquet('{path_parquet}', hive_partitioning=1)
            GROUP BY valor
            ORDER BY qtd DESC
            LIMIT 10
        """).df()

        df_top10 = df_top10.fillna("NULL")

        md += df_top10.to_markdown(index=False)
    except Exception as e:
        md += f"> ⚠️ Erro ao calcular distribuição para `{col}`: {e}"
        
    md += "\n\n"

print_and_save_md(md, md_file)