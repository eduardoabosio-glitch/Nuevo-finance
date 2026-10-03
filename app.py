import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 1. Configuración de pantalla para celulares
st.set_page_config(page_title="Nuevo Finance", layout="wide")

# 2. Estilos Visuales Avanzados para Celular
st.markdown('''
<style>
.block-container { padding-top: 0.4rem; padding-bottom: 0.4rem; padding-left: 0.3rem; padding-right: 0.3rem; }
h3 { font-size: 1.15rem !important; margin-top: 0.5rem; margin-bottom: 0.3rem; }
.styled-table { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 0.78rem; background-color: #161a22; }
.styled-table th { background-color: #1f2633; color: #2196f3; text-align: left; padding: 4px; font-weight: bold; }
.styled-table td { padding: 4px; border-bottom: 1px solid #232a38; color: #ffffff; }
.prob-alta { color: #00e676; font-weight: bold; }
.prob-media { color: #4caf50; font-weight: bold; }
.prob-neutral { color: #ffeb3b; font-weight: bold; }
.prob-baja { color: #f44336; font-weight: bold; }
.badge-nota { background-color: #1e293b; color: #2196f3; padding: 1px 4px; border-radius: 3px; font-weight: bold; font-size: 0.75rem; border: 1px solid #232a38; }
.veredicto-compra { color: #00e676; font-weight: bold; text-transform: uppercase; }
.veredicto-mantener { color: #2196f3; font-weight: bold; text-transform: uppercase; }
.veredicto-alerta { color: #ff9100; font-weight: bold; text-transform: uppercase; }
.veredicto-venta { color: #ff1744; font-weight: bold; text-transform: uppercase; }
</style>
''', unsafe_allow_html=True)

st.title("📊 Nuevo Finance Pro")

VALOR_DOLAR_MEP = 1250.0

# 3. Base de datos interna de la Cartera Inteligente
if 'cartera_montos' not in st.session_state:
    st.session_state.cartera_montos = {"AAPL": 22.00, "TSLA": 15.00}

# 4. BOTÓN SELECTOR DE MONEDA
moneda = st.radio("💵 Seleccioná la moneda del panel:", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True)
es_pesos = moneda == "Pesos (ARS)"
simbolo_moneda = "ARS $" if es_pesos else "USD $"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0

# 5. BUSCADOR UNIFICADO ARRIBA
st.subheader("🔍 Buscar y agregar empresa:")
nueva_empresa = st.text_input("Ingresá el símbolo (Ej: MSFT, NVDA):", value="", key="buscador").upper().strip()

if nueva_empresa and nueva_empresa not in st.session_state.cartera_montos:
    try:
        ticker_valido = yf.Ticker(nueva_empresa)
        _ = ticker_valido.info
        st.session_state.cartera_montos[nueva_empresa] = 10.00  
        st.success(f"¡{nueva_empresa} agregada correctamente!")
    except:
        st.error("No se encontró el símbolo en Yahoo Finance.")

# 6. PANEL DE MODIFICACIÓN DE MONTOS INTERACTIVO
st.subheader("⚙️ Asignar montos a tus inversiones:")
activo_a_modificar = st.selectbox("Elegí qué acción querés modificar:", list(st.session_state.cartera_montos.keys()))
monto_actual_usd = st.session_state.cartera_montos[activo_a_modificar]

nuevo_monto_usd = st.number_input(f"Modificar inversión para {activo_a_modificar} (en USD):", value=float(monto_actual_usd), step=5.0)
st.session_state.cartera_montos[activo_a_modificar] = nuevo_monto_usd

# 7. PROCESAMIENTO GENERAL CON TRIPLE FILTRO Y CONCORDANCIA
activos = list(st.session_state.cartera_montos.keys())
datos_tabla = []
patrimonio_total_usd = 0.0

for ticker in activos:
    try:
        t_data = yf.Ticker(ticker)
        hist = t_data.history(period="6mo")
        precio_base = hist["Close"].iloc[-1]
        
        # --- CÁLCULO PROBABILÍSTICO SEMANAL (Técnico) ---
        exp1 = hist["Close"].ewm(span=12, adjust=False).mean()
        exp2 = hist["Close"].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        voto_macd = 1 if macd.iloc[-1] > signal.iloc[-1] else -1
        
        delta = hist["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        voto_rsi = 1 if rsi < 40 else (-1 if rsi > 65 else 0)
        
        low_14 = hist["Low"].rolling(window=14).min()
        high_14 = hist["High"].rolling(window=14).max()
        k_percent = 100 * ((hist["Close"] - low_14) / (high_14 - low_14 + 1e-10))
        d_percent = k_percent.rolling(window=3).mean().iloc[-1]
        k_val = k_percent.iloc[-1]
        voto_stoch = 1 if k_val < 25 and k_val > d_percent else (-1 if k_val > 75 and k_val < d_percent else 0)
        
        puntaje_tecnico = voto_macd + voto_rsi + voto_stoch
        if puntaje_tecnico >= 2: prob_semanal = 68
        elif puntaje_tecnico == 1: prob_semanal = 58
        elif puntaje_tecnico == -1: prob_semanal = 42
        elif puntaje_tecnico <= -2: prob_semanal = 32
        else: prob_semanal = 50
            
        # --- CÁLCULO PROBABILÍSTICO ANUAL (Técnico) ---
        hist_200 = t_data.history(period="1y")
        sma_200 = hist_200["Close"].rolling(window=200).mean().iloc[-1]
        
        if precio_base > sma_200:
            distancia = ((precio_base - sma_200) / sma_200) * 100
            prob_anual = min(78, int(55 + (distancia / 2)))
        else:
            distancia = ((sma_200 - precio_base) / sma_200) * 100
            prob_anual = max(28, int(45 - (distancia / 2)))
            
        # --- CÁLCULO DEL ANÁLISIS FUNDAMENTAL ---
        info_f = t_data.info
        pe_ratio = info_f.get('trailingPE', None)
        margin = info_f.get('profitMargins', 0)
        
        puntaje_fund = 5 
        if pe_ratio and pe_ratio < 22: puntaje_fund += 2
        if pe_ratio and pe_ratio > 38: puntaje_fund -= 1
        if margin > 0.15: puntaje_fund += 2
        if margin > 0.28: puntaje_fund += 1
        puntaje_fund = max(1, min(10, puntaje_fund))
        
        # --- SIMULACIÓN DE IMPACTO DE NOTICIAS ---
        noticias_favorables = 1 if puntaje_fund >= 7 else 0
        
        # --- 🤖 CÁLCULO INTELIGENTE DEL VEREDICTO FINAL ---
        score_total = (prob_semanal + prob_anual) / 2 + (puntaje_fund * 5) + (noticias_favorables * 5)
        
        if score_total >= 88: veredicto_final = "Compra Fuerte"
        elif score_total >= 72: veredicto_final = "Compra"
        elif score_total >= 55: veredicto_final = "Mantener"
        elif score_total >= 42: veredicto_final = "Precaución"
        else: veredicto_final = "Venta"
        
    except:
        precios_ref = {"AAPL": 233.69, "TSLA": 260.40, "MSFT": 415.20, "NVDA": 127.40}
        precio_base = precios_ref.get(ticker, 150.00)
        prob_semanal = 55
        prob_anual = 58
        puntaje_fund = 8
        veredicto_final = "Compra"
    
    inversion_usd = st.session_state.cartera_montos[ticker]
    patrimonio_total_usd += inversion_usd

    precio_final = precio_base * factor_cambio
    inversion_final = inversion_usd * factor_cambio
    
    datos_tabla.append({
        "Acción": ticker,
        "Precio": f"{simbolo_moneda}{precio_final:,.2f}",
        "Inversión": f"{simbolo_moneda}{inversion_final:,.2f}",
        "Semanal": f"{prob_semanal}%",
        "Anual": f"{prob_anual}%",
        "Fundamental": f"⭐ {puntaje_fund}/10",
        "Veredicto": veredicto_final,
        "raw_sem": prob_semanal,
        "raw_anual": prob_anual
    })

# RENDERIZADO DE LA TABLA COMPLETA INTEGRADA
st.subheader("📁 Cuadrícula Integradora de Inversiones")
html_tabla = '''
<table class="styled-table">
    <tr>
        <th>Acción</th>
        <th>Precio</th>
        <th>Inversión</th>
        <th>Semanal (Téc)</th>
        <th>Anual (Téc)</th>
        <th>Fundamental</th>
        <th>🤖 Veredicto Final</th>
    </tr>
'''
for fila in datos_tabla:
    clase_sem = "prob-alta" if fila['raw_sem'] >= 60 else ("prob-media" if fila['raw_sem'] >= 51 else ("prob-neutral" if fila['raw_sem'] == 50 else "prob-baja"))
    clase_anual = "prob-alta" if fila['raw_anual'] >= 60 else ("prob-media" if fila['raw_anual'] >= 51 else "prob-baja")
    
    if "Fuerte" in fila['Veredicto'] or fila['Veredicto'] == "Compra": clase_ver = "veredicto-compra"
    elif fila['Veredicto'] == "Mantener": clase_ver = "veredicto-mantener"
    elif fila['Veredicto'] == "Precaución": clase_ver = "veredicto-alerta"
    else: clase_ver = "veredicto-venta"
    
    html_tabla += f'''
    <tr>
        <td><b>{fila['Acción']}</b></td>
        <td>{fila['Precio']}</td>
        <td><b>{fila['Inversión']}</b></td>
        <td><span class="{clase_sem}">{fila['Semanal']}</span></td>
        <td><span class="{clase_anual}">{fila['Anual']}</span></td>
        <td><span class="badge-nota">{fila['Fundamental']}</span></td>
        <td><span class="{clase_ver}">{fila['Veredicto']}</span></td>
    </tr>
    '''
html_tabla += "</table>"
 st.markdown(html_tabla, unsafe_allow_html=True)




# Patrimonio Total Destacado
patrimonio_mostrar = patrimonio_total_usd * factor_cambio
st.markdown(f"### 💰 Patrimonio Total Invertido: <span style='color:#4caf50;'>{simbolo_moneda}{patrimonio_mostrar:,.2f}</span>", unsafe_allow_html=True)

# Gráfico de Distribución abajo
st.subheader("📊 Distribución Patrimonial")
df_pie = pd.DataFrame({
    "Activo": activos,
    "Capital": [st.session_state.cartera_montos[t] for t in activos]
})
fig = px.pie(df_pie, values='Capital', names='Activo', hole=0.4, height=260)
fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)
