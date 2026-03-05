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
from catboost import CatBoostClassifier

# ==============================================================================
# 0. CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(
    page_title="SQUAD•03 - Painel de Análise e Decisão",
    page_icon="📈",
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
        process_demographics, 
        plot_age_analysis,   
        plot_geo_map,
        STATE_NAMES,
        STATE_COORDS,
        plot_tierizacao_financeira
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

# ==============================================================================
# CONTROLE DE MENU DIVIDIDO (SESSION STATE)
# ==============================================================================
grupo_diagnostico = [
    "👤 Geral | Análise de Dados",
    "📈 Performance & Benchmark",
    "💰 Impacto para o Negócio"
]

# Grupo 2: A inteligência de negócio
grupo_decisao = [
    "🎯 Estratégia de Política",
    "⚙️ Motor de Decisão"
]

if "view_mode" not in st.session_state:
    st.session_state.view_mode = grupo_diagnostico[0] 
    st.session_state.radio_analise = grupo_diagnostico[0]
    st.session_state.radio_intel = None 

def click_analise():
    if st.session_state.radio_analise is not None:
        st.session_state.view_mode = st.session_state.radio_analise
        st.session_state.radio_intel = None 

def click_intel():
    if st.session_state.radio_intel is not None:
        st.session_state.view_mode = st.session_state.radio_intel
        st.session_state.radio_analise = None 

st.sidebar.radio(
    "Análise:", 
    options=grupo_diagnostico,
    key="radio_analise",
    on_change=click_analise,
    label_visibility="visible" 
)

st.sidebar.write("<hr style='margin-top:-10px; margin-bottom:0px;'>", unsafe_allow_html=True)

st.sidebar.radio(
    "Decisão:",
    options=grupo_decisao,
    key="radio_intel",
    on_change=click_intel,
    label_visibility="visible"
)

view_mode = st.session_state.view_mode
# ==============================================================================

st.sidebar.write("<hr style='margin-top:-10px; margin-bottom:0px;'>", unsafe_allow_html=True)

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
    # 1. INGESTÃO CENTRALIZADA DE DADOS 
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

    try:
        assets = load_assets()
        feat_raw = assets['features_raw']
        X_all = df_master[feat_raw].apply(pd.to_numeric, errors='coerce').astype(float).fillna(0)
        probs_all = assets['model'].predict_proba(X_all)[:, 1]
        df_master['behavior_score'] = ((1 - probs_all) * 1000).astype(int)
    except:
        df_master['behavior_score'] = df_master.get('bur_score_02', pd.Series(0, index=df_master.index)).fillna(0)

    df_demo = prep_demographic_data(df_master)
    global_bad_rate_demo = df_demo['target'].mean()
    global_bad_rate_master = df_master['target'].mean()

# 1. Cria um "buraco negro" que engole o conteúdo antigo
    page_container = st.empty()

    # 2. Desenha o novo conteúdo DENTRO dele
    with page_container.container():

        if view_mode == "👤 Geral | Análise de Dados":

            st.markdown(
                f"""
                <h3 style="font-weight:700; margin-bottom: 0px;">
                    Visão Geral e Análise de Dados: Migração Pré para Controle - 
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

                with st.expander("📅 Evolução Temporal: Volume de Entrada & Risco Real", expanded=True):                      
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
                        sel_regiao = st.selectbox("1. Filtrar Região:", regioes_disponiveis, key="filtro_regiao")
                    
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
                            disabled=disabled_state,
                            key="filtro_estado"
                        )

                    with c_score:
                        min_score, max_score = st.slider(
                            "3. Faixa de Score (Behavior):",
                            0, 1000, (0, 1000)
                        )
                    
                    mask = pd.Series(True, index=df_demo.index)

                    if min_score > 0 or max_score < 1000:
                        mask &= df_demo['behavior_score'].between(min_score, max_score) 

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

                    ignored_cols = ['target', 'fpd', 'safra', 'num_cpf', 'cpf', 'behavior_score', 'prob_modelo']
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
                                index=0 ,
                                key="filtro_variavel_iv"
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

                ignored_cols = ['target', 'fpd', 'safra', 'num_cpf', 'cpf', 'behavior_score', 'prob_modelo']
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
                            var_x = st.selectbox("Eixo X (Variável 1):", valid_cols, index=idx_x, key="filtro_eixo_x")

                            idx_y = valid_cols.index('bur_score_01') if 'bur_score_01' in valid_cols else min(1, len(valid_cols)-1)
                            var_y = st.selectbox("Eixo Y (Variável 2):", valid_cols, index=idx_y, key="filtro_eixo_y")

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
                            df_features_only = df_master.drop(columns=['behavior_score', 'prob_modelo'], errors='ignore')
                            ranking_df = get_feature_ranking(df_features_only)
                            
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
                            cols_validas, key="filtro_variavel_psi",
                            index=cols_validas.index('bur_score_02') if 'bur_score_02' in cols_validas else 0 
                        )
                    
                    with c2:
                        safra_base = st.selectbox("📅 Safra de Referência (Base):", safras_disponiveis, index=0, key="filtro_base_psi")

                    with c3:
                        safra_atual = st.selectbox("📅 Safra em Análise (Atual):", safras_disponiveis, index=len(safras_disponiveis)-1, key="filtro_analise_psi")


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
        # IMPACTO PARA O NEGÓCIO (BUSINESS VALUATION DINÂMICO)
        # ==============================================================================
        elif view_mode == "💰 Impacto para o Negócio":
            
            st.markdown(
                f"""
                <h3 style="font-weight:700; margin-bottom: 0px;">
                    Impacto no Negócio - <span style="color: #888; font-weight: 500;">Behavior Score</span> -   
                    <code class="theme-1" style="font-size: 1.2rem;">Release 1.0</code>
                </h3>
                """,
                unsafe_allow_html=True
            )
            caminho_parquet = "base_escorada_swap_v1.parquet"
            st.caption(f"💰 **Impacto no Negócio** consolidado do Artefato do Lake: `{caminho_parquet}`")            
            st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)
            
            # ---------------------------------------------------------
            # 1. PREMISSAS DE NEGÓCIO (Do Notebook)
            # ---------------------------------------------------------
            ARPU_CONTROLE = 59.00
            ARPU_PRE = 39.59
            UPSELL = 19.41
            MESES_LTV = 12
            MESES_INADIMPLENCIA = 3
            CONVERSAO_ORGANICA = 0.0498 
            BASE_NACIONAL = 35_000_000 

            # ---------------------------------------------------------
            # 2. CARREGAMENTO DO ARTEFATO DO GRUPO CONTROLE
            # ---------------------------------------------------------
            df_biz = pd.DataFrame()
            with st.spinner("Buscando Base Escorada Oficial do Grupo Controle no Data Lake..."):
                try:
                    from config.data_connections import get_duckdb_connection
                    con_lake = get_duckdb_connection()
                    con_lake.execute("LOAD httpfs;") 
                    
                    path_swap = "s3://lake/observability/reports/run_id=*/modeling/v1/artifacts/base_escorada_swap_v1.parquet"
                    df_biz = con_lake.execute(f"SELECT target, bur_score_02, prob_modelo FROM read_parquet('{path_swap}')").df()
                
                except Exception as e:
                    st.error(f"Erro ao carregar o artefato de Swap do Lake: {e}")
                    st.stop()

            if df_biz.empty:
                st.warning("⚠️ A base de Controle retornou vazia.")
                st.stop()

            # ---------------------------------------------------------
            # 3. TOGGLE DE ESCALA E CONVERSÃO
            # ---------------------------------------------------------
            col_t1, col_t2 = st.columns([1, 1])

            with col_t1:

                usar_extrapolacao = st.toggle("🌎 Extrapolar para Escala Nacional (35M Clientes)", value=False)
                
                if usar_extrapolacao:
                    fator_escala = BASE_NACIONAL / len(df_biz)
                    label_escopo = "Projeção Nacional (35 Milhões de Clientes)"
                else:
                    fator_escala = 1.0
                    label_escopo = f"Grupo Controle ({len(df_biz):,} clientes)"
            
            with col_t2:
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; align-items: center; margin-top:8px;">
                        <span style="font-size: 12px; color: #BBB; background: rgba(255,255,255,0.05); padding: 3px 8px; border-radius: 4px; border: 1px solid #333;">
                            Escopo Ativo: <strong style="color: #FFF;">{label_escopo}</strong>
                        </span>
                    </div>
                """, unsafe_allow_html=True)

            # ----------------------------------------------------------------
            # 5. DASHBOARD SUPERIOR: CONCILIAÇÃO FINANCEIRA
            # ----------------------------------------------------------------
            with st.expander(f"Escopo Ativo: {label_escopo}", expanded=True):


                if usar_extrapolacao:
                    conversao_meta = st.slider("🎯 Taxa de Conversão Nacional Alvo (Marketing)", 1.0, 10.0, 3.0, 0.5) / 100
                else:
                    conversao_meta = st.slider("🎯 Conversão Orgânica Fixa (Grupo Controle)", 1.0, 10.0, float(CONVERSAO_ORGANICA*100), 0.01, disabled=True) / 100

                # ---------------------------------------------------------
                # 6. O MOTOR MATEMÁTICO DE RENTABILIDADE E TABELA DE VALOR
                # ---------------------------------------------------------
                df_biz['bur_score_02'] = df_biz.get('bur_score_02', pd.Series(0, index=df_biz.index)).fillna(0)
                df_biz['rank_bur'] = df_biz['bur_score_02'].rank(method='first', ascending=False)
                df_biz['rank_mod'] = df_biz['prob_modelo'].rank(method='first', ascending=True)

                percentis_alvo = [50, 60, 70, 75, 80, 85, 90]
                total_clientes = len(df_biz)
                cenarios_biz = []

                for pct in percentis_alvo:
                    n_aprov = int(total_clientes * (pct/100)) 
                    mask_bur = df_biz['rank_bur'] <= n_aprov
                    mask_mod = df_biz['rank_mod'] <= n_aprov
                    
                    # Réguas de Corte
                    cutoff_val_bur = df_biz.loc[df_biz['rank_bur'] == n_aprov, 'bur_score_02'].values[0] if n_aprov > 0 else 0
                    cutoff_val_mod = df_biz.loc[df_biz['rank_mod'] == n_aprov, 'prob_modelo'].values[0] if n_aprov > 0 else 0
                    
                    swap_in = (~mask_bur) & mask_mod
                    swap_out = mask_bur & (~mask_mod)
                    
                    in_goods = swap_in.sum() - df_biz.loc[swap_in, 'target'].sum()
                    in_bads = df_biz.loc[swap_in, 'target'].sum()
                    out_goods = swap_out.sum() - df_biz.loc[swap_out, 'target'].sum()
                    out_bads = df_biz.loc[swap_out, 'target'].sum()
                    
                    # Receita e Proteção Net (Líquida)
                    upsell_net = (in_goods - out_goods) * fator_escala * conversao_meta * UPSELL * MESES_LTV
                    pdd_net = (out_bads - in_bads) * fator_escala * conversao_meta * ARPU_CONTROLE * MESES_INADIMPLENCIA
                    ebitda_total = upsell_net + pdd_net

                    # Valores brutos para a Tabela de Comparação (Legado x Modelo)
                    bur_goods = mask_bur.sum() - df_biz.loc[mask_bur, 'target'].sum()
                    bur_bads = df_biz.loc[mask_bur, 'target'].sum()
                    rec_legado = (bur_goods * fator_escala * conversao_meta * UPSELL * MESES_LTV) - (bur_bads * fator_escala * conversao_meta * ARPU_CONTROLE * MESES_INADIMPLENCIA)
                    
                    mod_goods = mask_mod.sum() - df_biz.loc[mask_mod, 'target'].sum()
                    mod_bads = df_biz.loc[mask_mod, 'target'].sum()
                    rec_modelo = (mod_goods * fator_escala * conversao_meta * UPSELL * MESES_LTV) - (mod_bads * fator_escala * conversao_meta * ARPU_CONTROLE * MESES_INADIMPLENCIA)

                    cenarios_biz.append({
                        'Taxa de Aprovação': f"{pct}%",
                        'Régua Bureau': f"≥ {cutoff_val_bur:.0f}",
                        'Régua Modelo': f"≤ {cutoff_val_mod*100:.1f}%",
                        'Resultado Legado (12m)': rec_legado,
                        'Resultado Modelo (12m)': rec_modelo,
                        'GANHO LÍQUIDO': ebitda_total,
                        'Aprovacao_Num': pct,
                        'Upsell_Net': upsell_net,
                        'PDD_Net': pdd_net,
                        'EBITDA': ebitda_total
                    })

                df_report = pd.DataFrame(cenarios_biz)
                idx_otimo = df_report['EBITDA'].idxmax()
                dados_otimos = df_report.loc[idx_otimo]

                def format_moeda_kpi(v):
                    prefix = "-" if v < 0 else ""
                    v = abs(v)
                    if v >= 1e6: return f"{prefix}R$ {v/1e6:.2f}M"
                    elif v >= 1e3: return f"{prefix}R$ {v/1e3:.1f}k"
                    return f"{prefix}R$ {v:.0f}"

                def format_moeda_table(v):
                    prefix = "-" if v < 0 else ""
                    v = abs(v)
                    if v >= 1e6: return f"{prefix}R$ {v/1e6:.2f}M"
                    elif v >= 1e3: return f"{prefix}R$ {v/1e3:.1f}k" # Adicionado formatação em 'k'
                    return f"{prefix}R$ {v:.0f}"

                col_big1, col_big2, col_big3 = st.columns(3)
                with col_big1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #182B3A); padding: 20px; border-radius: 8px; border-top: 3px solid #1565C0; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.85rem; color: #999; font-weight: 600;">GERAÇÃO DE RECEITA (UPSELL LÍQUIDO)</div>
                        <div style="font-size: 2.2rem; font-weight: bold; color: #42A5F5; margin: 10px 0;">{format_moeda_kpi(dados_otimos['Upsell_Net'])}</div>
                        <div style="font-size: 0.75rem; color: #888;">LTV 12m dos bons clientes resgatados</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_big2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #1B3A1C); padding: 20px; border-radius: 8px; border-top: 3px solid #43A047; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.85rem; color: #999; font-weight: 600;">EFICIÊNCIA DE RISCO (PDD POUPADA)</div>
                        <div style="font-size: 2.2rem; font-weight: bold; color: #66BB6A; margin: 10px 0;">{format_moeda_kpi(dados_otimos['PDD_Net'])}</div>
                        <div style="font-size: 0.75rem; color: #888;">3 meses de ARPU salvos dos maus barrados</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_big3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #262118); padding: 20px; border-radius: 8px; border-top: 3px solid #D4A017; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.85rem; color: #999; font-weight: 600;">EBITDA INCREMENTAL TOTAL</div>
                        <div style="font-size: 2.2rem; font-weight: bold; color: #FFF; margin: 10px 0;">{format_moeda_kpi(dados_otimos['EBITDA'])}</div>
                        <div style="font-size: 0.75rem; color: #888;">No Corte Campeão de {dados_otimos['Taxa de Aprovação']} de Aprovação</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("<hr style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)

                # ----------------------------------------------------------------
                # 6. GRÁFICOS INFERIORES: TABELA DE RENTABILIDADE E BRIDGE
                # ----------------------------------------------------------------
                c_g1, c_g2 = st.columns([1.5, 1])

                with c_g1:
                    st.markdown("<p style='font-size: 16px; font-weight: 600; color: #FFF; margin-bottom: 10px;'>Rentabilidade Líquida da Campanha: Visão de Valor (LTV)</p>", unsafe_allow_html=True)
                    
                    label_ganho = "GANHO LÍQUIDO (ESCALA 12m)" if usar_extrapolacao else "GANHO LÍQUIDO (HOLD-OUT 12m)"
                    
                    df_table = df_report[['Taxa de Aprovação', 'Régua Bureau', 'Régua Modelo', 'Resultado Legado (12m)', 'Resultado Modelo (12m)', 'GANHO LÍQUIDO']].copy()
                    df_table.rename(columns={'GANHO LÍQUIDO': label_ganho}, inplace=True)
                    
                    for col in ['Resultado Legado (12m)', 'Resultado Modelo (12m)', label_ganho]:
                        df_table[col] = df_table[col].apply(format_moeda_table)
                        
                    def highlight_optimal(s):
                        if s.name == idx_otimo:
                            return ['background-color: #5EA758; color: #333; font-weight: bold'] * len(s)
                        return ['background-color: rgba(255,255,255,0.05)'] * len(s)

                    st.dataframe(
                        df_table.style.apply(highlight_optimal, axis=1),
                        use_container_width=True,
                        hide_index=True
                    )

                with c_g2:
                    st.markdown("<p style='font-size: 16px; font-weight: 600; color: #FFF; margin-bottom: 10px;'>Bridge de EBITDA (A Composição do Valor)</p>", unsafe_allow_html=True)
                    
                    fig_bridge = go.Figure(go.Waterfall(
                        name="Bridge", orientation="v", measure=["relative", "relative", "total"],
                        x=["Geração de Receita<br>(Upsell Líquido)", "Eficiência de Risco<br>(PDD Protegida)", "Impacto Líquido<br>(EBITDA Incremental)"],
                        y=[dados_otimos['Upsell_Net'], dados_otimos['PDD_Net'], 0],
                        text=[format_moeda_kpi(dados_otimos['Upsell_Net']), format_moeda_kpi(dados_otimos['PDD_Net']), format_moeda_kpi(dados_otimos['EBITDA'])],
                        textposition="outside",
                        connector={"line": {"color": "#666", "width": 2, "dash":"dot"}},
                        increasing={"marker": {"color": "#1565C0"}}, 
                        decreasing={"marker": {"color": "#C62828"}}, 
                        totals={"marker": {"color": "#5EA758"}}
                    ))

                    fig_bridge.update_layout(
                        template="plotly_dark", height=290, margin=dict(l=20, r=20, t=0, b=0),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        yaxis_title="Valor Financeiro Incremental (R$)"
                    )
                    
                    if usar_extrapolacao:
                        fig_bridge.add_annotation(x=2, y=dados_otimos['EBITDA'], text=f"Calculado com Conversão de {conversao_meta*100:.1f}%", showarrow=False, yshift=45, font=dict(color="#D4A017", size=11))
                    else:
                        fig_bridge.add_annotation(x=2, y=dados_otimos['EBITDA'], text=f"Calculado com Conversão Orgânica {CONVERSAO_ORGANICA*100:.2f}%", showarrow=False, yshift=35, font=dict(color="#D4A017", size=11))


                    st.plotly_chart(fig_bridge, use_container_width=True)
                    
                st.markdown(f"""
                <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 10px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                    <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">📋 Dicionário de Premissas Financeiras:</h6>
                    <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
                    <ul style="margin-top:10px; margin-bottom:0; padding-left: 10px; line-height: 1.5;">
                        <li style="margin-top:5px;"><strong>ARPU Controle: R$ {ARPU_CONTROLE:.2f}</strong> - <i>AVG(pagamento_fatura) | Filtro: RR 5,00 < val < R$ 300,00</li>
                        <li style="margin-top:5px;"><strong>ARPU Pré: R$ {ARPU_PRE:.2f}</strong> - <i>AVG(SUM(recarga) por CPF/Mês) | Filtro: PREPG</li>
                        <li style="margin-top:5px;"><strong>Upsell Incremental: R$ {UPSELL:.2f}</strong> - <i>ARPU Controle - ARPU Pré</li>
                        <li style="margin-top:5px;"><strong>LTV Considerado: {MESES_LTV} meses</strong> - <i>Multiplicador fixo baseado na regra contábil de LTV</li>
                        <li style="margin-top:5px;"><strong>Loss/PDD: {MESES_INADIMPLENCIA} meses</strong> - <i>Média de meses para provisionamento de PDD</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                st.write("")




# ==============================================================================
# PERFORMANCE & BENCHMARK (ESTÁTICO DO PKL - OFICIAL DO NOTEBOOK)
# ==============================================================================
        elif view_mode == "📈 Performance & Benchmark":
            
            st.markdown(
                f"""
                <h3 style="font-weight:700; margin-bottom: 0px;">
                    Avaliação de Performance e Benchmark - <span style="color: #888; font-weight: 500;">Behavior Score</span> -  
                    <code class="theme-1" style="font-size: 1.2rem;">model_v1.0</code>
                </h3>
                """,
                unsafe_allow_html=True
            )
            caminho = "models/behavior_catboost_v1.pkl"
            st.caption(f"🔬 **Validação Científica Oficial** extraída do Artefato MLOps: `{caminho.split('/')[-1]}`")
            st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

            # ---------------------------------------------------------
            # 1. LEITURA DOS METADADOS DO MODELO (SEM INFERÊNCIA PESADA)
            # ---------------------------------------------------------
            try:
                assets = load_assets()
                metadata = assets.get('metadata', {})
                
                # Resgate seguro dos KPIs OOT (Out-of-Time)
                ks_oot = metadata.get('ks_oot', 34.53)
                gini_oot = metadata.get('gini_oot', 46.60)
                psi_oot = metadata.get('psi_oot', 0.0010)
                ks_bench = metadata.get('ks_bench', 33.1)
                
                # Resgate seguro dos Swaps (Grupo Controle)
                swap_in_vol = metadata.get('swap_in_vol', 6837)
                swap_in_pct = metadata.get('swap_in_pct', 6.2)
                swap_in_br = metadata.get('swap_in_br', 32.88)
                
                swap_out_vol = metadata.get('swap_out_vol', 7066)
                swap_out_pct = metadata.get('swap_out_pct', 6.4)
                swap_out_br = metadata.get('swap_out_br', 52.12)
                bads_evitados = metadata.get('bads_evitados', 3683)

            except Exception as e:
                st.error(f"Erro ao ler metadados do modelo: {e}")
                st.stop()

            # ----------------------------------------------------------------
            # 2. PAINEL EXECUTIVO: MÉTRICAS OFICIAIS (OOT + CONTROLE)
            # ----------------------------------------------------------------
            st.markdown("""
                <div style="background-color:#1A1A1A; padding:15px; border-radius:8px; border-left:4px solid #4F1C22; margin-bottom:15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #FFF; font-size: 14px;">🔬 Escopo da Validação (Dados Oficiais do Treinamento)</strong>
                        <span style="font-size: 12px; color: #BBB; background: rgba(255,255,255,0.05); padding: 3px 8px; border-radius: 4px; border: 1px solid #333;">
                            Volume Processado: <strong style="color: #FFF;">2.633.900</strong> CPFs
                        </span>
                    </div>
                    <div style="font-size: 13.5px; color: #BBB; margin-top: 10px; line-height: 1.6;">
                        <div style="margin-bottom: 4px;">
                            • <b>Desenvolvimento (Out/24 a Jan/25):</b> Treino e Teste Out-of-Sample para calibração do algoritmo.
                            <span style="color: #999; background-color: rgba(255, 255, 255, 0.05); padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 5px; border: 1px solid #444;">N = 1.362.431 (Treino)</span>
                            <span style="color: #999; background-color: rgba(255, 255, 255, 0.05); padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 2px; border: 1px solid #444;">N = 340.608 (Teste)</span>
                        </div>
                        <div style="margin-bottom: 4px;">
                            • <b>Métricas de Separação (KS/Gini):</b> Aferidas sobre a Safra OOT <b>(Fev/25 a Mar/25)</b> atestando generalização no tempo.
                            <span style="color: #D4A017; background-color: rgba(212, 160, 23, 0.15); padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 5px; border: 1px solid rgba(212, 160, 23, 0.3);">N = 820.593 (OOT)</span>
                        </div>
                        <div>
                            • <b>Métricas de Negócio (Swap):</b> Aferidas sobre o Grupo Controle <b>(Holdout ZZ/ZX)</b> isento de viés.
                            <span style="color: #5EA758; background-color: rgba(94, 167, 88, 0.15); padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 5px; border: 1px solid rgba(94, 167, 88, 0.3);">N = 110.268 (Controle)</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("⚡ Performance do Modelo: Estabilidade Temporal e Eficiência", expanded=True):

                # Fileira 1: KPIs Oficiais
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    delta_ks = ks_oot - ks_bench
                    cor_delta = "#5EA758" if delta_ks >= 0 else "#B53744"
                    seta = "↑" if delta_ks >= 0 else "↓"
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid #D4A017; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">KS (SEPARAÇÃO OOT)</div>
                        <div style="display: flex; align-items: baseline; gap: 8px;">
                            <span style="font-size: 1.8rem; font-weight: 700; color: #FFF;">{ks_oot:.2f}%</span>
                            <span style="font-size: 0.9rem; color: {cor_delta}; font-weight: bold;">{seta} {abs(delta_ks):.2f}pp</span>
                        </div>
                        <div style="font-size: 0.75rem; color: #888;">Benchmark: {ks_bench:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid #455A64; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">GINI (ORDENAÇÃO OOT)</div>
                        <div style="font-size: 1.8rem; font-weight: 700; color: #FFF;">{gini_oot:.2f}%</div>
                        <div style="font-size: 0.75rem; color: #888;">Poder de Discriminação Real</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    status_psi = "Estável" if psi_oot < 0.1 else "Atenção" if psi_oot < 0.25 else "Drift"
                    cor_psi = "#5EA758" if psi_oot < 0.1 else "#D4A017" if psi_oot < 0.25 else "#B53744"
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid {cor_psi}; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">PSI (ESTABILIDADE)</div>
                        <div style="display: flex; align-items: baseline; gap: 8px;">
                            <span style="font-size: 1.8rem; font-weight: 700; color: #FFF;">{psi_oot:.4f}</span>
                            <span style="font-size: 0.9rem; color: {cor_psi}; font-weight: bold;">{status_psi}</span>
                        </div>
                        <div style="font-size: 0.75rem; color: #888;">Degradação Temporal (Train/OOT)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col4:
                    eficiencia_swap = swap_out_br - swap_in_br
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid #2196F3; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">REDUÇÃO DE FPD (SWAP)</div>
                        <div style="display: flex; align-items: baseline; gap: 8px;">
                            <span style="font-size: 1.8rem; font-weight: 700; color: #FFF;">{eficiencia_swap:.2f}pp</span>
                        </div>
                        <div style="font-size: 0.75rem; color: #888;">Geração de Valor no Controle</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.write("")

                # Fileira 2: Os Cards de Swap (Grupo Controle)
                ALTURA_CARD = "215px"
                kpi_swap01, kpi_swap02 = st.columns([1, 1])

                with kpi_swap01:
                    st.markdown(f"""
                    <div style="height: {ALTURA_CARD}; background: linear-gradient(145deg, #1A1C24, #1E2822); padding: 20px; border-radius: 10px; border-top: 4px solid #5EA758; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: flex; flex-direction: column;">
                        <h4 style="margin-top: 0; color: #5EA758;">🟩 Swap-In (Oportunidade)</h4>
                        <p style="font-size: 13px; color: #BBB; flex-grow: 1; margin-bottom: 0;">Clientes do <b>Grupo Controle</b> que seriam reprovados pelo mercado, mas resgatados pelo Behavior Score.</p>
                        <div style="background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; margin-top: auto;">
                            <span style="font-size: 2.2rem; font-weight: bold; color: #FFF; line-height: 1;">{int(swap_in_vol):,}</span> <span style="font-size: 14px; color: #888;">({swap_in_pct:.1f}% da base)</span><br>
                            <span style="font-size: 14px; color: #5EA758; font-weight:bold;">Bad Rate Real de {swap_in_br:.2f}%</span> <span style="font-size: 12px; color: #888;">(Risco absorvido com segurança)</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with kpi_swap02:
                    st.markdown(f"""
                    <div style="height: {ALTURA_CARD}; background: linear-gradient(145deg, #1A1C24, #2A1A1C); padding: 20px; border-radius: 10px; border-top: 4px solid #B53744; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: flex; flex-direction: column;">
                        <h4 style="margin-top: 0; color: #B53744;">🟥 Swap-Out (Proteção)</h4>
                        <p style="font-size: 13px; color: #BBB; flex-grow: 1; margin-bottom: 0;">Inadimplentes latentes do <b>Grupo Controle</b> que o Bureau aprovaria, mas o Behavior Score barrou.</p>
                        <div style="background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; margin-top: auto;">
                            <span style="font-size: 2.2rem; font-weight: bold; color: #FFF; line-height: 1;">{int(swap_out_vol):,}</span> <span style="font-size: 14px; color: #888;">({swap_out_pct:.1f}% da base)</span><br>
                            <span style="font-size: 14px; color: #B53744; font-weight:bold;">Bad Rate Real de {swap_out_br:.2f}%</span> <span style="font-size: 12px; color: #888;">(Evitou {int(bads_evitados):,} FPDs diretos)</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")

            # ----------------------------------------------------------------
            # 3. TABELA & GRÁFICO: KS INCREMENTAL (Exatamente como no Notebook)
            # ----------------------------------------------------------------
            with st.expander("📚 A Jornada de Modelagem: Valor Adicionado por Fonte (OOT)", expanded=True):
                
                tab_ks_01, tab_ks_02  = st.tabs(["📈 Evolução Incremental do KS", "📊 Tabela de Ganhos"])

                # Estrutura de dados
                incremental_data = [
                    {"Bloco": "Score 1", "Features": 1, "KS_OOT": 26.10, "Delta_KS": 26.10},
                    {"Bloco": "Score 2", "Features": 2, "KS_OOT": 30.71, "Delta_KS": 4.60},
                    {"Bloco": "Telco", "Features": 11, "KS_OOT": 30.94, "Delta_KS": 0.24},
                    {"Bloco": "Cadastro", "Features": 16, "KS_OOT": 31.19, "Delta_KS": 0.25},
                    {"Bloco": "Recarga", "Features": 41, "KS_OOT": 34.01, "Delta_KS": 2.82},
                    {"Bloco": "Pagamento e Atraso", "Features": 62, "KS_OOT": 34.46, "Delta_KS": 0.45}
                ]

                df_incr = pd.DataFrame(incremental_data)

                with tab_ks_02:

                    df_incr['Status'] = df_incr['KS_OOT'].apply(lambda x: "🚀 BATEU BENCHMARK!" if x >= ks_bench else "")
                    
                    df_tab = df_incr.copy()
                    df_tab.rename(columns={'Bloco': 'Bloco Adicionado', 'Features': 'Nº Features Acumuladas', 'KS_OOT': 'KS Acumulado (OOT)'}, inplace=True)
                    df_tab['Delta_KS'] = df_tab.apply(lambda row: f"+{row['Delta_KS']:.2f}pp" if row.name > 0 else f"{row['Delta_KS']:.2f}%", axis=1)
                    df_tab['KS Acumulado (OOT)'] = df_tab['KS Acumulado (OOT)'].apply(lambda x: f"{x:.2f}%")
                    
                    st.dataframe(
                        df_tab.style.apply(lambda x: ['color: #5EA758; font-weight: bold' if "🚀" in str(v) else '' for v in x], subset=['Status'])
                                    .apply(lambda x: ['background-color: rgba(255,255,255,0.05)' if i%2==0 else '' for i in range(len(x))]),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with tab_ks_01:
                    
                    fig_inc = make_subplots(specs=[[{"secondary_y": True}]])
                    colors_inc = [COLORS['good'] if d > 0 else COLORS['bad'] for d in df_incr['Delta_KS']]
                    
                    fig_inc.add_trace(go.Bar(
                        x=df_incr['Bloco'], 
                        y=df_incr['Delta_KS'], 
                        name='Delta KS Marginal', 
                        marker_color=colors_inc, 
                        text=df_incr['Delta_KS'].apply(lambda x: f'+{x:.2f}pp'), 
                        textposition='outside'
                    ), secondary_y=False)
                    
                    fig_inc.add_trace(go.Scatter(
                        x=df_incr['Bloco'], 
                        y=df_incr['KS_OOT'], 
                        mode='lines+markers+text', 
                        name='KS Acumulado OOT (%)', 
                        marker=dict(symbol='diamond', size=12, color='#1f77b4'), 
                        line=dict(width=3, color='#1f77b4'),
                        text=df_incr['KS_OOT'].apply(lambda x: f'{x:.2f}%'), 
                        textposition='top center'
                    ), secondary_y=True)
                    
                    fig_inc.add_hline(
                        y=ks_bench, 
                        line_dash="dash", 
                        line_color="#1f77b4", 
                        secondary_y=True,
                        annotation_text=f"Benchmark ({ks_bench}%)", 
                        annotation_position="bottom right",
                        annotation_font_color="#BBB",
                        annotation_yshift=-195
                    )

                    fig_inc.update_layout(
                        template='plotly_dark', 
                        height=450, 
                        margin=dict(l=20, r=0, t=0, b=0),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation="h", yanchor="bottom", y=0.90, xanchor="center", x=0.835)
                    )

                    fig_inc.update_yaxes(
                        title_text="Delta KS Marginal (pp)", 
                        secondary_y=False, 
                        showgrid=False, 
                        range=[-2, max(df_incr['Delta_KS'])+8]
                    )
                    
                    fig_inc.update_yaxes(
                        title_text="KS Acumulado OOT (%)", 
                        secondary_y=True, 
                        showgrid=True, 
                        gridcolor='rgba(255,255,255,0.1)', 
                        range=[20, 45]
                    )
                    
                    fig_inc.update_yaxes(title_text="Delta KS Marginal (pp)", secondary_y=False, range=[-2, max(df_incr['Delta_KS'])+8])
                    fig_inc.update_yaxes(title_text="KS Acumulado OOT (%)", secondary_y=True, range=[20, 45])
                    
                    st.plotly_chart(fig_inc, use_container_width=True)

                st.markdown("""
                <div style="background-color:#1A1A1A; padding:15px; border-radius:8px; border-left:4px solid #4F1C22; margin-top:0px; margin-bottom:10px; display: flex; flex-direction: column;">
                    <span style="font-size: 13.5px; color: #BBB;">
                        Dados extraídos da validação OOT. Demonstra o salto de performance e o peso informacional real de cada bloco de dados interno da Claro para superar o benchmark sem depender de variáveis sensíveis (ESG).
                    </span>
                </div>
                """, unsafe_allow_html=True)


# ==============================================================================
# SIMULADOR DE POLÍTICA (INTEGRADO AO MODELO DE PRODUÇÃO)
# ==============================================================================
        elif view_mode == "🎯 Estratégia de Política":
            
            st.markdown(
                f"""
                <h3 style="font-weight:700; margin-bottom: 0px;">
                    Estratégia de Política de Crédito - <span style="color: #888; font-weight: 500;">Behavior Score</span> - 
                    <code class="theme-1" style="font-size: 1.2rem;">Release 1.0</code>
                </h3>
                """,
                unsafe_allow_html=True
            )
            caminho = "models/behavior_catboost_v1.pkl"
            st.caption(f"⚖️ **Simulação e Otimização Estratégica** tracionadas pelo Artefato MLOps: `{caminho.split('/')[-1]}`")
            
            st.write("<hr style='margin-top:-6.5px; margin-bottom:-30px;'>", unsafe_allow_html=True)
            
            # ---------------------------------------------------------
            # 1. CARREGAMENTO DA BASE, ASSETS E ESCORAGEM OFICIAL
            # ---------------------------------------------------------
            df_sim = df_master.copy() 
            
            try:
                assets = load_assets()
                model_pkl = assets['model']
                feat_raw = assets['features_raw']
                metadata = assets.get('metadata', {})
                
                for col in feat_raw:
                    if col not in df_sim.columns:
                        df_sim[col] = np.nan
                        
                X_sim = df_sim[feat_raw].apply(pd.to_numeric, errors='coerce').astype(float).fillna(0)
                probs = model_pkl.predict_proba(X_sim)[:, 1]
                df_sim['behavior_score'] = ((1 - probs) * 1000).astype(int)
                
            except Exception as e:
                st.warning(f"⚠️ Operando em modo de contingência (sem modelo .pkl). Erro: {e}")
                if 'behavior_score' not in df_sim.columns:
                    df_sim['behavior_score'] = df_sim.get('bur_score_02', pd.Series(0, index=df_sim.index)).fillna(0)

            required_cols = ['behavior_score', 'idade', 'rec_vlr_total_l90d', 'target']
            missing = [c for c in required_cols if c not in df_sim.columns]

            if missing:
                st.error(f"Faltam colunas obrigatórias na ABT para o motor: {missing}")
                st.stop()

            # ---------------------------------------------------------
            # 2. CONTROLE DE NAVEGAÇÃO INTERNA
            # ---------------------------------------------------------
            aba_selecionada = st.radio(
                "Navegação:",
                ["🎯 Direcionamento Estratégico", "⚙️ Simulação de Política", "📡 Perfis de Risco"],
                horizontal=True,
                label_visibility="collapsed", 
                key="abas_estrategia_politica" 
            )
            st.write("<hr style='margin-top:-10px; margin-bottom:15px;'>", unsafe_allow_html=True)



            # =========================================================
            # SUB-ABA 1: DIRECIONAMENTO ESTRATÉGICO (PARETO)
            # =========================================================
            if aba_selecionada == "🎯 Direcionamento Estratégico":
                
                st.markdown("""
                <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px; margin-bottom: 15px;">
                    <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">⚖️ Motor de Otimização: Balanço entre Risco e Crescimento</h6>
                    <hr style="margin-top:0px; margin-bottom:5px; border:1px solid #444;">
                    <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                        <div style="flex:1; min-width: 200px;">
                            <p style="margin-top:5px;">O motor avalia a <b>amostra completa</b> simulando centenas de políticas simultâneas para encontrar o equilíbrio matemático ideal entre crescimento de vendas e saúde financeira. Ajuste os pesos dos objetivos abaixo para que o algoritmo identifique o ponto de corte mais adequado à estratégia atual da empresa.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("⚙️ Painel de Calibração: Definir Pesos Estratégicos", expanded=True):

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
                        mask = (df_sim["behavior_score"] >= c).fillna(False)
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

                    cutoff_sugerido = int(best_policy['cutoff'])
                    aprovacao_estimada = best_policy['approval']
                    risco_estimado = best_policy['bad_rate']
                    
                    # Consistência com o get_risk_tier do modelo principal
                    if cutoff_sugerido >= 800: tier_sug = "A (Premium)"
                    elif cutoff_sugerido >= 600: tier_sug = "B (Seguro)"
                    elif cutoff_sugerido >= 400: tier_sug = "C (Standard)"
                    elif cutoff_sugerido >= 200: tier_sug = "D (Atenção)"
                    else: tier_sug = "E (Alto Risco)"

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

                    st.markdown(f"""
                    <div style="background-color:#1A1A1A; color:#888; padding: 15px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                        <span style="font-weight: bold; font-size: 14px; letter-spacing: 0.5px;">🎯 PARECER DO MODELO: Estratégia </span> <span style="color: {perfil_cor}; font-weight: bold; font-size: 14px; letter-spacing: 0.5px;">{perfil_estrategia}</span><br>
                        <p style="margin-top: 8px; margin-bottom: 0;">
                            Com base na calibração atual, a política recomendada é o <span style="color: {perfil_cor}; font-weight: bold;">Cutoff {cutoff_sugerido}</span> - <span style="color: {perfil_cor}; font-weight: bold;"> Rating Mínimo: {tier_sug}</span>, {justificativa}
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
                            hover_data={"cutoff": True, "ai_score": ":.3f", "approval": ":.1%", "bad_rate": ":.1%"},
                            color_continuous_scale="RdYlGn",
                            title="Fronteira de Eficiência (Pareto)"
                        )
                        fig_pareto.update_layout(
                            height=350,
                            template="plotly_dark",
                            xaxis_title="Taxa de Aprovação",
                            yaxis_title="Inadimplência (FPD)",
                            coloraxis_colorbar=dict(title="Índice"), 
                            margin=dict(l=0, r=0, t=40, b=0),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)"
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
                            xaxis_title=None,
                            yaxis_title="Cutoff (Score)",
                            height=350,
                            margin=dict(l=0, r=50, t=40, b=0),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
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



            # =========================================================
            # SUB-ABA 2: SIMULAÇÃO DE POLÍTICA MANUAL E SWEET SPOT
            # =========================================================
            elif aba_selecionada == "⚙️ Simulação de Política":
                st.markdown("""
                <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px; margin-bottom: 15px;">
                    <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                        <div style="flex:1; min-width: 200px;">
                            <strong style="color: #DDD;">🎯 Sweet Spot:</strong>
                            <hr style="margin-top:7px; margin-bottom:5px; border:1px solid #444;">
                            <p style="margin-top:5px;">O algoritmo atua de forma dinâmica sobre a amostra, respeitando a <b>Idade e Recarga pré-selecionadas</b>. A partir desse público, ele calcula o Score ótimo (KS Máximo) para garantir o maior volume de aprovação de Bons Pagadores com o menor risco possível.</p>
                        </div>
                        <div style="flex:1; min-width: 200px;">
                            <strong style="color: #DDD;">🚧 Fronteira de Decisão:</strong>
                            <hr style="margin-top:7px; margin-bottom:5px; border:1px solid #444;">                    
                            <p style="margin-top:5px;">Mapeia graficamente a aplicação dos <b>filtros restritivos</b>. A área verde isola o público que atende simultaneamente aos critérios de Score, Idade e Recarga, enquanto a dispersão cinza identifica os proponentes barrados pela política atual.</p>
                        </div>
                        <div style="flex:1; min-width: 200px;">
                            <strong style="color: #DDD;">⚖️ Trade-off (Curva):</strong>
                            <hr style="margin-top:7px; margin-bottom:5px; border:1px solid #444;">
                            <p style="margin-top:5px;">Demonstra o <b>balanço entre apetite e segurança</b>: elevar o rigor do Score (deslocamento à direita) reduz drasticamente o risco de inadimplência (linha vermelha), porém impacta a conversão e o volume de aprovação (linha verde).</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("🛠️ Simulador de Regras de Negócio", expanded=True):
                    
                    c_params0, c_params1, c_params2, c_params3 = st.columns(4)

                    with c_params0:
                        mode = st.radio("Modo de Calibração do Score:", ["Manual", "Sweet Spot"], horizontal=True)

                    with c_params1:
                        min_idade = st.slider("Idade Mínima (Anos)", 18, 60, 21)

                    with c_params2:      
                        min_rec_90d = st.slider("Recarga Mínima (Total 90 Dias)", 0, 300, 60, step=10)
                    with c_params3:
                        if mode == "Sweet Spot":
                            # Lógica para encontrar o melhor KS considerando os filtros
                            best_ks, sweet_spot = 0, 300
                            total_bons = (df_sim['target'] == 0).sum()
                            total_maus = (df_sim['target'] == 1).sum()
                            
                            for c in np.arange(300, 901, 10):
                                mask = (
                                    (df_sim["behavior_score"] >= c) & 
                                    (df_sim["idade"] >= min_idade) & 
                                    (df_sim["rec_vlr_total_l90d"].fillna(0) >= min_rec_90d)
                                ).fillna(False)
                                
                                aprovados_bons = ((df_sim['target'] == 0) & mask).sum()
                                aprovados_maus = ((df_sim['target'] == 1) & mask).sum()
                                
                                tpr = aprovados_bons / total_bons if total_bons > 0 else 0
                                fpr = aprovados_maus / total_maus if total_maus > 0 else 0
                                ks = tpr - fpr
                                
                                if ks > best_ks:
                                    best_ks, sweet_spot = ks, c
                            
                            default_score = int(sweet_spot)
                        else:
                            default_score = 400

                        score_cutoff = st.slider(
                            "Score Mínimo para Aprovação",
                            0, 1000, 
                            value=default_score,
                            disabled=(mode == "Sweet Spot")
                        )

                    # Tiers padronizados
                    if score_cutoff >= 800: 
                        tier_minimo = "A (Premium)"
                        perfil_cor_tier = "#5EA758"

                    elif score_cutoff >= 600: 
                        tier_minimo = "B (Seguro)"
                        perfil_cor_tier = "#5EA758"

                    elif score_cutoff >= 400: 
                        tier_minimo = "C (Standard)"
                        perfil_cor_tier = "#D4A017"
                        
                    elif score_cutoff >= 200: tier_minimo = "D (Atenção)"
                    else: 
                        tier_minimo = "E (Alto Risco)"
                        perfil_cor_tier = "#B53744"
                    
                    st.markdown(f"""
                    <div style="background-color:#1A1A1A; color:#888; margin-bottom:15px; padding:16px 16px 4px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
                        <p style="margin-top:5px;">
                            🏷️ <strong>Perfil Operacional:</strong> Aprovando clientes a partir do Rating <span style="color: {perfil_cor_tier}; font-weight: bold;">{tier_minimo}</span> com os filtros acima aplicados.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    query_aprovados = f"""
                        SELECT * FROM df_sim 
                        WHERE behavior_score >= {score_cutoff} 
                        AND idade >= {min_idade}
                        AND COALESCE(rec_vlr_total_l90d, 0) >= {min_rec_90d}
                    """
                    try:
                        aprovados_df = duckdb.query(query_aprovados).df()
                    except Exception:
                        aprovados_df = pd.DataFrame()
                
                curve_df = calculate_policy_curve(df_sim, min_idade, min_rec_90d)
                taxa_aprovacao = len(aprovados_df) / len(df_sim)
                bad_rate_atual = df_master['target'].mean()
                bad_rate_novo = aprovados_df['target'].mean() if not aprovados_df.empty else 0.0
                reducao_risco = (bad_rate_atual - bad_rate_novo) / bad_rate_atual if bad_rate_atual > 0 else 0

                with st.expander("📊 Impacto Projetado na Carteira", expanded=True):
                    k1, k2, k3 = st.columns(3)
                    with k1:
                        vol_str = f"{len(aprovados_df):,.0f}".replace(",", ".")
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Taxa de Aprovação Projetada</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{taxa_aprovacao:.1%}</span>
                                    <span style="font-size: 0.9rem; color: #888; font-weight: normal;">(Vol = {vol_str})</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Proporção da amostra elegível</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with k2:
                        diff_br = bad_rate_novo - bad_rate_atual
                        if diff_br <= 0:
                            cor_delta, seta = "#5EA758", "↓"
                        else:
                            cor_delta, seta = "#B53744", "↑"
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Bad Rate da Safra Simulada</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{bad_rate_novo:.2%}</span>
                                    <span style="font-size: 1rem; color: {cor_delta}; font-weight: bold;">{seta} {abs(diff_br):.2%}</span>
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
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Mitigação de Risco</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{reducao_risco:.1%}</span>
                                    <span style="font-size: 1rem; color: {cor_delta_red}; font-weight: bold;">{seta_red} vs Base</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Melhoria relativa frente à política atual</p>
                            </div>
                        """, unsafe_allow_html=True)

                    st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

                    g1, g2 = st.columns([1.2,1])
                    with g1:
                        st.plotly_chart(
                            plot_decision_boundary(df_sim, score_cutoff, min_idade, min_rec_90d),
                            width='stretch'
                        )
                    with g2:
                        st.plotly_chart(
                            plot_policy_tradeoff(curve_df, score_cutoff, sweet_spot if mode == "Sweet Spot Automático" else None),
                            width='stretch'
                        )        



            # =========================================================
            # SUB-ABA 3: CLUSTERIZAÇÃO E PERSONAS DE NEGÓCIO
            # =========================================================
            elif aba_selecionada == "📡 Perfis de Risco":

                st.markdown("""
                <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px; margin-bottom: 15px;">
                    <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">📡 Motor de Clusterização - Identificação de Perfis Ocultos</h6>
                    <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
                    <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                        <div style="flex:1; min-width: 200px;">
                            <p style="margin-top:5px;">Utiliza Machine Learning (K-Means) integrado ao Behavior Score para segmentar clientes por similaridade de características etárias e consumo, revelando oportunidades de ações de CRM e Vendas Direcionadas.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("💎 Matriz Estratégica: Risco x Retorno", expanded=True):

                    cluster_features = ["behavior_score", "idade", "rec_vlr_total_l90d"]
                    df_cluster = df_sim[cluster_features].copy().fillna(0)
                    
                    # Tratamento de Outliers para estabilizar os centróides do KMeans
                    limite_recarga = df_cluster["rec_vlr_total_l90d"].quantile(0.99)
                    df_cluster["rec_vlr_total_l90d"] = df_cluster["rec_vlr_total_l90d"].clip(upper=limite_recarga)
                    
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
                            score_medio=("behavior_score", "mean"),
                            idade_media=("idade", "mean"),
                            recarga_acumulada_90d=("rec_vlr_total_l90d", "mean"),
                        ).reset_index()
                    )
                    
                    cluster_summary["recarga_mensal_estimada"] = cluster_summary["recarga_acumulada_90d"] / 3
                    cluster_summary["bad_rate"] *= 100

                    def classificar_persona(row):
                        if row['score_medio'] < 600:
                            return "Rating E (Risco Latente)", "#B53744", "Reprovado - Bloqueio"
                        elif row['recarga_mensal_estimada'] > 30:
                            return "VIPs (Heavy Users)", "#D4A017", "Aprovado - Oferta Alta (Cross-Sell)"
                        elif row['idade_media'] > 55:
                            return "Rating A (Seniores)", "#5EA758", "Aprovado - Controle Entrada Segura"
                        else:
                            return "Rating B/C (Massa Padrão)", "#4CAF50", "Aprovado - Ação de Engajamento"

                    res = cluster_summary.apply(classificar_persona, axis=1, result_type='expand')
                    cluster_summary[['Persona', 'Cor', 'Acao']] = res

                    mapa_cores = {
                        "Rating E (Risco Latente)": "#B53744",
                        "VIPs (Heavy Users)": "#D4A017",
                        "Rating A (Seniores)": "#5EA758",
                        "Rating B/C (Massa Padrão)": "#4CAF50"
                    }

                    col_bubble, col_insights = st.columns([6, 4])

                    with col_bubble:
                        fig_cluster = px.scatter(
                            cluster_summary, 
                            x="score_medio", 
                            y="recarga_mensal_estimada", 
                            size="clientes", 
                            color="Persona",
                            color_discrete_map=mapa_cores, 
                            text="cluster", 
                            title="Posicionamento de Portfólio: Receita vs Segurança"
                        )
                        fig_cluster.update_traces(textposition='top center', textfont=dict(color='#FFF', size=14))
                        fig_cluster.update_layout(
                            template="plotly_dark", 
                            xaxis_title="Behavior Score (Mais à direita = Menor Risco)", 
                            yaxis=dict(title="Consumo Mensal Estimado", tickprefix="R$ ", dtick=5),
                            height=425, 
                            margin=dict(l=0, r=0, t=40, b=0),
                            showlegend=False
                        )
                        st.plotly_chart(fig_cluster, use_container_width=True)

                    with col_insights:
                        for i, row in cluster_summary.sort_values("score_medio", ascending=False).iterrows():
                            st.markdown(f"""
                            <div style="background-color:#1A1A1A; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid {row['Cor']};">
                                <strong style="color: #DDD;">Cluster {int(row['cluster'])} - </strong><strong style="color: {row['Cor']};">{row['Persona']}</strong><br>
                                <span style="font-size: 0.85em; color: #BBB;">
                                Vol: {int(row['clientes']):,} | Score: ~{row['score_medio']:.0f} | Idade: ~{row['idade_media']:.0f} | Gasto: ~R$ {row['recarga_mensal_estimada']:.0f}<br>
                                <span style="color: {row['Cor']}; font-weight: bold;">Diretriz de Negócio:</span> {row['Acao']}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
 



# ==============================================================================
# MOTOR DE DECISÃO (INTEGRADO AO MODELO DE PRODUÇÃO)
# ==============================================================================
        elif view_mode == "⚙️ Motor de Decisão":

            st.markdown(
                f"""
                <h3 style="font-weight:700; margin-bottom: 0px;">
                    Credit Risk Engine - <span style="color: #888; font-weight: 500;">Behavior Score</span> - 
                    <code class="theme-1" style="font-size: 1.2rem;">Release 1.0</code>
                </h3>
                """,
                unsafe_allow_html=True
            )
            
            caminho = "models/behavior_catboost_v1.pkl"
            st.caption(f"⚡ **Escoragem em Tempo Real** executada pelo Artefato MLOps: `{caminho.split('/')[-1]}`")
            
            st.write("<hr style='margin-top:-6.5px; margin-bottom:-30px;'>", unsafe_allow_html=True)

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
            with st.expander("🏷️ Metadados do Modelo em Produção", expanded=True):
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
            # 4. ESTRUTURA PRINCIPAL 
            # ==========================================================
            p1, p2 = st.columns([1,2]) 
            
            with p1:
                
                @st.cache_data(show_spinner=False)
                def get_curated_cpfs(_df, _model, features, pct_bur):
                    X_all = _df[features].apply(pd.to_numeric, errors='coerce').astype(float)
                    probs = _model.predict_proba(X_all)[:, 1]
                    scores = ((1 - probs) * 1000).astype(int)
                    
                    cutoff_bur = np.nanpercentile(_df['bur_score_02'], pct_bur)
                    aprova_bur = _df['bur_score_02'] >= cutoff_bur
                    aprova_mod = scores >= 400
                    
                    m_si = aprova_mod & (~aprova_bur)
                    m_so = (~aprova_mod) & aprova_bur
                    m_aa = aprova_mod & aprova_bur
                    m_ar = (~aprova_mod) & (~aprova_bur)
                    
                    cpf_si = _df[m_si]['num_cpf'].dropna().astype(str).values[0]
                    cpf_so = _df[m_so]['num_cpf'].dropna().astype(str).values[0]
                    cpf_aa = _df[m_aa]['num_cpf'].dropna().astype(str).values[0]
                    cpf_ar = _df[m_ar]['num_cpf'].dropna().astype(str).values[0]
                    
                    top_4 = [
                        f"{cpf_si}",
                        f"{cpf_so}",
                        f"{cpf_aa}",
                        f"{cpf_ar}"
                    ]
                    
                    cpfs_demo = [cpf_si, cpf_so, cpf_aa, cpf_ar]
                    resto_normal = _df[~_df['num_cpf'].astype(str).isin(cpfs_demo)]['num_cpf'].dropna().astype(str).unique()[:5000].tolist()
                    
                    return top_4 + resto_normal
                    
                pct_bureau = metadata.get('cutoff_bureau_pct', 30.0)
                lista_cpfs_view = get_curated_cpfs(df_master, model, features_raw, pct_bureau)
            
                with st.expander("🔍 Buscar Cliente", expanded=True):

                    cpf_selecionado_raw = st.selectbox(
                        "Selecione ou Digite o CPF:", 
                        options=[""] + lista_cpfs_view, 
                        index=0,
                        help="Selecione ou Digite o CPF para Análise.",
                        key="filtro_motor_cpf"
                    )

                cpf_selecionado = cpf_selecionado_raw.split(" | ")[0] if cpf_selecionado_raw else ""

                if cpf_selecionado != "":

                    busca_cliente = df_master[df_master['num_cpf'].astype(str).str.contains(cpf_selecionado)].copy()
                    
                    if not busca_cliente.empty:
                        dados_cliente = busca_cliente.iloc[0]
                        
                        with st.expander("📋 Perfil do Cliente Capturado", expanded=False):
                            cols_feat = st.columns(2)
                            for i, feat in enumerate(features_raw):
                                val = dados_cliente.get(feat, 0.0)
                                with cols_feat[i % 2]:
                                    st.number_input(
                                        label=feat,
                                        value=float(val) if pd.notna(val) else 0.0,
                                        disabled=True,
                                        key=f"disabled_{feat}_{cpf_selecionado}" 
                                    )
                    
                    # ==========================================================
                    # 5. PROCESSAMENTO AUTOMÁTICO DO MOTOR
                    # ==========================================================
                    cor_gauge_aprovado = "rgba(94, 167, 88, 0.2)"
                    cor_gauge_mesa = "rgba(212, 160, 23, 0.2)"
                    cor_gauge_reprovado = "rgba(181, 55, 68, 0.2)"
                    
                    try:
                        features_cliente = pd.to_numeric(dados_cliente[features_raw], errors='coerce').astype(float)
                        X_model = features_cliente.to_frame().T
                        
                        prob = model.predict_proba(X_model)[:, 1][0]
                        score = calculate_score(prob)
                        tier, color_tier = get_risk_tier(score)
                        
                        if score >= 600:
                            decision = "APROVADO"
                            decision_sub = "Oferta Cross-Sell"
                            decision_color = "#4CAF50"
                        elif score >= 400:
                            decision = "MESA / LIMITADO"
                            decision_sub = "Oferta Plano Entrada"
                            decision_color = "#FFC107"
                        else:
                            decision = "REPROVADO"
                            decision_sub = "Bloqueio (Blindagem)"
                            decision_color = "#F44336"
                            
                    except Exception as e:
                        st.error(f"Erro ao calcular score do cliente: {e}")
                        prob, score, tier, decision, decision_sub, decision_color = 0, 0, "Erro", "ERRO", "Falha", "#B53744"

            # ==========================================================
            # 6. RENDERIZAÇÃO DO PAINEL DE RESULTADOS 
            # ==========================================================
            with p2:

                if cpf_selecionado != "":
                    with st.expander("📊 Painel de Decisão e Explicabilidade", expanded=True):
                        
                        # ==========================================================
                        # LÓGICA DE SWAP (DIRETO DO PKL)
                        # ==========================================================
                        pct_bureau = metadata.get('cutoff_bureau_pct', 30.0)
                        
                        cutoff_bureau = np.nanpercentile(df_master['bur_score_02'], pct_bureau)
                        bureau_score = float(dados_cliente.get('bur_score_02', 0))
                        
                        aprova_bureau = bureau_score >= cutoff_bureau
                        aprova_behavior = score >= 400 
                        
                        if aprova_behavior and aprova_bureau:
                            swap_status = "Ambos Aprovam"
                            swap_desc = f"Bureau ({bureau_score:.0f}) e Motor de Acordo"
                            swap_color = "#4CAF50" 
                        elif not aprova_behavior and not aprova_bureau:
                            swap_status = "Ambos Reprovam"
                            swap_desc = f"Bureau ({bureau_score:.0f}) e Motor Rejeitam"
                            swap_color = "#F44336"
                        elif aprova_behavior and not aprova_bureau:
                            swap_status = "Swap-In (Ganho)"
                            swap_desc = f"Resgatado! Bureau era {bureau_score:.0f} (Reprova)"
                            swap_color = "#2196F3"
                        else:
                            swap_status = "Swap-Out (Proteção)"
                            swap_desc = f"Barrado! Bureau era {bureau_score:.0f} (Aprova)"
                            swap_color = "#FF9800" 

                        # ==========================================================
                        # CARDS SUPERIORES 
                        # ==========================================================
                        st.markdown(f"""
                            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                                <div style="flex: 1; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid #455A64; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                    <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">PROBABILIDADE (PD)</div>
                                    <div style="font-size: 1.8rem; font-weight: 700; color: #FFF;">{prob:.2%}</div>
                                </div>
                                <div style="flex: 1; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid {color_tier}; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                    <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 5px;">RATING CRM</div>
                                    <div style="font-size: 1.5rem; font-weight: 700; color: {color_tier}; margin-top: 5px;">{tier}</div>
                                </div>
                                <div style="flex: 1.2; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid {decision_color}; border-bottom: 1px solid {decision_color}40; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                    <div style="font-size: 0.80rem; color: #999; font-weight: 600; margin-bottom: 0px;">DECISÃO (AÇÃO)</div>
                                    <div style="font-size: 1.4rem; font-weight: 700; color: {decision_color}; margin-top: 2px;">{decision}</div>
                                    <div style="font-size: 0.75rem; color: #BBB; margin-top: 2px;">{decision_sub}</div>
                                </div>
                                <div style="flex: 1.2; background: linear-gradient(145deg, #1A1C24, #1E1E1E); padding: 15px; border-radius: 8px; border-top: 3px solid {swap_color}; border-bottom: 1px solid {swap_color}40; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                    <div style="font-size: 0.75rem; color: #999; font-weight: 600; margin-bottom: 0px;">MATRIZ DE SWAP</div>
                                    <div style="font-size: 1.2rem; font-weight: 700; color: {swap_color}; margin-top: 2px;">{swap_status}</div>
                                    <div style="font-size: 0.70rem; color: #BBB; margin-top: 2px;">{swap_desc}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        c_gauge, c_expl = st.columns([1, 1.2])
                        
                        with c_gauge:
                            fig_gauge = go.Figure(go.Indicator(
                                mode="gauge+number", value=score,
                                title={'text': "<b>Behavior Score</b>", 'font': {'size': 14, 'color': '#BBB'}},
                                number={'font': {'size': 62, 'color': '#FFF'}},
                                gauge={
                                    'axis': {'range': [0, 1000], 'tickwidth': 1, 'tickcolor': "#666"}, 
                                    'bar': {'color': "#FFFFFF", 'thickness': 0.15}, 
                                    'bgcolor': "#1A1C24",
                                    'borderwidth': 0,
                                    'steps': [
                                        {'range': [0, 200], 'color': 'rgba(244, 67, 54, 0.4)'},     # E
                                        {'range': [200, 400], 'color': 'rgba(255, 152, 0, 0.4)'},   # D
                                        {'range': [400, 600], 'color': 'rgba(255, 193, 7, 0.4)'},   # C
                                        {'range': [600, 800], 'color': 'rgba(76, 175, 80, 0.4)'},   # B
                                        {'range': [800, 1000], 'color': 'rgba(27, 94, 32, 0.4)'}    # A
                                    ]
                                }
                            ))
                            fig_gauge.update_layout(
                                height=280, 
                                margin=dict(l=20, r=20, t=0, b=0),
                                paper_bgcolor="rgba(0,0,0,0)",
                                font={'family': "Inter, sans-serif"}
                            )
                            st.plotly_chart(fig_gauge, use_container_width=True)

                        with c_expl:
                            importances = model.get_feature_importance()
                            
                            contributions = []
                            for feat, imp in zip(features_raw, importances):
                                if feat not in ['bur_score_01', 'bur_score_02']:
                                    contributions.append({'Feature': feat, 'Impacto': imp})
                            
                            df_contrib = pd.DataFrame(contributions).sort_values('Impacto', ascending=False).head(8)
                            df_contrib = df_contrib.sort_values('Impacto', ascending=True) 
                            
                            fig_expl = go.Figure()
                            
                            fig_expl.add_trace(go.Bar(
                                x=df_contrib['Impacto'],
                                y=df_contrib['Feature'],
                                orientation='h',
                                marker_color=decision_color, 
                                width=0.15,      
                                hoverinfo="x+y"
                            ))

                            fig_expl.update_layout(
                                template="plotly_dark",
                                height=280, 
                                margin=dict(l=10, r=20, t=50, b=25),
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),
                                yaxis=dict(showgrid=False, zeroline=False, title=None),
                                showlegend=False,
                                title="<b>Drivers de Risco</b> (Top 8)",
                                title_font=dict(size=14, color='#BBB')
                            )
                            st.plotly_chart(fig_expl, use_container_width=True)

                        st.markdown(f"""
                        <div style="font-size: 14px; background-color: rgba(255, 255, 255, 0.05); border-left: 4px solid #4F1C22; padding: 10px 15px; border-radius: 4px; margin-top:-33px; margin-bottom: 15px;">
                                <strong>✓</strong> Análise Concluída para o CPF: <strong>{cpf_selecionado}</strong>
                        </div>
                        """, unsafe_allow_html=True)

                            
                else:
                        st.markdown("""
                            <div style="height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #1A1A1A; border: 2px dashed #444; border-radius: 12px; margin-top: 0px;">
                                <div style="background-color: #222; padding: 20px; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 20px;">
                                    <span style="font-size: 3.5rem;">⚙️</span>
                                </div>
                                <h3 style="color:#FFF; margin-bottom: 5px;">Motor Aguardando Seleção</h3>
                                <p style="color:#BBB; font-size: 1.1rem; text-align: center; max-width: 400px;">
                                    Busque o <b>CPF</b> do proponente na barra lateral para autocompletar as variáveis e processar o risco instantaneamente.
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()