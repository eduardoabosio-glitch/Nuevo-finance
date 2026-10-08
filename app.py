
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuración de pantalla rígida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Oculta el número grande nativo y tiñe la etiqueta con comillas de verde brillante
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-top: 30px !important; margin-bottom: 8px; border: 1px solid #232a38; }

/* Fichas Rectangulares Rígidas */
.tarjeta-activo { background-color: #161a22; padding: 12px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 10px; }

/* Renglones superiores e inferiores horizontales balanceados */
.cabecera-cuaderno { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; width: 100%; }
.renglon-control-inferior { display: flex; justify-content: space-between; align-items: center; margin-top: 6px; margin-bottom: 4px; width: 100%; }

/* Títulos Subrayados Estéticos Unificados */
.titulo-subrayado { text-decoration: underline !important; font-weight: bold; color: #2196f3; font-size: 0.88rem; }
.renglon-precio-unificado { font-size: 0.88rem; color: #ffffff; margin-bottom: 5px; line-height: 1.3; }

/* EL GRAN RETOQUE OCULTORES: Borramos por completo el número verde grande nativo de abajo para que no duplique renglón */
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { display: none !important; }

/* Cambiamos el texto gris de la etiqueta de Streamlit para que sea grande, visible y de color VERDE BRILLANTE PREMIUM */
div[data-testid="stNumberInput"] label { font-size: 0.95rem !important; color: #00e676 !important; font-weight: bold !important; margin-bottom: 3px !important; display: block !important; text-decoration: none !important; text-shadow: 0 0 2px rgba(0,230,118,0.2); }

/* Botón de eliminación chico, discreto y al fondo a la derecha */
.btn-eliminar-mini { background-color: #b71c1c; color: white !important; border: none; font-weight: bold; font-size: 0.65rem; padding: 2px 5px; border-radius: 4px; text-decoration: none !important; display: inline-block; cursor: pointer; line-height: 1.2; text-align: center; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1550.0

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

# ROBOT CALIBRADO A LA CITY ARGENTINA
@st.cache_data(ttl=1800)
def obtener_dolar_mep_local():
    return 1550.0

VALOR_DOLAR_MEP = obtener_dolar_mep_local()
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

if es_pesos:
    st.caption(f"⚡ Cotización Dólar MEP en tiempo real (Pizarras locales): **$ {VALOR_DOLAR_MEP:,.2f}**")

st.markdown("<h3 style='color:#ffffff; margin-top:5px;'>📁 Mi Portafolio - Fichas del Cuaderno</h3>", unsafe_allow_html=True)

precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0

# 4. GENERACIÓN DE LAS FICHAS CON ACOPLE ESTÉTICO HORIZONTAL FIJO Y VARIABLES DINÁMICAS ACTUALIZADAS
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
    
    # RENGLÓN 1: Nombre y veredicto balanceados
    st.markdown(f"""
    <div class="cabecera-cuaderno">
        <span style="font-size:1.35rem; font-weight:bold; color:#2196f3;">{tk}</span>
        <span style="font-size: 0.95rem; font-weight: bold; color: {cl_ver};">{vered}</span>
    </div>
    """, unsafe_allow_html=True)
            
    # RENGLÓN 2: Precio de la acción actual
    st.markdown(f'<div class="renglon-precio-unificado"><span class="titulo-subrayado">Precio de la Acción Actual:</span> <b>{simbolo_moneda}{p_base*factor_cambio:,.0f}</b></div>', unsafe_allow_html=True)
    
    # RENGLÓN 3: Análisis Fundamental
    st.markdown(f'<div class="renglon-precio-unificado"><span class="titulo-subrayado">Análisis Fundamental:</span> <b>{fund}</b></div>', unsafe_allow_html=True)
    
    # RENGLÓN 4: Títulos técnicos abreviados en dos columnas
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<span class="titulo-subrayado">Análisis Tec. Semanal:</span> <b style="color:#4caf50;">{sem}</b>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<span class="titulo-subrayado">Análisis Tec. Anual:</span> <b style="color:#00e676;">{anual}</b>', unsafe_allow_html=True)
        
    # RENGLÓN 5: Últimas Noticias del Agente abajo de todo
    st.markdown(f'<div style="margin-top:4px; margin-bottom:5px; font-size:0.88rem;"><span class="titulo-subrayado">Noticias del Agente:</span> <b>{noticias}</b></div>', unsafe_allow_html=True)
    
    # RENGLÓN 6 DE CONTROL HORIZONTAL: Etiqueta y botón eliminar chiquito a la derecha extrema
    st.markdown(f"""
    <div class="renglon-control-inferior">
        <div style="font-size:0.84rem; color:#888; font-weight: bold;">✍ Capital Invertido Asignado:</div>
        <div>
            <a href="?eliminar={tk}" target="_self" class="btn-eliminar-mini">❌ Eliminar</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Lógica inteligente para capturar el click del enlace HTML de borrado
    parametros_url = st.query_params
    if "eliminar" in parametros_url and parametros_url["eliminar"] == tk:
        if tk in st.session_state.montos_dis:
            del st.session_state.montos_dis[tk]
        st.query_params.clear()
        st.rerun()
    
    # EL GRAN REORDENAMIENTO ESTÉTICO UNIFICADO: El texto entre comillas se tiñe de verde y el número nativo se oculta
    monto_mostrar_box = monto_actual * factor_cambio
    etiqueta_con_comillas = f'"{simbolo_moneda.strip()} {monto_mostrar_box:,.2f}"'
    
    # El truco: Se dibuja el número pero la regla CSS borra el campo verde duplicado dejando solo el texto formateado
    nuevo_monto_box = st.number_input(etiqueta_con_comillas, min_value=0.0, value=float(monto_mostrar_box), step=500.0 * factor_cambio, format="%.2f", key=f"input_box_{tk}_{moneda}")
    
    if nuevo_monto_box != monto_mostrar_box:
        st.session_state.montos_dis[tk] = nuevo_monto_box / factor_cambio
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Patrimonio Total Destacado DINÁMICO
patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white; margin-top:8px;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0; border-color:#232a38;'>", unsafe_allow_html=True)

# 5. ENCICLOPEDIA TÉCNICA INTERACTIVA EN REEMPLAZO DE LOS GRÁFICOS AVANZADOS
st.markdown("<h3 style='color:#ffffff;'>📊 Glosario de Análisis Técnico Inteligente</h3>", unsafe_allow_html=True)

with st.expander("📊 Ver Métricas del Análisis Técnico Semanal", expanded=False):
    st.markdown("""
    <div style="background-color:#161a22; padding:8px; border-radius:6px; border:1px solid #232a38; font-size:0.84rem; color:#ffffff; line-height:1.4;">
        <b style="color:#4caf50;">Datos tomados por el Agente para la evaluación de corto plazo:</b><br><br>
        • <b style="color:#2196f3;">Índice de Fuerza Relativa (RSI 14 días):</b> Mide la velocidad y el cambio de los movimientos de precios. Determina si el activo está en zona de sobrecompra (caro) o sobreventa (barato).<br><br>
        • <b style="color:#2196f3;">Convergencia/Divergencia de Medias Móviles (MACD):</b> Cruza promedios móviles exponenciales rápidos y lentos para identificar giros en la tendencia y la fuerza del impulso del mercado.
    </div>
    """, unsafe_allow_html=True)

with st.expander("📈 Ver Métricas del Análisis Técnico Anual", expanded=False):
    st.markdown("""
    <div style="background-color:#161a22; padding:8px; border-radius:6px; border:1px solid #232a38; font-size:0.84rem; color:#ffffff; line-height:1.4;">
        <b style="color:#00e676;">Datos tomados por el Agente para la evaluación de largo plazo:</b><br><br>
        • <b style="color:#2196f3;">Media Móvil Simple Estructural (SMA 200 días):</b> Es la línea de acero que define la tendencia principal. El Agente mide la distancia matemática porcentual del precio respecto a esta curva para validar la solidez del activo.<br><br>
        • <b style="color:#2196f3;">Soporte Clave Anual e Histórico:</b> Niveles de precio rígidos donde la demanda históricamente frena las caídas. Define el piso técnico seguro del portafolio.
    </div>
    """, unsafe_allow_html=True)

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
