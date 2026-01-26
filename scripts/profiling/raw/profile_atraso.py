# %%
# PATH SETUP #####################################
##################################################
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

# %% 
# IMPORTS E CONFIGURAÇÃO #########################
##################################################
from config.data_connections import get_duckdb_connection
from scripts.profiling.utils.profiling_utils import init_md_report, print_and_save_md, df_to_md

path_parquet = "s3://lake/raw/atraso/*.parquet"

md_file = init_md_report(
    report_filename="raw_atraso_profiling.md",
    dataset_name="raw/atraso",
    layer="raw"
)

con = get_duckdb_connection()


# %%  
# VOLUMETRIA #####################################
##################################################
md = "### 📦 Volumetria: `raw/atraso`\n"

try:
    df_files = con.execute(f"""
        SELECT
            COUNT(DISTINCT file_name) AS qtd_arquivos,
            SUM(total_compressed_size) AS tamanho_comprimido_bytes,
            SUM(total_uncompressed_size) AS tamanho_descomprimido_bytes
        FROM parquet_metadata('{path_parquet}')
    """).df()


    df_files["tamanho_comprimido_mib"] = (
        df_files["tamanho_comprimido_bytes"] / 1024 / 1024
    ).round(2)

    df_files["tamanho_descomprimido_mib"] = (
        df_files["tamanho_descomprimido_bytes"] / 1024 / 1024
    ).round(2)


    total_registros = con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{path_parquet}')
    """).fetchone()[0]

    total_colunas = con.execute(f"""
        SELECT COUNT(*) FROM (
            DESCRIBE
            SELECT * FROM read_parquet('{path_parquet}')
        )
    """).fetchone()[0]

    df_files["registros"] = total_registros
    df_files["colunas"] = total_colunas

    df_files["registros"] = (
        df_files["registros"]
        .fillna(0)
        .astype("int64")
        .apply(lambda x: f"{x:,}".replace(",", "."))
    )

    md += df_files[
        [
            "qtd_arquivos",
            "registros",
            "colunas",
            "tamanho_comprimido_mib",
            "tamanho_descomprimido_mib",

        ]
    ].to_markdown(index=False)

except Exception as e:
    md += (
        "> ⚠️ Não há arquivos Parquet disponíveis para análise de volume."
    )

print_and_save_md(md, md_file)



# %% 
# SCHEMA #########################################
##################################################
md = "### 🧬 Schema: `raw/atraso`\n"

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
md = "### 📅 Campos de Data: `raw/atraso`\n"

date_cols_typed = df_schema[
    df_schema["column_type"].str.contains("DATE|TIMESTAMP", case=False, na=False)
]["column_name"].tolist()

date_name_patterns = r"^(?:date|dt|data|dat|safra|hor)"

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
        md += "\n"

# POSSÍVEIS DATAS
md += "#### ⚠️ Possíveis campos de data/hora sem tipagem (inferido pelo nome)\n\n"

if not date_cols_suspect:
    md += "> Nenhuma coluna com nome sugestivo de data encontrada."
else:
    for col in date_cols_suspect:
        md += f"- `{col}`\n"

print_and_save_md(md, md_file)


# %% 
# ESTATÍSTICA POR COLUNA #########################
##################################################
md = "### 📊 Estatísticas por Coluna: `raw/atraso`\n"

cols = df_schema["column_name"].tolist()
selects = []

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
                WHEN COUNT(DISTINCT "{col}") <= 0.001 * {total_registros} THEN 'BAIXA'
                WHEN COUNT(DISTINCT "{col}") <= 0.05 * {total_registros} THEN 'MEDIA'
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
md = "### 🔟 Distribuição de Valores (Top 10): `raw/atraso`\n"

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


# %% 
# STRINGS: MED, MIN, MÁX #########################
##################################################
md = "### 📏 Comprimento de Strings: `raw/atraso`\n"

string_cols = df_schema[
    df_schema["column_type"].str.contains("VARCHAR|STRING", case=False, na=False)
]["column_name"].tolist()

if not string_cols:
    md += "> ⚠️ Nenhuma coluna do tipo STRING ou VARCHAR encontrada.\n"
else:
    for col in string_cols:
        md += f"#### Coluna: `{col}`\n"

        df_str_len = con.execute(f"""
            SELECT
                MIN(LENGTH("{col}")) AS min_len,
                ROUND(AVG(LENGTH("{col}")), 2) AS avg_len,
                MAX(LENGTH("{col}")) AS max_len
            FROM read_parquet('{path_parquet}')
            WHERE "{col}" IS NOT NULL
        """).df()

        md += df_to_md(df_str_len)
        md += "\n\n"
    
print_and_save_md(md, md_file)
