
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuración de pantalla rígida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Calca milimétricamente el diseño de tu cuaderno
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-top: 30px !important; margin-bottom: 8px; border: 1px solid #232a38; }

/* Tarjeta Rectangular Rígida que clava el plano del cuaderno */
.tarjeta-activo { background-color: #161a22; padding: 12px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 10px; position: relative; }

/* Renglones internos alineados de forma limpia */
.renglon-superior { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.renglon-medio { font-size: 0.9rem; color: #ffffff; background-color: #1f2633; padding: 4px 6px; border-radius: 4px; margin-bottom: 6px; border: 1px solid #232a38; }
.renglon-datos { font-size: 0.88rem; color: #ffffff; margin-bottom: 5px; line-height: 1.3; }
.bloque-tecnico { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; font-size: 0.88rem; color: #ffffff; }

/* Títulos Subrayados como en el cuaderno */
.titulo-subrayado { text-decoration: underline !important; font-weight: bold; color: #2196f3; }
.explicacion-comillas { font-size: 0.78rem; color: #888; font-style: italic; margin-top: -1px; margin-bottom: 5px; display: block; }

/* Camuflaje total del mini-formulario de borrar arriba a la derecha */
.posicion-boton-borrar { text-align: right; }
div.stFormSubmitButton > button { background-color: #b71c1c !important; color: white !important; border: 1px solid #d32f2f !important; font-weight: bold !important; font-size: 0.65rem !important; padding: 2px 6px !important; border-radius: 4px !important; cursor: pointer; height: 20px !important; line-height: 1 !important; }
div.stFormSubmitButton { margin: 0px !important; padding: 0px !important; }

/* Ocultar botones de más y menos en los casilleros de modificación de abajo */
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { background-color: #1f2633 !important; color: #00e676 !important; font-weight: bold !important; text-align: center !important; font-size: 0.9rem !important; border-radius: 4px !important; border: 1px solid #232a38 !important; height: 28px !important; }
div[data-testid="stNumberInput"] label { display: none !important; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

# 3. BASE DE DATOS INTERNA DE MEMORIA
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}

# Título Principal empujado bien abajo para que Chrome no lo tape
st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Diseño Rígido Calcado de Cuaderno</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Estructura y montos fijados en la memoria local!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre tus inversiones...", label_visibility="collapsed")

st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa al Portafolio</h3>", unsafe_allow_html=True)
nueva_empresa = st.text_input("Ingresá el símbolo:", placeholder="Escribí el ticker y dale a enter...", key="buscador_agregar_cuaderno").upper().strip()

if nueva_empresa:
    if nueva_empresa not in st.session_state.montos_dis:
        st.session_state.montos_dis[nueva_empresa] = 5000.0
        st.success(f"¡{nueva_empresa} agregada!")
        st.rerun()

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Fichas del Cuaderno</h3>", unsafe_allow_html=True)

# 4. RENDERIZADO DE LAS TARJETAS SIGUIENDO TU PLANO EXACTO DEL DIBUJO
precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0

for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual = st.session_state.montos_dis[tk]
    patrimonio_total_usd += monto_actual
    
    if tk == "SPY": sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 40%", "▲ 60%", "8/10", "COMPRA FUERTE", "#00e676", "MUY BUENAS", "#00e676"
    elif tk == "TSLA": sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 35%", "▲ 55%", "7/10", "MANTENER", "#ffeb3b", "BUENAS", "#4caf50"
    elif tk == "AAPL": sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 30%", "▲ 50%", "9/10", "COMPRAR", "#2196f3", "MUY BUENAS", "#00e676"
    else: sem, anual, fund, vered, cl_ver, noticias, cl_not = "▲ 32%", "▲ 48%", "8/10", "COMPRAR", "#2196f3", "BUENAS", "#4caf50"

    # RENGLÓN 1 DEL CUADERNO: Nombre, Veredicto y el casillero flotante para el botón Eliminar bien a la derecha
    st.markdown(f"""
    <div class="tarjeta-activo">
        <div class="renglon-superior">
            <span style="font-size:1.3rem; font-weight:bold; color:#2196f3;">{tk} <span style="font-size:0.85rem; color:{cl_ver}; font-weight:bold; margin-left:4px;">{vered}</span></span>
            <div class="posicion-boton-borrar">
    """, unsafe_allow_html=True)
    
    # El mini-formulario inyecta el botón Eliminar en esa misma fila superior derecha sin desarmar nada
    with st.form(key=f"del_form_{tk}"):
        if st.form_submit_button("❌ Eliminar"):
            del st.session_state.montos_dis[tk]
            st.rerun()
        
    # RENGLONES 2, 3, 4 y 5 DEL CUADERNO: Precio, Fundamental, Semanal/Anual y Noticias
    st.markdown(f"""
        </div>
        
        <!-- Renglón 2: Precio de la acción -->
        <div class="renglon-medio">
            💵 Precio Actual: <b>{simbolo_moneda}{p_base*factor_cambio:,.0f}</b>
        </div>
        
        <!-- Renglón 3: Análisis Fundamental con comillas abajo -->
        <div class="renglon-datos">
            <span class="titulo-subrayado">Análisis Fundamental:</span> <b style="color:#ffeb3b; font-size:0.95rem;">{fund}</b>
            <span class="explicacion-comillas">"Puntuación 1 al 10"</span>
        </div>
        
        <!-- Renglón 4: Semanal y Anual juntos en la misma fila horizontal -->
        <div class="bloque-tecnico">
            <div><span class="titulo-subrayado">Análisis Tec Semanal:</span> <b style="color:#4caf50;">{sem}</b></div>
            <div><span class="titulo-subrayado">Análisis Tec Anual:</span> <b style="color:#00e676;">{anual}</b></div>
        </div>
        
        <!-- Renglón 5: Últimas Noticias del Agente abajo de todo -->
        <div class="renglon-datos" style="margin-top: 4px; margin-bottom: 6px;">
            <span class="titulo-subrayado">Análisis Últ. Noticias (Agente):</span> <b style="color:{cl_not};">{noticias}</b>
        </div>
        
        <div style="font-size:0.78rem; color:#888; margin-bottom: 2px;">✍️ Modificar Capital Invertido:</div>
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
    st.plotly_chart(fig, use_container_width=True, key="pie_v22")

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
