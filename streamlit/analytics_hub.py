import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
import sys
import numpy as np
import json
import pickle
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, roc_auc_score

# ==============================================================================
# 0. CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(
    page_title="SQUAD•03 - Painel de Análise e Decisão",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.utils import (
        load_data_summary, 
        load_sample_data,        
        calculate_iv,             
        plot_risk_curve_plotly,   
        plot_dist_comparison,     
        plot_bad_rate_trend, 
        plot_correlation_matrix,
        plot_interaction_matrix,
        get_feature_ranking,
        calculate_psi,
        plot_psi_distribution,
        load_assets, 
        calculate_score, 
        get_risk_tier,
        local_css,
        COLORS,
        calculate_policy_curve,
        plot_policy_tradeoff,  
        plot_decision_boundary,
        WoEEncoder,
        process_demographics, 
        plot_age_analysis,   
        plot_geo_map,
        STATE_NAMES,
        STATE_COORDS
    )
except ImportError:
    pass  

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

local_css("streamlit/assets/style.css")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# CONSTANTES E CORES
# ==============================================================================
ABT_PATH = "s3://lake/gold/abt_base_cmv/**/*.parquet"

COLORS = {
    'primary': '#731E27',   
    'dark': '#1A1C24',       
    'success': '#5EA758',    
    'warning': '#D4A017',   
    'danger': '#731E27',     
    'text_light': '#DAD0D1', 
    'bg_light': '#F8F9FA',  
    'neutral': '#455A64',    
    'good': '#3C6E3B',       
    'bad': '#731E27',       
    'accent': '#C62828'      
}

# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: flex-end; width: 100%; overflow: hidden; margin-top: 10px; margin-bottom: -5px;">
        <img src="https://i.postimg.cc/dQNRCk8X/Group-4.png" style="width: 100%; object-fit: contain;">
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <h3 style='font-size: 1.3rem; font-weight: 600; text-align: center; margin-top: 10px; line-height: 1.2;'>
        Painel de Análise e Decisão
    </h3>
    """, 
    unsafe_allow_html=True
)
st.sidebar.write("<hr style='margin-top:-10px; margin-bottom:0px;'>", unsafe_allow_html=True)

view_mode = st.sidebar.radio(
    "Selecione a Visualização",
    [
        "👤 Home | Estudo de Público",
        "🎯 Estratégia de Política",
        "⚙️ Motor de Decisão",
        "📈 Performance & Benchmark"
    ],
    index=0,
    label_visibility="collapsed"
)

st.sidebar.write("<hr style='margin-top:3px; margin-bottom:-8px;'><br>", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <p style='margin-top:18px;'>
    <style>
    .custom-sidebar-logo {
        position: relative;   
        top: -10px;            
        display: flex;
        justify-content: center;
        margin-bottom: -23px; 
        z-index: 10;        
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

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
def main():

    # ==============================================================================
    # 1. INGESTÃO CENTRALIZADA DE DADOS (SINGLE SOURCE OF TRUTH)
    # ==============================================================================
    @st.cache_data(ttl=3600)
    def load_master_data():
        """Carrega a ABT completa. Usada para cálculos de Safra, PSI e Modelagem."""
        return load_sample_data()

    @st.cache_data(ttl=3600)
    def prep_demographic_data(df_master):
        """Deriva a base demográfica garantindo CPFs únicos (safra mais recente)."""
        df_demo = df_master.drop_duplicates('num_cpf').copy()
        df_demo = process_demographics(df_demo)
        
        cols_categoricas = ['regiao', 'uf', 'estado_nome', 'faixa_etaria']
        for col in cols_categoricas:
            if col in df_demo.columns:
                df_demo[col] = df_demo[col].astype('category')
        return df_demo

    @st.cache_data(ttl=3600)
    def get_cached_iv_dict(df, features):
        iv_scores = {}
        for col in features:
            val, _ = calculate_iv(df, col)
            iv_scores[col] = val
        return iv_scores



    df_master = load_master_data()
    
    if df_master.empty:
        st.error("❌ Falha ao carregar a base de dados central.")
        st.stop()

    df_demo = prep_demographic_data(df_master)
    global_bad_rate_demo = df_demo['target'].mean()
    global_bad_rate_master = df_master['target'].mean()



    if view_mode == "👤 Home | Estudo de Público":

        st.markdown(
            f"""
            <h3 style="font-weight:700; margin-bottom: 0px;">
                Visão Geral e Estudo de Público: Migração Pré para Controle - 
                <code class="theme-1" style="font-size: 1.2rem;">eda_v1.0</code>
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.caption("📂 **Notebook de Referência:** `notebooks/eda/01_estudo_publico_alvo_cmv.ipynb`")
        st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)
        st.write("")

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Visão Geral",
            "Análise Demográfica",
            "Análise Univariada",
            "Análise Multivariada",
            "Ranking de Variáveis",
            "Estabilidade Temporal",
        ])

        # --- TAB 1: VISÃO GERAL ---
        with tab1:
            with st.expander("📊 Monitoramento de Carteira e Saúde do Modelo", expanded=True):
                
                summary_df = pd.DataFrame()
                
                try:
                    if 'lake_loaded' not in st.session_state:
                        st.toast("Conectando a OCI...", icon="📡")
                        with st.spinner("Consultando dados atualizados do Lake..."):
                            summary_df = load_data_summary()
                            assets = load_assets()
                            metadata = assets.get('metadata', {})
                        st.session_state['lake_loaded'] = True
                    else:
                        summary_df = load_data_summary()
                        assets = load_assets()
                        metadata = assets.get('metadata', {})
                        
                    if summary_df.empty:
                        st.warning("⚠️ A conexão funcionou, mas a tabela retornou vazia.")
                        st.stop()

                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    st.stop()

                if not summary_df.empty:
                    summary_df = summary_df.sort_values('safra')

                    total_reg = summary_df['total_registros'].sum()
                    total_bads = summary_df['total_bads'].sum()
                    avg_bad_rate = total_bads / total_reg if total_reg > 0 else 0

                    total_bad_absoluto = summary_df['total_bads'].sum()
                    avg_bad = total_bad_absoluto / total_reg if total_reg > 0 else 0
                    odds = (1 - avg_bad) / avg_bad if avg_bad > 0 else 0
                    
                    last_month = summary_df.iloc[-1]
                    prev_month = summary_df.iloc[-2] if len(summary_df) > 1 else last_month
                    
                    vol_mom = (last_month['total_registros'] - prev_month['total_registros']) / prev_month['total_registros']
                    risk_mom = (last_month['bad_rate'] - prev_month['bad_rate']) / prev_month['bad_rate']

                    k1, k2, k3, k4, k5 = st.columns(5)

                    with k1:

                        vol_str = f"{total_reg/1e6:.2f}M"
                        cor_delta = "#5EA758" if vol_mom >= 0 else "#B53744"
                        seta = "+" if vol_mom >= 0 else ""
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Volume Total (Full Sample)</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.6rem; font-weight: 600; color: #FFF;">{vol_str}</span>
                                    <span style="font-size: 0.9rem; color: {cor_delta}; font-weight: bold;">{seta}{vol_mom:.1%} (MoM)</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Registros processados</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with k2:
                        cor_delta = "#B53744" if risk_mom > 0 else "#5EA758"
                        seta = "+" if risk_mom >= 0 else ""
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Bad Rate Médio (FPD)</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.6rem; font-weight: 600; color: #FFF;">{avg_bad:.2%}</span>
                                    <span style="font-size: 0.9rem; color: {cor_delta}; font-weight: bold;">{seta}{risk_mom:.1%} (MoM)</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Média ponderada da safra</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with k3:
                        gini_atual = metadata.get('gini_oot', 0)
                        target_gini = 40.0
                        diff_gini = gini_atual - target_gini
                        cor_delta = "#5EA758" if diff_gini >= 0 else "#B53744"
                        seta = "+" if diff_gini >= 0 else ""
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Poder do Modelo (Gini)</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.6rem; font-weight: 600; color: #FFF;">{gini_atual:.1f}%</span>
                                    <span style="font-size: 0.9rem; color: {cor_delta}; font-weight: bold;">{seta}{diff_gini:.1f} p.p. (Meta)</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Performance OOT (Produção)</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with k4:
                        ks_atual = metadata.get('ks_oot', 0)
                        target_ks = 30.0
                        diff_ks = ks_atual - target_ks
                        cor_delta = "#5EA758" if diff_ks >= 0 else "#B53744"
                        seta = "+" if diff_ks >= 0 else ""
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Separação (KS)</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.6rem; font-weight: 600; color: #FFF;">{ks_atual:.1f}%</span>
                                    <span style="font-size: 0.9rem; color: {cor_delta}; font-weight: bold;">{seta}{diff_ks:.1f} p.p. (Meta)</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Capacidade de distinção</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with k5:
                        psi_atual = metadata.get('psi_oot', 0.0)
                        
                        target_psi = 0.25
                        if psi_atual < 0.10:
                            cor_delta = "#5EA758" 
                            status_psi = "Estável"
                        elif psi_atual < 0.25:
                            cor_delta = "#FFA500" 
                            status_psi = "Atenção"
                        else:
                            cor_delta = "#B53744" 
                            status_psi = "Drift"

                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Estabilidade (PSI)</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.6rem; font-weight: 600; color: #FFF;">{psi_atual:.4f}</span>
                                    <span style="font-size: 0.9rem; color: {cor_delta}; font-weight: bold;">{status_psi}</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Meta < 0.25 (Safras Recentes)</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("A consulta retornou vazia. Verifique os filtros ou a tabela no S3.")

            with st.expander("📅 Evolução Temporal: Volume de Entrada & Risco Real", expanded=False):                      
                st.plotly_chart(plot_bad_rate_trend(summary_df), width='stretch')

                st.markdown(
                    """
                    <div style="
                        height: 35px;            
                        min-height: 35px;
                        display: flex;
                        align-items: center;
                        padding: 0 0 0 0px;
                        font-size: 0.80rem;
                        color: rgba(255,255,255,0.65);
                        margin-top:-20px;
                        justify-content: center;
                        text-align: center;
                        margin-top: -17px
                    ">
                        Eixo esquerdo: Volumetria Real | Eixo direito: % de Bad Rate da Safra
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            bloco_contexto = """
            <div style="
                background-color:#1A1A1A;
                color:#888;
                padding:16px 16px 0px 16px;
                border-radius:8px;
                border-left:6px solid #4F1C22;
                font-family:sans-serif;
                font-size:14.5px;
            ">
                <h6 style="margin-top:0px; margin-bottom:3px;">
                    🎯 CONTEXTO DE NEGÓCIO E CRITÉRIOS DE SUCESSO
                </h6>   
                <hr style="margin-top:2px; margin-bottom:15px; border:1px solid #666;">   
                <div style="display:flex; gap:30px; align-items:flex-start; flex-wrap: wrap; margin-bottom: 16px;">     
                    <div style="flex:1; min-width: 240px;">
                        <strong style="color: #DDD;">- Objetivos & Estratégia:</strong>
                        <ul style="margin-top:10px; margin-bottom:0; padding-left: 10px; line-height: 1.5;">
                            <p><strong style="color:#BBB;">Expansão:</strong> Identificar usuários do Pré-Pago elegíveis para oferta Controle.</p>
                            <p><strong style="color:#BBB;">Qualidade:</strong> Garantir inadimplência controlada na entrada (FPD).</p>
                            <p><strong style="color:#BBB;">Dados:</strong> Utilizar comportamento de recarga e bureau.</p>
                        </ul>
                    </div>
                    <div style="flex:1; min-width: 240px;">
                        <strong style="color: #DDD;">- Metas Técnicas (KPIs):</strong>
                        <div style="margin-top:7px; padding-left: 8px; display:flex; flex-direction:column; gap:6px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #333; padding-bottom:3px;">
                                <span>Gini (Discriminação)</span>
                                <span style="color:#5EA758; font-weight:bold; background:rgba(55,181,68,0.1); padding:1px 6px; border-radius:4px; font-size:13px;">> 40%</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px dashed #333; padding-bottom:3px;">
                                <span>KS (Separação)</span>
                                <span style="color:#5EA758; font-weight:bold; background:rgba(55,181,68,0.1); padding:1px 6px; border-radius:4px; font-size:13px;">> 30%</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span>PSI (Estabilidade)</span>
                                <span style="color:#D4A017; font-weight:bold; background:rgba(255,165,0,0.1); padding:1px 6px; border-radius:4px; font-size:13px;">< 0.25</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(bloco_contexto, unsafe_allow_html=True)


        # --- TAB 2: ANÁLISE DEMOGRÁFICA ---
        with tab2:
            with st.expander("🗺️ Segmentação Demográfica e Geográfica", expanded=True):
                
                c_region, c_state, c_score = st.columns([1, 1, 1.2])
                
                with c_region:
                    regioes_disponiveis = ["Brasil (Todas)"] + sorted(df_demo['regiao'].unique().tolist())
                    sel_regiao = st.selectbox("1. Filtrar Região:", regioes_disponiveis)
                
                with c_state:
                    if sel_regiao == "Brasil (Todas)":
                        estados_filtrados = ["Todos"]
                        disabled_state = True
                        index_state = 0
                    else:
                        filtro_regiao = df_demo[df_demo['regiao'] == sel_regiao]
                        lista_ufs = sorted(filtro_regiao['uf'].unique())
                        estados_filtrados = ["Todos da Região"] + [f"{STATE_NAMES.get(uf, uf)} ({uf})" for uf in lista_ufs]
                        disabled_state = False
                        index_state = 0
                    
                    sel_estado_display = st.selectbox(
                        "2. Filtrar Estado:", 
                        estados_filtrados, 
                        index=index_state,
                        disabled=disabled_state
                    )

                with c_score:
                    min_score, max_score = st.slider(
                        "3. Faixa de Score (Bureau):", 
                        0, 1000, (0, 1000)
                    )
                
                mask = pd.Series(True, index=df_demo.index)

                if min_score > 0 or max_score < 1000:
                    mask &= df_demo['bur_score_02'].between(min_score, max_score)

                if sel_regiao != "Brasil (Todas)":
                    mask &= (df_demo['regiao'] == sel_regiao)

                    if sel_estado_display != "Todos da Região":
                        sigla_uf = sel_estado_display.split('(')[-1].replace(')', '')
                        mask &= (df_demo['uf'] == sigla_uf)

                df_filtered = df_demo[mask]
                
            with st.expander("📊 Resultados da Segmentação", expanded=True):

                if df_filtered.empty:
                    st.warning("Nenhum dado encontrado para os filtros selecionados.")
                else:
                    col_m1, col_m2, col_m3 = st.columns(3)

                    avg_risk = df_filtered['target'].mean()
                    delta_risk = avg_risk - global_bad_rate_demo

                    with col_m1:
                        vol_str = f"{len(df_filtered):,.0f}".replace(",", ".")
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Volume da Amostra</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{vol_str}</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Total de Clientes Únicos no Segmento</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with col_m2:
                        if delta_risk <= 0:
                            cor_delta = "#5EA758" 
                            seta = "↓"
                        else:
                            cor_delta = "#B53744" 
                            seta = "↑"
                        
                        val_fmt = f"{avg_risk:.2%}"
                        delta_fmt = f"{seta} {abs(delta_risk):.2%}"

                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Bad Rate (Inadimplência)</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{val_fmt}</span>
                                    <span style="font-size: 1rem; color: {cor_delta}; font-weight: bold;">{delta_fmt}</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">vs. Total da Amostra</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with col_m3:
                        idade_media = df_filtered['idade'].mean()
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Idade Média</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{idade_media:.1f}</span>
                                    <span style="font-size: 0.9rem; color: #888; font-weight: normal;">anos</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Média do Segmento</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

                    c_chart1, c_chart2 = st.columns([1.2, 1])
                    
                    with c_chart1:
                        st.plotly_chart(plot_age_analysis(df_filtered), width='stretch')

                        st.markdown(
                            """
                            <div style="
                                height: 35px;            
                                min-height: 35px;
                                display: flex;
                                align-items: center;
                                padding: 0 0 0 0px;
                                font-size: 0.80rem;
                                color: rgba(255,255,255,0.65);
                                justify-content: center;
                                text-align: center;
                                margin-top: -17px
                            ">
                                Distribuição de volume e risco de crédito por faixa etária da amostra.
                            </div>
                            """,
                            unsafe_allow_html=True)
                        
                    with c_chart2:
                        
                        uf_highlight = None
                        if sel_estado_display not in ["Todos da Região", "Todos"] and "(" in sel_estado_display:
                            uf_highlight = sel_estado_display.split('(')[-1].replace(')', '')

                        st.plotly_chart(
                            plot_geo_map(
                                df_filtered,
                                uf_selecionada=uf_highlight,
                                regiao_sel=sel_regiao
                            ),
                            width='stretch'
                        )

                        st.markdown(
                            """
                            <div style="
                                height: 35px;            
                                min-height: 35px;
                                display: flex;
                                align-items: center;
                                padding: 0 0 0 0px;
                                font-size: 0.80rem;
                                color: rgba(255,255,255,0.65);
                                justify-content: center;
                                text-align: center;
                                margin-top: -17px
                            ">
                                Distribuição Espacial: Concentração de clientes e Bad Rate.
                            </div>
                            """,
                            unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #731E27; font-family:sans-serif; font-size:14px;">
                <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">🌍 INSIGHTS DEMOGRÁFICOS</h6>
                <hr style="margin-top:2px; margin-bottom:15px; border:1px solid #444;">
                <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">🎂 Fator Idade:</strong>
                        <p style="margin-top:5px;">O risco cai drasticamente com a idade. O grupo 18-24 anos tem Bad Rate ~26%, enquanto o grupo 65+ tem ~17%.</p>
                    </div>
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">📍 Fator Região:</strong>
                        <p style="margin-top:5px;">Historicamente, estados do Norte/Nordeste apresentam risco ajustado maior que o Sudeste/Sul. Use os filtros acima para validar.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # --- TAB 3: ANÁLISE UNIVARIADA ---
        with tab3:
            with st.expander("🔍 Análise Univariada de Variáveis", expanded=True):
                
                df_sample = df_master.copy()

                ignored_cols = ['target', 'fpd', 'safra', 'num_cpf', 'cpf']
                numeric_cols = df_sample.select_dtypes(include=[np.number]).columns.tolist()
                available_features = [c for c in numeric_cols if c not in ignored_cols]

                if not available_features:
                    st.warning("Nenhuma variável numérica encontrada para análise.")
                else:
                    with st.spinner("Calculando ranking de variáveis (IV)"):
                        iv_scores = get_cached_iv_dict(df_sample, available_features)

                    sorted_features = sorted(available_features, key=lambda x: iv_scores.get(x, 0), reverse=True)

                    def format_func(option):
                        score = iv_scores.get(option, 0)
                        label = f"{option}"
                        if score > 0.3: return f"🔥 {label}"
                        if score > 0.1: return f"✨ {label}"
                        return label

                    c_sel, c_metrics = st.columns([1, 3])
                    with c_sel:
                        selected_feature = st.selectbox(
                            "Selecione a Variável (IV ↓):", 
                            sorted_features,
                            format_func=format_func,
                            index=0 
                        )

                    iv_val = iv_scores.get(selected_feature, 0)
                    
                    with c_metrics:

                        if iv_val > 0.3:
                            texto = "🔥 <b>Poder Preditivo: Muito Forte</b>"
                            cor = "#5EA758"
                        elif iv_val > 0.1:
                            texto = "✨ <b>Poder Preditivo: Médio</b>"
                            cor = "#D4A017"
                        else:
                            texto = "⚠️ <b>Poder Preditivo: Fraco</b>"
                            cor = "#B53744"

                        st.markdown(
                            f"""
                            <div style="
                                height: 70px;              
                                min-height: 70px;
                                display: flex;
                                flex-direction: column;
                                justify-content: center;  
                                padding: 10px 15px;
                                border-radius: 12px;
                                background-color: rgba(255,255,255,0.03);
                                border-left:6px solid #4F1C22;
                            ">
                                <span style="font-size: 1rem; color: {cor};">
                                    {texto}
                                </span>
                                <span style="font-size: 0.85rem; opacity: 0.7;">
                                    IV: {iv_val:.4f}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                if 'target' in df_sample.columns:
                    desc = df_sample.groupby('target')[selected_feature].describe().reset_index()
                    desc['target'] = desc['target'].map({0: 'Bom', 1: 'Mau'})
                    st.dataframe(desc.style.format("{:.2f}", subset=desc.columns[1:]), width='stretch')
                else:
                    st.write(df_sample[selected_feature].describe())


            col_chart1, col_chart2 = st.columns([1.5,1])

            with col_chart1:

                with st.expander("📈 Curva de Risco", expanded=True):

                    st.plotly_chart(
                        plot_risk_curve_plotly(df_sample, selected_feature), 
                        width='stretch'
                    )
                    st.markdown(
                        """
                        <div style="
                            height: 35px;            
                            min-height: 35px;
                            display: flex;
                            align-items: center;
                            padding: 0 0 0 0px;
                            font-size: 0.80rem;
                            color: rgba(255,255,255,0.65);
                            margin-top:-20px;
                            justify-content: center;
                            text-align: center;
                            margin-top: -17px
                        ">
                            Eixo esquerdo: Volumetria | Eixo direito: Bad Rate (Risco)
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                        
            with col_chart2:
                
                with st.expander("📊 Distrbuição por Classe", expanded=True):
                    
                    st.plotly_chart(
                        plot_dist_comparison(df_sample, selected_feature), 
                        width='stretch'
                    )
                    st.markdown(
                        """
                        <div style="
                            height: 35px;            
                            min-height: 35px;
                            display: flex;
                            align-items: center;
                            padding: 0 0 0 0px;
                            font-size: 0.80rem;
                            color: rgba(255,255,255,0.65);
                            margin-top:-20px;
                            justify-content: center;
                            text-align: center;
                            margin-top: -17px
                        ">
                            Comparação de densidade: Bons Pagadores (Verde) vs Maus Pagadores (Vermelho)
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


        # --- TAB 4: ANÁLISE MULTIVARIADA ---
        with tab4:
                
            df_multi = df_master.copy()

            ignored_cols = ['target', 'fpd', 'safra', 'num_cpf', 'cpf']
            numeric_cols = df_multi.select_dtypes(include=[np.number]).columns.tolist()
            valid_cols = [c for c in numeric_cols if c not in ignored_cols]
            
            with st.spinner("Filtrando variáveis relevantes (IV > 0.1)..."):
                dict_iv_aba3 = get_cached_iv_dict(df_multi, valid_cols)
                
                selected_cols_for_corr = [col for col, val in dict_iv_aba3.items() if val > 0.1]
            

            with st.expander("🔗 Matriz de Risco Combinada (Bad Rate %)", expanded=True):
                    
                mat1, mat2 = st.columns([1,2.5])

                if len(valid_cols) >= 2:

                    with mat1:

                        idx_x = valid_cols.index('bur_score_02') if 'bur_score_02' in valid_cols else 0
                        var_x = st.selectbox("Eixo X (Variável 1):", valid_cols, index=idx_x)

                        idx_y = valid_cols.index('bur_score_01') if 'bur_score_01' in valid_cols else min(1, len(valid_cols)-1)
                        var_y = st.selectbox("Eixo Y (Variável 2):", valid_cols, index=idx_y)

                        st.markdown("""
                        <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                            <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">💡 COMO LER ESTE GRÁFICO</h6>
                            <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
                            <div style="display:flex; gap:-2px; align-items:flex-start; flex-wrap: wrap;">
                                <div style="flex:1; min-width: 200px;">
                                    <strong style="color: #DDD;">Cores Vermelhas:</strong>
                                    <p style="margin-top:5px;">Alta concentração de maus pagadores (Bad Rate alto).</p>
                                </div>
                                <div style="flex:1; min-width: 200px;">
                                    <strong style="color: #DDD;">Cores Verdes:</strong>
                                    <p style="margin-top:5px;">Baixa concentração de maus pagadores (Bad Rate baixo).</p>
                                </div>
                                <div style="flex:1; min-width: 200px;">
                                    <strong style="color: #DDD;">Utilidade::</strong>
                                    <p style="margin-top:5px;">Se uma combinação de variáveis cria um quadrante muito vermelho, considere criar uma regra de política (Hard Cutoff).</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


                    with mat2:

                        st.plotly_chart(
                            plot_interaction_matrix(df_multi, var_x, var_y), 
                            width='stretch'
                        )

                        st.markdown(
                            """
                            <div style="
                                height: 35px;            
                                min-height: 35px;
                                display: flex;
                                align-items: center;
                                padding: 0 0 0 0px;
                                font-size: 0.80rem;
                                color: rgba(255,255,255,0.65);
                                margin-top:-20px;
                                padding-left: 170px;
                                margin-top: -17px
                            ">
                                Analise como o risco se comporta combinando duas variáveis. Ideal para encontrar 'bolsões' de risco.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:
                    st.warning("Variáveis insuficientes para análise cruzada.")


            with st.expander("🔗 Matriz de Correlação (Spearman)", expanded=True):

                if len(selected_cols_for_corr) < 2:

                    st.markdown(f"""
                    <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 4px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                        <p style="margin-top:5px;">
                            ⚠️ Poucas variáveis com IV > 0.1. Exibindo matriz completa.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    final_corr_cols = valid_cols

                else:

                    st.markdown(f"""
                    <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 4px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                        <p style="margin-top:5px;">
                            ✨ <strong>Filtrado:</strong> Exibindo as <strong>{len(selected_cols_for_corr)}</strong> variáveis com maior poder preditivo (IV > 0.1), priorizando atributos mais relevantes para modelagem e mitigação de multicolinearidade.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    final_corr_cols = selected_cols_for_corr

                st.plotly_chart(
                    plot_correlation_matrix(df_multi[final_corr_cols]), 
                    width='stretch'
                )

                st.markdown(
                    """
                    <div style="
                        height: 35px;            
                        min-height: 35px;
                        display: flex;
                        align-items: center;
                        padding: 0 0 0 0px;
                        font-size: 0.80rem;
                        color: rgba(255,255,255,0.65);
                        margin-top:-20px;
                        justify-content: center;
                        text-align: center;
                        margin-top: -17px
                    ">
                        Variáveis com IV > 0.1. Cores fortes indicam alta redundância.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # --- TAB 5: RANKING DE VARIÁVEIS ---
        with tab5:
            with st.expander("🏆 Ranking de Poder Discriminatório", expanded=True):
                
                try:
                    with st.spinner("Calculando Gini e IV para todas as variáveis..."):
                        ranking_df = get_feature_ranking(df_master)
                        
                except Exception as e:
                    st.error(f"Erro ao processar ranking: {e}")
                    ranking_df = pd.DataFrame()

                if ranking_df.empty:
                    st.warning("Não foi possível calcular o ranking.")
                else:
                    st.dataframe(
                        ranking_df,
                        width='stretch',
                        column_order=("Variável", "Qualidade", "IV", "Gini (%)"),
                        hide_index=True,
                        column_config={
                            "Variável": st.column_config.TextColumn(
                                "Variável",
                                help="Nome da feature na amostra em análise"
                            ),
                            "Qualidade": st.column_config.TextColumn(
                                "Poder (IV)",
                                width="small"
                            ),
                            "IV": st.column_config.ProgressColumn(
                                "Information Value (IV)",
                                format="%.4f",
                                min_value=0,
                                max_value=0.6, 
                                help="Mede a capacidade de separação entre Bons e Maus."
                            ),
                            "Gini (%)": st.column_config.ProgressColumn(
                                "Gini Univariado (%)",
                                format="%.1f%%",
                                min_value=0,
                                max_value=100,
                                help="Gini isolado da variável (0 a 100)."
                            ),
                        }
                    )

                    rank1, rank2 = st.columns([6.2,1])

                    with rank1:

                        st.markdown("""
                        <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 10px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                            <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">💡 NOTA TÉCNICA</h6>
                            <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
                            <ul style="margin-top:10px; margin-bottom:0; padding-left: 10px; line-height: 1.5;">
                                <li style="margin-top:5px;">O <strong>Gini Univariado</strong> calcula a performance da variável sozinha predizendo o alvo.</li>
                                <li style="margin-top:5px;"> O <strong>IV</strong> mede a quantidade de informação. Variáveis com <strong>IV > 0.5</strong> são suspeitas (leaking) e <strong>IV < 0.02</strong> são ruído.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                    with rank2:

                        st.download_button(
                            label="📥 Baixar Ranking (CSV)",
                            data=ranking_df.to_csv(index=False).encode('utf-8'),
                            file_name=f"feature_ranking_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )

                    st.write("")

        # --- TAB 6: ESTABILIDADE TEMPORAL (PSI) ---
        with tab6:
            with st.expander("⚖️ Monitoramento de Estabilidade (PSI)", expanded=True):
                
                df_psi = df_master.copy()

                if df_psi.empty or 'safra' not in df_psi.columns:
                    st.warning("Dados insuficientes ou coluna 'safra' ausente.")
                    st.stop()

                df_psi['safra_str'] = df_psi['safra'].dt.strftime('%Y-%m')
                safras_disponiveis = sorted(df_psi['safra_str'].unique())

                if len(safras_disponiveis) < 2:
                    st.warning("É necessário ter ao menos 2 safras para calcular estabilidade.")
                    st.stop()

                c1, c2, c3 = st.columns(3)
                
                with c1:
                    cols_psi = df_psi.select_dtypes(include=[np.number]).columns.tolist()
                    ignorar = ['target', 'fpd', 'cpf', 'num_cpf']
                    cols_validas = [c for c in cols_psi if c not in ignorar]
                    
                    feat_psi = st.selectbox(
                        "Variável para Análise:", 
                        cols_validas, 
                        index=cols_validas.index('bur_score_02') if 'bur_score_02' in cols_validas else 0
                    )
                
                with c2:
                    safra_base = st.selectbox("📅 Safra de Referência (Base):", safras_disponiveis, index=0)

                with c3:
                    safra_atual = st.selectbox("📅 Safra em Análise (Atual):", safras_disponiveis, index=len(safras_disponiveis)-1)


                v_base = df_psi[df_psi['safra_str'] == safra_base][feat_psi].dropna()
                v_atual = df_psi[df_psi['safra_str'] == safra_atual][feat_psi].dropna()

                if v_base.empty or v_atual.empty:
                    st.error("Dados insuficientes nas safras selecionadas.")
                else:
                    psi_value = calculate_psi(v_base, v_atual)
                    
                    m_col, g_col = st.columns([1, 2])
                    
                    with m_col:
                    
                        if psi_value < 0.10:
                            cor_psi = "#5EA758"
                            msg_psi = "✅ <b>Estável</b>"
                            desc_psi = "A distribuição da variável não mudou significativamente. O modelo permanece seguro."
                        elif psi_value < 0.25:
                            cor_psi = "#D4A017"
                            msg_psi = "⚠️ <b>Atenção (Alerta)</b>"
                            desc_psi = "Pequena mudança na distribuição. Monitorar próximas safras."
                        else:
                            cor_psi = "#B53744"
                            msg_psi = "🚨 <b>Instável (Crítico)</b>"
                            desc_psi = "Mudança drástica no perfil (Drift). O modelo pode estar descalibrado. Considere re-treino."
                        
                        st.write("")

                        st.markdown(
                            f"""
                            <div style="background-color: #1A1A1A; padding: 20px; border-radius: 10px; border-left: 8px solid {cor_psi};">
                                <h4 style="margin:0; color: #DAD0D1;">Population Stability Index (PSI)</h4>
                                <h1 style="margin:0; margin-top:-20px; font-size: 3.5rem; color: {cor_psi};">{psi_value:.4f}</h1>
                                <span style="font-size: 1.2rem; color: #DAD0D1;">{msg_psi}</span>
                                <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">{desc_psi}</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            """
                            <div style="
                                height: 35px;            
                                min-height: 35px;
                                display: flex;
                                align-items: center;
                                padding: 0 0 0 0px;
                                font-size: 0.80rem;
                                color: rgba(255,255,255,0.65);
                                justify-content: center;
                                text-align: center;
                                margin-top: 5px
                            ">
                                PSI < 0.10 = Estável | 0.10–0.25 = Alerta | > 0.25 = Drift relevante
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with g_col:
                        st.plotly_chart(
                            plot_psi_distribution(v_base, v_atual, safra_base, safra_atual, feat_psi),
                            width='stretch'
                        )

                        st.markdown(
                            """
                            <div style="
                                height: 35px;            
                                min-height: 35px;
                                display: flex;
                                align-items: center;
                                padding: 0 0 0 0px;
                                font-size: 0.80rem;
                                color: rgba(255,255,255,0.65);
                                justify-content: center;
                                text-align: center;
                                margin-top: -17px
                            ">
                                Analise como a distribuição da variável mudou ao longo do tempo. Ideal para identificar drift e perda de estabilidade do modelo.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    # ==============================================================================
    # PERFORMANCE & BENCHMARK 
    # ==============================================================================
    elif view_mode == "📈 Performance & Benchmark":
        
        st.markdown(
            f"""
            <h3 style="font-weight:700; margin-bottom: 0px;">
                Avaliação de Performance e Benchmark - 
                <code class="theme-1" style="font-size: 1.2rem;">model_v1.0</code>
            </h3>
            """,
            unsafe_allow_html=True
        )
        caminho = "models/behavior_baseline_woe_v1.pkl"
        st.caption(f"🎯 Escoragem real-time executada sobre o Asset de Modelagem: `{caminho.split('/')[-1]}`")
        st.write("<hr style='margin-top:-6.5px; margin-bottom:15px;'>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # CARREGAMENTO DA BASE & DO MODELO
        # ---------------------------------------------------------
        df_perf = pd.DataFrame()
        try:
            with st.spinner("Carregando amostra e escorando com o modelo de produção..."):
                df_perf = df_master.copy()
                assets = load_assets()
                model = assets['model']
                encoder = assets['woe_encoder']
                features_raw = assets['features_raw']

                metadata = assets.get('metadata', {})
        except Exception as e:
            st.error(f"Erro ao carregar modelo ou base de dados: {e}")
            st.stop()

        df_to_score = df_perf.copy()
        for col in features_raw:
            if col not in df_to_score.columns:
                df_to_score[col] = np.nan
        
        df_woe = encoder.transform(df_to_score, features_raw)
        woe_cols = [f'{col}_woe' for col in features_raw]
        X_model = df_woe[woe_cols].fillna(0)
        df_perf['prob_modelo'] = model.predict_proba(X_model)[:, 1]

        fpr, tpr, _ = roc_curve(df_perf['target'], df_perf['prob_modelo'])
        ks_live = max(tpr - fpr) * 100


        cutoff_bureau = np.nanpercentile(df_perf['bur_score_02'], 30)
        df_perf['aprova_bureau'] = df_perf['bur_score_02'] >= cutoff_bureau
        
        cutoff_modelo = np.percentile(df_perf['prob_modelo'], 70)
        df_perf['aprova_modelo'] = df_perf['prob_modelo'] <= cutoff_modelo

        swap_in_mask = (~df_perf['aprova_bureau']) & (df_perf['aprova_modelo'])
        swap_out_mask = (df_perf['aprova_bureau']) & (~df_perf['aprova_modelo'])

        n_swap_in = swap_in_mask.sum()
        br_swap_in = df_perf.loc[swap_in_mask, 'target'].mean() * 100 if n_swap_in > 0 else 0
        
        n_swap_out = swap_out_mask.sum()
        br_swap_out = df_perf.loc[swap_out_mask, 'target'].mean() * 100 if n_swap_out > 0 else 0

        bads_evitados = df_perf.loc[swap_out_mask, 'target'].sum()
        pct_swap_in = (n_swap_in / len(df_perf)) * 100
        pct_swap_out = (n_swap_out / len(df_perf)) * 100


        # ---------------------------------------------------------
        # 1. GRUPO CONTROLE & KPI DE BENCHMARK
        # ---------------------------------------------------------

        with st.expander("⚡ Performance do Modelo na Amostra (Real-Time)", expanded=True):

            excluir_controle = st.toggle("🔒 Excluir Grupo Controle da Avaliação de Performance", value=False)

            if excluir_controle:
                cpf_clean = df_perf['num_cpf'].astype(str).str.replace(r'[^a-zA-Z0-9]', '', regex=True).str.zfill(11).str.upper()
                mask_controle = cpf_clean.str[5:7].isin(['ZZ', 'ZX'])
                df_view = df_perf[~mask_controle].copy()
                label_amostra = f"Amostra Filtrada (Ex-Controle): <b>{len(df_view):,}</b> registros"
            else:
                df_view = df_perf.copy()
                label_amostra = f"Amostra Total (Sem Filtro): <b>{len(df_view):,}</b> registros"

            st.markdown(f"""
            <div style="background-color:#1A1A1A; padding:15px; border-radius:8px; border-left:4px solid #D4A017; margin-bottom:10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong style="color: #FFF;">Filtro de Grupo Controle</strong>
                    <span style="font-size: 12px; color: #D4A017; background: rgba(212, 160, 23, 0.1); padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(212, 160, 23, 0.2);">
                        {label_amostra}
                    </span>
                </div>
                <span style="font-size: 13px; color: #BBB;">Regra de identificação: 6º e 7º dígitos do CPF contendo combinações <b>ZZ</b> e <b>ZX</b>.</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("<hr style='margin-top:5px; margin-bottom:20px;'>", unsafe_allow_html=True)

            # =================================================================
            # 3. CÁLCULO DAS MÉTRICAS AO VIVO
            # =================================================================
            fpr, tpr, _ = roc_curve(df_view['target'], df_view['prob_modelo'])
            ks_live = max(tpr - fpr) * 100

            cutoff_bureau = np.nanpercentile(df_view['bur_score_02'], 30)
            df_view['aprova_bureau'] = df_view['bur_score_02'] >= cutoff_bureau
            cutoff_modelo = np.percentile(df_view['prob_modelo'], 70)
            df_view['aprova_modelo'] = df_view['prob_modelo'] <= cutoff_modelo

            swap_in_mask = (~df_view['aprova_bureau']) & (df_view['aprova_modelo'])
            swap_out_mask = (df_view['aprova_bureau']) & (~df_view['aprova_modelo'])

            n_swap_in = swap_in_mask.sum()
            br_swap_in = df_view.loc[swap_in_mask, 'target'].mean() * 100 if n_swap_in > 0 else 0
            n_swap_out = swap_out_mask.sum()
            br_swap_out = df_view.loc[swap_out_mask, 'target'].mean() * 100 if n_swap_out > 0 else 0

            bads_evitados = df_view.loc[swap_out_mask, 'target'].sum()
            pct_swap_in = (n_swap_in / len(df_view)) * 100 if len(df_view) > 0 else 0
            pct_swap_out = (n_swap_out / len(df_view)) * 100 if len(df_view) > 0 else 0

            # =================================================================
            # 4. RENDERIZAÇÃO DOS PAINÉIS ALINHADOS
            # =================================================================
            kpi_swap01, kpi_swap02 = st.columns([1, 2.5])
            ALTURA_CARD = "215px"

            with kpi_swap01:
                ks_bench = metadata.get('ks_bench', 33.1)
                delta_ks = ks_live - ks_bench
                cor_delta = "#5EA758" if delta_ks >= 0 else "#B53744"
                seta = "↑" if delta_ks >= 0 else "↓"

                st.markdown(f"""
                <div style="height: {ALTURA_CARD}; background: linear-gradient(145deg, #1A1C24, #262118); padding: 20px; border-radius: 10px; border-top: 4px solid #D4A017; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: flex; flex-direction: column;">
                    <h4 style="margin-top: 0; color: #D4A017;">🎯 KS do Modelo</h4>
                    <p style="font-size: 13px; color: #BBB; flex-grow: 1; margin-bottom: 0;">Poder de discriminação de risco calculado na amostra.</p>   
                    <div style="background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end;">
                        <div>
                            <span style="font-size: 2rem; font-weight: bold; color: #FFF; line-height: 1;">{ks_live:.1f}</span><br>
                            <span style="font-size: 12px; color: #888;">Benchmark: {ks_bench}</span>
                        </div>
                        <div style="text-align: right; margin-bottom: 2px;">
                            <div style="background-color: rgba(0,0,0,0.4); padding: 4px 8px; border-radius: 4px; border: 1px solid #333; display: inline-block;">
                                <span style="font-size: 13px; color: {cor_delta}; font-weight: bold;">{seta} {abs(delta_ks):.1f}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with kpi_swap02:
                st.markdown(f"""
                <div style="display: flex; gap: 20px;">
                    <div style="flex: 1; height: {ALTURA_CARD}; background: linear-gradient(145deg, #1A1C24, #1E2822); padding: 20px; border-radius: 10px; border-top: 4px solid #5EA758; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: flex; flex-direction: column;">
                        <h4 style="margin-top: 0; color: #5EA758;">🟩 Swap-In (Oportunidade)</h4>
                        <p style="font-size: 13px; color: #BBB; flex-grow: 1; margin-bottom: 0;">Clientes que seriam <b>reprovados</b> pelo Bureau, mas <b>aprovados</b> pelo Behavior Score.</p>
                        <div style="background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; margin-top: auto;">
                            <span style="font-size: 2rem; font-weight: bold; color: #FFF; line-height: 1;">{n_swap_in:,}</span> <span style="font-size: 13px; color: #888;">clientes ({pct_swap_in:.1f}%)</span><br>
                            <span style="font-size: 13px; color: #5EA758; font-weight:bold;">Bad Rate de {br_swap_in:.1f}%</span> <span style="font-size: 11px; color: #888;">(Risco controlado)</span>
                        </div>
                    </div>
                    <div style="flex: 1; height: {ALTURA_CARD}; background: linear-gradient(145deg, #1A1C24, #2A1A1C); padding: 20px; border-radius: 10px; border-top: 4px solid #B53744; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: flex; flex-direction: column;">
                        <h4 style="margin-top: 0; color: #B53744;">🟥 Swap-Out (Proteção)</h4>
                        <p style="font-size: 13px; color: #BBB; flex-grow: 1; margin-bottom: 0;">Clientes que seriam <b>aprovados</b> pelo Bureau, mas <b>reprovados</b> pelo Behavior Score.</p>
                        <div style="background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; margin-top: auto;">
                            <span style="font-size: 2rem; font-weight: bold; color: #FFF; line-height: 1;">{n_swap_out:,}</span> <span style="font-size: 13px; color: #888;">clientes ({pct_swap_out:.1f}%)</span><br>
                            <span style="font-size: 13px; color: #B53744; font-weight:bold;">Bad Rate de {br_swap_out:.1f}%</span> <span style="font-size: 11px; color: #888;">(Evitou {bads_evitados:,.0f} inadimplentes)</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # =================================================================
            # LÓGICA DE DIAGNÓSTICO DINÂMICO
            # =================================================================
            ks_status = "acima" if ks_live >= ks_bench else "abaixo"
            ks_cor = "#5EA758" if ks_live >= ks_bench else "#B53744"

            eficiencia_swap = br_swap_out - br_swap_in
            if eficiencia_swap > 0:
                swap_diag = f"ganho de qualidade de <b>{eficiencia_swap:.1f} p.p.</b> na troca de público"
                swap_conclusao = "confirmando a eficiência do modelo em substituir riscos elevados por oportunidades rentáveis."
            else:
                swap_diag = "atenção na calibração"
                swap_conclusao = "indicando que o público resgatado possui risco similar ou superior ao barrado. Recomenda-se revisar o cutoff."

            if ks_live >= ks_bench and eficiencia_swap > 0:
                header_str = "✅ DIAGNÓSTICO: ALTA PERFORMANCE"
                bg_opacity = "0.05"
                border_color = "rgba(94, 167, 88, 0.2)"
            else:
                header_str = "⚠️ DIAGNÓSTICO: NECESSITA ATENÇÃO"
                bg_opacity = "0.1"
                border_color = "rgba(212, 160, 23, 0.4)"

            # =================================================================
            # RENDERIZAÇÃO DO DISCLAIMER DINÂMICO
            # =================================================================
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, {bg_opacity}); border: 1px solid {border_color}; padding: 15px; border-radius: 8px; margin: 20px 0 20px 0;">
                <span style="color: {ks_cor}; font-weight: bold; font-size: 14px; letter-spacing: 0.5px;">{header_str}</span><br>
                <p style="font-size: 13.5px; color: #DDD; margin-top: 8px; line-height: 1.6; margin-bottom: 0;">
                    A análise da amostra {'<b>Ex-Controle</b>' if excluir_controle else '<b>Total</b>'} indica que o modelo opera com 
                    <span style="color: {ks_cor}; font-weight: bold;">KS de {ks_live:.1f}</span> (resultado {ks_status} do benchmark de {ks_bench}). 
                    Houve um {swap_diag}, {swap_conclusao}
                    A operação resultou na preservação de <b>{bads_evitados:,.0f} contratos</b> que resultariam em FPD (Bad Rate de {br_swap_out:.1f}% no Swap-Out).
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("<hr style='margin-top:5px; margin-bottom:20px;'>", unsafe_allow_html=True)


        with st.expander("📚 Construção do Modelo: KS Incremental por Fonte (Histórico)", expanded=True):

            st.markdown("""
            <div style="background-color:#1A1A1A; padding:15px; border-radius:8px; border-left:4px solid #455A64; margin-bottom:15px; display: flex; flex-direction: column;">
                <strong style="color: #FFF; font-size: 14px;">📸 Foto do Treinamento (Out-of-Time)</strong>
                <span style="font-size: 13px; color: #BBB; margin-top: 4px;">
                    Evolução do poder de separação aferido na documentação oficial de modelagem (OOT). Nota: Esta visão reflete a validação histórica do treinamento do modelo.
                </span>
            </div>
            """, unsafe_allow_html=True)

            metadata = assets.get('metadata', {})
            ks_bench = metadata.get('ks_bench', 33.1)
            ks_final_notebook = metadata.get('ks_oot', 32.71)
            
            fallback_steps = {
                'Bureau': 31.71,
                '+ Cadastral': 0.02,
                '+ Telco': -0.01,
                '+ Recarga': 0.82,
                '+ Pagamento': 0.09,
                '+ Atraso': 0.07
            }
            
            wf_steps = metadata.get('waterfall_steps', fallback_steps)

            x_labels = list(wf_steps.keys()) + ["KS Final (Treino)"]
            y_values = list(wf_steps.values()) + [ks_final_notebook]
            
            measures = ["relative"] * len(wf_steps) + ["total"]
            
            text_labels = [f"+{v:.2f}" if v > 0 else f"{v:.2f}" for v in wf_steps.values()] + [f"{ks_final_notebook:.2f}"]
            if text_labels and '+' in text_labels[0]:
                text_labels[0] = text_labels[0].replace('+', '')

            fig_wf = go.Figure(go.Waterfall(
                name="KS Incremental",
                orientation="v",
                measure=measures,
                x=x_labels,
                y=y_values,
                textposition="outside",
                text=text_labels,
                connector={"line": {"color": "#555", "width": 1.5, "dash": "dot"}},
                decreasing={"marker": {"color": "#B53744"}}, #
                increasing={"marker": {"color": "#5EA758"}}, 
                totals={"marker": {"color": "#D4A017"}}     
            ))

            fig_wf.update_layout(
                template="plotly_dark",
                height=380,
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Poder de Separação (KS)",
                font=dict(color="#BBB")
            )
            
            # Linha de Benchmark
            fig_wf.add_hline(
                y=ks_bench, 
                line_dash="dash", 
                line_color="#455A64", 
                annotation_text=f"Benchmark ({ks_bench})", 
                annotation_position="top left",
                annotation_font_color="#BBB"
            )
            
            st.plotly_chart(fig_wf, use_container_width=True)





    # ==============================================================================
    # SIMULADOR DE POLÍTICA
    # ==============================================================================
    elif view_mode == "🎯 Estratégia de Política":
        
        st.markdown(
            f"""
            <h3 style="font-weight:700; margin-bottom: 0px;">
                Estratégia de Política de Crédito - 
                <code class="theme-1" style="font-size: 1.2rem;">Release 1.0</code>
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.caption("🎯 Simulação, Otimização e Insights para Definição de Regras de Aprovação")
        st.write("<hr style='margin-top:-6.5px; margin-bottom:15px;'>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # CARREGAMENTO DA BASE & FILTROS GLOBAIS
        # ---------------------------------------------------------
        df_sim = df_master.copy()

        required_cols = ['bur_score_02', 'idade', 'pag_vlr_total_geral', 'target']
        missing = [c for c in required_cols if c not in df_sim.columns]
        if missing:
            st.error(f"Faltam colunas para o simulador: {missing}")
            st.stop()
            
        st.caption(f"📦 Volume da amostra (5% da base): **{len(df_sim):,} registros**")
        
        # =========================================================
        # CRIAÇÃO DAS ABAS
        # =========================================================
        tab_engine, tab_simulacao  = st.tabs(["⚖️ Policy Engine", "🎛️ Simulação"])


        # =========================================================
        # ABA 1: O SEU CÓDIGO ORIGINAL INTACTO
        # =========================================================
        with tab_simulacao:
            st.markdown("""
            <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px; margin-bottom: 15px;">
                <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">🧠 GUIA DE ESTRATÉGIA E SIMULAÇÃO</h6>
                <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
                <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">🎯 Sweet Spot:</strong>
                        <p style="margin-top:5px;">O algoritmo usa a métrica matemática KS (Kolmogorov-Smirnov) para varrer a <b>amostra</b> e encontrar o ponto exato que maximiza a aprovação de Bons Pagadores limitando a entrada de Maus Pagadores.</p>
                    </div>
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">🚧 Fronteira de Decisão:</strong>
                        <p style="margin-top:5px;">Visualiza os "Hard Cutoffs". A área verde representa os clientes que seriam aprovados com a política atual. Pontos cinzas são rejeitados.</p>
                    </div>
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">⚖️ Trade-off (Curva):</strong>
                        <p style="margin-top:5px;">Mostra a relação inversa: quanto mais exigente o Score (para a direita), menor o risco (linha vermelha cai), mas menor a aprovação (linha verde cai).</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🛠️ Simulador de Política de Crédito", expanded=True):
                
                c_params0, c_params1, c_params2, c_params3 = st.columns(4)

                with c_params0:
                    mode = st.radio("Modo de Definição:", ["Manual", "Sweet Spot"], horizontal=True)

                with c_params1:
                    min_idade = st.slider("Idade Mínima (Anos)", 18, 60, 18)

                with c_params2:     
                    min_pagto = st.slider("Pagamento Total Mínimo (R$)", 0, 1000, 0, step=50)

                with c_params3:
                    if mode == "Sweet Spot":

                        total_bons = (df_sim['target'] == 0).sum()
                        total_maus = (df_sim['target'] == 1).sum()
                        
                        best_ks = 0
                        sweet_spot = 300
                        
                        for c in np.arange(300, 901, 10):
                            mask = (
                                (df_sim["bur_score_02"] >= c) & 
                                (df_sim["idade"] >= min_idade) & 
                                (df_sim["pag_vlr_total_geral"].fillna(0) >= min_pagto)
                            ).fillna(False)
                            
                            aprovados_bons = ((df_sim['target'] == 0) & mask).sum()
                            aprovados_maus = ((df_sim['target'] == 1) & mask).sum()
                            
                            tpr = aprovados_bons / total_bons if total_bons > 0 else 0
                            fpr = aprovados_maus / total_maus if total_maus > 0 else 0
                            
                            ks = tpr - fpr
                            if ks > best_ks:
                                best_ks = ks
                                sweet_spot = c
                        
                        default_score = int(sweet_spot)
                    else:
                        default_score = 0

                    score_cutoff = st.slider(
                        "Score Mínimo (Bureau)", 
                        0, 1000, 
                        value=default_score,
                        disabled=(mode == "Sweet Spot")
                    )

                    query_aprovados = f"""
                        SELECT * FROM df_sim 
                        WHERE bur_score_02 >= {score_cutoff}
                        AND idade >= {min_idade}
                        AND COALESCE(pag_vlr_total_geral, 0) >= {min_pagto}
                    """
                    try:
                        aprovados_df = duckdb.query(query_aprovados).df()
                    except Exception:
                        aprovados_df = pd.DataFrame()
            
            curve_df = calculate_policy_curve(df_sim, min_idade, min_pagto)
            taxa_aprovacao = len(aprovados_df) / len(df_sim)
            bad_rate_atual = global_bad_rate_master
            bad_rate_novo = aprovados_df['target'].mean() if not aprovados_df.empty else 0.0
            reducao_risco = (bad_rate_atual - bad_rate_novo) / bad_rate_atual if bad_rate_atual > 0 else 0

            with st.expander("📊 Impacto Projetado na Carteira", expanded=True):
                k1, k2, k3 = st.columns(3)
                with k1:
                    vol_str = f"{len(aprovados_df):,.0f}".replace(",", ".")
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column;">
                            <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Taxa de Aprovação</p>
                            <div style="display: flex; align-items: baseline; gap: 8px;">
                                <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{taxa_aprovacao:.1%}</span>
                                <span style="font-size: 0.9rem; color: #888; font-weight: normal;">(N={vol_str})</span>
                            </div>
                            <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">% da amostra (exclui histórico nulo e < 18 anos)</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with k2:
                    diff_br = bad_rate_novo - bad_rate_atual
                    if diff_br <= 0:
                        cor_delta, seta = "#5EA758", "↓"
                    else:
                        cor_delta, seta = "#B53744", "↑"
                    val_fmt = f"{bad_rate_novo:.2%}"
                    delta_fmt = f"{seta} {abs(diff_br):.2%}"
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column;">
                            <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Bad Rate Esperado</p>
                            <div style="display: flex; align-items: baseline; gap: 8px;">
                                <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{val_fmt}</span>
                                <span style="font-size: 1rem; color: {cor_delta}; font-weight: bold;">{delta_fmt}</span>
                            </div>
                            <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Inadimplência do público aprovado</p>
                        </div>
                    """, unsafe_allow_html=True)

                with k3:
                    if reducao_risco > 0:
                        cor_delta_red, seta_red = "#5EA758", "↑"
                    else:
                        cor_delta_red, seta_red = "#B53744", "↓"
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column;">
                            <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Redução de Risco</p>
                            <div style="display: flex; align-items: baseline; gap: 8px;">
                                <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{reducao_risco:.1%}</span>
                                <span style="font-size: 1rem; color: {cor_delta_red}; font-weight: bold;">{seta_red} vs atual</span>
                            </div>
                            <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Queda relativa na inadimplência</p>
                        </div>
                    """, unsafe_allow_html=True)

                st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

                st.plotly_chart(
                    plot_decision_boundary(df_sim, score_cutoff, min_idade, min_pagto),
                    width='stretch'
                )
        
                st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

                # Mantido o seu gráfico de Trade-off
                st.plotly_chart(
                    plot_policy_tradeoff(curve_df, score_cutoff, sweet_spot if mode == "Sweet Spot" else None),
                    width='stretch'
                )



        with tab_engine:

            st.markdown("""
            <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px; margin-bottom: 15px;">
                <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">🧠 INTELIGÊNCIA ESTRATÉGICA E SEGMENTAÇÃO</h6>
                <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
                <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">📡 Motor de Clusterização - Identificação de Perfis Ocultos:</strong>
                        <p style="margin-top:5px;">Utiliza Machine Learning para agrupar clientes por similaridade de comportamento (Score, Idade, Pagamento), revelando "bolsões" de risco ocultos que filtros manuais não capturariam.</p>
                    </div>
                    <div style="flex:1; min-width: 200px;">
                        <strong style="color: #DDD;">⚖️ Policy Engine - Otimização Multiobjetivo da Estratégia:</strong>
                        <p style="margin-top:5px;">O motor avalia a <b>amostra completa</b> simulando centenas de políticas simultâneas para encontrar o equilíbrio matemático ideal entre crescimento de vendas e saúde financeira.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)




            # ---------------------------------------------------------
            # 1. EXTENDER DE SEGMENTAÇÃO (MACHINE LEARNING)
            # ---------------------------------------------------------
            with st.expander("📡 Motor de Clusterização - Identificação de Perfis Ocultos", expanded=True):
                st.caption("O motor agrupa a amostra para identificar padrões comuns de risco e oportunidade ocultos.")

                cluster_features = ["bur_score_02", "idade", "pag_vlr_total_geral"]
                df_cluster = df_sim[cluster_features].copy().fillna(0)
                
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(df_cluster)
                
                kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
                df_cluster["cluster"] = kmeans.fit_predict(X_scaled)
                df_cluster["target"] = df_sim["target"].values

                cluster_summary = (
                    df_cluster.groupby("cluster")
                    .agg(
                        clientes=("cluster", "count"), 
                        bad_rate=("target", "mean"),
                        score_medio=("bur_score_02", "mean"), 
                        idade_media=("idade", "mean"),
                        pagamento_medio=("pag_vlr_total_geral", "mean"),
                    ).reset_index()
                )
                cluster_summary["bad_rate"] *= 100

                col_bubble, col_insights = st.columns([6, 4])

                with col_bubble:
                    fig_cluster = px.scatter(
                        cluster_summary, x="score_medio", y="bad_rate", size="clientes", color="bad_rate",
                        text="cluster", color_continuous_scale="RdYlGn_r", title="Mapa de Segmentos de Risco"
                    )
                    fig_cluster.update_layout(template="plotly_dark", xaxis_title="Score Médio", height=320, yaxis_title="Bad Rate (%)", margin=dict(l=0, r=0, t=20, b=0))
                    st.plotly_chart(fig_cluster, use_container_width=True)

                with col_insights:
                    for _, row in cluster_summary.sort_values("bad_rate").iterrows():
                        risco = row["bad_rate"]
                        if risco < 15: tag, cor = "🟢 Baixo Risco", "#5EA758"
                        elif risco < 30: tag, cor = "🟡 Médio Risco", "#D4A017"
                        else: tag, cor = "🔴 Alto Risco", "#B53744"

                        st.markdown(f"""
                        <div style="background-color:#1A1A1A; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid {cor};">
                            <strong>Cluster {int(row['cluster'])} - {tag}</strong><br>
                            <span style="font-size: 0.85em; color: #BBB;">
                            Vol: {int(row['clientes']):,} | Score: {row['score_medio']:.0f} | Idade: {row['idade_media']:.0f}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)


            st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

            # ---------------------------------------------------------
            # 2. EXTENDER DE OTIMIZAÇÃO (POLICY ENGINE)
            # ---------------------------------------------------------
            with st.expander("⚖️ Policy Engine - Otimização Multiobjetivo da Estratégia", expanded=True):
                st.caption("Ajuste os pesos dos objetivos para que o motor de política identifique o Cutoff mais adequado à estratégia da empresa.")

                c1, c2, c3 = st.columns(3)
                with c1: w_growth = st.slider("Peso Crescimento (Aprovação)", 0.0, 1.0, 0.5, 0.05, key="ai_w1")
                with c2: w_risk = st.slider("Peso Risco (Inadimplência)", 0.0, 1.0, 0.5, 0.05, key="ai_w2")
                with c3: w_quality = st.slider("Peso Eficiência (Qualidade)", 0.0, 1.0, 0.5, 0.05, key="ai_w3")

                total_w = w_growth + w_risk + w_quality
                if total_w == 0: total_w = 1
                w_growth, w_risk, w_quality = w_growth/total_w, w_risk/total_w, w_quality/total_w

                policy_rows = []
                cutoffs = np.arange(300, 901, 10)

                for c in cutoffs:
                    mask = (df_sim["bur_score_02"] >= c).fillna(False)
                    approval = mask.mean()
                    bad_rate = df_sim.loc[mask, "target"].mean() if mask.sum() > 0 else np.nan
                    efficiency = approval * (1 - bad_rate) if pd.notna(bad_rate) else 0
                    policy_rows.append({"cutoff": c, "approval": approval, "bad_rate": bad_rate, "efficiency": efficiency})

                df_policy = pd.DataFrame(policy_rows).dropna()

                df_policy["approval_n"] = (df_policy["approval"] - df_policy["approval"].min()) / (df_policy["approval"].max() - df_policy["approval"].min() + 1e-9)
                df_policy["risk_n"] = (df_policy["bad_rate"].max() - df_policy["bad_rate"]) / (df_policy["bad_rate"].max() - df_policy["bad_rate"].min() + 1e-9)
                df_policy["eff_n"] = (df_policy["efficiency"] - df_policy["efficiency"].min()) / (df_policy["efficiency"].max() - df_policy["efficiency"].min() + 1e-9)
                
                df_policy["ai_score"] = (w_growth * df_policy["approval_n"] + w_risk * df_policy["risk_n"] + w_quality * df_policy["eff_n"])
                best_policy = df_policy.sort_values("ai_score", ascending=False).iloc[0]


                # =================================================================
                # LÓGICA DE DIAGNÓSTICO DA POLÍTICA (AI ENGINE)
                # =================================================================
                cutoff_sugerido = int(best_policy['cutoff'])
                aprovacao_estimada = best_policy['approval']
                risco_estimado = best_policy['bad_rate']

                if w_growth > w_risk:
                    perfil_estrategia = "EXPANSIVA (Foco em Market Share)"
                    perfil_cor = "#5EA758"
                    justificativa = "priorizando a aprovação de novos clientes e o crescimento da carteira."
                elif w_risk > w_growth:
                    perfil_estrategia = "CONSERVADORA (Foco em Rentabilidade)"
                    perfil_cor = "#B53744"
                    justificativa = "priorizando a blindagem contra inadimplência e a saúde da carteira."
                else:
                    perfil_estrategia = "EQUILIBRADA (Foco em Eficiência)"
                    perfil_cor = "#D4A017"
                    justificativa = "buscando o ponto ótimo entre volume de vendas e risco aceitável."

                # =================================================================
                # RENDERIZAÇÃO DO DIAGNÓSTICO DA ESTRATÉGIA
                # =================================================================
                st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(212, 160, 23, 0.2); padding: 15px; border-radius: 8px;">
                    <span style="color: {perfil_cor}; font-weight: bold; font-size: 14px; letter-spacing: 0.5px;">🎯 PARECER DO MODELO: {perfil_estrategia}</span><br>
                    <p style="font-size: 13.5px; color: #DDD; margin-top: 8px; line-height: 1.6; margin-bottom: 0;">
                        Com base na calibração atual, a política recomendada é o <span style="color: {perfil_cor}; font-weight: bold;">Cutoff {cutoff_sugerido}</span></b>, {justificativa}
                        Esta configuração projeta uma <b>taxa de aprovação de {aprovacao_estimada:.1%}</b> com uma 
                        <b>inadimplência esperada (FPD) de {risco_estimado:.1%}</b>. 
                        Este cenário maximiza o índice de aderência estratégica em relação aos objetivos de negócio definidos nos parâmetros acima.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.write("<hr style='margin-top:25px; margin-bottom:25px;'>", unsafe_allow_html=True)

                col_pareto, col_ranking = st.columns([6, 4])

                with col_pareto:
                    fig_pareto = px.scatter(
                        df_policy, 
                        x="approval", 
                        y="bad_rate", 
                        color="ai_score", 
                        size="ai_score",
                        hover_data=["cutoff", "ai_score"],
                        color_continuous_scale="RdYlGn",
                        title="Fronteira de Eficiência (Pareto)"
                    )
                    fig_pareto.update_layout(
                        height=350,
                        template="plotly_dark",
                        xaxis_title="Taxa de Aprovação",
                        yaxis_title="Inadimplência (FPD)",
                        coloraxis_colorbar=dict(title="Índice"),  # muda legenda da cor
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    fig_pareto.add_vline(x=best_policy["approval"], line_dash="dash", line_color="#4F1C22")
                    fig_pareto.add_hline(y=best_policy["bad_rate"], line_dash="dash", line_color="#4F1C22")
                    st.plotly_chart(fig_pareto, use_container_width=True)

                with col_ranking:
                    top_policies = df_policy.sort_values("ai_score", ascending=False).head(10)
                    
                    fig_top = go.Figure()

                    for i in range(len(top_policies)):
                        fig_top.add_shape(
                            type='line', x0=0, y0=i, x1=top_policies["ai_score"].iloc[i], y1=i,
                            line=dict(color='rgba(115, 30, 39, 0.5)', width=3)
                        )

                    fig_top.add_trace(go.Scatter(
                        x=top_policies["ai_score"],
                        y=top_policies["cutoff"].astype(str),
                        mode='markers+text',
                        marker=dict(color='#731E27', size=12),
                        text=[f"<b>{x:.4f}</b>" if i == 0 else f"{x:.4f}" for i, x in enumerate(top_policies["ai_score"])],
                        textposition="middle right",
                        name='Aderência',
                    ))

                    fig_top.update_layout(
                        template="plotly_dark",
                        title="Top 10 Cutoffs por Índice de Aderência",
                        xaxis_title="Índice de Aderência",
                        yaxis_title="Corte de Score",
                        height=350,
                        margin=dict(l=0, r=50, t=40, b=0),
                        xaxis=dict(range=[top_policies["ai_score"].min() - 0.01, top_policies["ai_score"].max() + 0.005])
                    )
                    st.plotly_chart(fig_top, use_container_width=True)

                with st.expander("🧾 Detalhamento Técnico das Políticas Avaliadas", expanded=False):

                    df_detalhe = df_policy[["ai_score", "cutoff", "approval", "bad_rate", "efficiency"]].sort_values(
                        ["ai_score", "efficiency"], ascending=[False, False]
                    )
                    
                    df_detalhe.columns = ["Índice de Aderência", "Corte (Score)", "Taxa Aprovação", "Inadimplência (FPD)", "Eficiência"]


                    styled_df = (
                        df_detalhe.style
                        .background_gradient(subset=["Índice de Aderência"], cmap="RdYlGn")      
                        .background_gradient(subset=["Inadimplência (FPD)"], cmap="RdYlGn_r")     
                        .background_gradient(subset=["Eficiência"], cmap="Blues")                  
                        .apply(lambda x: ["font-weight: bold" if x.name == 0 else "" for i in x], axis=1)
                        .set_properties(**{"text-align": "right"})
                        .format({
                            "Índice de Aderência": "{:.4f}",
                            "Taxa Aprovação": "{:.1%}",
                            "Inadimplência (FPD)": "{:.2%}",
                            "Eficiência": "{:.4f}"
                        })
                    )

                    st.dataframe(styled_df, use_container_width=True, hide_index=True)


    elif view_mode == "⚙️ Motor de Decisão":
        # ==========================================================
        # 1. CABEÇALHO DA PÁGINA
        # ==========================================================
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="font-weight:700; margin-bottom: 0px; color: #DAD0D1;">
                    Credit Risk Engine - <span style="color: #888; font-weight: 500;">Behavior Score</span>
                    <code style="font-size: 1rem; margin-left: 10px; background-color: #1A1C24; color: #5EA758; border: 1px solid #333; padding: 4px 8px; border-radius: 6px;">woe_v1.0</code> 
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        caminho = "models/behavior_baseline_woe_v1.pkl"
        st.caption(f"🛠️ **Modelo de Produção (Artefato):** `{caminho.split('/')[-1]}`")
        
        st.write("<hr style='margin-top:0px; margin-bottom:15px; border:1px solid #444;'>", unsafe_allow_html=True)

        # ==========================================================
        # 2. CARREGAMENTO DE ASSETS E TRATAMENTO DE ERROS
        # ==========================================================
        try:
            asset = load_assets()
            model = asset['model']
            encoder = asset['woe_encoder']
            features_raw = asset['features_raw'] 
            metadata = asset.get('metadata', {})
        except FileNotFoundError:
            st.error("⚠️ Modelo não encontrado localmente. Certifique-se de baixar o artefato da OCI/MLflow.")
            return
        except Exception as e:
            st.error(f"⚠️ Erro crítico ao carregar o modelo: {e}")
            return

        # ==========================================================
        # 3. METADADOS DO MODELO
        # ==========================================================
        with st.expander("🔍 Metadados do Modelo em Produção", expanded=False):
            st.markdown(f"""
                <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 5px;">
                    <div style="background-color: #1A1A1A; border-left: 4px solid #4F1C22; border-radius: 6px; padding: 12px 20px; flex: 1; min-width: 150px;">
                        <div style="font-size: 0.8rem; color: #999; text-transform: uppercase; font-weight: 600;">Versão</div>
                        <div style="font-size: 1.3rem; font-weight: 600; color: #FFF;">{metadata.get('version', 'N/A')}</div>
                    </div>
                    <div style="background-color: #1A1A1A; border-left: 4px solid #4F1C22; border-radius: 6px; padding: 12px 20px; flex: 1; min-width: 150px;">
                        <div style="font-size: 0.8rem; color: #999; text-transform: uppercase; font-weight: 600;">Algoritmo</div>
                        <div style="font-size: 1.3rem; font-weight: 600; color: #FFF;">{metadata.get('algorithm', 'LogisticRegression')}</div>
                    </div>
                    <div style="background-color: #1A1A1A; border-left: 4px solid #4F1C22; border-radius: 6px; padding: 12px 20px; flex: 1; min-width: 150px;">
                        <div style="font-size: 0.8rem; color: #999; text-transform: uppercase; font-weight: 600;">Data Treino</div>
                        <div style="font-size: 1.3rem; font-weight: 600; color: #FFF;">{metadata.get('created_at', 'N/A')}</div>
                    </div>
                    <div style="background-color: #1A1A1A; border-left: 4px solid #4F1C22; border-radius: 6px; padding: 12px 20px; flex: 1; min-width: 150px;">
                        <div style="font-size: 0.8rem; color: #999; text-transform: uppercase; font-weight: 600;">KS OOT / Gini OOT</div>
                        <div style="font-size: 1.3rem; font-weight: 600; color: #FFF;">{metadata.get('ks_oot', 0.0):.1f} <span style="font-size:1rem; color:#888;">/ {metadata.get('gini_oot', 0.0):.1f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.write("") 

        # ==========================================================
        # 4. ESTRUTURA PRINCIPAL (Formulário e Dashboard)
        # ==========================================================
        p1, p2 = st.columns([1, 1.4]) 
        
        with p1:
            with st.form("risk_form", clear_on_submit=False):
                st.markdown("<h4 style='margin-bottom: 10px; color: #DAD0D1;'>📝 Dados do Proponente</h4>", unsafe_allow_html=True)
                
                UI_CONFIG = {
                    'bur_score_02': {'label': 'Bureau Score 02', 'min': 0.0, 'max': 1000.0, 'default': 450.0, 'grupo': '🏛️ Bureau & Cadastro', 'help': 'Principal score de mercado'},
                    'bur_score_01': {'label': 'Bureau Score 01', 'min': 0.0, 'max': 1000.0, 'default': 500.0, 'grupo': '🏛️ Bureau & Cadastro', 'help': 'Score secundário'},
                    'cad_var_02': {'label': 'Tempo Residência (Meses)', 'min': 0.0, 'max': 360.0, 'default': 24.0, 'grupo': '🏛️ Bureau & Cadastro', 'help': ''},
                    
                    'rec_vlr_avg_geral': {'label': 'Vlr Médio Recarga (R$)', 'min': 0.0, 'max': 500.0, 'default': 35.0, 'grupo': '📱 Comportamento Recarga', 'help': ''},
                    'rec_dias_desde_ultima': {'label': 'Dias desde última recarga', 'min': 0.0, 'max': 365.0, 'default': 5.0, 'grupo': '📱 Comportamento Recarga', 'help': ''},
                    'rec_ratio_vlr_l30d_l60d': {'label': 'Razão Recarga L30/L60', 'min': 0.0, 'max': 10.0, 'default': 1.0, 'grupo': '📱 Comportamento Recarga', 'help': ''},
                    
                    'pag_dias_desde_ultimo_pagamento': {'label': 'Recência Pagamento (Dias)', 'min': 0.0, 'max': 365.0, 'default': 10.0, 'grupo': '💳 Pagamentos & Atrasos', 'help': ''},
                    'atr_vlr_acumulado_geral': {'label': 'Valor em Atraso (R$)', 'min': 0.0, 'max': 10000.0, 'default': 0.0, 'grupo': '💳 Pagamentos & Atrasos', 'help': ''},
                    'tel_var_28': {'label': 'Idade na Telco (Meses)', 'min': 0.0, 'max': 240.0, 'default': 12.0, 'grupo': '💳 Pagamentos & Atrasos', 'help': ''}
                }

                inputs = {}
                grupos_para_renderizar = {}
                
                for feat in features_raw:
                    config = UI_CONFIG.get(feat, {
                        'label': feat, 
                        'min': 0.0, 
                        'max': 100000.0, 
                        'default': 0.0, 
                        'grupo': '🔄 Novas Variáveis', 
                        'help': 'Variável adicionada na última versão'
                    })
                    
                    nome_grupo = config['grupo']
                    if nome_grupo not in grupos_para_renderizar:
                        grupos_para_renderizar[nome_grupo] = []
                    
                    grupos_para_renderizar[nome_grupo].append({'id': feat, **config})

                for nome_grupo, lista_feats in grupos_para_renderizar.items():
                    st.markdown(f"<div style='font-size: 0.9rem; font-weight: 600; color: #BBB; margin-top: 15px; margin-bottom: 5px; border-bottom: 1px dashed #444; padding-bottom: 5px;'>{nome_grupo}</div>", unsafe_allow_html=True)
                    cols = st.columns(2)
                    
                    for i, f_data in enumerate(lista_feats):
                        with cols[i % 2]: 
                            inputs[f_data['id']] = st.number_input(
                                label=f_data['label'], 
                                min_value=float(f_data['min']), 
                                max_value=float(f_data['max']), 
                                value=float(f_data['default']),
                                help=f_data['help'],
                                key=f"input_{f_data['id']}" 
                            )

                st.write("")
                submit_val = st.form_submit_button("🚀 PROCESSAR MOTOR", use_container_width=True)

        # ==========================================================
        # 5. PROCESSAMENTO E RESULTADOS 
        # ==========================================================
        if submit_val:
            try:
                df_input = pd.DataFrame([inputs])
                for col in features_raw:
                    if col not in df_input.columns:
                        df_input[col] = np.nan 
                df_input = df_input[features_raw]
                
                df_woe = encoder.transform(df_input, features_raw)
                woe_cols = [f'{col}_woe' for col in features_raw]
                X_model = df_woe[woe_cols].fillna(0) 
                
                prob = model.predict_proba(X_model)[:, 1][0]
                score = calculate_score(prob)
                tier, color_tier = get_risk_tier(score) # color_tier original
                
                decision = "APROVADO" if score >= 600 else "MESA DE CRÉDITO" if score >= 450 else "REPROVADO"
                
                decision_color = "#5EA758" if decision == "APROVADO" else "#D4A017" if decision == "MESA DE CRÉDITO" else "#B53744"
                
                cor_gauge_aprovado = "rgba(94, 167, 88, 0.2)"
                cor_gauge_mesa = "rgba(212, 160, 23, 0.2)"
                cor_gauge_reprovado = "rgba(181, 55, 68, 0.2)"

                with p2:
                    st.markdown(f"""
                    <div style="background-color: rgba(94, 167, 88, 0.1); border-left: 4px solid #5EA758; padding: 10px 15px; border-radius: 4px; margin-bottom: 20px;">
                        <span style="color: #5EA758; font-weight: 600; font-size: 14px;">✅ Análise Concluída com Sucesso.</span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<h4 style='color: #DAD0D1; margin-bottom: 15px;'>📊 Painel de Decisão</h4>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                            <div style="flex: 1; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid #455A64; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">PROBABILIDADE (PD)</div>
                                <div style="font-size: 1.8rem; font-weight: 700; color: #FFF;">{prob:.2%}</div>
                            </div>
                            <div style="flex: 1; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid {decision_color}; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">FAIXA DE RISCO</div>
                                <div style="font-size: 1.8rem; font-weight: 700; color: {decision_color};">{tier}</div>
                            </div>
                            <div style="flex: 1.2; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid {decision_color}; border-bottom: 1px solid {decision_color}40; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">DECISÃO DO MOTOR</div>
                                <div style="font-size: 1.5rem; font-weight: 700; color: {decision_color}; margin-top: 5px;">{decision}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    c_gauge, c_expl = st.columns([1, 1.2])
                    
                    with c_gauge:
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number", value=score,
                            title={'text': "Behavior Score", 'font': {'size': 16, 'color': '#BBB'}},
                            number={'font': {'size': 42, 'color': '#FFF'}},
                            gauge={
                                'axis': {'range': [0, 1000], 'tickwidth': 1, 'tickcolor': "#666"}, 
                                'bar': {'color': decision_color, 'thickness': 0.25},
                                'bgcolor': "#1A1C24",
                                'borderwidth': 0,
                                'steps': [
                                    {'range': [0, 450], 'color': cor_gauge_reprovado}, 
                                    {'range': [450, 600], 'color': cor_gauge_mesa}, 
                                    {'range': [600, 1000], 'color': cor_gauge_aprovado}
                                ]
                            }
                        ))
                        fig_gauge.update_layout(
                            height=280, 
                            margin=dict(l=20, r=20, t=40, b=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font={'family': "Inter, sans-serif"}
                        )
                        st.plotly_chart(fig_gauge, use_container_width=True)

                    # Explainability Chart Dark
                    with c_expl:
                        contributions = []
                        for feat, woe_col in zip(features_raw, woe_cols):
                            idx_feature = features_raw.index(feat)
                            coef = model.coef_[0][idx_feature]
                            val_woe = X_model[woe_col].values[0]
                            impact = coef * val_woe
                            nome_amigavel = UI_CONFIG.get(feat, {}).get('label', feat)
                            contributions.append({'Feature': nome_amigavel, 'Impacto': impact})
                        
                        df_contrib = pd.DataFrame(contributions).sort_values('Impacto', ascending=False)
                        
                        fig_expl = px.bar(
                            df_contrib, x='Impacto', y='Feature', orientation='h',
                            color='Impacto', color_continuous_scale='RdYlGn',
                            title="Drivers de Risco (Log-Odds)"
                        )
                        fig_expl.update_layout(
                            template="plotly_dark",
                            height=280, 
                            margin=dict(l=10, r=20, t=40, b=20),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            xaxis_title=None,
                            yaxis_title=None,
                            showlegend=False,
                            yaxis={'categoryorder':'total ascending'},
                            title_font=dict(size=14, color='#BBB')
                        )
                        st.plotly_chart(fig_expl, use_container_width=True)
                        
            except Exception as e:
                st.error(f"Erro no processamento do motor: {str(e)}")
        
        else:
            with p2:
                st.markdown("""
                    <div style="height: 650px; display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #1A1A1A; border: 2px dashed #444; border-radius: 12px; margin-top: 45px;">
                        <div style="background-color: #222; padding: 20px; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 20px;">
                            <span style="font-size: 3.5rem;">⚙️</span>
                        </div>
                        <h3 style="color:#FFF; margin-bottom: 5px;">Motor Aguardando Parâmetros</h3>
                        <p style="color:#BBB; font-size: 1.1rem; text-align: center; max-width: 400px;">
                            Preencha as informações do proponente no formulário ao lado e clique em <b>Processar Motor</b> para visualizar a decisão.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()