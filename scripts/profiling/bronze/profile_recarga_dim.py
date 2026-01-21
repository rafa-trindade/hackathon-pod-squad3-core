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

path_parquet_glob = "s3://lake/bronze/recarga_dim/*.parquet"

md_file = init_md_report(
    report_filename="bronze_recarga_dim_multi_profiling.md",
    dataset_name="bronze/recarga_dim",
    layer="bronze"
)

con = get_duckdb_connection(memory_limit="6GB", threads=5)
files = con.execute(f"SELECT file FROM glob('{path_parquet_glob}')").df()['file'].tolist()

# %% 
# PROCESSAMENTO DOS ARQUIVOS #####################
##################################################

for file_path in files:
    file_name = file_path.split('/')[-1]
    md = f"## 📄 Arquivo: `{file_name}`\n\n"

    # 1. VOLUMETRIA (Ajustado para read_parquet)
    total_registros = con.execute(f"SELECT COUNT(*) FROM read_parquet('{file_path}')").fetchone()[0]
    df_schema = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{file_path}')").df()
    
    md += f"#### 📦 Volumetria - `{file_name}`\n\n"
    md += f"| Arquivo | Registros | Colunas |\n| :--- | :--- | :--- |\n| {file_name} | {total_registros:,} | {len(df_schema)} |\n".replace(",", ".")
    print_and_save_md(md, md_file)

    md+= "---"

    # 2. AMOSTRA DE DADOS (HEAD 20) 
    md = f"#### 🔍 Amostra de Dados (Head 20)  - `{file_name}`\n\n"
    df_head = con.execute(f"SELECT * FROM read_parquet('{file_path}') LIMIT 20").df()
    md += df_head.to_markdown(index=False)
    print_and_save_md(md, md_file)

    md+= "---"

    # 3. ESTATÍSTICAS E TIPAGEM (MODELO COMPLETO)
    md = f"#### 📊 Estatísticas e Tipagem  - `{file_name}`\n\n"
    dict_types = dict(zip(df_schema['column_name'], df_schema['column_type']))
    selects = []

    for col in df_schema["column_name"].tolist():
        selects.append(f"""
            SELECT
                '{col}' AS coluna,
                '{dict_types[col]}' AS tipo,
                COUNT(DISTINCT "{col}") AS distintos,
                COUNT(*) FILTER (WHERE "{col}" IS NULL) AS nulos,
                ROUND(COUNT(DISTINCT "{col}") * 100.0 / {total_registros}, 2) || '%' AS pct_distintos,
                ROUND(COUNT(*) FILTER (WHERE "{col}" IS NULL) * 100.0 / {total_registros}, 2) || '%' AS pct_nulos,
                CASE
                    WHEN COUNT(DISTINCT "{col}") <= 0.001 * {total_registros} THEN 'BAIXA'
                    WHEN COUNT(DISTINCT "{col}") <= 0.05 * {total_registros} THEN 'MEDIA'
                    ELSE 'ALTA'
                END AS cardinalidade
            FROM read_parquet('{file_path}')
        """)

    df_stats = con.execute(" UNION ALL ".join(selects)).df()
    md += df_stats.to_markdown(index=False)
    print_and_save_md(md, md_file)

    md+= "---"

print(f"🏁 Profiling finalizado: {md_file}")