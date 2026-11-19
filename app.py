import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import yfinance as yf
import numpy as np
import datetime
import json
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Nuevo Finance Pro", layout="wide")

st.markdown("""
<style>
.block-container { padding: 0.2rem 0.2rem; }
h3 { font-size: 1.05rem !important; margin: 0.3rem 0 0.1rem 0; }
.header-container { background-color: #1f2633; padding: 6px; border-radius: 4px; text-align: center; margin-top: 30px !important; margin-bottom: 8px; border: 1px solid #232a38; }
.tarjeta-activo { background-color: #161a22; padding: 12px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 10px; }
.cabecera-cuaderno { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; width: 100%; }
.renglon-precio-unificado { font-size: 0.88rem; color: #ffffff; margin-bottom: 5px; line-height: 1.3; }
.caja-swing { background-color: #1b212c; padding: 8px; border-radius: 6px; border: 1px solid #2c3545; margin: 6px 0; font-size: 0.82rem; line-height: 1.45; }
.dataframe { width: 100% !important; font-size: 0.72rem !important; color: white !important; background-color: #161a22 !important; border: 1px solid #232a38 !important; text-align: center !important; }
.dataframe th { background-color: #1f2633 !important; color: #2196f3 !important; font-weight: bold !important; padding: 2px !important; }
.dataframe td { padding: 2px !important; border: 1px solid #232a38 !important; }
div[data-testid="stTextInput"] input { background-color: #1f2633 !important; color: #00e676 !important; font-weight: bold !important; text-align: left !important; font-size: 0.92rem !important; border-radius: 6px !important; border: 1px solid #232a38 !important; height: 34px !important; }
div[data-testid="stTextInput"] label, div[data-testid="stTextInput"] p { display: none !important; }
.caja-noticia-link { background-color: #161a22; padding: 10px; border-radius: 6px; border: 1px solid #232a38; margin-bottom: 8px; font-size: 0.84rem; color: #ffffff; line-height: 1.4; }
.enlace-noticia-azul { color: #2196f3 !important; text-decoration: underline !important; font-weight: bold; display: inline-block; margin-top: 4px; }
div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; width: 100% !important; gap: 8px !important; }
div[data-testid="stHorizontalBlock"] > div { width: 50% !important; flex: 1 1 auto !important; min-width: 0 !important; }
div.stButton > button { height: 38px !important; font-size: 0.82rem !important; font-weight: bold !important; border-radius: 6px !important; border: none !important; width: 100% !important; color: white !important; }
div[data-testid="stHorizontalBlock"] > div:nth-of-type(1) button { background-color: #2196f3 !important; }
div[data-testid="stHorizontalBlock"] > div:nth-of-type(2) button { background-color: #00e676 !important; color: #161a22 !important; }
div.stButton > button[key*="delete_btn"] { background-color: #f44336 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <h2 style="margin:0; font-size:1.2rem; color:#00e676; font-weight:bold;">📊 Nuevo Finance Pro</h2>
    <div style="font-size:0.7rem; color:#888;">Motor Cuantitativo & Swing Trading AI</div>
</div>
""", unsafe_allow_html=True)

def agente_calcular_mep_bonos_real():
    mep_respaldo = 1568.50
    try:
        al30_ars = yf.Ticker("AL30.BA").history(period="15d")
        al30_usd = yf.Ticker("AL30D.BA").history(period="15d")
        if not al30_ars.empty and not al30_usd.empty:
            serie_ars = al30_ars["Close"].dropna()
            serie_usd = al30_usd["Close"].dropna()
            p_ars = float(serie_ars.iloc[-1])
            p_usd = float(serie_usd.iloc[-1])
            fecha_cierre = serie_ars.index[-1].strftime("%d/%m/%Y")
            if p_usd > 0 and (p_ars / p_usd) > 500:
                return {"valor": round(p_ars / p_usd, 2), "texto": f"⚡ MEP Real vía AL30 (Cierre {fecha_cierre})", "al30_ars": p_ars, "al30_usd": p_usd, "fecha": fecha_cierre}
    except:
        pass
    try:
        r_api = requests.get("https://dolarapi.com" + "/v1/dolares/bolsa", timeout=4)
        if r_api.status_code == 200:
            v_mep = float(r_api.json().get("venta", 0.0))
            if v_mep > 500:
                return {"valor": v_mep, "texto": "⚡ Cotización MEP Oficial (Último Cierre Hábil)", "al30_ars": None, "al30_usd": None, "fecha": "Último cierre"}
    except:
        pass
    return {"valor": mep_respaldo, "texto": "📅 Cierre de Emergencia: Datos de Respaldo", "al30_ars": None, "al30_usd": None, "fecha": "Respaldo"}

datos_mep = agente_calcular_mep_bonos_real()
VALOR_DOLAR_MEP = datos_mep["valor"]
origen_mep_txt = datos_mep["texto"]

MAPEO_ACTIVOS_CSV = {}
try:
    df_csv = pd.read_csv("activos.csv")
    df_csv['Ticker'] = df_csv['Ticker'].astype(str).str.strip().str.upper()
    df_csv['Nombre'] = df_csv['Nombre'].astype(str).str.strip()
    for _, row in df_csv.iterrows():
        tk, nom = row['Ticker'], row['Nombre']
        if tk.endswith(".BA"):
            MAPEO_ACTIVOS_CSV[f"🟢 {nom} ({tk})"] = {"orig": "No Aplica", "arg": tk}
        else:
            MAPEO_ACTIVOS_CSV[f"🔵 {nom} ({tk})"] = {"orig": tk, "arg": f"{tk}.BA"}
except:
    MAPEO_ACTIVOS_CSV = {"🔵 SPDR S&P 500 (SPY)": {"orig": "SPY", "arg": "SPY.BA"}, "🔵 Coca-Cola Co. (KO)": {"orig": "KO", "arg": "KO.BA"}}
 def leer_local_storage(clave_ls, key_comp):
    try:
        raw = streamlit_js_eval(js_expressions=f"localStorage.getItem('{clave_ls}')", key=key_comp)
        if raw and isinstance(raw, str):
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
    except:
        pass
    return None

def guardar_todo_en_navegador():
    try:
        st.session_state.carteras[st.session_state.cartera_activa] = st.session_state.montos_dis.copy()
        st.session_state.ppcs[st.session_state.cartera_activa] = st.session_state.ppc_actual.copy()
        txt_c = json.dumps(st.session_state.carteras, separators=(",", ":")).replace("\\", "\\\\").replace("'", "\\'")
        txt_p = json.dumps(st.session_state.ppcs, separators=(",", ":")).replace("\\", "\\\\").replace("'", "\\'")
        tick = st.session_state.get("ls_tick", 0)
        js_cmd = f"localStorage.setItem('nuevo_finance_carteras', '{txt_c}'); localStorage.setItem('nuevo_finance_ppcs', '{txt_p}');"
        streamlit_js_eval(js_expressions=js_cmd, key=f"ls_save_{tick}")
        st.session_state.ls_tick = tick + 1
    except:
        pass

datos_ls = leer_local_storage("nuevo_finance_carteras", "ls_read_carteras")
ppcs_ls = leer_local_storage("nuevo_finance_ppcs", "ls_read_ppcs")

if "carteras" not in st.session_state:
    st.session_state.carteras = datos_ls if datos_ls else {"Principal": {"SPY": 10000.0, "TSLA": 10000.0, "AAPL": 10000.0, "KO": 5000.0}}
elif datos_ls and not st.session_state.get("ls_sincronizado", False):
    st.session_state.carteras = datos_ls
    st.session_state.ls_sincronizado = True

if "ppcs" not in st.session_state:
    st.session_state.ppcs = ppcs_ls if ppcs_ls else {}
elif ppcs_ls and not st.session_state.get("ls_ppc_sinc", False):
    st.session_state.ppcs = ppcs_ls
    st.session_state.ls_ppc_sinc = True

if "cartera_activa" not in st.session_state or not isinstance(st.session_state.cartera_activa, str) or st.session_state.cartera_activa not in st.session_state.carteras:
    st.session_state.cartera_activa = next(iter(st.session_state.carteras))
if st.session_state.cartera_activa not in st.session_state.ppcs:
    st.session_state.ppcs[st.session_state.cartera_activa] = {}
if "version_input" not in st.session_state:
    st.session_state.version_input = 0

st.session_state.montos_dis = st.session_state.carteras[st.session_state.cartera_activa]
st.session_state.ppc_actual = st.session_state.ppcs[st.session_state.cartera_activa]

with st.expander(f"💼 Mis Portafolios: {st.session_state.cartera_activa}", expanded=False):
    nombres_disponibles = list(st.session_state.carteras.keys())
    idx_actual = nombres_disponibles.index(st.session_state.cartera_activa)
    seleccion_cartera = st.selectbox("Elegir portafolio:", nombres_disponibles, index=idx_actual, key="sel_cartera_url")
    if seleccion_cartera != st.session_state.cartera_activa:
        st.session_state.carteras[st.session_state.cartera_activa] = st.session_state.montos_dis.copy()
        st.session_state.ppcs[st.session_state.cartera_activa] = st.session_state.ppc_actual.copy()
        st.session_state.cartera_activa = seleccion_cartera
        st.session_state.montos_dis = st.session_state.carteras[seleccion_cartera].copy()
        st.session_state.ppc_actual = st.session_state.ppcs.get(seleccion_cartera, {}).copy()
        guardar_todo_en_navegador()
        st.session_state.version_input += 1
        st.rerun()

    nuevo_nombre = st.text_input("Nuevo portafolio:", placeholder="Ej: CEDEARs o Swing USA", key="inp_nuevo_port")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("➕ Crear / Guardar", key="btn_crear_port", use_container_width=True):
            nom_limpio = nuevo_nombre.strip()
            if nom_limpio:
                st.session_state.carteras[st.session_state.cartera_activa] = st.session_state.montos_dis.copy()
                st.session_state.ppcs[st.session_state.cartera_activa] = st.session_state.ppc_actual.copy()
                st.session_state.carteras[nom_limpio] = st.session_state.montos_dis.copy()
                st.session_state.ppcs[nom_limpio] = st.session_state.ppc_actual.copy()
                st.session_state.cartera_activa = nom_limpio
                guardar_todo_en_navegador()
                st.session_state.version_input += 1
                st.rerun()
            else:
                guardar_todo_en_navegador()
                st.success("¡Guardado en memoria del navegador!")
    with col_p2:
        if len(nombres_disponibles) > 1:
            if st.button("🗑️ Borrar activo", key="btn_borrar_port", use_container_width=True):
                del st.session_state.carteras[st.session_state.cartera_activa]
                st.session_state.ppcs.pop(st.session_state.cartera_activa, None)
                st.session_state.cartera_activa = next(iter(st.session_state.carteras))
                st.session_state.montos_dis = st.session_state.carteras[st.session_state.cartera_activa].copy()
                st.session_state.ppc_actual = st.session_state.ppcs.get(st.session_state.cartera_activa, {}).copy()
                guardar_todo_en_navegador()
                st.session_state.version_input += 1
                st.rerun()
        else:
            st.button("🗑️ Borrar activo", key="btn_borrar_dis", disabled=True, use_container_width=True)

st.markdown("<h3 style='color:#ffffff;'>🕵️‍♂️ Panel de Consulta Avanzada Unificada</h3>", unsafe_allow_html=True)
if 'reset_buscador' not in st.session_state:
    st.session_state.reset_buscador = 0

sugerencias_buscador = ["- Escribe o selecciona un activo -"] + sorted(list(MAPEO_ACTIVOS_CSV.keys()))
seleccion_activo = st.selectbox("Buscador:", sugerencias_buscador, key=f"buscador_v30_{st.session_state.reset_buscador}", label_visibility="collapsed")

activo_a_cargar = None
if seleccion_activo != "- Escribe o selecciona un activo -":
    datos_sel = MAPEO_ACTIVOS_CSV[seleccion_activo]
    tk_usa, tk_byma = datos_sel["orig"], datos_sel["arg"]
    col_izq, col_der = st.columns(2)
    with col_izq:
        if tk_usa != "No Aplica":
            if st.button(f"➕ {tk_usa}", key="btn_add_usa"): activo_a_cargar = tk_usa
        else:
            st.button("-", key="btn_no_usa", disabled=True)
    with col_der:
        if st.button(f"➕ {tk_byma}", key="btn_add_byma"): activo_a_cargar = tk_byma
    if st.button("🧹 Limpiar Buscador", key="btn_clear_top", use_container_width=True):
        st.session_state.reset_buscador += 1
        st.rerun()

if activo_a_cargar:
    copia = st.session_state.montos_dis.copy()
    if activo_a_cargar in copia: del copia[activo_a_cargar]
    nuevo_dict = {activo_a_cargar: 5000.0}
    nuevo_dict.update(copia)
    st.session_state.montos_dis = nuevo_dict
    guardar_todo_en_navegador()
    st.session_state.reset_buscador += 1
    st.rerun()

moneda = st.radio("M", ["Dólares (USD)", "Pesos (ARS)"], horizontal=True, label_visibility="collapsed", key="moneda_v30")
es_pesos = moneda == "Pesos (ARS)"
factor_cambio = VALOR_DOLAR_MEP if es_pesos else 1.0
st.info(f"⚡ Cotización MEP: ARS \$ {VALOR_DOLAR_MEP:,.2f} | {origen_mep_txt}")
st.markdown(f"<h3 style='color:#ffffff; margin-top:5px;'>📁 {st.session_state.cartera_activa} - Fichas Swing & Control</h3>", unsafe_allow_html=True)
def agente_swing_trading_vivo(simbolo_ticket):
    sigla_limpia = simbolo_ticket.replace(".BA", "")
    es_nativo_pesos = simbolo_ticket.endswith(".BA")
    moneda_simb = "ARS $" if es_nativo_pesos else "USD $"
    valores_respaldo = {"KO": 98.00, "AAPL": 360.00, "TSLA": 392.42, "SPY": 810.00, "NVDA": 245.00}
    
    try:
        df_hist = yf.Ticker(simbolo_ticket).history(period="90d")
        if not df_hist.empty and len(df_hist) > 25:
            close, high, low, vol = df_hist["Close"], df_hist["High"], df_hist["Low"], df_hist["Volume"]
            precio_actual = float(close.iloc[-1])

            ema9 = float(close.ewm(span=9).mean().iloc[-1])
            ema21 = float(close.ewm(span=21).mean().iloc[-1])
            sma50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else float(close.mean())

            delta = close.diff()
            gan = delta.where(delta > 0, 0).rolling(14).mean()
            per = (-delta.where(delta < 0, 0)).rolling(14).mean() + 1e-10
            rsi_val = float((100 - (100 / (1 + (gan / per)))).iloc[-1])

            macd_line = close.ewm(span=12).mean() - close.ewm(span=26).mean()
            sig_line = macd_line.ewm(span=9).mean()
            macd_hist = float((macd_line - sig_line).iloc[-1])
            macd_txt = "▲ Alcista" if macd_hist > 0 else "▼ Ajuste"

            vol_prom = float(vol.tail(20).mean()) + 1e-10
            vol_rel = float(vol.iloc[-1]) / vol_prom

            tr1 = high - low
            tr2 = (high - close.shift(1)).abs()
            tr3 = (low - close.shift(1)).abs()
            atr = float(pd.concat([tr1, tr2, tr3], axis=1).max(axis=1).rolling(14).mean().iloc[-1])
            if np.isnan(atr) or atr <= 0:
                atr = precio_actual * 0.025

            stop_loss = max(precio_actual - (1.8 * atr), precio_actual * 0.85)
            take_profit = precio_actual + (3.2 * atr)
            riesgo = max(precio_actual - stop_loss, 1e-6)
            beneficio = max(take_profit - precio_actual, 0.0)
            ratio_rb = round(beneficio / riesgo, 1)

            target_dinamico = None
            try:
                target_dinamico = yf.Ticker(sigla_limpia).info.get("targetMeanPrice")
            except:
                pass
            target_base = float(target_dinamico) if (target_dinamico and target_dinamico > 0) else valores_respaldo.get(sigla_limpia, precio_actual * 1.1)
            if es_nativo_pesos and target_dinamico:
                target_base = target_base * VALOR_DOLAR_MEP

            puntos = 50
            if precio_actual > ema21: puntos += 12
            if ema9 > ema21: puntos += 10
            if precio_actual > sma50: puntos += 8
            if 35 <= rsi_val <= 62: puntos += 10
            elif rsi_val < 35: puntos += 15
            elif rsi_val > 72: puntos -= 18
            if macd_hist > 0: puntos += 8
            if vol_rel >= 1.1: puntos += 5
            if target_base > precio_actual * 1.08: puntos += 7
            puntos = max(0, min(100, int(puntos)))

            if puntos >= 68 and rsi_val <= 70:
                senal, color_borde, motivo = "🟢 COMPRA SWING", "#00e676", "Tendencia y momentum favorables con buen recorrido."
            elif rsi_val > 72 or puntos <= 38:
                senal, color_borde, motivo = "🔴 TOMA DE GANANCIAS", "#f44336", "Sobrecompra o debilidad de tendencia; proteger capital."
            else:
                senal, color_borde, motivo = "🟡 ESPERAR / MANTENER", "#ffeb3b", "En consolidación; aguardar ruptura o retroceso a soporte."

            dist_sma = ((precio_actual - sma50) / sma50) * 100
            piso, techo = float(low.tail(60).min()), float(high.tail(60).max())

            return {
                "precio": precio_actual, "target": target_base, "nativo_pesos": es_nativo_pesos,
                "prob_sem": f"{puntos}%", "prob_anu": "82%" if dist_sma >= 0 else "73%",
                "rsi": f"{rsi_val:.1f}", "macd": macd_txt, "dist_sma": f"{dist_sma:+.1f}%",
                "piso": f"{moneda_simb}{piso:,.2f}", "techo": f"{moneda_simb}{techo:,.2f}",
                "senal": senal, "color_borde": color_borde, "motivo": motivo,
                "sl": stop_loss, "tp": take_profit, "ratio_rb": ratio_rb,
                "vol_rel": f"{vol_rel:.2f}x", "score": puntos
            }
    except:
        pass
    return {
        "precio": 100.0, "target": 110.0, "nativo_pesos": es_nativo_pesos,
        "prob_sem": "60%", "prob_anu": "80%", "rsi": "50.0", "macd": "▲ Alcista",
        "dist_sma": "+0.0%", "piso": f"{moneda_simb}90.00", "techo": f"{moneda_simb}110.00",
        "senal": "🟡 ESPERAR / MANTENER", "color_borde": "#ffeb3b", "motivo": "Sin datos suficientes.",
        "sl": 95.0, "tp": 110.0, "ratio_rb": 2.0, "vol_rel": "1.00x", "score": 55
    }
activos_actuales = list(st.session_state.montos_dis.keys())
patrimonio_total_usd = 0.0
ganancia_total_usd = 0.0
lista_matriz = []

def actualizar_monto_callback(ticker_key, key_widget, factor):
    try:
        solo_num = "".join(c for c in str(st.session_state[key_widget]) if c.isdigit() or c == '.')
        if solo_num:
            st.session_state.montos_dis[ticker_key] = float(solo_num) / factor
            guardar_todo_en_navegador()
            st.session_state.version_input += 1
    except:
        pass

def actualizar_ppc_callback(ticker_key, key_widget, factor):
    try:
        solo_num = "".join(c for c in str(st.session_state[key_widget]) if c.isdigit() or c == '.')
        if solo_num and float(solo_num) > 0:
            st.session_state.ppc_actual[ticker_key] = float(solo_num) / factor
        else:
            st.session_state.ppc_actual.pop(ticker_key, None)
        guardar_todo_en_navegador()
        st.session_state.version_input += 1
    except:
        pass

for tk in activos_actuales:
    tk_up = str(tk).strip().upper()
    datos = agente_swing_trading_vivo(tk_up)
    p_base, p_target, nativo_ars = datos["precio"], datos["target"], datos["nativo_pesos"]
    monto_usd = float(st.session_state.montos_dis[tk])
    patrimonio_total_usd += monto_usd
    
    conv = (1.0 if nativo_ars else VALOR_DOLAR_MEP) if es_pesos else ((1.0 / VALOR_DOLAR_MEP) if nativo_ars else 1.0)
    p_show, t_show = p_base * conv, p_target * conv
    sl_show, tp_show = datos["sl"] * conv, datos["tp"] * conv
    simb = "ARS $" if es_pesos else "USD $"

    ppc_usd = float(st.session_state.ppc_actual.get(tk, 0.0))
    p_actual_usd = (p_base / VALOR_DOLAR_MEP) if nativo_ars else p_base
    ppc_show = ppc_usd * factor_cambio

    pnl_html = ""
    if ppc_usd > 0 and p_actual_usd > 0:
        rend_pct = ((p_actual_usd - ppc_usd) / ppc_usd) * 100
        gan_usd = monto_usd * (rend_pct / 100.0)
        ganancia_total_usd += gan_usd
        gan_show = gan_usd * factor_cambio
        color_pnl = "#00e676" if gan_usd >= 0 else "#f44336"
        signo = "+" if gan_usd >= 0 else ""
        pnl_html = f"<div style='font-size:0.84rem; margin-top:4px; color:{color_pnl}; font-weight:bold;'>📈 Resultado Real: {signo}{simb}{gan_show:,.2f} ({rend_pct:+.2f}%)</div>"

    senal_corta = "Compra" if "COMPRA" in datos["senal"] else ("Venta" if "GANANCIAS" in datos["senal"] else "Esperar")
    lista_matriz.append({"Activo": tk_up, "Señal": senal_corta, "Precio": f"{p_show:,.2f}", "Stop": f"{sl_show:,.2f}", "TP": f"{tp_show:,.2f}", "R/B": f"1:{datos['ratio_rb']}"})

    st.markdown(f'<div class="tarjeta-activo" style="border-left: 4px solid {datos["color_borde"]};">', unsafe_allow_html=True)
    st.markdown(f'<div class="cabecera-cuaderno"><span style="font-size:1.3rem; font-weight:bold; color:#2196f3;">{tk_up}</span><span style="font-size:0.82rem; font-weight:bold; color:{datos["color_borde"]};">{datos["senal"]} ({datos["score"]}/100)</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="renglon-precio-unificado"><b>Precio Actual: {simb}{p_show:,.2f}</b> | <span style="color:#ffeb3b;">🎯 Target:</span> <b style="color:#00e676;">{simb}{t_show:,.2f}</b></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="caja-swing">
        • <b>Plan Swing:</b> Stop Loss <span style="color:#f44336; font-weight:bold;">{simb}{sl_show:,.2f}</span> | Take Profit <span style="color:#00e676; font-weight:bold;">{simb}{tp_show:,.2f}</span> (R/B <b>1:{datos['ratio_rb']}</b>)<br>
        • <b>Agente AI:</b> {datos['motivo']}
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"📊 Indicadores Técnicos (RSI {datos['rsi']} | Vol {datos['vol_rel']})", expanded=False):
        st.markdown(f"• **RSI (14):** {datos['rsi']} | **MACD:** {datos['macd']} | **Dist. SMA50:** {datos['dist_sma']}\n• **Rango 60d:** Piso {datos['piso']} — Techo {datos['techo']}")
        
    if st.button("❌ Borrar", key=f"delete_btn_{tk_up}"):
        del st.session_state.montos_dis[tk]
        st.session_state.ppc_actual.pop(tk, None)
        guardar_todo_en_navegador()
        st.rerun()
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        monto_box = float(monto_usd * factor_cambio)
        st.markdown(f"<div style='font-size:0.8rem; color:#ccc; margin-top:4px;'>Capital ({simb.strip()}):</div>", unsafe_allow_html=True)
        w_key = f"txt_box_{tk_up}_{moneda}_{st.session_state.version_input}"
        st.text_input(f"M_{tk_up}", value=f"{monto_box:,.2f}", key=w_key, on_change=actualizar_monto_callback, args=(tk, w_key, factor_cambio), label_visibility="collapsed")
    with col_m2:
        st.markdown(f"<div style='font-size:0.8rem; color:#ccc; margin-top:4px;'>Precio Compra ({simb.strip()}):</div>", unsafe_allow_html=True)
        p_key = f"ppc_box_{tk_up}_{moneda}_{st.session_state.version_input}"
        val_ppc_txt = f"{ppc_show:,.2f}" if ppc_show > 0 else ""
        st.text_input(f"P_{tk_up}", value=val_ppc_txt, placeholder="Opcional", key=p_key, on_change=actualizar_ppc_callback, args=(tk, p_key, factor_cambio), label_visibility="collapsed")

    if pnl_html:
        st.markdown(pnl_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
 def traducir_y_analizar(texto_en):
    txt_low = texto_en.lower()
    pos = sum(1 for p in ["surge", "soar", "gain", "buy", "upgrade", "beat", "growth", "high", "rally", "bull", "profit", "strong", "record", "better"] if p in txt_low)
    neg = sum(1 for n in ["drop", "fall", "slump", "uncertainty", "plunge", "sell", "downgrade", "miss", "loss", "risk", "bear", "weak", "cut", "lawsuit", "resigns", "lose", "skip"] if n in txt_low)
    sent = "🟢 Sentimiento: Alcista / Positivo" if pos > neg else ("🔴 Sentimiento: Bajista / Precaución" if neg > pos else "🟡 Sentimiento: Neutral / Informativo")
    
    texto_es = texto_en
    traducido = False
    try:
        base_g = "https://translate." + "googleapis.com" + "/translate_a/single"
        params_g = {"client": "gtx", "sl": "en", "tl": "es", "dt": "t", "q": texto_en}
        r = requests.get(base_g, params=params_g, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if r.status_code == 200:
            data = r.json()
            partes = [seg for seg in data if isinstance(seg, list) and len(seg) > 0 and seg]
            if partes:
                texto_es = "".join(partes)
                traducido = True
    except:
        pass

    if not traducido:
        try:
            base_m = "https://api.mymemory." + "translated.net" + "/get"
            params_m = {"q": texto_en, "langpair": "en|es"}
            r2 = requests.get(base_m, params=params_m, timeout=5)
            if r2.status_code == 200:
                trad = r2.json().get("responseData", {}).get("translatedText", "")
                if trad and trad.lower() != texto_en.lower():
                    texto_es = trad
        except:
            pass

    return texto_es, sent

pat_show = patrimonio_total_usd * factor_cambio
gan_tot_show = ganancia_total_usd * factor_cambio
simb_tot = "ARS $" if es_pesos else "USD $"

st.markdown(f"<p style='font-size:0.95rem; font-weight:bold; text-align:center; color:white; margin:8px 0 4px 0;'>💰 Patrimonio Total = <span style='color:#00e676;'>{simb_tot}{pat_show:,.2f}</span></p>", unsafe_allow_html=True)
if ganancia_total_usd != 0:
    col_g_tot = "#00e676" if ganancia_total_usd >= 0 else "#f44336"
    sig_g = "+" if ganancia_total_usd >= 0 else ""
    st.markdown(f"<p style='font-size:0.86rem; font-weight:bold; text-align:center; color:{col_g_tot}; margin:0 0 10px 0;'>📈 Ganancia / Pérdida Registrada = {sig_g}{simb_tot}{gan_tot_show:,.2f}</p>", unsafe_allow_html=True)

if activos_actuales:
    df_pie = pd.DataFrame({"Activo": [str(k).upper() for k in st.session_state.montos_dis.keys()], "Capital": [float(v) * factor_cambio for v in st.session_state.montos_dis.values()]})
    fig = px.pie(df_pie, values='Capital', names='Activo', hole=0.4, height=230)
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white", size=11))
    st.plotly_chart(fig, use_container_width=True, key="pie_v30", config={'displayModeBar': False})

if "ver_resumen" not in st.session_state: st.session_state.ver_resumen = False
if st.button("📊 Mostrar / Ocultar Planilla Swing General", key="btn_res_v30", use_container_width=True):
    st.session_state.ver_resumen = not st.session_state.ver_resumen
    st.rerun()

if st.session_state.ver_resumen and lista_matriz:
    st.markdown(pd.DataFrame(lista_matriz).to_html(index=False, classes='dataframe'), unsafe_allow_html=True)

st.markdown("<h3 style='color:#ffffff; margin-top:12px;'>🚀 Escáner Top 5 Oportunidades Swing (CSV)</h3>", unsafe_allow_html=True)
if "top5_swing" not in st.session_state:
    st.session_state.top5_swing = []

if st.button("🔍 Escanear Mejores Oportunidades Ahora", key="btn_scan_top5", use_container_width=True):
    candidatos = []
    universo = [v["orig"] if v["orig"] != "No Aplica" else v["arg"] for v in list(MAPEO_ACTIVOS_CSV.values())[:25]]
    barra = st.progress(0)
    for idx_u, tk_scan in enumerate(universo):
        res_s = agente_swing_trading_vivo(tk_scan)
        candidatos.append((res_s["score"], tk_scan, res_s))
        barra.progress((idx_u + 1) / len(universo))
    barra.empty()
    candidatos.sort(key=lambda item: item.get("score", 0) if isinstance(item, dict) else item, reverse=True)
    st.session_state.top5_swing = candidatos[:5]

if st.session_state.top5_swing:
    for score_op, tk_op, info_op in st.session_state.top5_swing:
        p_op_show = (info_op["precio"] if info_op["nativo_pesos"] else info_op["precio"] * VALOR_DOLAR_MEP) if es_pesos else ((info_op["precio"] / VALOR_DOLAR_MEP) if info_op["nativo_pesos"] else info_op["precio"])
        st.markdown(f"""
        <div class="tarjeta-activo" style="border-left: 4px solid {info_op['color_borde']}; padding:8px 12px;">
            <div style="display:flex; justify-content:space-between; font-size:0.86rem;">
                <b>🔥 {tk_op} ({info_op['senal']})</b>
                <span style="color:#00e676; font-weight:bold;">Puntaje: {score_op}/100</span>
            </div>
            <div style="font-size:0.8rem; color:#ccc; margin-top:3px;">
                Precio: {simb_tot}{p_op_show:,.2f} | RSI: {info_op['rsi']} | Ratio R/B: <b>1:{info_op['ratio_rb']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"➕ Agregar {tk_op} a {st.session_state.cartera_activa}", key=f"add_top5_{tk_op}"):
            st.session_state.montos_dis[tk_op] = 5000.0
            guardar_todo_en_navegador()
            st.rerun()

st.markdown("<h3 style='color:#ffffff; margin-top:12px;'>💵 Ticket de Referencia Dólar MEP (AL30)</h3>", unsafe_allow_html=True)
if datos_mep["al30_ars"] and datos_mep["al30_usd"]:
    st.markdown(f"""
    <div class="tarjeta-activo" style="border-left: 4px solid #2196f3;">
        <div style="font-size:0.86rem; color:#ffffff; line-height:1.5;">
            • <b>Bono AL30.BA (Pesos):</b> ARS $ {datos_mep['al30_ars']:,.2f}<br>
            • <b>Bono AL30D.BA (Dólares):</b> USD $ {datos_mep['al30_usd']:,.2f}<br>
            • <b>Cálculo MEP ({datos_mep['fecha']}):</b> ARS $ {datos_mep['al30_ars']:,.2f} / USD $ {datos_mep['al30_usd']:,.2f} = <b style="color:#00e676;">ARS $ {VALOR_DOLAR_MEP:,.2f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="tarjeta-activo" style="border-left: 4px solid #ffeb3b;">
        <div style="font-size:0.86rem; color:#ffffff; line-height:1.4;">
            • <b>Cotización MEP Aplicada:</b> <b style="color:#00e676;">ARS $ {VALOR_DOLAR_MEP:,.2f}</b> ({origen_mep_txt})
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h3 style='color:#ffffff;'>📰 Central de Noticias y Análisis en Español</h3>", unsafe_allow_html=True)
alcistas, bajistas = 0, 0
base_yf = "https://finance." + "yahoo.com" + "/quote/"

for simbolo in activos_actuales:
    s_fijo = str(simbolo).strip().upper()
    s_usa = s_fijo.replace(".BA", "")
    noticias = []
    try:
        noticias = yf.Ticker(s_usa).news[:2]
    except:
        pass

    if noticias:
        for item in noticias:
            cont = item.get("content", item)
            tit_orig = cont.get("title", "Actualización de mercado")
            link_obj = cont.get("canonicalUrl", {})
            url_not = link_obj.get("url") if isinstance(link_obj, dict) else item.get("link", f"{base_yf}{s_usa}")
            
            tit_es, sent = traducir_y_analizar(tit_orig)
            if "Positivo" in sent: alcistas += 1
            elif "Precaución" in sent: bajistas += 1
            
            st.markdown(f"""
            <div class="caja-noticia-link">
                <span style="color:#2196f3; font-weight:bold;">[{s_fijo}]</span> <b>{tit_es}</b>
                <div style="font-size:0.78rem; color:#ccc; margin-top:4px;">{sent}</div>
                <a href="{url_not}" target="_blank" class="enlace-noticia-azul">🔗 Leer nota completa en Yahoo Finance</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="caja-noticia-link">
            <span style="color:#2196f3; font-weight:bold;">[{s_fijo}]</span> <b>Sin titulares recientes en el feed directo.</b><br>
            <a href="{base_yf}{s_usa}" target="_blank" class="enlace-noticia-azul">🔗 Ver panel en Yahoo Finance</a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h3 style='color:#ffffff; margin-top:12px;'>🧠 Análisis General del Portafolio</h3>", unsafe_allow_html=True)
diag = "Sesgo <b>positivo</b> en tus activos." if alcistas > bajistas else ("Titulares de <b>cautela o volatilidad</b>." if bajistas > alcistas else "<b>Equilibrio informativo</b> en tu cartera.")
st.markdown(f"""
<div class="tarjeta-activo" style="border-left: 4px solid #00e676; margin-bottom: 50px;">
    <div style="font-size:0.86rem; color:#ffffff; line-height:1.4;">
        • <b>Balance:</b> {alcistas} favorables vs. {bajistas} de precaución.<br>
        • <b>Conclusión:</b> {diag}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('''
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161a22; border-top: 1px solid #232a38; display: flex; justify-content: space-around; padding: 4px 0; z-index: 1000; font-size:0.68rem; text-align:center;">
    <div style="color:#888;">🏠<br>Inicio</div>
    <div style="color:#2196f3; font-weight:bold;">💼<br>Portafolio</div>
    <div style="color:#888;">📊<br>Análisis</div>
    <div style="color:#888;">💬<br>Chat</div>
    <div style="color:#888;">👤<br>Perfil</div>
</div>
''', unsafe_allow_html=True)
            
