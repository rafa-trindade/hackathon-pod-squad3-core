import streamlit as st
import pandas as pd
import json
import os
import sys
import plotly.graph_objects as go
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.data_connections import get_s3_client
from botocore.exceptions import ClientError

st.set_page_config(page_title="SQUAD•03 - Painel de Observabilidade", layout="wide", initial_sidebar_state="expanded", page_icon="⚙️")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("streamlit/assets/style.css")


st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: flex-end; width: 100%; overflow: hidden; margin-top: 10px; margin-bottom: 20px;">
        <img src="https://i.postimg.cc/dQNRCk8X/Group-4.png" style="width: 100%; object-fit: contain;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)




BUCKET_NAME = os.getenv("S3_BUCKET", "lake")
BASE_PATH = "observability/reports/"

@st.cache_resource
def get_client():
    return get_s3_client()

def list_runs():
    """Lista as runs disponíveis (pastas run_id=...)"""
    s3 = get_client()
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=BASE_PATH, Delimiter='/')
        runs = []
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                folder = prefix['Prefix'].replace(BASE_PATH, "").strip("/")
                if "run_id=" in folder:
                    runs.append(folder.replace("run_id=", ""))
        return sorted(runs, reverse=True)
    except Exception as e:
        st.error(f"Erro ao listar runs no S3: {e}")
        return []

def list_reports(run_id):
    """Lista todos os arquivos JSON dentro de uma run específica."""
    s3 = get_client()
    prefix = f"{BASE_PATH}run_id={run_id}/"
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix)
        files = []
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].endswith('.json'):
                        files.append(obj['Key'])
        return files
    except Exception as e:
        st.error(f"Erro ao listar arquivos da run {run_id}: {e}")
        return []

def load_json_from_s3(key):
    """Carrega um arquivo JSON do S3."""
    s3 = get_client()
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar {key}: {e}")
        return None

def render_timestamp(global_timestamp):

    if not global_timestamp:
        st.caption("\u200B")
        return

    try:
        dt = datetime.fromisoformat(str(global_timestamp).replace("Z", ""))
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        formatted = str(global_timestamp)

    st.caption(f"🕒 Data/Hora da Auditoria: {formatted}")


##################################       
# --- Sidebar ---
##################################   
st.sidebar.title("Painel de Observabilidade")

st.sidebar.write("<hr style='margin-top:30px; margin-bottom:10px;'>", unsafe_allow_html=True)




runs = list_runs()
if not runs:
    st.warning("Nenhuma run encontrada no Lake.")
    st.stop()

selected_run = st.sidebar.selectbox("Selecione a Run (ID)", runs)

all_files = list_reports(selected_run)
if not all_files:
    st.info(f"Nenhum relatório JSON encontrado para a run {selected_run}.")
    st.stop()

categories = {
    "Pipeline Execution": [f for f in all_files if "pipeline_execution" in f.lower()],
    "Profiling": [f for f in all_files if "profiling" in f.lower()],
    "Quality": [f for f in all_files if "quality" in f.lower()],
    "Integrity": [f for f in all_files if "integrity" in f.lower() or "inspect_partition" in f.lower()],
}

category = st.sidebar.selectbox("Categoria de Relatório", list(categories.keys()))
available_reports = categories[category]

if not available_reports:
    st.sidebar.info("Nenhum relatório nesta categoria.")
    st.stop()

order_map = {"gold": 1, "silver": 2, "bronze": 3, "raw": 4}

detected_layers = set()
for f in available_reports:
    normalized_path = f.lower().replace('-', '_')
    path_segments = normalized_path.split('/')
    
    for segment in path_segments:
        if segment in order_map:
            detected_layers.add(segment)
        else:
            file_parts = segment.split('_')
            for fp in file_parts:
                if fp in order_map:
                    detected_layers.add(fp)

layers = sorted(list(detected_layers), key=lambda x: order_map.get(x, 99))

if layers:
    default_index = 0 
    
    selected_layer = st.sidebar.selectbox(
        "Selecione a Camada", 
        layers, 
        index=default_index,
        format_func=lambda x: x.capitalize()
    )
    
    available_reports = [
        f for f in available_reports 
        if f"/{selected_layer}/" in f.lower() or 
           selected_layer in f.lower().split('/')[-1].replace('-', '_').split('_')
    ]
else:
    selected_layer = None

def format_report_name(path):
    filename = path.split("/")[-1].replace(".json", "")
    
    if "integrity" in path.lower() or "inspect_partition" in path.lower():
        name = filename.split('-')[-1] if '-' in filename else filename
        return name.replace("_", " ").capitalize()

    if "-" in filename:
        parts = filename.split("-")
        if len(parts) >= 3:
            return parts[1].lower()
        return parts[-1].lower()
    
    parts = filename.split("_")
    if len(parts) > 2:
        return "_".join(parts[1:-1]).lower()
    
    return filename.lower()

report_options = {format_report_name(f): f for f in available_reports}

if report_options:
    def get_sort_key(name):
        n = name.lower()
        if "gold" in n: return 1
        if "silver" in n: return 2
        if "bronze" in n: return 3
        if "raw" in n: return 4
        return 99

    sorted_display_names = sorted(list(report_options.keys()), key=get_sort_key)

    selected_report_display = st.sidebar.selectbox(
        "Selecione o Relatório", 
        options=sorted_display_names
    )
    selected_report_key = report_options[selected_report_display]
else:
    st.sidebar.warning("Nenhum relatório formatado disponível.")
    st.stop()

st.sidebar.divider()

st.sidebar.markdown(
    """
    <style>
    /* Logo customizado */
    .custom-sidebar-logo {
        position: relative;   /* permite mover com top */
        top: -10px;           /* desloca para cima */
        display: flex;
        justify-content: center;
        margin-bottom: -23px;  /* espaço para itens abaixo */
        z-index: 10;          /* sobreposição */
    }
    .custom-sidebar-logo img {
        max-width: 260px; 
        height: auto;
        border-radius: 7px;
    }
    </style>
    <div class="custom-sidebar-logo">
        <a href="https://github.com/rafa-trindade/hackathon-pod-squad3-core" target="_blank">
            <img src="https://img.shields.io/badge/hackathon--pod--academy-SQUAD•03-731E27?style=for-the-badge&logo=github&logoColor=DAD0D1&logoWidth=40&scale=1" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)



##################################   
# --- Principal ---
##################################   

data = load_json_from_s3(selected_report_key)

integrity_timestamp = None

integrity_files = categories.get("Integrity", [])

if integrity_files:
    integrity_data = load_json_from_s3(integrity_files[0])
    if integrity_data:
        integrity_timestamp = integrity_data.get("timestamp")

if data:

    if category == "Pipeline Execution":

        run_id = data.get("run_id", "N/I")

        st.markdown(
            f"""
            <h3 style="font-weight:semi-bold; display: flex; align-items: center; gap: 8px;">
                Relatório de Execução do Pipeline: 
                <code class="theme-1">{run_id}</code>
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"Caminho no Lake: s3://{BUCKET_NAME}/{selected_report_key}")
        st.divider()
        render_timestamp(integrity_timestamp)

        if "steps" in data:
            df_steps = pd.DataFrame(data["steps"])

            column_mapping = {
                "step": "Etapa",
                "status": "Status",
                "duration": "Duração",
            }
            
            df_steps = df_steps.rename(columns=column_mapping)

            def dur_to_sec(ts):
                if ":" not in str(ts): return 0
                try:
                    h, m, s = map(int, ts.split(':'))
                    return h * 3600 + m * 60 + s
                except:
                    return 0

            def format_hhmmss(total_seconds):
                total_seconds = int(total_seconds)
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                segundos = total_seconds % 60
                return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

            def detect_layer(step_name):
                s = str(step_name).upper()
                if "RAW" in s: return "RAW"
                if "BRONZE" in s: return "BRONZE"
                if "SILVER" in s: return "SILVER"
                if "GOLD" in s: return "GOLD"
                return "OTHER"

            df_steps["Segundos"] = df_steps["Duração"].apply(dur_to_sec)
            df_steps["Layer"] = df_steps["Etapa"].apply(detect_layer)

            layer_order = ["RAW", "BRONZE", "SILVER", "GOLD"]
            layer_summary = df_steps.groupby("Layer").agg(
                Total_Steps=("Etapa", "count"), 
                Tempo_Total_Segundos=("Segundos", "sum")
            ).reset_index()

            ls_plot = layer_summary[layer_summary["Layer"] != "OTHER"].copy()
            ls_plot["Layer"] = pd.Categorical(ls_plot["Layer"], categories=layer_order, ordered=True)
            ls_plot = ls_plot.sort_values("Layer")
            
            tempo_total_seg = ls_plot["Tempo_Total_Segundos"].sum()
            tempo_total_formatado = format_hhmmss(tempo_total_seg)

            with st.expander(f"**⏱️ Tempo de Execução:** `{tempo_total_formatado}`", expanded=True):
                fig_cascade = go.Figure(go.Waterfall(
                    name="Pipeline",
                    orientation="v",
                    measure=(["relative"] * len(ls_plot)) + ["total"],
                    x=list(ls_plot["Layer"]) + ["GERAL"],
                    textposition="outside",
                    text=[format_hhmmss(v) for v in ls_plot["Tempo_Total_Segundos"]] + [tempo_total_formatado],
                    y=list(ls_plot["Tempo_Total_Segundos"]) + ([0] if len(ls_plot) > 0 else []),
                    connector={"line": {"color": "#731E27", "width": 1, "dash": "dot"}},
                    increasing={"marker": {"color": "#731E27"}},
                    totals={"marker": {"color": "#1A1C24", "line": {"color": "#731E27", "width": 2}}}
                ))

                fig_cascade.update_layout(
                    xaxis_title="Camada",
                    yaxis_title="Tempo",
                    showlegend=False,
                    height=450,
                    margin=dict(t=20, b=40, l=40, r=10),
                    yaxis=dict(
                        tickvals=list(range(0, int(tempo_total_seg) + 450, 450)),
                        ticktext=[format_hhmmss(v) for v in range(0, int(tempo_total_seg) + 450, 450)]
                    )
                )
                st.plotly_chart(fig_cascade, use_container_width=True)

            ordered_layers = ["RAW", "BRONZE", "SILVER", "GOLD"]
            for layer in ordered_layers:
                df_layer = df_steps[df_steps["Layer"] == layer].copy()
                if df_layer.empty: continue

                total_proc = len(df_layer)
                success_count = len(df_layer[df_layer["Status"].str.contains('OK|SUCCESS|SUCESSO|✅', case=False, na=False)])
                fail_count = total_proc - success_count
                t_camada = format_hhmmss(df_layer["Segundos"].sum())

                with st.expander(f"⚙️ Auditoria Camada {layer}", expanded=True):
                    m1, m2, m3, m4 = st.columns(4)
                    m1.markdown(f"**Tempo**: `{t_camada}`")
                    m2.markdown(f"**Processos**: {total_proc}")
                    m3.markdown(f"**Sucesso**: {success_count}")
                    m4.markdown(f"**Falhas**: {fail_count}")
                    st.divider()

                    st.dataframe(
                        df_layer[["Etapa", "Status", "Duração"]],
                        use_container_width=True, 
                        hide_index=True
                    )


    if category == "Profiling":
        title = data.get("title", "Profiling Report")
        title_clean = title.replace("`", "")
        
        try:
            _, code_part = title_clean.split(": ", 1)
            camada_nome, run_display = [x.strip() for x in code_part.split("-", 1)]
        except Exception:
            camada_nome = title_clean
            run_display = ""
        
        
        st.markdown(
            f"""
            <h3 style="font-weight:semi-bold;">
                Relatório de Profiling: 
                <code class="theme-1">{camada_nome}</code> - 
                <code class="theme-1">{run_display}</code>
            </h3>
            """,
            unsafe_allow_html=True
        )
        
        st.caption(f"Caminho no Lake: s3://{BUCKET_NAME}/{selected_report_key}")
        st.divider()
        render_timestamp(integrity_timestamp)

        
        if "sections" in data:
            for section in data["sections"]:
                header_text = section.get("header", "")
                content = section.get("content", [])
                metadata = section.get("metadata", {})

                if not content and not metadata:
                    st.markdown(f"### {header_text}")
                
                else:
                    with st.expander(header_text, expanded=True):
                        if metadata:
                            cols = st.columns(len(metadata))
                            for i, (k, v) in enumerate(metadata.items()):
                                cols[i].metric(k, v)
                        
                        for item in content:
                            if item["type"] == "table":
                                df = pd.DataFrame(item["data"])
                                st.dataframe(df, width='stretch')
                            elif item["type"] == "text":
                                st.info(item["data"])

    elif category == "Integrity":
        filename = selected_report_key.split('/')[-1].replace(".json", "")
        camada_nome = filename.split('-')[-1].upper() if '-' in filename else filename.upper()
        run_display = selected_run
        
        st.markdown(
            f"""
            <h3 style="font-weight:semi-bold;">
                Auditoria de Partições: 
                <code class="theme-1">{camada_nome}</code> - 
                <code class="theme-1">{run_display}</code>
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"Caminho no Lake: s3://{BUCKET_NAME}/{selected_report_key}")
        st.divider()
        render_timestamp(integrity_timestamp)

        for table in data.get("tables", []):
            df_part = pd.DataFrame(table["partitions"])
            
            status_col = "status" if "status" in df_part.columns else df_part.columns[-1]
            status_series = df_part[status_col].astype(str).str.upper()
            
            passed = len(df_part[status_series.str.contains('OK|PASS|SUCCESS|✅', na=False)])
            failed = len(df_part[status_series.str.contains('NOK|FAIL|ERROR|❌', na=False)])

            with st.expander(f"📊 Tabela: {table['table']}", expanded=True):
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.markdown(f"**Janela:** `{table['window']}` | **Coluna:** `{table['column']}`")
                c2.metric("Sucesso", passed)
                c3.metric("Falhas", failed)
                
                def format_integrity_status(val):
                    v = str(val).upper()
                    if any(emoji in v for emoji in ['✅', '❌', '⚠️']):
                        return val
                    if "OK" in v or "PASS" in v:
                        return f"✅ {val}"
                    if "NOK" in v or "FAIL" in v:
                        return f"❌ {val}"
                    return val

                df_display = df_part.copy()
                df_display[status_col] = df_display[status_col].apply(format_integrity_status)

                st.dataframe(
                    df_display, 
                    width='stretch',
                    hide_index=True
                )


    elif category == "Quality":
        report_name = selected_report_display
        run_display = selected_run

        st.markdown(
            f"""
            <h3 style="font-weight:semi-bold;">
                Relatório de Qualidade: 
                <code class="theme-1">{selected_layer}/{report_name}</code> - 
                <code class="theme-1">{run_display}</code>
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"Caminho no Lake: s3://{BUCKET_NAME}/{selected_report_key}")
        st.divider()
        render_timestamp(integrity_timestamp)

        if data.get("report_type") == "ABT Technical Report":
            content = data.get("content", {})

            
            with st.expander(f"Metadados e Volumetria da ABT: `{data.get('entity', 'Gold')}`", expanded=True):
                st.markdown(
                    f"""
                    <div style="background-color:#1A1C24; padding:15px; border-radius:8px; border-left: 5px solid #731E27;">
                        <span style="color:#808495; text-transform:uppercase; font-size:12px; font-weight:700;">📌 Grão da Tabela (Primary Key)</span>
                        <h2 style="color:#FFFFFF; margin:0; font-family:'Inter'; font-size:24px;">{content.get('grain', 'N/I')}</h2>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

                def format_milhar(valor):
                    if valor is None or valor == "N/I":
                        return "N/I"
                    
                    try:
                        valor_limpo = "".join(filter(str.isdigit, str(valor)))
                        
                        if not valor_limpo:
                            return str(valor)
                        
                        return f"{int(valor_limpo):,}".replace(",", ".")
                    except Exception:
                        return str(valor)

                st.write("")
                m1, m2, m3 = st.columns(3)
                m1.metric("📦 Total de Variáveis", f"{format_milhar(content.get('variables', 'N/I'))} Features")
                m2.metric("📊 Volumetria Total", f"{format_milhar(content.get('volumetry', 'N/I'))} Registros")
                m3.metric("👤 Cardinalidade", f"{format_milhar(content.get('cardinality', 'N/I'))} CPFs Únicos")

            st.stop()

        COLUMN_ORDER_MAP = {
            "bronze": {
                "order": ["test", "description", "status", "obs"],
                "rename": {"test": "Teste", "description": "Descrição", "status": "Status", "obs": "Informação"}
            },
            "silver": {
                "order": ["test", "description", "status", "obs"],
                "rename": {"test": "Pareamento (Chave -> Desc)", "status": "Status", "obs": "Reg. sem Correspondência", "description": "Descrição"}
            },
            "gold": { 
                "order": ["test", "description", "status", "obs"],
                "rename": {"test": "Teste", "description": "Descrição", "status": "Status", "obs": "Informação"}
            },
            "raw": {
                "order": ["status", "description", "cols", "detail"],
                "rename": {"status": "Status", "description": "Descrição", "cols": "Colunas Verificadas", "detail": "Informação"}
            }
        }

        if "groups" in data:
            groups = data.get("groups", [])
            
            total_tests = sum(len(g.get("tests", [])) for g in groups)
            total_pass = total_fail = total_info = 0
            for group in groups:
                for test in group.get("tests", []):
                    status = str(test.get("status", "")).upper()
                    if "PASS" in status: total_pass += 1
                    elif "FAIL" in status: total_fail += 1
                    else: total_info += 1
            
            with st.expander("📊 Sumário de Qualidade", expanded=True):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total de Testes", total_tests)
                m2.metric("Sucesso", total_pass)
                m3.metric("Falhas", total_fail)
                m4.metric("Informativos", total_info)

            st.divider()

            def format_status_smart(val):
                v = str(val).upper()
                if any(emoji in v for emoji in ['✅', '❌', '⚠️', 'ℹ️']): return val
                if any(x in v for x in ['PASS', 'SUCCESS', 'SUCESSO', 'OK']): return f"✅ {val}"
                if any(x in v for x in ['FAIL', 'ERROR', 'FAILED', 'ERR']): return f"❌ {val}"
                if any(x in v for x in ['WARN', 'WARNING', 'ALERTA']): return f"⚠️ {val}"
                return f"ℹ️ {val}"

            for group in sorted(groups, key=lambda x: x.get("group_id", 99)):
                group_name = group.get("group_name", f"Grupo {group.get('group_id', '')}")
                with st.expander(f"▶️ {group_name}", expanded=True):
                    tests = group.get("tests", [])
                    if not tests:
                        st.info("Nenhum teste neste grupo.")
                        continue
                    
                    df_group = pd.DataFrame(tests)
                    
                    gold_config = COLUMN_ORDER_MAP.get("gold", {})
                    cols_order = gold_config.get("order", [])
                    rename_map = gold_config.get("rename", {})

                    ordered_present = [c for c in cols_order if c in df_group.columns]
                    extras = [c for c in df_group.columns if c not in ordered_present]
                    df_group = df_group[ordered_present + extras]
                    df_group = df_group.rename(columns=rename_map)

                    status_col = "Status" if "Status" in df_group.columns else df_group.columns[-2]
                    df_group[status_col] = df_group[status_col].apply(format_status_smart)
                    
                    st.dataframe(df_group, width='stretch', hide_index=True)
            st.stop()


        results_key = "results" if "results" in data else "tests"
        
        if results_key in data and "reports" not in data and "groups" not in data:
            raw_results = data[results_key]
            forbidden_terms = ["Status Geral", "RELATÓRIO TÉCNICO", "RUNINFO", "======"]
            filtered_results = [r for r in raw_results if not any(term in str(list(r.values())) for term in forbidden_terms)]
            
            df_qual = pd.DataFrame(filtered_results)
            
            if 'description' not in df_qual.columns:
                df_qual['description'] = "Validação de Schema."
            

            layer_key = selected_layer.lower()
            config = COLUMN_ORDER_MAP.get(layer_key, {})
            cols_ordered = config.get("order", [])
            rename_map = config.get("rename", {})

            ordered_present = [c for c in cols_ordered if c in df_qual.columns]
            extras = [c for c in df_qual.columns if c not in ordered_present]
            df_qual = df_qual[ordered_present + extras].rename(columns=rename_map)
            
            status_col = rename_map.get("status", df_qual.columns[-1])

            status_series = df_qual[status_col].astype(str).str.upper()
            passed = len(df_qual[status_series.str.contains('PASS|SUCCESS|SUCESSO|OK|✅', na=False)])
            failed = len(df_qual[status_series.str.contains('FAIL|ERROR|FAILED|ERR|❌', na=False)])
            warns = len(df_qual) - passed - failed

            with st.expander("📊 Sumário de Qualidade", expanded=True):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total", len(df_qual)); m2.metric("Sucesso", passed); m3.metric("Atenção", warns); m4.metric("Falhas", failed)
            
            def format_status_smart(val):
                v = str(val).upper()
                if any(emoji in v for emoji in ['✅', '❌', '⚠️', 'ℹ️']): return val
                if any(x in v for x in ['PASS', 'SUCCESS', 'SUCESSO', 'OK']): return f"✅ {val}"
                if any(x in v for x in ['FAIL', 'ERROR', 'FAILED', 'ERR']): return f"❌ {val}"
                if any(x in v for x in ['WARN', 'WARNING', 'ALERTA']): return f"⚠️ {val}"
                return f"ℹ️ {val}"

            df_display = df_qual.copy()
            df_display[status_col] = df_display[status_col].apply(format_status_smart)
            st.dataframe(df_display, width='stretch', hide_index=True)
            st.stop()

        if "reports" not in data:
            st.warning("Formato inesperado de relatório de qualidade.")
            st.stop()

        reports = data["reports"]

        layer_key = selected_layer.lower()
        layer_config = COLUMN_ORDER_MAP.get(layer_key, {})
        cols_ordered = layer_config.get("order", [])
        rename_map = layer_config.get("rename", {})

        total_entities = sum(r.get("total_added_columns", 1) for r in reports) if layer_key == "silver" else len(reports)

        total_pass = total_warn = total_fail = 0
        for report in reports:
            for test in report.get("tests", []):
                status = str(test.get("status", "")).upper()
                if any(x in status for x in ["PASS", "SUCCESS", "SUCESSO", "OK", "✅"]): total_pass += 1
                elif any(x in status for x in ["WARN", "CHECK", "⚠️"]): total_warn += 1
                elif any(x in status for x in ["FAIL", "ERROR", "FAILED", "ERR", "❌"]): total_fail += 1

        with st.expander("📊 Visão Geral da Execução", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Dimensões", total_entities); c2.metric("Sucesso", total_pass); c3.metric("Atenção", total_warn); c4.metric("Falhas", total_fail)

        for report in reports:
            entity = report["entity"]
            entity_short = entity.split("_")[0]
            final_result = report.get("final_result", "UNKNOWN")
            icon = "✅" if final_result == "SUCCESS" else "⚠️" if final_result == "CHECK_REQUIRED" else "❌"

            with st.expander(f"{icon} Dimensão: `{entity}`", expanded=True):
                tests = report.get("tests", [])
                if not tests:
                    st.info("Nenhum teste encontrado."); continue

                df = pd.DataFrame(tests)
                if cols_ordered:
                    ordered_present = [c for c in cols_ordered if c in df.columns]
                    extras = [c for c in df.columns if c not in ordered_present]
                    df = df[ordered_present + extras]
                if rename_map: df = df.rename(columns=rename_map)

                def format_status(val):
                    v = str(val).upper()
                    if any(x in v for x in ["PASS", "SUCCESS", "SUCESSO", "OK", "✅"]): return f"✅ {val}"
                    if any(x in v for x in ["WARN", "CHECK", "⚠️"]): return f"⚠️ {val}"
                    if any(x in v for x in ["FAIL", "ERROR", "FAILED", "ERR", "❌"]): return f"❌ {val}"
                    return f"ℹ️ {val}"

                status_col = "Status" if "Status" in df.columns else df.columns[-1]
                df[status_col] = df[status_col].apply(format_status)

                st.dataframe(df, width='stretch', hide_index=True)

                if layer_key == "silver":
                    total_desc_cols = report.get("total_added_columns", 0)
                    st.info(f"ℹ️ Total de colunas de descrição adicionadas na tabela {entity_short}: {total_desc_cols}")

else:
    st.error("Não foi possível processar o conteúdo do arquivo.")

