import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuracion de pantalla rigida para celulares
st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

# 2. Estilos CSS Avanzados para tu diseno exacto de foto
st.markdown('''
<style>
.block-container { padding: 0.3rem 0.2rem; }
h3 { font-size: 1.1rem !important; margin: 0.4rem 0 0.2rem 0; }
.header-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.btn-guardar { background-color: #198754; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; border: none; }
.styled-table { width: 100%; border-collapse: collapse; font-size: 0.76rem; background-color: #161a22; table-layout: fixed; }
.styled-table th { background-color: #1f2633; color: #2196f3; text-align: center; padding: 4px 2px; font-weight: bold; line-height: 1.1; font-size: 0.72rem; border: 1px solid #232a38; }
.styled-table td { padding: 4px 2px; border: 1px solid #232a38; color: #ffffff; text-align: center; vertical-align: middle; }
.prob-alta { color: #00e676; font-weight: bold; }
.prob-media { color: #4caf50; font-weight: bold; }
.prob-baja { color: #f44336; font-weight: bold; }
.badge-nota { background-color: #1e293b; color: #ffeb3b; padding: 1px 3px; border-radius: 3px; font-weight: bold; font-size: 0.72rem; }
.veredicto-strong { color: #00e676; font-weight: bold; font-size: 0.72rem; }
.veredicto-hold { color: #ffeb3b; font-weight: bold; font-size: 0.72rem; }
.veredicto-buy { color: #2196f3; font-weight: bold; font-size: 0.72rem; }
</style>
''', unsafe_allow_html=True)

# 3. Encabezado con titulo y Boton de Guardar superior en verde
st.markdown('''
<div class="header-container">
    <h2 style="margin:0; font-size:1.35rem; color:white;">📊 Nuevo Finance Pro</h2>
    <button class="btn-guardar">💾 Guardar Cambios</button>
</div>
''', unsafe_allow_html=True)

st.text_input("ChatBot", placeholder="💬 Chat Bot - Preguntá algo sobre finanzas...", label_visibility="collapsed")

VALOR_DOLAR_MEP = 1250.0

if 'montos_dis' not in st.session_state:
    st.session_state.montos_dis = {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0}

moneda = st.radio("Moneda", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed")
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

st.markdown("<h3 style='color:#ffffff;'>📁 Mi Portafolio - Integración de Inversión</h3>", unsafe_allow_html=True)

# 4. Modificacion Directa de Montos (Renglon compacto arriba de la cuadricula)
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.session_state.montos_dis["SPY"] = st.number_input("SPY", value=float(st.session_state.montos_dis["SPY"]), step=500.0)
with col_m2:
    st.session_state.montos_dis["TSLA"] = st.number_input("TSLA", value=float(st.session_state.montos_dis["TSLA"]), step=500.0)
with col_m3:
    st.session_state.montos_dis["AAPL"] = st.number_input("AAPL", value=float(st.session_state.montos_dis["AAPL"]), step=500.0)

datos_foto = [
    {"Accion": "SPY", "Precio": 510.0, "Monto": st.session_state.montos_dis["SPY"], "Semanal": "▲ 40%", "Anual": "▲ 60%", "Fundamental": "8/10", "Veredicto": "STRONG BUY", "clase_ver": "veredicto-strong", "raw_sem": 40, "raw_anual": 60},
    {"Accion": "TSLA", "Precio": 300.0, "Monto": st.session_state.montos_dis["TSLA"], "Semanal": "▲ 35%", "Anual": "▲ 55%", "Fundamental": "7/10", "Veredicto": "HOLD", "clase_ver": "veredicto-hold", "raw_sem": 35, "raw_anual": 55},
    {"Accion": "AAPL", "Precio": 210.0, "Monto": st.session_state.montos_dis["AAPL"], "Semanal": "▲ 30%", "Anual": "▲ 50%", "Fundamental": "9/10", "Veredicto": "BUY", "clase_ver": "veredicto-buy", "raw_sem": 30, "raw_anual": 50}
]

# 5. Renderizado de la Cuadricula Fija de 7 Columnas con titulos verticales
html_tabla = '''
<table class="styled-table">
    <tr>
        <th style="width: 13%;">Acción</th>
        <th style="width: 14%;">Precio</th>
        <th style="width: 17%;">Inversión</th>
        <th style="width: 14%;">Análisis<br>Tec.<br>Semanal</th>
        <th style="width: 14%;">Análisis<br>Tec.<br>Anual</th>
        <th style="width: 14%;">Análisis<br>Funda-<br>mental</th>
        <th style="width: 14%;">Análisis<br>Final<br>(Agente)</th>
    </tr>
'''

patrimonio_total_usd = 0.0
for fila in datos_foto:
    p_final = fila["Precio"] * factor_cambio
    inv_final = fila["Monto"] * factor_cambio
    patrimonio_total_usd += fila["Monto"]
    clase_sem = "prob-media" if fila['raw_sem'] >= 50 else "prob-baja"
    clase_anual = "prob-alta" if fila['raw_anual'] >= 60 else "prob-media"
    
    html_tabla += f'''
    <tr>
        <td><b>{fila['Accion']}</b></td>
        <td>{simbolo_moneda}{p_final:,.0f}</td>
        <td><b>{simbolo_moneda}{inv_final:,.0f}</b></td>
        <td><span class="{clase_sem}">{fila['Semanal']}</span></td>
        <td><span class="{clase_anual}">{fila['Anual']}</span></td>
        <td><span class="badge-nota">{fila['Fundamental']}</span></td>
        <td><span class="{fila['clase_ver']}">{fila['Veredicto']}</span></td>
    </tr>
    '''
html_tabla += "</table>"
st.markdown(html_tabla, unsafe_allow_html=True)

patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; margin-top:6px; color:white;'>💰 Patrimonio Total Inversión = <span style='color:#00e676;'>{simbolo_moneda}{patrimonio_mostrar:,.0f}</span></p>", unsafe_allow_html=True)

st.markdown("<hr style='margin:8px 0; border-color:#232a38;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#ffffff;'>📊 Resumen y Distribución de Patrimonio</h3>", unsafe_allow_html=True)

# 6. Bloque Inferior: Grafico de Torta + Reporte de Noticias
col_g1, col_g2 = st.columns(2)
with col_g1:
    df_pie = pd.DataFrame({"Activo": ["SPY", "TSLA", "AAPL"], "Capital": [st.session_state.montos_dis["SPY"], st.session_state.montos_dis["TSLA"], st.session_state.montos_dis["AAPL"]]})
    fig = px.pie(df_pie, values='Capital', names='Activo', hole=0.4, height=130)
    fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, key="pie_cartera")

with col_g2:
    st.markdown('''
    <div style="background-color:#161a22; padding:6px; border-radius:4px; font-size:0.74rem; border:1px solid #232a38; height:130px;">
        <b style="color:#2196f3;">Resumen de Agente sobre las Noticias</b>
        <ul style="margin: 4px 0; padding-left: 12px; color:#ffffff; line-height:1.2;">
            <li>• 📊 <b>Impacto en 'SPY':</b> Positivo</li>
            <li>• 🌐 <b>Análisis General:</b> Sólido</li>
            <li>• 🎯 <b>Sugerencia de Acción:</b> Mantener</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<hr style='margin:8px 0; border-color:#232a38;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#ffffff;'>📰 Títulos de Noticias sobre mis Acciones</h3>", unsafe_allow_html=True)
st.markdown('''
<div style="font-size:0.74rem; line-height:1.4; color:#ffffff;">
    • <b>1. 'SPY' alcanza nuevo máximo histórico</b>... <a href="#" style="color:#2196f3; text-decoration:none;">🔗 Ver</a><br>
    • <b>2. Análisis Técnico: Niveles clave para 'TSLA'</b>... <a href="#" style="color:#2196f3; text-decoration:none;">🔗 Ver</a><br>
    • <b>3. Nuevas regulaciones financieras</b>... <a href="#" style="color:#2196f3; text-decoration:none;">🔗 Ver</a>
</div>
''', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 7. Barra de Navegacion Fija Inferior
st.markdown('''
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161a22; border-top: 1px solid #232a38; display: flex; justify-content: space-around; padding: 4px 0; z-index: 1000; font-size:0.68rem; text-align:center;">
    <div style="color:#888;">🏠<br>Inicio</div>
    <div style="color:#2196f3; font-weight:bold;">💼<br>Portafolio</div>
    <div style="color:#888;">📊<br>Análisis</div>
    <div style="color:#888;">💬<br>Chat</div>
    <div style="color:#888;">👤<br>Perfil</div>
</div>
''', unsafe_allow_html=True)
