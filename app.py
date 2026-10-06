
import streamlit as st

# Configuración de la página optimizada para celulares
st.set_page_config(
    page_title="Nuevo Finance Pro",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados con el nuevo reordenamiento simétrico
st.markdown("""
    <style>
    /* Ocultar elementos estándar de Streamlit para simular App nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor principal de la ficha independiente */
    .crypto-card {
        background-color: #1E1E1E;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #2D2D2D;
        color: #FFFFFF;
    }
    
    /* Renglón 1: Ticker y Clasificación alineados en los extremos */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .ticker-text {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .status-badge {
        font-size: 14px;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 6px;
        background-color: #2D2D2D;
        color: #FFD700;
    }
    
    /* Renglón 2 y texto estandarizado: Subrayado azul y texto blanco */
    .price-fundamental-style {
        color: #FFFFFF !important;
        text-decoration: underline #0000FF 2px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-bottom: 8px;
    }
    
    /* Renglones de análisis intermedios */
    .analysis-text {
        font-size: 14px;
        color: #CCCCCC;
        margin-bottom: 6px;
        line-height: 1.4;
    }
    
    /* Renglón de Control Alto: Alineación perfecta de la Moneda y Eliminar */
    .control-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 14px;
        margin-bottom: 4px;
    }
    .currency-label {
        font-size: 12px;
        color: #888888;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* Botón Eliminar ultra discreto y achicado */
    div.stButton > button {
        background-color: transparent !important;
        color: #FF4B4B !important;
        border: 1px solid #331A1A !important;
        padding: 2px 8px !important;
        font-size: 11px !important;
        border-radius: 4px !important;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #331A1A !important;
        border-color: #FF4B4B !important;
    }
    
    /* Input numérico verde limpio (Ocupa el 100% del ancho abajo) */
    div[data-testid="stNumberInput"] input {
        color: #00FF00 !important;
        background-color: #121212 !important;
        border: 1px solid #2D2D2D !important;
        font-size: 16px !important;
        border-radius: 6px !important;
    }
    
    /* Barra de Navegación Fija Inferior Simétrica */
    .nav-bar-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #121212;
        border-top: 1px solid #2D2D2D;
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 999;
    }
    .nav-item {
        color: #888888;
        font-size: 11px;
        text-align: center;
        text-decoration: none;
        flex: 1;
    }
    .nav-item.active {
        color: #0088FF;
        font-weight: bold;
    }
    .nav-icon {
        font-size: 18px;
        display: block;
        margin-bottom: 2px;
    }
    .main-content {
        margin-bottom: 90px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar simulación de activos en sesión
if "activos" not in st.session_state:
    st.session_state.activos = {
        "SPY": {"clase": "COMPRAR", "precio": "USD $545.20", "funda": "Nota 8/10 \"Sólido respaldo institucional e indexado\"", "tec_sem": "Alcista controlado", "tec_anual": "Tendencia histórica positiva", "noticias": "Debate de tasas favorece fondos indexados"},
        "TSLA": {"clase": "COMPRA FUERTE", "precio": "USD $220.45", "funda": "Nota 9/10 \"Alta innovación tecnológica y expansión masiva\"", "tec_sem": "Ruptura de resistencia clave", "tec_anual": "Volatilidad alta con sesgo alcista", "noticias": "Nuevas proyecciones de entregas superan expectativas"},
        "AAPL": {"clase": "MANTENER", "precio": "USD $182.10", "funda": "Nota 7/10 \"Flujo de caja predecible pero crecimiento maduro\"", "tec_sem": "Consolidación lateral", "tec_anual": "Soporte fuerte en medias móviles largas", "noticias": "Lanzamiento de funciones IA genera cautela"},
        "KO": {"clase": "MANTENER", "precio": "USD $62.30", "funda": "Nota 7/10 \"Dividendo seguro y negocio anticíclico estable\"", "tec_sem": "Sobrecompra de corto plazo", "tec_anual": "Refugio seguro sin grandes variaciones", "noticias": "Costos de distribución impactan márgenes operativos"}
    }
# Contenedor para aplicar el margen inferior de seguridad móvil
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Renderizado de Fichas independientes verticales
for ticker, info in list(st.session_state.activos.items()):
    
    # Bloque de información del Activo
    st.markdown(f"""
    <div class="crypto-card">
        <!-- Renglón 1: Ticker y Clasificación -->
        <div class="card-header">
            <span class="ticker-text">{ticker}</span>
            <span class="status-badge">{info['clase']}</span>
        </div>
        <!-- Renglón 2: Precio de la Acción Actual -->
        <div class="price-fundamental-style">Precio de la Acción Actual: {info['precio']}</div>
        <!-- Renglón 3: Análisis Fundamental -->
        <div class="analysis-text"><b>Fundamental:</b> {info['funda']}</div>
        <!-- Renglón 4: Análisis Técnico Semanal y Anual -->
        <div class="analysis-text"><b>Técnico Semanal:</b> {info['tec_sem']} | <b>Anual:</b> {info['tec_anual']}</div>
        <!-- Renglón 5: Análisis Últimas Noticias por el Agente -->
        <div class="analysis-text"><b>Noticias del Agente:</b> {info['noticias']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Renglón de Control: Símbolo de Dinero alineado con el botón Eliminar
    col_label, col_btn = st.columns([0.65, 0.35])
    with col_label:
        st.markdown('<p class="currency-label">USD $ / ARS $</p>', unsafe_allow_html=True)
    with col_btn:
        if st.button("❌ Eliminar", key=f"del_{ticker}"):
            del st.session_state.activos[ticker]
            st.rerun()
            
    # Casillero numérico verde limpio posicionado ABAJO de manera independiente
    st.number_input(
        "Monto a simular",
        min_value=0,
        value=0,
        step=100,
        key=f"cap_{ticker}",
        label_visibility="collapsed"
    )
    
    # Espaciador sutil entre tarjetas
    st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)

# Cierre del contenedor principal
st.markdown('</div>', unsafe_allow_html=True)

# Barra de Navegación Fija Inferior Simétrica
st.markdown("""
    <div class="nav-bar-footer">
        <a href="#inicio" class="nav-item">
            <span class="nav-icon">🏠</span>Inicio
        </a>
        <a href="#portafolio" class="nav-item">
            <span class="nav-icon">💼</span>Portafolio
        </a>
        <a href="#analisis" class="nav-item active">
            <span class="nav-icon">📊</span>Análisis
        </a>
        <a href="#chat" class="nav-item">
            <span class="nav-icon">💬</span>Chat
        </a>
        <a href="#perfil" class="nav-item">
            <span class="nav-icon">👤</span>Perfil
        </a>
    </div>
""", unsafe_allow_html=True)
