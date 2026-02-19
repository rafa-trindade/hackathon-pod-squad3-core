import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
import numpy as np

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
except ImportError as e:
    st.error(f"Erro ao importar utils: {e}")
    st.stop()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
    ["👤 Home | Estudo de Público", "🧪 Simulação de Política", "⚙️ Motor de Decisão"],
    index=0,
    label_visibility="collapsed"
)

st.sidebar.write("<hr style='margin-top:3px; margin-bottom:-8px;'><br>", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <p style='margin-top:18px;'>
    <style>
    /* Logo customizado */
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
            "Análise Univariada",
            "Análise Multivariada",
            "Ranking de Variáveis",
            "Estabilidade Temporal",
            "Análise Demográfica"
        ])

        # --- TAB 1: VISÃO GERAL ---
        with tab1:
            with st.expander("📊 Monitoramento de Carteira e Saúde do Modelo", expanded=True):
                
                # Inicializa variavel
                summary_df = pd.DataFrame()
                
                # 1. Carregamento dos Dados com Tratamento de Erro na UI
                try:
                    # O Toast e Spinner ficam AQUI fora
                    st.toast("Conectando a OCI...", icon="📡")
                    
                    with st.spinner("Consultando dados atualizados do Lake..."):
                        summary_df = load_data_summary()
                        assets = load_assets()
                        metadata = assets.get('metadata', {})
                        
                    if summary_df.empty:
                        st.warning("⚠️ A conexão funcionou, mas a tabela retornou vazia.")
                        st.stop()

                except Exception as e:
                    # Mostra o erro aqui na UI
                    st.error(f"❌ {str(e)}")
                    st.stop()

                # 2. Cálculo dos KPIs (Só executa se summary_df existir)
                if not summary_df.empty:
                    # Ordena por data
                    summary_df = summary_df.sort_values('safra')


                    
                    # Cálculos Gerais
                    total_reg = summary_df['total_registros'].sum()
                    total_bads = summary_df['total_bads'].sum()
                    avg_bad_rate = total_bads / total_reg if total_reg > 0 else 0

                    total_bad_absoluto = summary_df['total_bads'].sum()
                    avg_bad = total_bad_absoluto / total_reg if total_reg > 0 else 0
                    odds = (1 - avg_bad) / avg_bad if avg_bad > 0 else 0
                    
                    # Cálculos do Último Mês vs Mês Anterior
                    last_month = summary_df.iloc[-1]
                    prev_month = summary_df.iloc[-2] if len(summary_df) > 1 else last_month
                    
                    vol_mom = (last_month['total_registros'] - prev_month['total_registros']) / prev_month['total_registros']
                    risk_mom = (last_month['bad_rate'] - prev_month['bad_rate']) / prev_month['bad_rate']

                    k1, k2, k3, k4, k5 = st.columns(5)

                    with k1:

                        vol_str = f"{total_reg/1e6:.2f}M"
                        # Lógica MoM
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



                    # KPI 2: Inadimplência (FPD)
                    with k2:
                        # Lógica MoM Invertida (Subir risco é ruim)
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
                        delta_gini = gini_atual - 40 # Meta de 40 definida no notebook
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
                        delta_ks = ks_atual - 30

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

                    # KPI 5: Estabilidade (PSI)
                    with k5:
                        # Tenta pegar do metadata ou calcula proxy básico
                        psi_atual = metadata.get('psi_oot', 0.0)
                        
                        # Lógica de Meta (PSI < 0.25 é o alvo)
                        target_psi = 0.25
                        diff_psi = target_psi - psi_atual # Quanto maior a "sobra" até 0.25, melhor
                        
                        # Definição de Cores/Status
                        if psi_atual < 0.10:
                            cor_delta = "#5EA758" # Verde (Excelente)
                            status_psi = "Estável"
                        elif psi_atual < 0.25:
                            cor_delta = "#FFA500" # Laranja (Alerta)
                            status_psi = "Atenção"
                        else:
                            cor_delta = "#B53744" # Vermelho (Crítico)
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






        # --- TAB 2: ANÁLISE UNIVARIADA ---
        with tab2:

            with st.expander("🔍 Análise Univariada de Variáveis", expanded=True):
                
                df_sample = pd.DataFrame()
                try:
                    with st.spinner("Carregando amostra estatística (100k linhas)..."):
                        df_sample = load_sample_data(n_samples=100000)
                except Exception as e:
                    st.error(f"Erro ao carregar amostra: {str(e)}")
                    st.stop()

                if df_sample.empty:
                    st.warning("Amostra vazia. Verifique a conexão.")
                    st.stop()

                ignored_cols = ['target', 'fpd', 'safra', 'num_cpf', 'cpf']
                numeric_cols = df_sample.select_dtypes(include=[np.number]).columns.tolist()
                available_features = [c for c in numeric_cols if c not in ignored_cols]

                if not available_features:
                    st.warning("Nenhuma variável numérica encontrada para análise.")
                else:
                    # Pré-cálculo dos IVs para ordenação
                    iv_scores = {}
                    with st.spinner("Calculando ranking de variáveis (IV)"):
                        for col in available_features:
                            val, _ = calculate_iv(df_sample, col)
                            iv_scores[col] = val

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
                            index=0 # Seleciona automaticamente a melhor variável
                        )

                    # Recupera o IV da variável selecionada (já calculado)
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



        # --- TAB 3: ANÁLISE MULTIVARIADA ---
        with tab3:
                
            # 1. Carregamento dos Dados
            df_multi = pd.DataFrame()
            try:
                with st.spinner("Carregando dados para correlação..."):
                    df_multi = load_sample_data(n_samples=100000)
            except:
                st.stop() 

            if df_multi.empty:
                st.warning("Dados indisponíveis.")
                st.stop()

            # 2. Identificação de Variáveis Numéricas
            ignored_cols = ['target', 'fpd', 'safra', 'num_cpf', 'cpf']
            numeric_cols = df_multi.select_dtypes(include=[np.number]).columns.tolist()
            valid_cols = [c for c in numeric_cols if c not in ignored_cols]

            # 3. Filtragem por IV > 0.1 (NOVO BLOCO)
            selected_cols_for_corr = []
            
            # Barra de progresso visual (opcional, mas bom para UX)
            with st.spinner("Filtrando variáveis relevantes (IV > 0.1)..."):
                for col in valid_cols:
                    iv_val, _ = calculate_iv(df_multi, col)
                    if iv_val > 0.1:
                        selected_cols_for_corr.append(col)
            

            with st.expander("🔗 Matriz de Risco Combinada (Bad Rate %)", expanded=True):
                    
                mat1, mat2 = st.columns([1,2.5])

                if len(valid_cols) >= 2:

                    with mat1:

                        # Tenta selecionar scores como padrão se existirem
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

        # --- TAB 4: RANKING DE VARIÁVEIS ---
        with tab4:
            with st.expander("🏆 Ranking de Poder Discriminatório", expanded=True):
                
                df_rank_sample = pd.DataFrame()
                try:
                    with st.spinner("Calculando Gini e IV para todas as variáveis..."):
                        df_rank_sample = load_sample_data(n_samples=100000)
                        
                        if not df_rank_sample.empty:
                            ranking_df = get_feature_ranking(df_rank_sample)
                        else:
                            ranking_df = pd.DataFrame()
                except Exception as e:
                    st.error(f"Erro ao processar ranking: {e}")
                    st.stop()

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
                                help="Nome da feature na base de dados"
                            ),
                            "Qualidade": st.column_config.TextColumn(
                                "Poder (IV)",
                                width="small"
                            ),
                            "IV": st.column_config.ProgressColumn(
                                "Information Value (IV)",
                                format="%.4f",
                                min_value=0,
                                max_value=0.6, # Teto visual para a barra
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

        # --- TAB 5: ESTABILIDADE TEMPORAL (PSI) ---
        with tab5:
            with st.expander("⚖️ Monitoramento de Estabilidade (PSI)", expanded=True):
                
                df_psi = pd.DataFrame()
                try:
                    with st.spinner("Carregando dados históricos..."):
                        df_psi = load_sample_data(n_samples=100000)
                except:
                    st.stop()

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

        # --- TAB 6: ANÁLISE DEMOGRÁFICA ---
        with tab6:
            with st.expander("🗺️ Segmentação Demográfica e Geográfica", expanded=True):
                
                df_demo = pd.DataFrame()
                try:
                    df_demo = load_sample_data(n_samples=100000)
                    df_demo = process_demographics(df_demo)
                except:
                    st.stop()
                
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
                
                if min_score > 0 or max_score < 1000:
                    df_filtered = df_demo[df_demo['bur_score_02'].between(min_score, max_score)]
                else:
                    df_filtered = df_demo.copy()
                
                if sel_regiao != "Brasil (Todas)":
                    df_filtered = df_filtered[df_filtered['regiao'] == sel_regiao]
                    
                    if sel_estado_display != "Todos da Região":
                        sigla_uf = sel_estado_display.split('(')[-1].replace(')', '')
                        df_filtered = df_filtered[df_filtered['uf'] == sigla_uf]

            with st.expander("📊 Resultados da Segmentação", expanded=True):

                if df_filtered.empty:
                    st.warning("Nenhum dado encontrado para os filtros selecionados.")
                else:
                    col_m1, col_m2, col_m3 = st.columns(3)

                    avg_risk = df_filtered['target'].mean()
                    delta_risk = avg_risk - df_demo['target'].mean()

                    with col_m1:
                        vol_str = f"{len(df_filtered):,.0f}".replace(",", ".")
                        
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column;">
                                <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Volume da Amostra</p>
                                <div style="display: flex; align-items: baseline; gap: 8px;">
                                    <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{vol_str}</span>
                                </div>
                                <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">Total de Clientes no Segmento</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with col_m2:
                        if delta_risk <= 0:
                            cor_delta = "#5EA758" # Verde
                            seta = "↓"
                        else:
                            cor_delta = "#B53744" # Vermelho
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
                        st.plotly_chart(plot_geo_map(df_filtered), width='stretch')

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

            # Bloco de Contexto
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

    elif view_mode == "🧪 Simulação de Política":

        st.markdown(
            f"""
            <h3 style="font-weight:700; margin-bottom: 0px;">
                Simulador de Política de Crédito - 
                <code class="theme-1" style="font-size: 1.2rem;">eda_v1.0</code>
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.caption("📂 **Notebook de Referência:** `notebooks/eda/01_estudo_publico_alvo_cmv.ipynb`")
        st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color:#1A1A1A; color:#888; padding:16px 16px 0px 16px; border-radius:8px; border-left:6px solid #4F1C22; font-family:sans-serif; font-size:14px;">
            <h6 style="margin-top:0px; margin-bottom:-10px; color:#DDD;">🧠 GUIA DE ESTRATÉGIA E SIMULAÇÃO</h6>
            <hr style="margin-top:0px; margin-bottom:15px; border:1px solid #444;">
            <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap: wrap;">
                <div style="flex:1; min-width: 200px;">
                    <strong style="color: #DDD;">🤖 AI Sweet Spot:</strong>
                    <p style="margin-top:5px;">O algoritmo analisa a curva de risco e sugere automaticamente o ponto de corte (Score) que maximiza a aprovação sem piorar a inadimplência média atual.</p>
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

        st.write("")

        with st.expander("🛠️ Simulador de Política de Crédito", expanded=True):
            
            # 1. Carregar Dados
            df_sim = pd.DataFrame()
            try:
                df_sim = load_sample_data(n_samples=50000) # Amostra menor para ser rápido no loop
            except:
                st.stop()

            # Verifica colunas necessárias
            required_cols = ['bur_score_02', 'idade', 'pag_vlr_total_geral', 'target']
            missing = [c for c in required_cols if c not in df_sim.columns]
            
            if missing:
                st.error(f"Faltam colunas para o simulador: {missing}")
                st.stop()


            c_params0, c_params1, c_params2, c_params3 = st.columns(4)

            with c_params0:
                mode = st.radio("Modo de Definição:", ["Manual", "AI Sweet Spot"], horizontal=True)

            with c_params1:
                min_idade = st.slider("Idade Mínima (Anos)", 18, 60, 21)

            with c_params2:     
                min_pagto = st.slider("Pagamento Total Mínimo (R$)", 0, 1000, 100, step=50)

            with c_params3:
                curve_df = calculate_policy_curve(df_sim, min_idade, min_pagto)
                bad_rate_target = df_sim['target'].mean() * 100 
                candidates = curve_df[curve_df['bad_rate'] <= bad_rate_target]
                sweet_spot = int(candidates.iloc[0]['cutoff']) if not candidates.empty else int(curve_df.iloc[-1]['cutoff'])
                default_score = sweet_spot if mode == "AI Sweet Spot" else 550
                score_cutoff = st.slider(
                    "Score Mínimo (Bureau)", 
                    300, 900, 
                    value=default_score,
                    disabled=(mode == "AI Sweet Spot")
                )

            mask_aprov = (
                (df_sim['bur_score_02'] >= score_cutoff) &
                (df_sim['idade'] >= min_idade) &
                (df_sim['pag_vlr_total_geral'].fillna(0) >= min_pagto)
            )
            
        aprovados_df = df_sim[mask_aprov]
        
        # Métricas
        taxa_aprovacao = len(aprovados_df) / len(df_sim)
        bad_rate_atual = df_sim['target'].mean()
        bad_rate_novo = aprovados_df['target'].mean() if not aprovados_df.empty else 0.0
        reducao_risco = (bad_rate_atual - bad_rate_novo) / bad_rate_atual if bad_rate_atual > 0 else 0

        with st.expander("📊 Impacto Projetado na Carteira", expanded=True):
            k1, k2, k3 = st.columns(3)
            with k1:
                # Formata o volume com separador de milhar (ponto)
                vol_str = f"{len(aprovados_df):,.0f}".replace(",", ".")
                
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column;">
                        <p style="font-size: 0.85rem; color: #999; margin-bottom: 0px;">Taxa de Aprovação</p>
                        <div style="display: flex; align-items: baseline; gap: 8px;">
                            <span style="font-size: 1.8rem; font-weight: 600; color: #FFF;">{taxa_aprovacao:.1%}</span>
                            <span style="font-size: 0.9rem; color: #888; font-weight: normal;">(N={vol_str})</span>
                        </div>
                        <p style="font-size: 0.75rem; color: #666; margin-top: 0px;">% da base elegível na regra</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # K2: Bad Rate Esperado 
            with k2:
                diff_br = bad_rate_novo - bad_rate_atual
                
                if diff_br <= 0:
                    cor_delta = "#5EA758" 
                    seta = "↓"
                else:
                    cor_delta = "#B53744" 
                    seta = "↑"
                
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

            # K3: Redução de Risco 
            with k3:
                if reducao_risco > 0:
                    cor_delta_red = "#5EA758"
                    seta_red = "↑" 
                else:
                    cor_delta_red = "#B53744"
                    seta_red = "↓"

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

            # 4. Visualização da Fronteira
            st.plotly_chart(
                plot_decision_boundary(df_sim, score_cutoff, min_idade, min_pagto),
                width='stretch'
            )
    
            st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)

            st.plotly_chart(
                plot_policy_tradeoff(curve_df, score_cutoff, sweet_spot if mode == "AI Sweet Spot" else None),
                width='stretch'
            )



    elif view_mode == "⚙️ Motor de Decisão":
        st.markdown(
            f"""
            <h3 style="font-weight:700; margin-bottom: 0px;">
                Credit Risk Engine - <code class="theme-1" style="font-size: 1.2rem;">Behavior Score</code> <code class="theme-1" style="font-size: 1.2rem;">woe_v1.0</code> 
            </h3>
            """,
            unsafe_allow_html=True
        )
        
        caminho = "models/behavior_baseline_woe_v1.pkl"
        st.caption(f"🛠️ **Modelo de Produção (Artefato):** `{caminho}`")
        
        st.write("<hr style='margin-top:-6.5px; margin-bottom:0px;'>", unsafe_allow_html=True)
        st.write("")

        # 1. Carregar Modelo
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

        with st.expander("🔍 Metadados do Modelo em Produção", expanded=True):
            c_meta1, c_meta2 = st.columns(2)
            with c_meta1:
                st.write(f"**Versão:** {metadata.get('version', 'N/A')}")
                st.write(f"**Algoritmo:** {metadata.get('algorithm', 'LogisticRegression')}")
                st.write(f"**Gini OOT:** {metadata.get('gini_oot', 0.0):.2f}%")
            with c_meta2:
                st.write(f"**Data Treino:** {metadata.get('created_at', 'N/A')}")
                st.write(f"**Features:** {len(features_raw)}")
                st.write(f"**KS OOT:** {metadata.get('ks_oot', 0.0):.2f}%")

        # 2. Formulário de Input 
        p1, p2 = st.columns([1, 1.2])
        
        with p1:
            with st.form("risk_form"):
                st.subheader("📝 Dados do Proponente")
                
                # Inputs agrupados por domínio
                inputs = {}
                
                st.markdown("**🏛️ Bureau & Cadastro**")
                c1a, c1b = st.columns(2)
                with c1a:
                    inputs['bur_score_02'] = st.number_input("Bureau Score 02", 0, 1000, 450, help="Principal score de mercado")
                    inputs['cad_var_02'] = st.number_input("Tempo Residência (Meses)", 0, 360, 24)
                with c1b:
                    inputs['bur_score_01'] = st.number_input("Bureau Score 01", 0, 1000, 500, help="Score secundário")
                
                st.markdown("**📱 Comportamento Recarga (Rec)**")
                c2a, c2b = st.columns(2)
                with c2a:
                    inputs['rec_vlr_avg_geral'] = st.number_input("Vlr Médio Recarga (R$)", 0.0, 500.0, 35.0)
                    inputs['rec_dias_desde_ultima'] = st.number_input("Dias desde última recarga", 0, 365, 5)
                with c2b:
                    inputs['rec_ratio_vlr_l30d_l60d'] = st.number_input("Razão Recarga L30/L60", 0.0, 10.0, 1.0)

                st.markdown("**💳 Pagamentos & Atrasos (Pag/Atr)**")
                c3a, c3b = st.columns(2)
                with c3a:
                    inputs['pag_dias_desde_ultimo_pagamento'] = st.number_input("Recência Pagamento (Dias)", 0, 365, 10)
                    inputs['atr_vlr_acumulado_geral'] = st.number_input("Valor em Atraso (R$)", 0.0, 10000.0, 0.0)
                with c3b:
                    inputs['tel_var_28'] = st.number_input("Idade na Telco (Meses)", 0, 240, 12)

                submit_val = st.form_submit_button("🚀 CALCULAR RISCO")

        # 3. Processamento e Resultados
        if submit_val:
            try:
                df_input = pd.DataFrame([inputs])
                

                for col in features_raw:
                    if col not in df_input.columns:
                        df_input[col] = np.nan # WoE encoder lida com NaN
                
                # Transformação WoE
                df_woe = encoder.transform(df_input, features_raw)
                
                # Seleciona apenas as colunas de woe geradas
                woe_cols = [f'{col}_woe' for col in features_raw]
                X_model = df_woe[woe_cols].fillna(0) 
                
                # Predição
                prob = model.predict_proba(X_model)[:, 1][0]
                score = calculate_score(prob)
                tier, color = get_risk_tier(score)

                with p2:
                    
                    with st.expander("**📊 Painel de Decisão**", expanded=True):
                        # Gauge Chart
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number", value=score,
                            title={'text': "Behavior Score"},
                            gauge={
                                'axis': {'range': [0, 1000]}, 
                                'bar': {'color': color},
                                'steps': [
                                    {'range': [0, 450], 'color': "#ffebee"}, 
                                    {'range': [450, 600], 'color': "#fff3e0"}, 
                                    {'range': [600, 1000], 'color': "#e8f5e9"}
                                ]
                            }
                        ))
                        fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=0))
                        st.plotly_chart(fig_gauge, width='stretch')

                        c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
                        c_kpi1.metric("Risco (PD)", f"{prob:.2%}")
                        c_kpi2.metric("Tier", tier)
                        
                        decision = "APROVADO" if score >= 600 else "MESA DE CRÉDITO" if score >= 450 else "REPROVADO AUTOMÁTICO"
                        c_kpi3.metric("Decisão", decision)

                        # Explainability (Contribuição das Features)
                        # Coeficientes * Valor WoE = Impacto no LogOdds
                        intercept = model.intercept_[0]
                        contributions = []
                        
                        for feat, woe_col in zip(features_raw, woe_cols):
                            coef = model.coef_[0][features_raw.index(feat)]
                            val_woe = X_model[woe_col].values[0]
                            impact = coef * val_woe
                            contributions.append({'Feature': feat, 'Impacto': impact})
                        
                        df_contrib = pd.DataFrame(contributions).sort_values('Impacto', ascending=False)
                        
                        fig_expl = px.bar(
                            df_contrib, x='Impacto', y='Feature', orientation='h',
                            color='Impacto', color_continuous_scale='RdYlGn',
                            title="Contribuição por Variável (Log-Odds)"
                        )
                        fig_expl.update_layout(height=300, yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig_expl, width='stretch')
                        st.write("")
                        st.write("")
                        st.write("")
                    st.markdown("Cálculo realizado com sucesso!")
            except Exception as e:
                st.error(f"Erro no processamento: {str(e)}")
                # st.exception(e) # Descomente para debug detalhado
        
        else:
            with p2:
                st.markdown("""
                    <div style="height: 755px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed #363434; border-radius: 7px; color: #DAD0D1; margin-top: 4px;">
                        <span style="font-size: 3rem; color: rgba(54,52,52,0.2);">⚙️</span>
                        <h3 style="color:#363434;">Aguardando Parâmetros</h3><p style="color:#363434;">Preencha o formulário à esquerda e clique em Calcular.</p>
                    </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()