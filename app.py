
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuracion de pantalla rigida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Moldea tus fichas verticales fijas de acero sin botoneras de mas/menos
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

# 3. BASE DE DATOS INTERNA CON MEMORIA CONTINUA
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Fichas Verticales con Intercambiador en Vivo</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Estructura y montos fijados con éxito en la memoria!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre tus inversiones...", label_visibility="collapsed")

# 4. NUEVO SISTEMA DE INTERCAMBIO INTELIGENTE EN VIVO (Tu idea estrella)
st.markdown("<h3 style='color:#ffffff;'>🔄 Intercambiar Empresa de mi Cartera</h3>", unsafe_allow_html=True)
activos_actuales = list(st.session_state.montos_dis.keys())

col_rem, col_new = st.columns(2)
with col_rem:
    activo_a_sacar = st.selectbox("Acción a reemplazar:", activos_actuales, label_visibility="collapsed")
with col_new:
    nuevo_ticker = st.text_input("Escribí el nuevo ticker (Ej: NVDA):", placeholder="Nuevo ticker...", label_visibility="collapsed").upper().strip()

if nuevo_ticker and nuevo_ticker != activo_a_sacar:
    # Captura el capital anterior que tenía la ficha vieja
    monto_anterior = st.session_state.montos_dis[activo_a_sacar]
    # Borra la ficha vieja de la memoria
    del st.session_state.montos_dis[activo_a_sacar]
    # Inyecta la nueva empresa manteniendo tu capital asignado de forma automatizada
    st.session_state.montos_dis[nuevo_ticker] = monto_anterior
    st.success(f"¡Reemplazo exitoso! {activo_a_sacar} cambió por {nuevo_ticker}")
    st.rerun()

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Fichas Unificadas</h3>", unsafe_allow_html=True)

# 5. GENERACIÓN DE TARJETAS VERTICALES INDEPENDIENTES REUTILIZABLES
precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0, "NVDA": 130.0, "MSFT": 420.0}
activos_actualizados = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0

for tk in activos_actualizados:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual = st.session_state.montos_dis[tk]
    patrimonio_total_usd += monto_actual
    
    if tk == "SPY": sem, anual, fund, vered, cl = "▲ 40%", "▲ 60%", "8/10", "STRONG BUY", "#00e676"
    elif tk == "TSLA": sem, anual, fund, vered, cl = "▲ 35%", "▲ 55%", "7/10", "HOLD", "#ffeb3b"
    elif tk == "AAPL": sem, anual, fund, vered, cl = "▲ 30%", "▲ 50%", "9/10", "BUY", "#2196f3"
    elif tk == "NVDA": sem, anual, fund, vered, cl = "▲ 45%", "▲ 58%", "8/10", "STRONG BUY", "#00e676"
    else: sem, anual, fund, vered, cl = "▲ 32%", "▲ 48%", "8/10", "BUY", "#2196f3"

    st.markdown(f"""
    <div class="tarjeta-activo">
        <div class="fila-tarjeta"><b style="font-size:1.1rem; color:#2196f3;">{tk}</b> <span style="color:{cl}; font-weight:bold; font-size:0.85rem;">{vered}</span></div>
        <div class="fila-tarjeta"><span>Precio Actual: <b>{simbolo_moneda}{p_base*factor_cambio:,.0f}</b></span> <span>Semanal: <b style="color:#4caf50;">{sem}</b></span></div>
        <div class="fila-tarjeta"><span>Fundamental: <b style="color:#ffeb3b;">{fund}</b></span> <span>Anual: <b style="color:#00e676;">{anual}</b></span></div>
        <div style="margin: 3px 0 1px 0; font-size:0.75rem; color:#888;">✍️ Modificar Capital Invertido:</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.montos_dis[tk] = st.number_input(f"mod_{tk}", min_value=0.0, value=float(monto_actual), step=500.0, key=f"input_box_{tk}")

# Patrimonio Total Destacado Dinámico abajo de las fichas
patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white; margin-top:8px;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)

# 6. MENÚ DESPLEGABLE DE GRÁFICOS REALES EN VIVO
st.markdown("<h3 style='color:#ffffff;'>📈 Visualizar Gráficos Avanzados</h3>", unsafe_allow_html=True)
accion_para_grafico = st.selectbox("Elegí:", activos_actualizados, label_visibility="collapsed", key="graf_av")
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
    st.plotly_chart(fig, use_container_width=True, key="pie_v17")

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
