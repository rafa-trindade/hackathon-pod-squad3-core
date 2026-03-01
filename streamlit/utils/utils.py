import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import os
import sys
from sklearn.metrics import roc_auc_score
import json

# ==============================================================================
# CONFIGURAÇÃO DE CAMINHOS E IMPORTS EXTERNOS
# ==============================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("streamlit/assets/style.css")

try:
    from config.data_connections import get_duckdb_connection
except ImportError:
    st.warning("⚠️ Módulo 'config.data_connections' não encontrado. Verifique o caminho.")

# ==============================================================================
# CONSTANTES E CORES (CORRIGIDO)
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
    
    # Cores Específicas para Gráficos
    'neutral': '#455A64',    
    'good': '#3C6E3B',       
    'bad': '#731E27',       
    'accent': '#C62828'      
}

# ==============================================================================
# FUNÇÕES DE ESTILO (UI)
# ==============================================================================
def local_css(file_name):
    """Aplica CSS local a partir de um arquivo."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

# ==============================================================================
# DATA LAYER (Conexão e Carregamento)
# ==============================================================================
@st.cache_resource
def get_db_connection():
    """Gerencia a conexão com DuckDB/S3 com tratamento de SSL."""
    try:
        con = get_duckdb_connection()
        con.execute("LOAD httpfs;")

        #con.execute("INSTALL httpfs; LOAD httpfs;")
        #con.execute("SET s3_use_ssl=false;")      
        #con.execute("SET s3_url_style='path';")   
        
        return con
    except Exception as e:
        st.error(f"Erro ao conectar ao DuckDB/S3: {e}")
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def load_data_summary():

    con = get_db_connection()
    if con is None: raise Exception("Não foi possível estabelecer conexão com o DuckDB.")

    query = f"""
        SELECT 
            safra,
            COUNT(*) as total_registros,
            AVG(CAST(fpd AS INTEGER)) as bad_rate,
            SUM(CAST(fpd AS INTEGER)) as total_bads
        FROM read_parquet('{ABT_PATH}')
        GROUP BY 1
        ORDER BY 1
    """
    try:
        return con.execute(query).df()
    except Exception as e:
        raise Exception(f"Erro técnico ao ler S3: {e}")

# ==============================================================================
# DATA LAYER - AMOSTRAGEM E PREPARAÇÃO
# ==============================================================================
def prepare_features(df):
    """Padronização rigorosa: Garante a existência do 'target' e 'idade'."""
    df.columns = [str(c).lower() for c in df.columns]
    
    for col in ['safra', 'cad_datadenascimento']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if 'target' not in df.columns:
        if 'fpd' in df.columns:
            df['target'] = pd.to_numeric(df['fpd'], errors='coerce').fillna(0).astype("int8")
        else:
            df['target'] = 0

    if 'idade' not in df.columns:
        if 'safra' in df.columns and 'cad_datadenascimento' in df.columns:
            df['idade'] = ((df['safra'] - df['cad_datadenascimento']).dt.days / 365.25).round(0)
            df.loc[(df['idade'] < 18) | (df['idade'] > 100), 'idade'] = np.nan
        else:
            df['idade'] = np.nan
            
    return df

@st.cache_data(ttl=3600)
def load_sample_data():
    con = get_db_connection()
    if con is None: return pd.DataFrame()
    
    query = f"SELECT * FROM read_parquet('{ABT_PATH}') USING SAMPLE 5 PERCENT (bernoulli)"
    try:
        df = con.execute(query).df()
        return prepare_features(df)
    except Exception as e:
        st.error(f"Erro na carga real: {e}")
        return pd.DataFrame()

@st.cache_resource
def load_assets():
    base_dir = Path(__file__).resolve().parent.parent.parent
    path = base_dir / "reports" / "observability" / "modeling" / "v1" / "models" / "behavior_catboost_v1.pkl"

    if not path.exists(): raise FileNotFoundError(f"Modelo não encontrado em: {path}")

    with open(path, 'rb') as f:
        return pickle.load(f)

# ==============================================================================
# CÁLCULOS ESTATÍSTICOS (IV, WOE)
# ==============================================================================
def calculate_iv(df, feature, target='target', bins=10):
    if feature not in df.columns or target not in df.columns: return 0, pd.DataFrame()
        
    df_valid = df[[feature, target]].dropna().copy()
    if len(df_valid) < 10: return 0, pd.DataFrame()
    
    try:
        df_valid['bin'] = pd.qcut(df_valid[feature], q=bins, duplicates='drop').astype(str)
    except:
        try:
            df_valid['bin'] = pd.cut(df_valid[feature], bins=bins, duplicates='drop').astype(str)
        except:
            df_valid['bin'] = df_valid[feature].astype(str)
        
    grouped = df_valid.groupby('bin', observed=True).agg(n=(target, 'count'), bads=(target, 'sum')).reset_index()
    
    grouped['goods'] = grouped['n'] - grouped['bads']
    if grouped['goods'].sum() == 0 or grouped['bads'].sum() == 0: return 0, grouped
    
    grouped['pct_goods'] = (grouped['goods'] / grouped['goods'].sum()).replace(0, 0.0001)
    grouped['pct_bads'] = (grouped['bads'] / grouped['bads'].sum()).replace(0, 0.0001)
    
    grouped['woe'] = np.log(grouped['pct_goods'] / grouped['pct_bads'])
    grouped['iv'] = (grouped['pct_goods'] - grouped['pct_bads']) * grouped['woe']
    
    return grouped['iv'].sum(), grouped

# ==============================================================================
# FUNÇÕES DE PLOTAGEM E SCORING
# ==============================================================================
def calculate_score(prob):
    return int((1 - prob) * 1000)

def get_risk_tier(score):
    """Tierização alinhada com a estratégia de Marketing/CRM (A a E)"""
    if score >= 800: return "A (Premium)", "#1B5E20"    # Verde Escuro
    if score >= 600: return "B (Seguro)", "#4CAF50"     # Verde Claro
    if score >= 400: return "C (Standard)", "#FFC107"   # Amarelo/Ouro
    if score >= 200: return "D (Atenção)", "#FF9800"    # Laranja
    return "E (Alto Risco)", "#F44336"                  # Vermelho

def plot_bad_rate_trend(summary_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=summary_df['safra'], 
            y=summary_df['total_registros'], 
            name="Volume", 
            marker_color=COLORS['neutral'], 
            opacity=0.3, 
            text=summary_df['total_registros'].apply(lambda x: f"{x/1000:.0f}k"), 
            textposition='auto'
        ), 
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=summary_df['safra'], 
            y=summary_df['bad_rate']*100, 
            name="Bad Rate (%)", 
            line=dict(color=COLORS['bad'], width=4), 
            marker=dict(size=10, symbol='circle'),
            mode='lines+markers+text',
            text=(summary_df['bad_rate']*100).apply(lambda x: f"{x:.1f}%"),
            textposition='top center',
            textfont=dict(color=COLORS['accent'], size=11, weight='bold')
        ), 
        secondary_y=True
    )

    avg_volume = summary_df['total_registros'].mean()

    avg_volume = summary_df['total_registros'].mean()
    fig.add_hline(y=avg_volume, line_dash="dash", line_width=2, line_color=COLORS['text_light'], secondary_y=False)
    fig.add_annotation(x=summary_df['safra'].iloc[-1], y=avg_volume, xref="x", yref="y", text=f"Média: {avg_volume/1000:.0f}k", showarrow=False, yshift=10, font=dict(size=12, color=COLORS['text_light']), xanchor="left", align="left")

    max_vol = summary_df['total_registros'].max()
    max_bad = (summary_df['bad_rate']*100).max()
    min_bad = (summary_df['bad_rate']*100).min()

    fig.update_layout(
        title_text="<b>Evolução Temporal:</b> Volume vs Risco / Safra", 
        hovermode="x unified", 
        legend=dict(orientation="h", y=1.2, x=0.8), 
        height=350, 
        margin=dict(l=20, r=20, t=60, b=20), 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(
        title_text="Volume de Registros", 
        secondary_y=False, 
        showgrid=False,
        range=[0, max_vol * 1.05], 
        showticklabels=False 
    )
    
    fig.update_yaxes(
        title_text="FPD (%)", 
        secondary_y=True, 
        showgrid=True, 
        gridcolor='rgba(255,255,255,0.05)',
        range=[min_bad * 0.9, max_bad * 1.4],
        showticklabels=False 
    )
    
    return fig

def plot_risk_curve_plotly(df, var, n_bins=10):
    iv, stats = calculate_iv(df, var, bins=n_bins)
    
    if stats.empty:
        fig = go.Figure(); fig.add_annotation(text="Dados insuficientes", showarrow=False); return fig
        
    stats['bin_str'] = stats['bin'].astype(str)
    stats['bad_rate'] = stats['bads'] / stats['n'] * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=stats['bin_str'], y=stats['n'], name="Volume", marker_color=COLORS['neutral'], opacity=0.4), secondary_y=False)
    fig.add_trace(go.Scatter(x=stats['bin_str'], y=stats['bad_rate'], name="Bad Rate (%)", line=dict(color=COLORS['bad'], width=3), marker=dict(size=8)), secondary_y=True)
    
    avg_bad = df['target'].mean() * 100
    fig.add_hline(y=avg_bad, line_dash="dash", line_width=1, line_color=COLORS['text_light'], secondary_y=True)
    fig.add_annotation(x=len(stats)-1, y=avg_bad, xref="x", yref="y2", text=f"Média: {avg_bad:.1f}%", showarrow=False, yshift=-10, font=dict(size=12))

    fig.update_layout(title=f"<b>Curva de Risco:</b> {var} <br><span style='font-size:12px;color:grey;'>IV: {iv:.4f}</span>", xaxis_title=f"Faixas de {var}", legend=dict(orientation="h", y=1.3, x=0.7), height=350, margin=dict(l=20, r=20, t=60, b=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(title_text="Volume", secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="Bad Rate (%)", secondary_y=True, showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    return fig

def plot_dist_comparison(df, var):
    if var not in df.columns: return go.Figure()
    plot_df = df.sample(min(10000, len(df))) if len(df) > 10000 else df
    
    fig = px.histogram(plot_df, x=var, color="target", marginal="box", barmode="overlay", nbins=50, color_discrete_map={0: COLORS['good'], 1: COLORS['bad']}, labels={'target': 'Classe (0=Bom, 1=Mau)'}, title=f"<b>Distribuição:</b> {var} por Classe")
    fig.update_layout(xaxis_title=var, yaxis_title="Frequência", legend_title="", height=350, margin=dict(l=20, r=20, t=50, b=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(y=1.2, x=0.7, orientation="h"))
    return fig


# ==============================================================================
# PLOTS DA ABA 3 (MULTIVARIADA)
# ==============================================================================
@st.cache_data(ttl=3600)
def cached_spearman_corr(df):
    """Calcula a correlação pesada uma única vez e guarda na memória."""
    return df.corr(method='spearman')

@st.cache_data(ttl=3600)
def cached_interaction_pivot(df, feat_x, feat_y, target):
    """Calcula os quintis e o pivot pesados uma única vez."""
    plot_df = df[[feat_x, feat_y, target]].dropna().copy()
    try:
        plot_df['qx'] = pd.qcut(plot_df[feat_x], 5, labels=['Q1 (Baixo)','Q2','Q3','Q4','Q5 (Alto)'], duplicates='drop')
        plot_df['qy'] = pd.qcut(plot_df[feat_y], 5, labels=['Q1 (Baixo)','Q2','Q3','Q4','Q5 (Alto)'], duplicates='drop')
        plot_df['qx'] = plot_df['qx'].astype(str)
        plot_df['qy'] = plot_df['qy'].astype(str)
    except:
        plot_df['qx'] = pd.cut(plot_df[feat_x], 5, duplicates='drop').astype(str)
        plot_df['qy'] = pd.cut(plot_df[feat_y], 5, duplicates='drop').astype(str)
        
    return plot_df.pivot_table(index='qy', columns='qx', values=target, aggfunc='mean') * 100


def plot_correlation_matrix(df):
    """Gera matriz de correlação de Spearman para variáveis numéricas."""
    numeric_df = df.select_dtypes(include=[np.number])
    cols_to_drop = ['target', 'fpd', 'num_cpf', 'cpf', 'safra_int']
    numeric_df = numeric_df.drop(columns=[c for c in cols_to_drop if c in numeric_df.columns], errors='ignore')

    if numeric_df.empty:
        return go.Figure()

    corr = cached_spearman_corr(numeric_df)

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale='RdBu_r', 
        zmin=-1, zmax=1,
        aspect="auto",
        title="<b>Matriz de Correlação (Spearman)</b>"
    )
    
    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def plot_interaction_matrix(df, feat_x, feat_y, target='target'):
    """Gera Heatmap de Risco cruzando quintis de duas variáveis."""
    if feat_x not in df.columns or feat_y not in df.columns or target not in df.columns:
        return go.Figure()

    pivot = cached_interaction_pivot(df, feat_x, feat_y, target)

    fig = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale='RdYlGn_r',
        labels=dict(x=f"{feat_x} (Faixas)", y=f"{feat_y} (Faixas)", color="Bad Rate %"),
        origin='lower',
        title=f"<b>Matriz de Risco Combinada:</b> {feat_x} vs {feat_y}"
    )

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# ==============================================================================
# RANKING E IMPORTÂNCIA DE VARIÁVEIS (ABA 4)
# ==============================================================================
@st.cache_data(ttl=3600)
def get_feature_ranking(df, target='target'):
    """
    Gera um DataFrame com o ranking de IV e Gini para todas as variáveis numéricas.
    """
    if df.empty or target not in df.columns:
        return pd.DataFrame()

    ignored = ['target', 'fpd', 'safra', 'num_cpf', 'cpf', 'safra_int']
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    candidates = [c for c in numeric_cols if c not in ignored]

    metrics_list = []

    for feature in candidates:
        iv_val, _ = calculate_iv(df, feature, target)

        try:
            clean_series = df[feature].fillna(df[feature].median())
            
            auc = roc_auc_score(df[target], clean_series)
            
            if auc < 0.5: 
                auc = 1 - auc
            
            gini = (2 * auc - 1) * 100
        except:
            gini = 0.0

        if iv_val < 0.02: quality = "Inútil"
        elif iv_val < 0.1: quality = "Fraco"
        elif iv_val < 0.3: quality = "Médio"
        elif iv_val < 0.5: quality = "Forte"
        else: quality = "Muito Forte"

        metrics_list.append({
            'Variável': feature,
            'IV': iv_val,
            'Gini (%)': gini,
            'Qualidade': quality
        })

    rank_df = pd.DataFrame(metrics_list).sort_values(by='IV', ascending=False)
    
    return rank_df


# ==============================================================================
# ESTABILIDADE (PSI) - ABA 5
# ==============================================================================
def calculate_psi(expected, actual, bins=10):
    """
    Calcula o Population Stability Index (PSI) entre duas distribuições.
    """
    try:
        expected = np.array(expected)
        actual = np.array(actual)
        
        min_val = min(np.min(expected), np.min(actual))
        max_val = max(np.max(expected), np.max(actual))
        
        edges = np.linspace(min_val, max_val, bins + 1)
        
        expected_cnt, _ = np.histogram(expected, bins=edges)
        actual_cnt, _ = np.histogram(actual, bins=edges)
        
        epsilon = 0.0001
        expected_dist = (expected_cnt / len(expected)) + epsilon
        actual_dist = (actual_cnt / len(actual)) + epsilon
        
        psi_values = (expected_dist - actual_dist) * np.log(expected_dist / actual_dist)
        psi = np.sum(psi_values)
        
        return psi
    except:
        return 0.0

def plot_psi_distribution(expected, actual, label_base, label_curr, feature):
    """Gera histograma comparativo para análise visual de Drift."""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=expected, 
        name=f"Base: {label_base}", 
        opacity=0.6, 
        marker_color=COLORS['neutral'],
        histnorm='probability'
    ))
    
    fig.add_trace(go.Histogram(
        x=actual, 
        name=f"Atual: {label_curr}", 
        opacity=0.6, 
        marker_color=COLORS['accent'], 
        histnorm='probability'
    ))
    
    fig.update_layout(
        title=f"<b>Comparativo de Distribuição:</b> {feature}",
        barmode='overlay',
        xaxis_title=feature,
        yaxis_title="Densidade (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1),
        height=300,
        margin=dict(l=20, r=20, t=60, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


# ==============================================================================
# SIMULADOR DE POLÍTICA (ABA 6)
# ==============================================================================
def calculate_policy_curve(df, min_age, min_payment):
    """
    Calcula o trade-off entre Aprovação e Bad Rate para diferentes cutoffs de score.
    Retorna um DataFrame pronto para plotagem.
    """
    cutoffs = np.arange(300, 901, 25)
    rows = []
    
    mask_static = (
        (df['idade'] >= min_age) & 
        (df['pag_vlr_total_geral'].fillna(0) >= min_payment)
    ).fillna(False) 
    
    total_obs = len(df)
    
    for c in cutoffs:
        mask_score = (df['behavior_score'] >= c).fillna(False)
        mask_final = mask_static & mask_score
        
        aprovados = mask_final.sum()
        approval_rate = aprovados / total_obs
        
        if aprovados > 0:
            bad_rate = df.loc[mask_final, 'target'].mean()
        else:
            bad_rate = np.nan
            
        rows.append({
            "cutoff": c,
            "approval_rate": approval_rate * 100,
            "bad_rate": bad_rate * 100
        })
        
    return pd.DataFrame(rows)

def plot_policy_tradeoff(curve_df, active_cutoff, sweet_spot):
    """Plota a curva de Aprovação vs Risco."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=curve_df['cutoff'], y=curve_df['approval_rate'], name="Aprovação (%)",
                   line=dict(color=COLORS['success'], width=3)),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=curve_df['cutoff'], y=curve_df['bad_rate'], name="Bad Rate (%)",
                   line=dict(color=COLORS['danger'], width=3, dash='dot')),
        secondary_y=True
    )
    
    fig.add_vline(x=active_cutoff, line_dash="solid", line_color="white", 
                  annotation_text=f"Cutoff: {active_cutoff}")
    
    if sweet_spot:
        fig.add_vline(x=sweet_spot, line_dash="dash", line_color=COLORS['warning'], 
                      annotation_text=f"Sugestão IA: {sweet_spot}", annotation_position="bottom right")
    
    fig.update_layout(
        title="<b>Curva de Trade-off:</b> Risco vs Retorno",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02, x=1),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(title_text="Taxa de Aprovação (%)", secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="Bad Rate Esperado (%)", secondary_y=True, showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def plot_decision_boundary(df, cutoff, min_age, min_pay):
    """Scatter plot mostrando a fronteira de decisão (Idade vs Score)."""
    plot_df = df.sample(min(2000, len(df))).copy()
    
    mask = (
        (plot_df['behavior_score'] >= cutoff) & 
        (plot_df['idade'] >= min_age) & 
        (plot_df['pag_vlr_total_geral'].fillna(0) >= min_pay)
    )
    
    mask = mask.fillna(False)

    plot_df['Decisão'] = np.where(mask, 'Aprovado', 'Reprovado')
    
    fig = px.scatter(
        plot_df, x='idade', y='behavior_score', color='Decisão',
        color_discrete_map={'Aprovado': COLORS['success'], 'Reprovado': COLORS['neutral']},
        title="<b>Fronteira de Decisão:</b> Score vs Idade",
        opacity=0.6
    )
    
    fig.add_hline(y=cutoff, line_dash="dash", line_color="white")
    fig.add_vline(x=min_age, line_dash="dash", line_color="white")
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig



# ==============================================================================
# ANÁLISE DEMOGRÁFICA (ABA 6)
# ==============================================================================

STATE_COORDS = {
    'AC': (-8.77, -70.55), 'AL': (-9.71, -35.73), 'AM': (-4.9, -64.56),
    'AP': (1.41, -51.77), 'BA': (-12.96, -38.51), 'CE': (-3.71, -38.54),
    'DF': (-15.83, -47.86), 'ES': (-19.19, -40.34), 'GO': (-16.64, -49.31),
    'MA': (-2.55, -44.30), 'MG': (-18.10, -44.38), 'MS': (-20.51, -54.54),
    'MT': (-12.64, -55.42), 'PA': (-5.53, -52.29), 'PB': (-7.06, -35.55),
    'PE': (-8.28, -35.07), 'PI': (-8.28, -43.68), 'PR': (-24.89, -51.55),
    'RJ': (-22.84, -43.15), 'RN': (-5.22, -36.52), 'RO': (-11.22, -62.80),
    'RR': (1.87, -61.21), 'RS': (-30.01, -51.22), 'SC': (-27.33, -49.44),
    'SE': (-10.90, -37.07), 'SP': (-23.55, -46.64), 'TO': (-10.25, -48.25)
}

STATE_NAMES = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
    'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
    'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
    'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins', 'OUTROS': 'Outros'
}

REGION_MAP = {
    'AC': 'Norte', 'AL': 'Nordeste', 'AP': 'Norte', 'AM': 'Norte',
    'BA': 'Nordeste', 'CE': 'Nordeste', 'DF': 'Centro-Oeste', 'ES': 'Sudeste',
    'GO': 'Centro-Oeste', 'MA': 'Nordeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'MG': 'Sudeste', 'PA': 'Norte', 'PB': 'Nordeste', 'PR': 'Sul',
    'PE': 'Nordeste', 'PI': 'Nordeste', 'RJ': 'Sudeste', 'RN': 'Nordeste',
    'RS': 'Sul', 'RO': 'Norte', 'RR': 'Norte', 'SC': 'Sul',
    'SP': 'Sudeste', 'SE': 'Nordeste', 'TO': 'Norte', 'OUTROS': 'Outros'
}

def map_cep_to_uf(cep_3):
    """Mapeia os 3 primeiros dígitos do CEP para UF (Lógica simplificada do notebook)."""
    try:
        c = int(cep_3)
        if 10 <= c <= 199: return 'SP'
        if 200 <= c <= 289: return 'RJ'
        if 290 <= c <= 299: return 'ES'
        if 300 <= c <= 399: return 'MG'
        if 400 <= c <= 489: return 'BA'
        if 490 <= c <= 499: return 'SE'
        if 500 <= c <= 569: return 'PE'
        if 570 <= c <= 579: return 'AL'
        if 580 <= c <= 589: return 'PB'
        if 590 <= c <= 599: return 'RN'
        if 600 <= c <= 639: return 'CE'
        if 640 <= c <= 649: return 'PI'
        if 650 <= c <= 659: return 'MA'
        if 660 <= c <= 688: return 'PA'
        if 689 <= c <= 689: return 'AP'
        if 690 <= c <= 692: return 'AM'
        if 693 <= c <= 693: return 'RR'
        if 694 <= c <= 698: return 'AM'
        if 699 <= c <= 699: return 'AC'
        if 700 <= c <= 736: return 'DF'
        if 737 <= c <= 767: return 'GO'
        if 768 <= c <= 769: return 'RO'
        if 770 <= c <= 779: return 'TO'
        if 780 <= c <= 788: return 'MT'
        if 790 <= c <= 799: return 'MS'
        if 800 <= c <= 879: return 'PR'
        if 880 <= c <= 899: return 'SC'
        if 900 <= c <= 999: return 'RS'
        return 'OUTROS'
    except:
        return 'OUTROS'

def process_demographics(df):
    """
    Transformação 100% Real: Mapeia CEP para UF e trata Unicidade por CPF.
    """
    df.columns = [str(c).lower() for c in df.columns]

    if 'cad_cep_3_digitos' in df.columns:
        df['uf'] = df['cad_cep_3_digitos'].apply(map_cep_to_uf)
    else:
        df['uf'] = 'OUTROS'

    df['estado_nome'] = df['uf'].map(STATE_NAMES).fillna(df['uf'])
    df['regiao'] = df['uf'].map(REGION_MAP).fillna('Outros')

    if 'idade' in df.columns:
        bins_idade = [18, 25, 35, 45, 55, 65, 100]
        labels_idade = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        df['faixa_etaria'] = pd.cut(df['idade'], bins=bins_idade, labels=labels_idade, right=False)

    return df

def plot_age_analysis(df):
    """Gráfico Volume vs Risco por Idade."""
    stats = df.groupby('faixa_etaria', observed=True).agg(
        n=('target', 'count'),
        bad_rate=('target', 'mean')
    ).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=stats['faixa_etaria'], y=stats['n'], name="Volume", 
               marker_color=COLORS['neutral'], opacity=0.5),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=stats['faixa_etaria'], y=stats['bad_rate']*100, name="Bad Rate (%)",
                   line=dict(color=COLORS['bad'], width=3), marker=dict(size=8)),
        secondary_y=True
    )
    
    avg_bad = df['target'].mean() * 100
    fig.add_hline(
        y=avg_bad,
        line_dash="dash",
        line_width=2,
        line_color=COLORS['text_light'],
        secondary_y=True
    )

    fig.add_annotation(
        x=stats['faixa_etaria'].iloc[-1],
        y=avg_bad,
        xref="x",
        yref="y2",
        text=f"Média: {avg_bad:.1f}%",
        showarrow=False,
        yshift=10,
        font=dict(size=12, color=COLORS['text_light']),
        xanchor="left",
        align="left"
    )

    fig.update_layout(
        title="<b>Risco por Faixa Etária</b>",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(title_text="Volume", secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="Bad Rate (%)", secondary_y=True, showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

@st.cache_data(show_spinner=False)
def get_cached_geojson():
    """Lê o arquivo de mapas uma única vez e guarda em cache."""
    try:
        with open("streamlit/utils/br_states.geojson", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"features": []}

def plot_geo_map(df, uf_selecionada=None, regiao_sel=None):
    """
    Mapa de Bolhas Geolocalizado.
    Visualização profissional com foco em densidade e risco.
    """
    geojson = get_cached_geojson()
    locations = [f["properties"]["sigla"] for f in geojson.get("features", [])]

    stats = df.groupby(['uf', 'estado_nome']).agg(
        n=('target', 'count'),
        bad_rate=('target', 'mean')
    ).reset_index()
    
    coords_df = (
        pd.DataFrame.from_dict(
            STATE_COORDS,
            orient="index",
            columns=["lat", "lon"]
        )
        .reset_index()
        .rename(columns={"index": "uf"})
    )

    stats = stats.merge(coords_df, on="uf", how="left")
    stats = stats.dropna(subset=["lat"])

    if len(stats) == 1:
        center_lat = stats['lat'].values[0]
        center_lon = stats['lon'].values[0]
        zoom_level = 5
    else:
        center_lat = -15.5
        center_lon = -49.5
        zoom_level = 2.8

    fig = px.scatter_mapbox(
        stats,
        lat="lat", 
        lon="lon",
        size="n",
        color="bad_rate",
        hover_name="estado_nome",
        hover_data={
            'bad_rate': ':.1%', 
            'n': True, 
            'lat': False, 
            'lon': False, 
            'uf': False
        },
        color_continuous_scale="RdYlGn_r", 
        size_max=45, 
        zoom=zoom_level,
        center={"lat": center_lat, "lon": center_lon},
        title="<b>Mapa de Risco (UF)</b>"
    )

    fig.update_layout(
        mapbox_style="carto-positron", 
        margin=dict(l=20, r=20, t=40, b=20),
        height=450,
        
        coloraxis_colorbar=dict(
            title="Bad Rate",
            thickness=12,
            len=0.5,
            yanchor="top", y=0.95,
            xanchor="right", x=0.98,
            title_font=dict(size=10, color="gray"),
            tickfont=dict(size=9, color="gray"),
            bgcolor="rgba(255,255,255,0.8)" 
        ),
        
        hoverlabel=dict(
            bgcolor="#1A1C24",
            font_size=12,
            font_family="Inter, sans-serif"
        )
    )


    z = [0] * len(locations)
    line_widths = [0.4] * len(locations)
    line_colors = ["#3A7C89"] * len(locations)

    reg = regiao_sel if regiao_sel is not None else "Todas"
    est = uf_selecionada if uf_selecionada is not None else "Todos"

    if reg not in ["Brasil (Todas)", "Todas"] and est in ["Todos", None]:

        estados_da_regiao = [
            uf for uf, r in REGION_MAP.items() if r == reg
        ]

        z = [1.8 if sigla in estados_da_regiao else 0 for sigla in locations]
        line_widths = [1.4 if sigla in estados_da_regiao else 0.4 for sigla in locations]
        line_colors = ["#3A7C89"] * len(locations)

    elif est not in ["Todos", None]:

        z = [1.8 if sigla == est else 0 for sigla in locations]
        line_widths = [1.4 if sigla == est else 0.4 for sigla in locations]
        line_colors = ["#3A7C89"] * len(locations)


    fig.add_trace(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=locations,
            z=[0] * len(locations),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            showscale=False,
            marker_line_width=line_widths,
            marker_line_color=line_colors,
            featureidkey="properties.sigla",
            hoverinfo="skip",
            autocolorscale=False
        )
    )
    
    return fig


def plot_tierizacao_financeira(df, conversao, upsell, ltv, arpu, meses_inad, fator_escala=20):
    """
    Gera o gráfico de EBITDA Potencial vs Bad Rate por Tier de Risco.
    fator_escala=20 assume que o df é uma amostra de 5% da base total (20 * 5 = 100%).
    """
    # Cria os 5 decis (Ratings A-E) com base na probabilidade do modelo
    df_plot = df.copy()
    
    # Evita erro caso os decis gerem bordas duplicadas
    df_plot['rating_crm'] = pd.qcut(df_plot['prob_modelo'], q=5, labels=['A (Premium)', 'B (Seguro)', 'C (Standard)', 'D (Atenção)', 'E (Alto Risco)'], duplicates='drop')

    analise_tier = df_plot.groupby('rating_crm', observed=True).agg(
        Volume_CPFs=('prob_modelo', 'count'),
        Inadimplencia_FPD=('target', 'mean')
    ).reset_index()

    # Escala os volumes e calcula a receita potencial por Tier
    analise_tier['Vol_Nacional'] = analise_tier['Volume_CPFs'] * fator_escala * conversao
    
    # Lógica de negócio: Receita (Bons) - Prejuízo (Maus)
    receita = (analise_tier['Vol_Nacional'] * (1 - analise_tier['Inadimplencia_FPD']) * upsell * ltv)
    prejuizo = (analise_tier['Vol_Nacional'] * analise_tier['Inadimplencia_FPD'] * arpu * meses_inad)
    analise_tier['EBITDA_Potencial'] = receita - prejuizo

    # Criação do gráfico com 2 eixos
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=analise_tier['rating_crm'], 
        y=analise_tier['EBITDA_Potencial'],
        name="EBITDA Incremental Projetado (R$)",
        marker_color=['#1B5E20', '#4CAF50', '#D4A017', '#FF9800', '#B53744'], # Cores alinhadas ao tema
        opacity=0.85,
        text=analise_tier['EBITDA_Potencial'].apply(lambda x: f"R$ {x/1e6:.1f}M" if x > 0 else f"-R$ {abs(x)/1e6:.1f}M"),
        textposition="outside"
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=analise_tier['rating_crm'], 
        y=analise_tier['Inadimplencia_FPD'] * 100,
        name="Inadimplência FPD (%)",
        mode="lines+markers+text",
        text=(analise_tier['Inadimplencia_FPD'] * 100).apply(lambda x: f"{x:.1f}%"),
        textposition="top center",
        line=dict(color='#DAD0D1', width=3, dash='dot'), 
        marker=dict(size=10, color='#FFF')
    ), secondary_y=True)

    fig.update_layout(
        title="<b>Tierização Estratégica: Receita vs Risco por Segmento</b>",
        height=450,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
    )
    
    # Ajusta o eixo Y para dar espaço aos rótulos
    max_ebitda = analise_tier['EBITDA_Potencial'].max()
    min_ebitda = analise_tier['EBITDA_Potencial'].min()
    fig.update_yaxes(title_text="EBITDA Projetado (R$)", secondary_y=False, range=[min_ebitda * 1.2, max_ebitda * 1.3])
    fig.update_yaxes(title_text="FPD (%)", secondary_y=True, showgrid=False)

    return fig