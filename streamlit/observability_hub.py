import streamlit as st
import pandas as pd
import json
import os
import sys
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_simple_metric(col, label, value):
    col.markdown(f"""
        <div style="display: flex; flex-direction: column;">
            <p style="font-size: 0.9rem; color: gray; margin-bottom: 0;">{label}</p>
            <div style="display: flex; align-items: baseline;">
                <span style="font-size: 1.6rem; color: #DAD0D1; font-weight: bold;">{value}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

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

        dt = dt - timedelta(hours=3)

        formatted = dt.strftime("%d/%m/%Y %H:%M:%S")

    except Exception:
        formatted = str(global_timestamp)

    st.caption(f"🕒 Data/Hora da Auditoria: {formatted}")


##################################       
# --- Sidebar ---
##################################   
st.sidebar.title("Painel de Observabilidade")

st.sidebar.write("<hr style='margin-top:20px; margin-bottom:10px;'>", unsafe_allow_html=True)

pilar_options = {
    "Execução | Pipeline": "Pipeline Execution",
    "Análise | Profiling": "Profiling",
    "Validação | Data Quality": "Quality",
    "Estrutura | Integrity": "Integrity",
    "Custos | FinOps": "FinOps"
}

runs = list_runs()
if not runs:
    st.warning("Nenhuma run encontrada no Lake.")
    st.stop()

selected_run = st.sidebar.selectbox(
    "Selecione a Run (ID)", 
    runs, 
    disabled=(st.session_state.get("pilar_key") == "💰 Gestão de Custos (FinOps)")
)

selected_pilar_display = st.sidebar.selectbox(
    "Pilar de Observabilidade", 
    list(pilar_options.keys()),
    key="pilar_key"
)
category = pilar_options[selected_pilar_display]


all_files = list_reports(selected_run)

if not all_files and category != "FinOps":
    st.info(f"Nenhum relatório JSON encontrado para a run {selected_run}.")
    st.stop()

categories = {
    "Pipeline Execution": [f for f in all_files if "pipeline_execution" in f.lower()],
    "Profiling": [f for f in all_files if "profiling" in f.lower()],
    "Quality": [f for f in all_files if "quality" in f.lower()],
    "Integrity": [f for f in all_files if "integrity" in f.lower() or "inspect_partition" in f.lower()],
    "FinOps": ["observability/reports/observability_reports_oci_costs.json"] 
}

available_reports = categories[category]

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
    selected_layer = st.sidebar.selectbox(
        "Selecione a Camada", 
        layers, 
        index=0,
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
        return parts[1].lower() if len(parts) >= 3 else parts[-1].lower()
    parts = filename.split("_")
    return "_".join(parts[1:-1]).lower() if len(parts) > 2 else filename.lower()

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
    selected_report_display = st.sidebar.selectbox("Selecione o Relatório", options=sorted_display_names)
    selected_report_key = report_options[selected_report_display]
else:
    if category != "FinOps":
        st.sidebar.warning("Nenhum relatório formatado disponível.")
        st.stop()
    else:
        selected_report_key = categories["FinOps"][0]
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

if category == "FinOps":
    selected_report_key = "observability/reports/observability_reports_oci_costs.json"
else:
    selected_report_key = selected_report_key 

data = load_json_from_s3(selected_report_key)

integrity_timestamp = None
if category != "FinOps":
    integrity_files = categories.get("Integrity", [])
    if integrity_files:
        integrity_data = load_json_from_s3(integrity_files[0])
        if integrity_data:
            integrity_timestamp = integrity_data.get("timestamp")

if data:

    if category == "FinOps":

        selected_report_key = "observability/reports/observability_reports_oci_costs.json"
        data = load_json_from_s3(selected_report_key)

        if data:

            try:
                dt_utc = datetime.fromisoformat(data.get('updated_at').replace("Z", ""))
                timestamp_final = (dt_utc - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M:%S")
            except:
                timestamp_final = data.get('updated_at', 'N/I')

            st.markdown(f"### Painel de Custos Cloud (OCI): <code class='theme-1'>SQUAD•03</code>", unsafe_allow_html=True)
            
            st.caption(f"🕒 Dados atualizados em **{timestamp_final}**")
            
            total_val = data.get("total_amount", 0)
            budget_limit = 2500.00
            usage_pct = (total_val / budget_limit)

            with st.expander("✅ Indicadores Financeiros", expanded=True):
                m1, m2, m3, m4 = st.columns(4)

                def format_brl(valor):
                    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                render_simple_metric(m1, "Custo Total (ITD)", format_brl(total_val))
                render_simple_metric(m2, f"Budget SQUAD 03", format_brl(budget_limit))
                render_simple_metric(m3, "Consumo do Budget (%)", f"{usage_pct:.2%}")

                st.progress(min(usage_pct, 1.0))

                df_raw_items = pd.DataFrame(data.get("items", []))
                df_costs = df_raw_items.groupby('service')['amount'].sum().reset_index() if not df_raw_items.empty else pd.DataFrame()
                if not df_costs.empty:
                    df_costs = df_costs[df_costs['amount'] > 0].sort_values(by='amount', ascending=False)

                df_daily = pd.DataFrame(data.get("daily_items", []))
                if not df_daily.empty:
                    df_daily['amount'] = pd.to_numeric(df_daily['amount'], errors='coerce').fillna(0)
                    df_daily['date'] = pd.to_datetime(df_daily['date'])
                    df_daily = df_daily.sort_values('date')

                    ultimo_dia = df_daily['date'].iloc[-1]
                    valor_ultimo_dia = df_daily['amount'].iloc[-1]
                    
                    valor_penultimo_dia = df_daily['amount'].iloc[0] if len(df_daily) > 1 else valor_ultimo_dia
                    delta_valor = valor_ultimo_dia - valor_penultimo_dia

                    delta_color = "#37B5A8" if delta_valor <= 0 else "#B53744"
                    setinha = "↓" if delta_valor <= 0 else "↑"

                    m4.markdown(f"""
                        <div style="display: flex; flex-direction: column;">
                            <p style="font-size: 0.9rem; color: gray; margin-bottom: 0;">Custo {ultimo_dia.strftime('%d/%m/%Y')}</p>
                            <div style="display: flex; align-items: baseline; gap: 10px;">
                                <span style="font-size: 1.6rem; font-weight: bold;">{format_brl(valor_ultimo_dia)}</span>
                                <span style="font-size: 1rem; color: {delta_color}; font-weight: bold;">{setinha} {format_brl(delta_valor)}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    render_simple_metric(m4, "Custo Último Dia", "N/I")

            with st.expander("📑 Breakdown por Serviço", expanded=True):

                if not df_costs.empty:
                    df_display = df_costs.copy()
                    df_display['amount'] = df_display['amount'].map(format_brl)

                    row_height = 35
                    header_height = 38

                    height_dynamic = min(
                        700,
                        header_height + len(df_display) * row_height
                    )

                    st.dataframe(
                        df_display.rename(columns={
                            "service": "Serviço",
                            "amount": "Valor"
                        }),
                        use_container_width=True,
                        hide_index=True,
                        height=height_dynamic
                    )


            c1, c2 = st.columns([3, 1.1])    

            with c1:
                with st.expander("📈 Trend de Consumo Diário", expanded=True):

                    if not df_daily.empty:

                        df_daily['date'] = pd.to_datetime(df_daily['date'])

                        x_labels = df_daily['date'].dt.strftime('%d/%m')

                        fig_daily = go.Figure(go.Bar(
                            x=x_labels,
                            y=df_daily['amount'],
                            marker_color='#731E27',
                            text=df_daily['amount'].map(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
                            textposition='auto',
                        ))

                        fig_daily.update_layout(
                            height=350,
                            margin=dict(t=0, b=0, l=0, r=0),
                            xaxis_title="Data",
                            yaxis_title="Valor",
                            yaxis=dict(
                                tickprefix="R$ ",
                                separatethousands=True,
                                tickformat=".2f"
                            )
                        )

                        fig_daily.update_yaxes(
                            tickformat=",.2f"
                        )

                        st.plotly_chart(fig_daily, use_container_width=True)

                    else:
                        st.info("Série temporal diária não disponível.")

            with c2:
                with st.expander("📊 Distribuição de Custos", expanded=True):
                    if not df_costs.empty:
                        fig_pie = go.Figure(data=[go.Pie(
                            labels=df_costs['service'], 
                            values=df_costs['amount'],
                            hole=.4, 
                            textinfo='percent',
                            marker_colors=['#1A1C24', '#731E27', '#9E9E9E', '#555555', '#DAD0D1'],
                            rotation=45  # gira as fatias em 45 graus
                        )])
                        fig_pie.update_layout(
                            margin=dict(t=10, b=10, l=0, r=0), 
                            height=350,
                            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)

            if not df_costs.empty:
                top_service = df_costs.iloc[0]['service']
                col_info, col_alert = st.columns([2, 1.1])
                
                with col_info:
                    st.info(f">💡 **FinOps Insight:** O serviço **{top_service}** lidera os gastos. " + 
                            ("Considere instâncias 'Preemptible' para economizar." if top_service == 'Compute' else "Revise políticas de expiração de objetos."))
                
                with col_alert:
                    if usage_pct > 0.9:
                        st.info(">🚨 **Crítico:** 90% do budget atingido!")
                    elif usage_pct > 0.7:
                        st.info(">⚠️ **Atenção:** 70% do budget consumido.")
                    else:
                        st.info(">✅ Orçamento dentro do esperado, continue monitorando.")

            st.stop()


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
                        tickvals=list(range(0, int(tempo_total_seg) + 300, 300)),
                        ticktext=[format_hhmmss(v) for v in range(0, int(tempo_total_seg) + 300, 300)]
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

        COLUMN_ORDER_MAP = {
            "bronze": {
                "order": ["test", "description", "status", "obs"],
                "rename": {"test": "Teste", "description": "Descrição", "status": "Status", "obs": "Informação"}
            },
            "silver": {
                "order": ["pairing","description", "status", "efficiency_score", "null_values", "no_match_values"],
                "rename": {
                    "pairing": "Pareamento (Chave -> Desc)", 
                    "status": "Status", 
                    "efficiency_score": "Tratados (%)", 
                    "null_values": "Dados Ausentes", 
                    "no_match_values": "Sem Correspondência",
                    "description": "Descrição"
                }
            },
            "gold_abt": { 
                "order": ["source", "type", "status", "coverage", "additional_info"],
                "rename": {
                    "source": "Fonte de Dados", "type": "Tipo", "status": "Status", 
                    "coverage": "Preenchimento (%)", "additional_info": "Informação Adicional"
                }
            },
            "gold_labels": { 
                "order": ["test", "description", "status", "obs"],
                "rename": {"test": "Teste", "description": "Descrição", "status": "Status", "obs": "Informação"}
            },
            "raw": {
                "order": ["status", "description", "cols", "detail"],
                "rename": {"status": "Status", "description": "Descrição", "cols": "Colunas Verificadas", "detail": "Informação"}
            }
        }

        if data.get("report_type") == "ABT Technical Report":
            metadata = data.get("metadata", {})
            
            with st.expander(f"💎 Metadados e Volumetria da ABT: `{data.get('entity', 'Gold')}`", expanded=True):

                def format_milhar(valor):
                    if not valor or valor == "N/I": return "N/I"
                    try:
                        v = str(valor).replace(".", "")
                        return f"{int(v):,}".replace(",", ".")
                    except: return str(valor)

                m1, m2, m3 = st.columns(3)
                m1.metric("📦 Escopo da ABT", f"{metadata.get('variables', '0')} Features Analíticas")
                m2.metric("📊 Volumetria Total", f"{format_milhar(metadata.get('volumetry', '0'))} Registros")
                m3.metric("👤 Cardinalidade", f"{format_milhar(metadata.get('cardinality', '0'))} CPFs Únicos")
                
                st.divider()
                
                integrity_data = data.get("integrity_table", [])
                if integrity_data:
                    df_gold = pd.DataFrame(integrity_data)
                    
                    gold_config = COLUMN_ORDER_MAP.get("gold_abt", {})

                    df_gold = df_gold[gold_config["order"]].rename(columns=gold_config["rename"])
                    
                    def format_status_gold(val):
                        v = str(val).upper()
                        if "PASS" in v or "OK" in v: return f"✅ {val}"
                        if "INFO" in v: return f"ℹ️ {val}"
                        return val
                    
                    df_gold["Status"] = df_gold["Status"].apply(format_status_gold)
                    
                    st.dataframe(df_gold, use_container_width=True, hide_index=True)

                    detalhamento_gold = f"""
                        ###### DETALHAMENTO DE CONFORMIDADE (GOLD)
                        ---
                        > **Master Join (Lógica Point-in-Time):** Cruza as informações respeitando a **Safra** do evento. Garante que o dado cadastral seja contemporâneo à foto, evitando vazamento de dados (data leakage) em modelos preditivos.
                        > 
                        > **Agregação:** Percentual de CPFs da âncora com transações detectadas nas janelas históricas (L30D, L60D, L90D ou Geral).
                        >
                        > **Grão da ABT:** `{metadata.get('grain', 'CPF + SAFRA + PROD')}`
                        >
                        > **🛡️ Metodologia de Sentinelas (Data Trust):**
                        > A saúde da ABT é validada por atributos de presença obrigatória identificados via Profiling:
                        > - **Fontes Cadastrais (Join):** `bur_score_02`, `cad_statusrf` e `tel_var_78`. A ausência indica **Registro Órfão** (falha de enriquecimento).
                        > - **Fontes Comportamentais (Atividade):** `rec_qtd_geral`, `pag_vlr_total_geral` e `atr_vlr_max_geral`. A ausência indica **Inatividade** (traço do perfil do cliente).
                        >
                        > ---
                        > *ℹ️ Nota: A baixa densidade em Agregações reflete apenas a ausência de atividade ou dado cadastral do cliente e não deve ser confundida com uma falha técnica de cruzamento.*                    """

                st.info(detalhamento_gold)
            
            st.stop()

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
                    
                    layer_key = selected_layer.lower()
                    config_key = "gold_labels" if layer_key == "gold" else layer_key
                    gold_config = COLUMN_ORDER_MAP.get(config_key, {})
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
            if layer_key == "gold":
                config = COLUMN_ORDER_MAP.get("gold_labels", {})
            else:
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

            if layer_key == "raw":
                detalhamento_raw = f"""
                    ###### AUDITORIA DE CONTRATO DE DADOS (RAW)
                    ---
                    > **Data Contract:** Validação rigorosa do schema original via Pandera para garantir que a estrutura técnica foi preservada.  
                    > **Conformidade (COLS):** Verifica se o número de colunas entregue pela origem coincide com a definição técnica esperada.  
                    > **Status de Auditoria:** Garante que tipos de dados e nomes de campos não sofreram alterações inesperadas na extração.
                    >
                    > ---
                    > *Nota: Um 'FAIL' na camada Raw indica uma quebra de contrato na origem, impedindo o processamento seguro para as camadas subsequentes.*
                """
                st.info(detalhamento_raw)

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


                    detalhamento_html = f"""
                                        ###### DETALHAMENTO DE AGREGAÇÃO (SILVER)
                                        ---
                                        > **Dados Ausentes:** Identificados na origem (Bronze) como `NULL` e normalizados para 'Sem Descricao'.   
                                        > **Sem Correspondência:** IDs na Fato ausentes na Dimensão, mapeados como 'Sem Correspondencia (ID)'.    
                                        > **Tratados (%):** Eficácia da higienização e rotulagem das inconsistências encontradas   
                                        >
                                        > ---
                                        > *Nota: 'Tratados (%)' representa a soma de Dados Ausentes e Sem Correspondência que foram higienizados na agregação.*
                                        """
                                        
                    st.info(detalhamento_html)

        if layer_key == "bronze":
            detalhamento_bronze = f"""
                ###### DETALHAMENTO DE INTEGRIDADE (BRONZE)
                ---
                > **Match de Tipagem:** Garante que o ID da Fato e da Dimensão possuam o mesmo formato técnico para evitar falhas de JOIN.  
                > **Integridade de Chave:** Identifica códigos (IDs) que circulam na transação (Fato) mas não possuem cadastro na tabela de suporte (Dimensão).  
                > **Registros Órfãos:** Quantidade de IDs distintos ausentes no cadastro que impedem o enriquecimento completo dos dados na Silver.
                >
                > ---
                > *Nota: Um 'WARN' em Integridade de Chave indica que existem novos domínios de dados que ainda não foram mapeados.*
            """
            st.info(detalhamento_bronze)

else:
    st.error("Não foi possível processar o conteúdo do arquivo.")

