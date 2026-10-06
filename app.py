
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# 1. Configuracion de pantalla rigida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados: Congela la tabla oficial (SIN DESPLAZAMIENTOS MAÑOSOS DE GUÍAS)
st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-bottom: 6px; border: 1px solid #232a38; }

/* Fuerza a la tabla oficial a quedarse fija en el molde del celular */
div[data-testid="stDataFrame"] { width: 100% !important; }
div[data-testid="stDataFrame"] th { white-space: normal !important; word-wrap: break-word !important; line-height: 1.1 !important; font-size: 0.72rem !important; text-align: center !important; }
div[data-testid="stDataFrame"] td { font-size: 0.75rem !important; text-align: center !important; }
</style>
""", unsafe_allow_html=True)

VALOR_DOLAR_MEP = 1250.0

# 3. BASE DE DATOS INTERNA DE INVERSIONES
if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}
if 'activo_sel' not in st.session_state:
    st.session_state.activo_sel = "SPY"

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Estructura Oficial Blindada Anti-Errores</div>
</div>
""", unsafe_allow_html=True)

if st.button("💾 Guardar Cambios en Dispositivo", use_container_width=True):
    st.success("¡Montos fijados con éxito en la memoria!")

st.markdown("<h3 style='color:#ffffff;'>💬 Consulta al Chat Bot</h3>", unsafe_allow_html=True)
consulta_chat = st.text_input("Chat:", placeholder="Pregunta algo sobre tus inversiones...", label_visibility="collapsed")

st.markdown("<h3 style='color:#ffffff;'>🔍 Agregar Nueva Empresa</h3>", unsafe_allow_html=True)
nueva_accion = st.text_input("Ticker:", placeholder="Ej: NVDA, MSFT...", key="buscador_tk").upper().strip()
if nueva_accion and nueva_accion not in st.session_state.montos_dis:
    st.session_state.montos_dis[nueva_accion] = 5000.0
    st.success(f"¡{nueva_accion} agregada!")

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

# 4. CASILLERO COMPACTO DE MODIFICACIÓN DE CAPITALES (Fijo arriba para alimentar la tabla)
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

# 5. CONSTRUCCIÓN DE FILAS DINÁMICAS EN LA PLANILLA OFICIAL (Cero códigos HTML rotos)
datos_tabla = []
precios_ref = {"SPY": 510.0, "TSLA": 300.0, "AAPL": 210.0, "KO": 150.0}
patrimonio_total_usd = sum(st.session_state.montos_dis.values())

for tk in activos_actuales:
    p_base = precios_ref.get(tk, 150.0)
    monto_actual_tk = st.session_state.montos_dis[tk]
    if tk == "SPY": sem, anual, fund, vered = "▲ 40%", "▲ 60%", "8/10", "STRONG BUY"
    elif tk == "TSLA": sem, anual, fund, vered = "▲ 35%", "▲ 55%", "7/10", "HOLD"
    else: sem, anual, fund, vered = "▲ 30%", "▲ 50%", "9/10", "BUY"
        
    datos_tabla.append({
        "Acción": tk,
        "Precio Actual": f"{simbolo_moneda}{p_base*factor_cambio:,.0f}",
        "Inversión Asignada": f"{simbolo_moneda}{monto_actual_tk*factor_cambio:,.0f}",
        "Análisis\nTec.\nSemanal": sem,
        "Análisis\nTec.\nAnual": anual,
        "Análisis\nFunda-\nmental": fund,
        "Análisis\nFinal\n(Agente)": vered
    })
# Forzar el orden estricto de tu boceto original en la tabla nativa
columnas_ordenadas = ["Acción", "Precio Actual", "Inversión Asignada", "Análisis\nTec.\nSemanal", "Análisis\nTec.\nAnual", "Análisis\nFunda-\nmental", "Análisis\nFinal\n(Agente)"]
df_display = pd.DataFrame(datos_tabla).reindex(columns=columnas_ordenadas)


# Renderizado oficial nativo aceptado por el sistema sin posibilidad de romperse
st.dataframe(df_display, use_container_width=True, hide_index=True)

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
    st.plotly_chart(fig, use_container_width=True, key="pie_v12")

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
