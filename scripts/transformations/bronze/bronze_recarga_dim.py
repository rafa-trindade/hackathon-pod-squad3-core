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

# ------------------------------------------------------------------
# CONFIGURAÇÕES DO PIPELINE
# ------------------------------------------------------------------
TABLE_GROUP = "recarga_dim"
BRONZE_RECARGA_FATO = "s3://lake/bronze/recarga/**/*.parquet"
QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"bronze-{TABLE_GROUP}-quality.log"

DIMENSIONS_CONFIG = {
    "canal_aquisicao_credito": {
        "csv": "BI_DIM_CANAL_AQUISICAO_CREDITO.csv",
        "pk": "cod_canal_aquisicao",
        "sql": """
            TRIM(COD_CANAL_AQUISICAO::VARCHAR) as cod_canal_aquisicao,
            TRIM(LOWER(DSC_CANAL_AQUISICAO::VARCHAR)) as dsc_canal_aquisicao,
            TRIM(COD_TIPO_CREDITO::VARCHAR) as cod_tipo_credito_aquisicao
        """
    },
    "forma_pagamento": {
        "csv": "BI_DIM_FORMA_PAGAMENTO.csv",
        "pk": "dw_forma_pagamento",
        "sql": """
            TRIM(DW_FORMA_PAGAMENTO::VARCHAR) as dw_forma_pagamento,
            TRIM(LOWER(DSC_FORMA_PAGAMENTO::VARCHAR)) as dsc_forma_pagamento,
            TRIM(COD_FORMA_PAGAMENTO::VARCHAR) as desc_cod_forma_pagamento
        """
    },
    "instituicao": {
        "csv": "BI_DIM_INSTITUICAO.csv",
        "pk": "dw_instituicao",
        "sql": """
            TRIM(DW_INSTITUICAO::VARCHAR) as dw_instituicao,
            TRIM(COD_INSTITUICAO::VARCHAR) as cod_instituicao,
            TRIM(LOWER(DSC_INSTITUICAO::VARCHAR)) as dsc_instituicao,
            TRIM(COD_TIPO_INSTITUICAO::VARCHAR) as cod_tipo_instituicao,
            TRIM(LOWER(DSC_TIPO_INSTITUICAO::VARCHAR)) as dsc_tipo_instituicao
        """
    },
    "plano_preco": {
        "csv": "BI_DIM_PLANO_PRECO.csv",
        "pk": "dw_plano_tarifacao",
        "sql": """
            TRIM(DW_PLANO::VARCHAR) as dw_plano_tarifacao,
            TRIM(COD_PLANO_PRECO::VARCHAR) as cod_plano_preco,
            TRIM(LOWER(DSC_PLANO_PRECO::VARCHAR)) as dsc_plano_tarifacao,
            TRIM(COD_TIPO_CLIENTE::VARCHAR) as cod_tipo_cliente,
            TRIM(DW_TIPO_CLIENTE::VARCHAR) as dw_tipo_cliente,
            TRY_CAST(DAT_EFETIVACAO AS DATE) as dat_efetivacao,
            TRIM(LOWER(DSC_PLANO_PRECO_BI::VARCHAR)) as dsc_plano_preco_bi,
            TRIM(LOWER(DSC_GRUPO_PLANO_BI::VARCHAR)) as dsc_grupo_plano_bi,
            TRIM(LOWER(DSC_TIPO_PLANO_BI::VARCHAR)) as dsc_tipo_plano_bi,
            TRIM(LOWER(IND_AMDOCS_PLAT_PRE::VARCHAR)) as ind_amdocs_plat_pre,
            TRIM(COD_TRATAMENTO_ESPECIAL::VARCHAR) as cod_tratamento_especial,
            TRIM(NUM_FRANQUIA_MINUTOS_BI::VARCHAR) as num_franquia_minutos_bi,
            TRIM(NUM_FRANQUIA_REAIS_BI::VARCHAR) as num_franquia_reais_bi,
            TRIM(NUM_FRANQUIA_EVENTOS_BI::VARCHAR) as num_franquia_eventos_bi,
            TRIM(NUM_FRANQUIA_VOLUME_BI::VARCHAR) as num_franquia_volume_bi,
            TRIM(COD_PLANO_COMPONENTE::VARCHAR) as cod_plano_componente,
            TRIM(LOWER(DSC_PLANO_PRECO_UNICO_BI::VARCHAR)) as dsc_plano_preco_unico_bi,
            TRIM(LOWER(DSC_MODALIDADE_PLANO::VARCHAR)) as dsc_modalidade_plano
        """
    },
    "plataforma": {
        "csv": "BI_DIM_PLATAFORMA.csv",
        "pk": "cod_plataforma_atu",
        "sql": """
            TRIM(DSC_PLATAFORMA::VARCHAR) as cod_plataforma_atu,
            TRIM(LOWER(DSC_PLATAFORMA_BI::VARCHAR)) as dsc_plataforma_atu,
            TRIM(columns('COD_GRUPO_PLATAFORMA')::VARCHAR) as cod_grupo_plataforma,
            TRIM(LOWER(columns('DSC_GRUPO_PLATAFORMA')::VARCHAR)) as dsc_grupo_plataforma
        """
    },
    "promocao_credito": {
        "csv": "BI_DIM_PROMOCAO_CREDITO.csv",
        "pk": "cod_promocao",
        "sql": """
            TRIM(COD_PROMOCAO::VARCHAR) as cod_promocao,
            TRIM(LOWER(DSC_PROMOCAO::VARCHAR)) as dsc_promocao,
            TRIM(COD_PROM_GRUPO_CARTAO::VARCHAR) as cod_prom_grupo_cartao,
            TRIM(LOWER(DSC_NOME_PROMOCAO::VARCHAR)) as dsc_nome_promocao,
            TRIM(COD_TIPO_PROMOCAO::VARCHAR) as cod_tipo_promocao,
            VAL_PROMOCAO::DOUBLE as val_promocao,
            TRIM(NUM_CONTA_DEDICADA::VARCHAR) as num_conta_dedicada
        """
    },
    "status_plataforma": {
        "csv": "BI_DIM_STATUS_PLATAFORMA.csv",
        "pk": "cod_status_plataforma",
        "sql": """
            TRIM(COD_STATUS_PLATAFORMA::VARCHAR) as cod_status_plataforma,
            TRIM(LOWER(DSC_STATUS_PLATAFORMA::VARCHAR)) as dsc_status_plataforma,
            TRIM(LOWER(IND_ATIVO::VARCHAR)) as ind_ativo,
            TRIM(COD_STATUS_PLAT_GRP::VARCHAR) as cod_status_plat_grp,
            TRIM(LOWER(IND_STS_PLAT_GRP_ATIVO::VARCHAR)) as ind_sts_plat_grp_ativo
        """
    },
    "tecnologia": {
        "csv": "BI_DIM_TECNOLOGIA.csv",
        "pk": "cod_tecnologia_dw",
        "sql": """
            TRIM(COD_TECNOLOGIA_DW::VARCHAR) as cod_tecnologia_dw,
            TRIM(LOWER(DSC_TECNOLOGIA::VARCHAR)) as dsc_tecnologia
        """
    },
    "tipo_credito": {
        "csv": "BI_DIM_TIPO_CREDITO.csv",
        "pk": "cod_tipo_credito",
        "sql": """
            TRIM(COD_TIPO_CREDITO::VARCHAR) as cod_tipo_credito,
            TRIM(LOWER(DSC_TIPO_CREDITO::VARCHAR)) as dsc_tipo_credito
        """
    },
    "tipo_insercao": {
        "csv": "BI_DIM_TIPO_INSERCAO.csv",
        "pk": "dw_tipo_insercao",
        "sql": """
            TRIM(DW_TIPO_INSERCAO::VARCHAR) as dw_tipo_insercao,
            TRIM(LOWER(DSC_TIPO_INSERCAO::VARCHAR)) as dsc_tipo_insercao
        """
    },
    "tipo_recarga": {
        "csv": "BI_DIM_TIPO_RECARGA.csv",
        "pk": "dw_tipo_recarga",
        "sql": """
            TRIM(DW_TIPO_RECARGA::VARCHAR) as dw_tipo_recarga,
            TRIM(LOWER(DSC_TIPO_RECARGA::VARCHAR)) as dsc_tipo_recarga
        """
    }
}

def run():
    con = get_duckdb_connection()
    con.execute("SET preserve_insertion_order = true")
    
    fato_schema = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{BRONZE_RECARGA_FATO}')").df()
    now_str = datetime.now().strftime('%Y%m%d')
    
    full_log = ""

    for dim_name, config in DIMENSIONS_CONFIG.items():
        print(f"🚀 Processando Dimensão: {dim_name}")
        raw_path = f"s3://lake/raw/{TABLE_GROUP}/{config['csv']}"
        dest_path = f"s3://lake/bronze/{TABLE_GROUP}/{dim_name}.parquet"
        pk = config['pk']

        con.execute(f"CREATE OR REPLACE TABLE temp_dim AS SELECT {config['sql']} FROM read_csv_auto('{raw_path}')")
        
        dim_count = con.execute("SELECT COUNT(*) FROM temp_dim").fetchone()[0]
        
        if pk in fato_schema['column_name'].values:
            target_type = fato_schema.loc[fato_schema['column_name'] == pk, 'column_type'].values[0]
            match_status = "PASS" if target_type in ["VARCHAR", "DATE"] else "FAIL"
        else:
            target_type = "NOT_FOUND"
            match_status = "FAIL"

        # Check Órfãos (Agora o match deve ser PASS sem o LOWER na Fato)
        orphans = con.execute(f"""
            SELECT COUNT(DISTINCT f.{pk}) 
            FROM read_parquet('{BRONZE_RECARGA_FATO}') f
            LEFT JOIN temp_dim d ON f.{pk} = d.{pk}
            WHERE d.{pk} IS NULL AND f.{pk} IS NOT NULL
        """).fetchone()[0]

        res_final = "SUCCESS" if orphans == 0 and match_status == "PASS" else "CHECK_REQUIRED"
        
        full_log += f"\n📋 QUALITY REPORT - {dim_name} | RUN: {now_str}\n"
        full_log += "-" * 82 + "\n"
        full_log += f"{'TESTE':<30} | {'STATUS':<9} | {'OBSERVAÇÃO':<20}\n"
        full_log += "-" * 82 + "\n"
        full_log += f"{'Volumetria Dimensão':<30} | {'INFO':<9} | {dim_count} registros\n"
        full_log += f"{'Chave Técnica':<30} | {'INFO':<9} | {pk}\n"
        full_log += f"{'Match de Tipagem Chave Técnica':<30} | {match_status:<9} | Fato: {target_type} - Dim: {target_type}\n"
        full_log += f"{'Integridade de Chave (Fato)':<30} | {('PASS' if orphans == 0 else 'WARN'):<9} | {orphans} registros órfãos\n"
        full_log += "-" * 82 + "\n"
        full_log += f"Resultado Final: {res_final}\n"
        full_log += "-" * 82 + "\n"

        con.execute(f"COPY (SELECT * FROM temp_dim) TO '{dest_path}' (FORMAT PARQUET)")
        print(f"✅ {dim_name} gravado com sucesso.")

    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f:
        f.write(full_log)
    
    print(full_log)
    print(f"🏁 Pipeline {TABLE_GROUP} finalizado. Relatório salvo em: {QUALITY_REPORT_PATH}")

if __name__ == "__main__":
    run()