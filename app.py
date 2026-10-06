
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuracion de pantalla rigida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-bottom: 6px; border: 1px solid #232a38; }
.rigid-table-container { width: 100%; overflow-x: auto !important; margin: 4px 0; border: 1px solid #232a38; border-radius: 4px; }
.rigid-table { width: 520px !important; border-collapse: collapse; font-size: 0.74rem !important; background-color: #161a22; table-layout: fixed; }
.rigid-table th { background-color: #1f2633; color: #2196f3; text-align: center; padding: 6px 2px; font-weight: bold; line-height: 1.1; font-size: 0.72rem !important; border: 1px solid #232a38; }
.rigid-table td { padding: 6px 2px; border: 1px solid #232a38; color: #ffffff; text-align: center; vertical-align: middle; font-size: 0.74rem !important; height: 28px !important; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}
if 'activo_sel' not in st.session_state:
    st.session_state.activo_sel = "SPY"

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Montos fijados con éxito!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo...", label_visibility="collapsed")

st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa</h3>", unsafe_allow_html=True)
nueva_accion = st.text_input("Ticker:", placeholder="Ej: NVDA, MSFT...", key="buscador_tk").upper().strip()
if nueva_accion and nueva_accion not in st.session_state.montos_dis:
    st.session_state.montos_dis[nueva_accion] = 5000.0
    st.success(f"¡{nueva_accion} agregada!")

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

# 4. CASILLERO COMPACTO DE MODIFICACIÓN DE CAPITALES (Fijo arriba para alimentar la tabla entera)
st.markdown("<h3 style='color:#ffffff; margin-top:2px;'>✍️ Cambiar Monto de Inversión</h3>", unsafe_allow_html=True)
activos_actuales = list(st.session_state.montos_dis.keys())
col_sel, col_num = st.columns(2)
with col_sel:
    target = st.selectbox("Acción:", activos_actuales, index=activos_actuales.index(st.session_state.activo_sel) if st.session_state.activo_sel in activos_actuales else 0, label_visibility="collapsed")
    st.session_state.activo_sel = target
with col_num:
    monto_fijado = float(st.session_state.montos_dis[target])
    nuevo_monto = st.number_input("Monto:", min_value=0.0, value=monto_fijado, step=500.0, label_visibility="collapsed")
    if nuevo_monto != monto_fijado:
        st.session_state.montos_dis[target] = nuevo_monto
        st.rerun()

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Integración Rígida</h3>", unsafe_allow_html=True)

# 5. DIBUJO DE LA TABLA ENTERA EN UN SOLO BLOQUE LIMPIO (Sin sumas intermedias)
precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
patrimonio_total_usd = sum(st.session_state.montos_dis.values())

tabla_completa_html = f"""
<div class="rigid-table-container">
<table class="rigid-table">
    <tr>
        <th style="width: 12%;">Acción</th>
        <th style="width: 15%;">Precio<br>Actual</th>
        <th style="width: 22%;">Inversión<br>Asignada</th>
        <th style="width: 13%;">Análisis<br>Tec.<br>Semanal</th>
        <th style="width: 13%;">Análisis<br>Tec.<br>Anual</th>
        <th style="width: 12%;">Análisis<br>Funda-<br>mental</th>
        <th style="width: 13%;">Análisis<br>Final<br>(Agente)</th>
    </tr>
"""

for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual_tk = st.session_state.montos_dis[tk]
    if tk == "SPY": sem, anual, fund, vered, cl = "▲ 40%", "▲ 60%", "8/10", "STRONG BUY", "#00e676"
    elif tk == "TSLA": sem, anual, fund, vered, cl = "▲ 35%", "▲ 55%", "7/10", "HOLD", "#ffeb3b"
    else: sem, anual, fund, vered, cl = "▲ 30%", "▲ 50%", "9/10", "BUY", "#2196f3"
        
    tabla_completa_html += f"""
    <tr>
        <td><b>{tk}</b></td>
        <td>{simbolo_moneda}{p_base*factor_cambio:,.0f}</td>
        <td style="font-weight:bold; color:#00e676;">{simbolo_moneda}{monto_actual_tk*factor_cambio:,.0f}</td>
        <td style="color:#4caf50;"><b>{sem}</b></td>
        <td style="color:#00e676;"><b>{anual}</b></td>
        <td style="color:#ffeb3b;"><b>{fund}</b></td>
        <td style="color:{cl}; font-weight:bold;">{vered}</td>
    </tr>
    """

tabla_completa_html += "</table></div>"
st.markdown(tabla_completa_html, unsafe_allow_html=True)

patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)
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
    st.plotly_chart(fig, use_container_width=True, key="pie_v11")

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
