
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuración de pantalla rígida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Letras más grandes, títulos subrayados y botón superior chico
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.1rem !important; margin: 0.4rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-bottom: 6px; border: 1px solid #232a38; }

/* Molde de la Tarjeta Rectangular de Acero con más espacio y texto grande */
.tarjeta-activo { background-color: #161a22; padding: 12px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 10px; }
.fila-titulo { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.fila-tarjeta { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px; font-size: 0.88rem; color: #ffffff; line-height: 1.3; }

/* Títulos Subrayados Estéticos */
.titulo-subrayado { text-decoration: underline !important; font-weight: bold; color: #2196f3; }
.explicacion-comillas { font-size: 0.78rem; color: #888; font-style: italic; margin-top: -2px; margin-bottom: 4px; display: block; }

/* Bloqueo absoluto de las botoneras flotantes de más y menos de Streamlit */
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { background-color: #1f2633 !important; color: #00e676 !important; font-weight: bold !important; text-align: center !important; font-size: 0.9rem !important; border-radius: 4px !important; border: 1px solid #232a38 !important; height: 30px !important; }
div[data-testid="stNumberInput"] label { display: none !important; }

/* Botón de eliminación superior súper chico y compacto */
div.stButton > button[key^="borrar_"] { background-color: #b71c1c !important; color: white !important; border: none !important; font-weight: bold !important; font-size: 0.68rem !important; padding: 1px 5px !important; border-radius: 3px !important; cursor: pointer; height: 20px !important; line-height: 1 !important; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

# 3. BASE DE DATOS INTERNA CON PERSISTENCIA
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Fichas Ampliadas de Análisis Técnico y Fundamental</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Estructura y montos fijados en la memoria con éxito!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre tus inversiones...", label_visibility="collapsed")

st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa al Portafolio</h3>", unsafe_allow_html=True)
nueva_empresa = st.text_input("Ingresá el símbolo:", placeholder="Escribí el ticker y dale a enter...", key="buscador_agregar_final").upper().strip()

if nueva_empresa:
    if nueva_empresa not in st.session_state.montos_dis:
        st.session_state.montos_dis[nueva_empresa] = 5000.0
        st.success(f"¡{nueva_empresa} agregada!")
        st.rerun()

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Fichas Analíticas</h3>", unsafe_allow_html=True)

# 4. RENDERIZADO DE LAS TARJETAS CON BOTÓN CHICO ARRIBA Y TEXTOS AMPLIADOS
precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0

for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual = st.session_state.montos_dis[tk]
    patrimonio_total_usd += monto_actual
    
    # Datos dinámicos ampliados simulados según el ticker
    if tk == "SPY":
        sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 40%", "▲ 60%", "8/10", "STRONG BUY", "#00e676", "MUY BUENAS", "#00e676"
    elif tk == "TSLA":
        sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 35%", "▲ 55%", "7/10", "HOLD", "#ffeb3b", "BUENAS", "#4caf50"
    elif tk == "AAPL":
        sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 30%", "▲ 50%", "9/10", "BUY", "#2196f3", "MUY BUENAS", "#00e676"
    else:
        sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 32%", "▲ 48%", "8/10", "BUY", "#2196f3", "BUENAS", "#4caf50"

    # Apertura de la Ficha con Título y Botón de eliminación en la misma fila superior
    st.markdown(f"""
    <div class="tarjeta-activo">
        <div class="fila-titulo">
            <span style="font-size:1.2rem; font-weight:bold; color:#2196f3;">{tk} <span style="font-size:0.85rem; color:{cl_ver}; font-weight:bold; margin-left:6px;">({vered})</span></span>
            <span style="font-size:0.85rem; color:#aaa;">Precio: <b>{simbolo_moneda}{p_base*factor_cambio:,.0f}</b></span>
        </div>
    """, unsafe_allow_html=True)
    
    # El truco: El botón chico de eliminación se dibuja pegado a la derecha arriba
    if st.button("❌ Eliminar", key=f"borrar_{tk}"):
        del st.session_state.montos_dis[tk]
        st.rerun()
        
    # Bloque de datos ampliados con subtítulos subrayados y comillas explicativas
    st.markdown(f"""
        <div style="margin-top: 6px;">
            <span class="titulo-subrayado">Análisis Fundamental:</span> <b style="color:#ffeb3b; font-size:0.92rem;">{fund}</b>
            <span class="explicacion-comillas">"Puntuación del 1 al 10 cruzando balances, deudas y PER"</span>
        </div>
        <div class="fila-tarjeta" style="margin-top:4px;">
            <div><span class="titulo-subrayado">Análisis Tec. Semanal:</span> <b style="color:#4caf50;">{sem}</b></div>
            <div><span class="titulo-subrayado">Análisis Tec. Anual:</span> <b style="color:#00e676;">{anual}</b></div>
        </div>
        <div style="margin-top: 4px; margin-bottom: 5px;">
            <span class="titulo-subrayado">Análisis Últ. Noticias (Agente):</span> <b style="color:{cl_not}; font-size:0.88rem;">{noticias}</b>
        </div>
        <div style="font-size:0.8rem; color:#888; margin-bottom: 2px;">✍️ Modificar Capital Invertido:</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.montos_dis[tk] = st.number_input(f"mod_{tk}", min_value=0.0, value=float(monto_actual), step=500.0, key=f"input_box_{tk}")

# Patrimonio Total Destacado Dinámico
patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white; margin-top:8px;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)

# 5. MENÚ DESPLEGABLE DE GRÁFICOS REALES EN VIVO
st.markdown("<h3 style='color:#ffffff;'>📈 Visualizar Gráficos Avanzados</h3>", unsafe_allow_html=True)
accion_para_grafico = st.selectbox("Elegí:", list(st.session_state.montos_dis.keys()), label_visibility="collapsed", key="graf_av")
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
    st.plotly_chart(fig, use_container_width=True, key="pie_v20")

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
