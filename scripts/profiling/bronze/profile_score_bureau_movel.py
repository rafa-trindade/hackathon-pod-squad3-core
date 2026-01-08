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

BRONZE_BASE_PATH = "s3://lake/bronze/score_bureau_movel"

con = get_duckdb_connection(
    memory_limit="2GB",
    threads=4
)

latest_run_id = con.execute(f"""
    SELECT MAX(run_id) AS run_id
    FROM read_parquet(
        '{BRONZE_BASE_PATH}/run_id=*/**/*.parquet',
        hive_partitioning=1
    )
""").fetchone()[0]

if latest_run_id is None:
    raise RuntimeError("Nenhuma run_id encontrada na camada Bronze")

print(f"📌 Última run_id encontrada: {latest_run_id}")

path_parquet = (
    f"s3://lake/bronze/score_bureau_movel/"
    f"run_id={latest_run_id}/**/*.parquet"
)

md_file = init_md_report(
    report_filename="bronze_score_bureau_movel_profiling.md",
    dataset_name=f"bronze/score_bureau_movel` - `{latest_run_id}",
    layer="bronze"
)


# %%
# VOLUMETRIA #####################################
##################################################
md = "### 📦 Volumetria: `raw/score_bureau_movel`\n"

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
                    'safra=[^/]+'
                ) AS safra_dir,
                file_name,
                total_compressed_size,
                total_uncompressed_size
            FROM meta
        ),
        base AS (
            SELECT
                safra_dir AS diretorio,
                COUNT(DISTINCT file_name) AS qtd_arquivos,
                SUM(total_compressed_size) AS tamanho_comprimido_bytes,
                SUM(total_uncompressed_size) AS tamanho_descomprimido_bytes
            FROM enriched
            GROUP BY safra_dir
        ),
        registros AS (
            SELECT
                safra,
                COUNT(*) AS qtd_registros
            FROM read_parquet(
                '{path_parquet}',
                hive_partitioning=1
            )
            GROUP BY safra
        ),
        colunas AS (
            SELECT COUNT(*) AS qtd_colunas
            FROM (
                DESCRIBE
                SELECT *
                FROM read_parquet('{path_parquet}')
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
                ON b.diretorio = 'safra=' || CAST(r.safra AS VARCHAR)
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
            FROM (
                SELECT
                    b.qtd_arquivos,
                    r.qtd_registros,
                    c.qtd_colunas,
                    b.tamanho_comprimido_bytes,
                    b.tamanho_descomprimido_bytes
                FROM base b
                LEFT JOIN registros r
                    ON b.diretorio = 'safra=' || CAST(r.safra AS VARCHAR)
                CROSS JOIN colunas c
            )
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
md = "### 🧬 Schema: `raw/score_bureau_movel`\n"

df_schema = con.execute(f"""
    DESCRIBE
    SELECT *
    FROM read_parquet('{path_parquet}')
""").df()

md += df_schema.to_markdown(index=False)

print_and_save_md(md, md_file)



# %%  
# CAMPOS DATE/TIME ###############################
##################################################
md = "### 📅 Campos de Data: `raw/score_bureau_movel`\n"

date_cols_typed = df_schema[
    df_schema["column_type"].str.contains("DATE|TIMESTAMP", case=False, na=False)
]["column_name"].tolist()

date_name_patterns = r"^(?:date|dt|data|dat|hor)"

date_cols_by_name = df_schema[
    df_schema["column_name"].str.contains(date_name_patterns, case=False, na=False)
]["column_name"].tolist()

date_cols_suspect = sorted(
    set(date_cols_by_name) - set(date_cols_typed)
)

# DATAS TIPADAS
md += "#### ✅ Datas com tipagem (DATE / TIMESTAMP)\n"

if not date_cols_typed:
    md += "> ⚠️ Nenhuma coluna DATE ou TIMESTAMP encontrada.\n\n"
else:
    for col in date_cols_typed:
        md += f"**Coluna:** `{col}`\n\n"

        df_datas = con.execute(f"""
            SELECT
                MIN("{col}") AS min_data,
                MAX("{col}") AS max_data
            FROM read_parquet('{path_parquet}')
        """).df()

        md += df_datas.to_markdown(index=False)
        md += "\n\n"

print_and_save_md(md, md_file)


# %% 
# ESTATÍSTICA POR COLUNA #########################
##################################################
md = "### 📊 Estatísticas por Coluna: `raw/score_bureau_movel`\n"

cols = df_schema["column_name"].tolist()
selects = []

total_linhas = con.execute(f"""
    SELECT COUNT(*)
    FROM read_parquet('{path_parquet}')
""").fetchone()[0]

for col in cols:
    selects.append(f"""
        SELECT
            '{col}' AS coluna,
            COUNT(DISTINCT "{col}") AS distintos,
            COUNT(*) FILTER (WHERE "{col}" IS NULL) AS nulos,
            COUNT(*) - COUNT(DISTINCT "{col}") AS duplicados,
            ROUND(COUNT(*) FILTER (WHERE "{col}" IS NULL) * 100.0 / COUNT(*), 2) || '%' AS pct_nulos,
            ROUND((COUNT(*) - COUNT(DISTINCT "{col}")) * 100.0 / COUNT(*), 2) || '%' AS pct_duplicados,
            CASE
                WHEN COUNT(DISTINCT "{col}") <= 0.001 * {total_linhas} THEN 'BAIXA'
                WHEN COUNT(DISTINCT "{col}") <= 0.05 * {total_linhas} THEN 'MEDIA'
                ELSE 'ALTA'
            END AS cardinalidade
        FROM read_parquet('{path_parquet}')
    """)

sql_column_statistics = " UNION ALL ".join(selects)
df_column_statistics = con.execute(sql_column_statistics).df()

md += df_column_statistics.to_markdown(index=False)

print_and_save_md(md, md_file)


# %%  
# DISTRIBUIÇÃO POR VALORES (TOP 10) ##############
##################################################
md = "### 🔟 Distribuição de Valores (Top 10): `raw/score_bureau_movel`\n"

for col in df_column_statistics["coluna"]:
    
    md += f"#### Coluna: `{col}`\n\n"

    df_top10 = con.execute(f"""
        SELECT
            "{col}" AS valor,
            COUNT(*) AS qtd
        FROM read_parquet('{path_parquet}')
        GROUP BY "{col}"
        ORDER BY qtd DESC
        LIMIT 10
    """).df()

    md += df_top10.to_markdown(index=False)
    md+= "\n\n"

print_and_save_md(md, md_file)
