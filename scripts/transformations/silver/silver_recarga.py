import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# ------------------------------------------------------------------
# PATH SETUP
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from config.data_connections import get_duckdb_connection
from scripts.transformations.utils.lake_retention import cleanup_old_runs

# ------------------------------------------------------------------
# CONFIGURAÇÕES DO PIPELINE
# ------------------------------------------------------------------
TABLE_NAME = "recarga"

BRONZE_PATH = f"s3://lake/bronze/{TABLE_NAME}/**/*.parquet"
BRONZE_DIM_PATH = "s3://lake/bronze/recarga_dim/"
RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
SILVER_BASE_PATH = f"silver/{TABLE_NAME}/"
SILVER_PATH = f"s3://lake/{SILVER_BASE_PATH}run_id={RUN_ID}/"

MAX_SILVER_RUNS = int(os.getenv("SILVER_MAX_RUNS", 1))
QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"silver-{TABLE_NAME}_agg-quality.log"

# ------------------------------------------------------------------
# CONFIGURAÇÃO DE SANEAMENTO
# ------------------------------------------------------------------
keys_to_clean = {
    'num_cpf': {
        'replace': [], 
        'default': '0'
    },
    
    'dat_insercao_credito': {
        'replace': [], 
        'default': '1900-01-01'
    },

    'hor_insercao_credito': {
        'replace': [], 
        'default': '00:00:00'
    },
}

def run():
    con = get_duckdb_connection(
        memory_limit="6GB", 
        threads=5
    )

    con.execute("SET preserve_insertion_order = false")
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TABLE_NAME}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🚀 Iniciando Silver: {TABLE_NAME}")
    print(f"🧾 run_id = {RUN_ID}")
    
    initial_count = con.execute(f"SELECT COUNT(*) FROM read_parquet('{BRONZE_PATH}')").fetchone()[0]
    print(f"📥 Registros carregados da Bronze: {initial_count:,}".replace(",", "."))

    # ------------------------------------------------------------------
    # ETAPA 1: Normalização de Chaves
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🔑 Etapa 1: Saneando identificadores e colunas do grão...")
    
    col_types_df = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{BRONZE_PATH}')").df()
    col_types = dict(zip(col_types_df['column_name'], col_types_df['column_type']))

    sql_transform = []
    diff_conditions = []

    for col, config in keys_to_clean.items():
        val_default = config['default']
        target_type = col_types.get(col, 'VARCHAR') 
        blacklist = config['replace'] + ['', 'nan', 'NULL']
        formatted_blacklist = ", ".join([f"'{x}'" for x in blacklist])

        transform_expr = f"""
            (CASE 
                WHEN TRIM({col}::VARCHAR) IN ({formatted_blacklist}) OR {col} IS NULL 
                THEN '{val_default}' 
                ELSE {col}::VARCHAR 
            END)::{target_type}
        """
        sql_transform.append(f"{transform_expr} AS {col}")
        diff_conditions.append(f"SUM(CASE WHEN {col}::VARCHAR IS DISTINCT FROM ({transform_expr})::VARCHAR THEN 1 ELSE 0 END) AS diff_{col}")

    con.execute(f"""
        CREATE TABLE work_db.silver_{TABLE_NAME}_step1 AS
        SELECT 
            * EXCLUDE({', '.join(keys_to_clean.keys())}),
            {', '.join(sql_transform)}
        FROM read_parquet('{BRONZE_PATH}')
    """)
    con.execute("CHECKPOINT work_db")

    # ------------------------------------------------------------------
    # ETAPA 2: Deduplicação
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("💎 Etapa 2: Validando necessidade de deduplicação...")
    
    step1_table = f"work_db.silver_{TABLE_NAME}_step1"
    chave_tecnica_cols = list(keys_to_clean.keys())
    chave_cols_str = ", ".join(chave_tecnica_cols)

    check_duplicados = con.execute(f"SELECT COUNT(*) as total, COUNT(DISTINCT ({chave_cols_str})) as distintos FROM {step1_table}").fetchone()
    qtd_duplicados = check_duplicados[0] - check_duplicados[1]

    if qtd_duplicados > 0:
        print(f"⚠️ Detectados {qtd_duplicados:,} duplicados. Deduplicando...".replace(",", "."))
        con.execute(f"CREATE TABLE work_db.chaves_duplicadas AS SELECT {chave_cols_str} FROM {step1_table} GROUP BY {chave_cols_str} HAVING COUNT(*) > 1")
        con.execute(f"""
            CREATE TABLE work_db.silver_{TABLE_NAME}_step2 AS
            SELECT * FROM {step1_table} t WHERE NOT EXISTS (SELECT 1 FROM work_db.chaves_duplicadas d WHERE {' AND '.join([f't.{c} = d.{c}' for c in chave_tecnica_cols])})
            UNION ALL
            SELECT * EXCLUDE(row_num) FROM (
                SELECT t.*, ROW_NUMBER() OVER(PARTITION BY {", ".join([f"t.{c}" for c in chave_tecnica_cols])} ORDER BY ingestion_ts DESC) as row_num
                FROM {step1_table} t JOIN work_db.chaves_duplicadas d ON {' AND '.join([f't.{c} = d.{c}' for c in chave_tecnica_cols])}
            ) WHERE row_num = 1
        """)
        con.execute("CHECKPOINT work_db")
    else:
        print("✅ Nenhuma duplicata detectada.")
        con.execute(f"CREATE VIEW work_db.silver_{TABLE_NAME}_step2 AS SELECT * FROM {step1_table}")

    # ------------------------------------------------------------------
    # ETAPA 3: Agregação de Dimensões (Enriquecimento)
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🧩 Etapa 3: Agregando dimensões (Enriquecimento)...")

    con.execute(f"""
        CREATE TABLE work_db.silver_{TABLE_NAME}_step3 AS
        SELECT 
            f.*,
            COALESCE(d1.dsc_canal_aquisicao, 'não informado') as dsc_canal_aquisicao,
            COALESCE(d2.dsc_forma_pagamento, 'não informado') as dsc_forma_pagamento,
            
            -- Tratamento para Instituição
            CASE 
                WHEN f.dw_instituicao = '-1' THEN 'não mapeado (código -1)'
                ELSE COALESCE(d3.dsc_instituicao, 'não informado') 
            END as dsc_instituicao,
            
            COALESCE(d4.dsc_plano_tarifacao, 'não informado') as dsc_plano_tarifacao, 
            COALESCE(d5.dsc_plataforma_atu, 'não informado') as dsc_plataforma_atu,
            
            -- Tratamento para Promoção
            CASE 
                WHEN f.cod_promocao = '-1' THEN 'não mapeado (código -1)'
                ELSE COALESCE(d6.dsc_promocao, 'não informado') 
            END as dsc_promocao,
            
            COALESCE(d7.dsc_status_plataforma, 'não informado') as dsc_status_plataforma,
            COALESCE(d8.dsc_tecnologia, 'não informado') as dsc_tecnologia,
            COALESCE(d9.dsc_tipo_credito, 'não informado') as dsc_tipo_credito,
            COALESCE(d10.dsc_tipo_insercao, 'não informado') as dsc_tipo_insercao,
            COALESCE(d11.dsc_tipo_recarga, 'não informado') as dsc_tipo_recarga
        FROM work_db.silver_{TABLE_NAME}_step2 f
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}canal_aquisicao_credito.parquet') d1 ON f.cod_canal_aquisicao = d1.cod_canal_aquisicao
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}forma_pagamento.parquet') d2 ON f.dw_forma_pagamento = d2.dw_forma_pagamento
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}instituicao.parquet') d3 ON f.dw_instituicao = d3.dw_instituicao
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}plano_preco.parquet') d4 ON f.dw_plano_tarifacao = d4.dw_plano_tarifacao
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}plataforma.parquet') d5 ON f.cod_plataforma_atu = d5.cod_plataforma_atu
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}promocao_credito.parquet') d6 ON f.cod_promocao = d6.cod_promocao
        
        -- Adicionado ::VARCHAR nestes dois porque confirmamos que o valor existe no CSV mas deu WARN
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}status_plataforma.parquet') d7 ON f.cod_status_plataforma::VARCHAR = d7.cod_status_plataforma::VARCHAR
        
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}tecnologia.parquet') d8 ON f.cod_tecnologia_dw = d8.cod_tecnologia_dw
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}tipo_credito.parquet') d9 ON f.cod_tipo_credito = d9.cod_tipo_credito
        
        -- Adicionado ::VARCHAR neste porque confirmamos que o valor existe no CSV mas deu WARN
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}tipo_insercao.parquet') d10 ON f.dw_tipo_insercao::VARCHAR = d10.dw_tipo_insercao::VARCHAR
        
        LEFT JOIN read_parquet('{BRONZE_DIM_PATH}tipo_recarga.parquet') d11 ON f.dw_tipo_recarga = d11.dw_tipo_recarga
    """)

    # ------------------------------------------------------------------
    # GERAÇÃO DO LOG DE QUALIDADE (ESTILO DIMENSÕES)
    # ------------------------------------------------------------------
    pair_map = {
        'cod_canal_aquisicao': 'dsc_canal_aquisicao',
        'dw_forma_pagamento': 'dsc_forma_pagamento',
        'dw_instituicao': 'dsc_instituicao',
        'dw_plano_tarifacao': 'dsc_plano_tarifacao',
        'cod_plataforma_atu': 'dsc_plataforma_atu',
        'cod_promocao': 'dsc_promocao',
        'cod_status_plataforma': 'dsc_status_plataforma',
        'cod_tecnologia_dw': 'dsc_tecnologia',
        'cod_tipo_credito': 'dsc_tipo_credito',
        'dw_tipo_insercao': 'dsc_tipo_insercao',
        'dw_tipo_recarga': 'dsc_tipo_recarga'
    }

    now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_content = f"📋 QUALITY REPORT - {TABLE_NAME}_aggregation | RUN: {now_str}\n"
    log_content += "-" * 82 + "\n"
    log_content += f"{'PAREAMENTO (CHAVE -> DESC)':<50} | {'STATUS':<9} | {'NÃO INFORMADOS':<15}\n"
    log_content += "-" * 82 + "\n"

    for key, desc in pair_map.items():
        # O log agora conta apenas o que o seu CASE e o seu JOIN não alcançaram
        missing_count = con.execute(f"""
            SELECT COUNT(*) 
            FROM work_db.silver_{TABLE_NAME}_step3 
            WHERE {desc} = 'não informado'
        """).fetchone()[0]      
        
        status = "WARN" if missing_count > 0 else "PASS"
        log_content += f"{f'{key} -> {desc}':<50} | {status:<9} | {missing_count:,}\n".replace(",", ".")

    log_content += "-" * 82 + "\n"
    log_content += f"Total de Colunas Adicionadas: {len(pair_map)}\n"
    log_content += "-" * 82 + "\n"

    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f:
        f.write(log_content)
    print(log_content)

    # ------------------------------------------------------------------
    # ETAPA 4: Reordenação Chave/Descrição (Pareamento)
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🧹 Etapa 4: Pareando chaves com descrições e limpando schema...")
    
    step3_table = f"work_db.silver_{TABLE_NAME}_step3"
    all_cols = con.execute(f"DESCRIBE {step3_table}").df()['column_name'].tolist()
    
    null_counts = con.execute(f"SELECT {', '.join([f'COUNT({c}) AS {c}' for c in all_cols])} FROM {step3_table}").df()
    cols_to_drop = [col for col in null_counts.columns if null_counts[col][0] == 0]
    cols_remaining = [c for c in all_cols if c not in cols_to_drop]

    ordered_cols = []
    grain_keys = list(keys_to_clean.keys())
    for gk in grain_keys:
        if gk in cols_remaining: ordered_cols.append(gk)
    
    for key, desc in pair_map.items():
        if key in cols_remaining:
            ordered_cols.append(key)
            if desc in cols_remaining:
                ordered_cols.append(desc)

    metadata = ['ingestion_ts', 'run_id', 'ano_mes']
    others = sorted([c for c in cols_remaining if c not in ordered_cols and c not in metadata])
    final_ordered_list = ordered_cols + others + [m for m in metadata if m in cols_remaining]

    final_table = f"work_db.silver_{TABLE_NAME}_final"
    con.execute(f"CREATE TABLE {final_table} AS SELECT {', '.join(final_ordered_list)} FROM {step3_table}")

    final_count = con.execute(f"SELECT COUNT(*) FROM {final_table}").fetchone()[0]
    print(f"🔄 Schema reordenado com sucesso ({len(final_ordered_list)} colunas).")

    # ------------------------------------------------------------------
    # Gravação Parquet (S3)
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print(f"💾 Gravando Silver (Run: {RUN_ID})...")
    con.execute(f"COPY (SELECT * FROM {final_table} ORDER BY ano_mes) TO '{SILVER_PATH}' (FORMAT PARQUET, PARTITION_BY (ano_mes), OVERWRITE_OR_IGNORE 1)")
    
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)

    cleanup_old_runs(bucket="lake", base_path=SILVER_BASE_PATH, max_runs=MAX_SILVER_RUNS, protect_run_id=RUN_ID)
    print(f"🏁 Pipeline {TABLE_NAME} Silver finalizado! Registros: {final_count:,}".replace(",", "."))

if __name__ == "__main__":
    run()