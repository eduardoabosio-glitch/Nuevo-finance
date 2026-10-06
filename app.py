
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuracion de pantalla rigida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Diseña las Fichas Rectangulares de Acero sin botoneras de mas/menos
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-bottom: 6px; border: 1px solid #232a38; }

/* Molde de la Tarjeta Rectangular de Acero Inmóvil por Empresa */
.tarjeta-activo { background-color: #161a22; padding: 10px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 10px; }
.fila-tarjeta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; font-size: 0.82rem; color: #ffffff; }

/* Bloqueo absoluto de las botoneras flotantes de mas y menos de Streamlit */
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { background-color: #1f2633 !important; color: #00e676 !important; font-weight: bold !important; text-align: center !important; font-size: 0.88rem !important; border-radius: 4px !important; border: 1px solid #232a38 !important; height: 28px !important; }
div[data-testid="stNumberInput"] label { display: none !important; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

# 3. BASE DE DATOS INTERNA DE INVERSIONES DINÁMICAS
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Fichas de Inversión Verticales Anti-Desarme</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Estructura y montos fijados con éxito en la memoria!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre tus inversiones...", label_visibility="collapsed")

st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa</h3>", unsafe_allow_html=True)
nueva_accion = st.text_input("Ticker:", placeholder="Ej: NVDA, MSFT...", key="buscador_tk").upper().strip()
if nueva_accion and nueva_accion not in st.session_state.montos_dis:
    st.session_state.montos_dis[nueva_accion] = 5000.0
    st.success(f"¡{nueva_accion} agregada con éxito!")

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Fichas Unificadas</h3>", unsafe_allow_html=True)

# 4. GENERACIÓN DE TARJETAS VERTICALES INDEPENDIENTES REUTILIZABLES
precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0, "NVDA": 130.0, "MSFT": 420.0}
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0

for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual = st.session_state.montos_dis[tk]
    patrimonio_total_usd += monto_actual
    
    if tk == "SPY": sem, anual, fund, vered, cl = "▲ 40%", "▲ 60%", "8/10", "STRONG BUY", "#00e676"
    elif tk == "TSLA": sem, anual, fund, vered, cl = "▲ 35%", "▲ 55%", "7/10", "HOLD", "#ffeb3b"
    elif tk == "AAPL": sem, anual, fund, vered, cl = "▲ 30%", "▲ 50%", "9/10", "BUY", "#2196f3"
    else: sem, anual, fund, vered, cl = "▲ 32%", "▲ 48%", "8/10", "BUY", "#2196f3"

    # Estructura limpia en HTML rígido para acomodar los 7 datos ordenados por bloque
    st.markdown(f"""
    <div class="tarjeta-activo">
        <div class="fila-tarjeta"><b style="font-size:1.1rem; color:#2196f3;">{tk}</b> <span style="color:{cl}; font-weight:bold; font-size:0.85rem;">{vered}</span></div>
        <div class="fila-tarjeta"><span>Precio Actual: <b>{simbolo_moneda}{p_base*factor_cambio:,.0f}</b></span> <span>Semanal: <b style="color:#4caf50;">{sem}</b></span></div>
        <div class="fila-tarjeta"><span>Fundamental: <b style="color:#ffeb3b;">{fund}</b></span> <span>Anual: <b style="color:#00e676;">{anual}</b></span></div>
        <div style="margin: 3px 0 1px 0; font-size:0.75rem; color:#888;">✍️ Modificar Capital Invertido:</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Caja numérica fina perfectamente camuflada adentro de la base de cada bloque
    st.session_state.montos_dis[tk] = st.number_input(f"mod_{tk}", min_value=0.0, value=float(monto_actual), step=500.0, key=f"input_box_{tk}")

# Patrimonio Total Destacado Dinámico abajo de las fichas
patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white; margin-top:8px;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)

# 5. MENÚ DESPLEGABLE DE GRÁFICOS REALES EN VIVO
st.markdown("<h3 style='color:#ffffff;'>📈 Visualizar Gráficos Avanzados</h3>", unsafe_allow_html=True)
accion_para_grafico = st.selectbox("Elegí:", activos_actuales, label_visibility="collapsed", key="graf_av")
if accion_para_grafico:
    with st.expander(f"📊 Ver Gráfico para {accion_para_grafico}", expanded=False):
        try:
            ticker_y = yf.Ticker(accion_para_grafico)
            historial = ticker_y.history(period="6mo")
            if not historial.empty: st.line_chart(historial["Close"], height=130)
        except: st.caption("Cargando curvas...")

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)
col_g1, col_g2 = st.columns(2)
with col_g1:
    df_pie = pd.DataFrame({"Activo": list(st.session_state.montos_dis.keys()), "Capital": list(st.session_state.montos_dis.values())})
    fig = px.pie(df_pie, values='Capital', names='Activo', hole=0.4, height=120)
    fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, key="pie_v16")

with col_g2:
    st.markdown('''
    <div style="background-color:#161a22; padding:5px; border-radius:4px; font-size:0.72rem; border:1px solid #232a38; height:120px; color:white;">
        <b style="color:#2196f3;">Resumen de Agente</b><br>• Impacto: Favorable<br>• Análisis: Cartera Diversificada<br>• Sugerencia: Mantener Capitales
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)
st.markdown('''
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161a22; border-top: 1px solid #232a38; display: flex; justify-content: space-around; padding: 4px 0; z-index: 1000; font-size:0.68rem; text-align:center;">
    <div style="color:#888;">🏠<br>Inicio</div>
    <div style="color:#2196f3; font-weight:bold;">💼<br>Portafolio</div>
    <div style="color:#888;">📊<br>Análisis</div>
    <div style="color:#888;">💬<br>Chat</div>
    <div style="color:#888;">👤<br>Perfil</div>
</div>
''', unsafe_allow_html=True)
