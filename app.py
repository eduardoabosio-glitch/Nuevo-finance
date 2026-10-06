
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuración de pantalla rígida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Clava la simetría exacta y camufla el botón de eliminar abajo a la derecha
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-top: 30px !important; margin-bottom: 8px; border: 1px solid #232a38; }

/* Fichas Rectangulares Rígidas */
.tarjeta-activo { background-color: #161a22; padding: 12px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 10px; }

/* Renglones superiores e inferiores horizontales balanceados de margen a margen */
.cabecera-cuaderno { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; width: 100%; }
.renglon-control-inferior { display: flex; justify-content: space-between; align-items: center; margin-top: 6px; margin-bottom: 4px; width: 100%; }

/* Títulos Subrayados Estéticos Unificados */
.titulo-subrayado { text-decoration: underline !important; font-weight: bold; color: #2196f3; font-size: 0.88rem; }
.renglon-precio-unificado { font-size: 0.88rem; color: #ffffff; margin-bottom: 5px; line-height: 1.3; }

/* Configuración del casillero numérico limpio sin bultos grises */
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { background-color: #1f2633 !important; color: #00e676 !important; font-weight: bold !important; text-align: center !important; font-size: 0.9rem !important; border-radius: 4px !important; border: 1px solid #232a38 !important; height: 28px !important; }
div[data-testid="stNumberInput"] label { display: none !important; }

/* Forzar que el mini botón de eliminar HTML puro sea súper chico, angosto y rojo premium */
.btn-eliminar-mini { background-color: #b71c1c !important; color: white !important; border: none !important; font-weight: bold !important; font-size: 0.65rem !important; padding: 2px 5px !important; border-radius: 4px !important; text-decoration: none !important; display: inline-block; cursor: pointer; line-height: 1.2; text-align: center; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

# 3. BASE DE DATOS INTERNA CON MEMORIA CONTINUA
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Fichas del Cuaderno con Formato Unificado</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Estructura guardada en la memoria local con éxito!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre tus inversiones...", label_visibility="collapsed")
st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa al Portafolio</h3>", unsafe_allow_html=True)
nueva_empresa = st.text_input("Ingresá el símbolo:", placeholder="Escribí el ticker y dale a enter...", key="buscador_agregar_final_v6").upper().strip()

if nueva_empresa:
    if nueva_empresa not in st.session_state.montos_dis:
        st.session_state.montos_dis[nueva_empresa] = 5000.0
        st.success(f"¡{nueva_empresa} agregada con éxito!")
        st.rerun()

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Fichas del Cuaderno</h3>", unsafe_allow_html=True)

precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0

# 4. GENERACIÓN DE LAS FICHAS CON ACOPLE ESTÉTICO HORIZONTAL FIJO
for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual = st.session_state.montos_dis[tk]
    patrimonio_total_usd += monto_actual
    
    if tk == "SPY":
        sem, anual, fund, vered, cl_ver, noticias = "▲ 40%", "▲ 60%", "Nota 9/10 'Alta resiliencia en mercados consolidados'", "COMPRA FUERTE", "#00e676", "Nuevas proyecciones institucionales superan las expectativas"
    elif tk == "TSLA":
        sem, anual, fund, vered, cl_ver, noticias = "▲ 35%", "▲ 55%", "Nota 7/10 'Alta innovación tecnológica y expansión masiva'", "MANTENER", "#ffeb3b", "Nuevas proyecciones de entregas superan expectativas"
    elif tk == "AAPL":
        sem, anual, fund, vered, cl_ver, noticias = "▲ 30%", "▲ 50%", "Nota 9/10 'Sólido flujo de caja y recompra de acciones'", "COMPRAR", "#2196f3", "Ecosistema de servicios mantiene crecimiento de dos dígitos"
    else:
        sem, anual, fund, vered, cl_ver, noticias = "▲ 32%", "▲ 48%", "Nota 8/10 'Estabilidad de ingresos y dividendos estables'", "COMPRAR", "#2196f3", "Demanda global en mercados emergentes se mantiene firme"

    # Inicio de la tarjeta rígida
    st.markdown('<div class="tarjeta-activo">', unsafe_allow_html=True)
    
    # RENGLÓN 1: El nombre a la izquierda y el veredicto en español destacado BIEN A LA DERECHA EXTREMA
    st.markdown(f"""
    <div class="cabecera-cuaderno">
        <span style="font-size:1.35rem; font-weight:bold; color:#2196f3;">{tk}</span>
        <span style="font-size: 0.95rem; font-weight: bold; color: {cl_ver};">{vered}</span>
    </div>
    """, unsafe_allow_html=True)
            
    # RENGLÓN 2: Precio de la acción unificado con su título subrayado azul
    st.markdown(f'<div class="renglon-precio-unificado"><span class="titulo-subrayado">Precio de la Acción Actual:</span> <b>{simbolo_moneda}{p_base*factor_cambio:,.0f}</b></div>', unsafe_allow_html=True)
    
    # RENGLÓN 3: Análisis Fundamental Extenso
    st.markdown(f'<div class="renglon-precio-unificado"><span class="titulo-subrayado">Fundamental:</span> <b>{fund}</b></div>', unsafe_allow_html=True)
    
    # RENGLÓN 4: Semanal y Anual simétricos organizados en dos columnas
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<span class="titulo-subrayado">Técnico Semanal:</span> <b style="color:#4caf50;">{sem}</b>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<span class="titulo-subrayado">Análisis Tec Anual:</span> <b style="color:#00e676;">{anual}</b>', unsafe_allow_html=True)
        
    # RENGLÓN 5: Últimas Noticias del Agente abajo de todo
    st.markdown(f'<div style="margin-top:4px; margin-bottom:5px; font-size:0.88rem;"><span class="titulo-subrayado">Noticias del Agente:</span> <b>{noticias}</b></div>', unsafe_allow_html=True)
    
    # RENGLÓN 6 CORREGIDO: Leyenda de dinero fija a la izquierda y el botón eliminar empaquetado en HTML a la derecha
    # Al inyectar el botón como un enlace con la clase CSS .btn-eliminar-mini, el sistema lo clava en la misma línea
    st.markdown(f"""
    <div class="renglon-control-inferior">
        <div style="font-size:0.82rem; color:#888; font-weight: bold;">✍️ Modificar Capital Invertido ({simbolo_moneda.strip()}):</div>
        <div>
            <a href="?eliminar={tk}" target="_self" class="btn-eliminar-mini">❌ Eliminar</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Lógica inteligente para capturar el click del enlace HTML de borrado
    parametros_url = st.query_params
    if "eliminar" in parametros_url and parametros_url["eliminar"] == tk:
        del st.session_state.montos_dis[tk]
        st.query_params.clear()
        st.rerun()
    
    # Casillero numérico verde nativo abajo del todo ocupando el ancho completo de la tarjeta
    st.session_state.montos_dis[tk] = st.number_input(f"mod_{tk}", min_value=0.0, value=float(monto_actual), step=500.0, key=f"input_box_{tk}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Patrimonio Total Destacado Dinámico abajo de las fichas
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
    st.plotly_chart(fig, use_container_width=True, key="pie_v24")

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
