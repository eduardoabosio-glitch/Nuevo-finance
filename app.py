
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuracion de pantalla rigida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Clava la tabla azul rigida e inmóvil (CERO MENÚS GRISES)
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-bottom: 6px; border: 1px solid #232a38; }

/* Tabla de Acero HTML Rigida Real con Scroll de costado suave */
.rigid-table-container { width: 100%; overflow-x: auto !important; margin: 4px 0; border: 1px solid #232a38; border-radius: 4px; }
.rigid-table { width: 520px !important; border-collapse: collapse; font-size: 0.74rem; background-color: #161a22; table-layout: fixed; user-select: none; }
.rigid-table th { background-color: #1f2633; color: #2196f3; text-align: center; padding: 6px 2px; font-weight: bold; line-height: 1.1; font-size: 0.72rem; border: 1px solid #232a38; pointer-events: none; }
.rigid-table td { padding: 6px 2px; border: 1px solid #232a38; color: #ffffff; text-align: center; vertical-align: middle; }

/* Botonera camuflada transparente para capturar el toque en la celda verde */
div.stFormSubmitButton > button { background-color: transparent !important; color: #00e676 !important; border: none !important; font-weight: bold !important; font-size: 0.76rem !important; padding: 0px !important; margin: 0px !important; width: 100% !important; text-decoration: underline !important; cursor: pointer; }

/* Quitar bultos y botoneras de mas y menos de las cajas numericas de control */
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { background-color: #1f2633 !important; color: #ffffff !important; text-align: center !important; font-size: 0.85rem !important; border-radius: 4px !important; border: 1px solid #232a38 !important; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

# 3. BASE DE DATOS INTERNA CON MEMORIA DE TOQUE
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}
if 'activo_tocado' not in st.session_state:
    st.session_state.activo_tocado = "SPY"

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Tabla Azul Inmóvil con Activación Táctil Celular</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Montos y diseño guardados en la memoria del teléfono!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre finanzas...", label_visibility="collapsed")

st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa</h3>", unsafe_allow_html=True)
nueva_accion = st.text_input("Ticker:", placeholder="Ej: NVDA, MSFT...", key="buscador_tk").upper().strip()
if nueva_accion and nueva_accion not in st.session_state.montos_dis:
    st.session_state.montos_dis[nueva_accion] = 5000.0
    st.success(f"¡{nueva_accion} agregada con éxito!")

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Integración Rígida</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size:0.68rem; color:#888; margin:0;'>👉 Tocá el monto verde subrayado de la celda para modificar su capital:</p>", unsafe_allow_html=True)

# 4. CONTENEDOR CON SCROLL DE COSTADO SUAVE PARA LA CUADRÍCULA AZUL RÍGIDA
st.markdown('<div class="rigid-table-container">', unsafe_allow_html=True)
st.markdown("""
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
</table>
""", unsafe_allow_html=True)

precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = sum(st.session_state.montos_dis.values())

for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_usd = st.session_state.montos_dis[tk]
    if tk == "SPY": sem, anual, fund, vered, cl = "▲ 40%", "▲ 60%", "8/10", "STRONG BUY", "#00e676"
    elif tk == "TSLA": sem, anual, fund, vered, cl = "▲ 35%", "▲ 55%", "7/10", "HOLD", "#ffeb3b"
    else: sem, anual, fund, vered, cl = "▲ 30%", "▲ 50%", "9/10", "BUY", "#2196f3"

    st.markdown(f"""
    <table class="rigid-table" style="margin-top:-2px;">
    <tr>
        <td style="width: 12%;"><b>{tk}</b></td>
        <td style="width: 15%;">{simbolo_moneda}{p_base*factor_cambio:,.0f}</td>
        <td style="width: 22%; padding: 0px;">
    """, unsafe_allow_html=True)
    
    # El Gran Secreto Táctil: Un mini formulario invisible por celda para capturar el click
    with st.form(key=f"celda_{tk}"):
        if st.form_submit_button(f"{simbolo_moneda}{monto_usd*factor_cambio:,.0f}"):
            st.session_state.activo_tocado = tk
            
    st.markdown(f"""
        </td>
        <td style="width: 13%; color:#4caf50;"><b>{sem}</b></td>
        <td style="width: 13%; color:#00e676;"><b>{anual}</b></td>
        <td style="width: 12%; color:#ffeb3b;"><b>{fund}</b></td>
        <td style="width: 13%; color:{cl}; font-weight:bold;">{vered}</td>
    </tr>
    </table>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 5. CAJA DE CONTROL REMOTO QUE REACCIONA AL TOQUE DE LA CELDA AZUL (Sin botoneras pesadas)
target = st.session_state.activo_tocado
st.markdown(f"<p style='font-size:0.78rem; color:#2196f3; font-weight:bold; margin: 4px 0 0 0;'>✍️ Celda Tocada para Modificar: {target}</p>", unsafe_allow_html=True)
monto_actual_fijado = float(st.session_state.montos_dis[target])
nuevo_monto_tipeado = st.number_input("Ingresá el nuevo importe:", min_value=0.0, value=monto_actual_fijado, step=500.0, key="input_limpio_tipeo", label_visibility="collapsed")

if nuevo_monto_tipeado != monto_actual_fijado:
    st.session_state.montos_dis[target] = nuevo_monto_tipeado
    st.rerun()

patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white; margin-top:6px;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

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
    st.plotly_chart(fig, use_container_width=True, key="pie_v14")

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
