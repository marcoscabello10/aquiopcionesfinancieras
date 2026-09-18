import streamlit as st  
import numpy as np  
import matplotlib.pyplot as plt  
import yfinance as yf

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Manual Interactivo de Opciones", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def obtener_precio_actual(ticker):  
    try:  
        data = yf.Ticker(ticker)  
        precio = data.history(period="1d")['Close'].iloc[-1]  
        return round(precio, 2)  
    except:  
        return None

def graficar_payoff(precios, payoff, precio_actual, titulo, x_label, y_label):  
    fig, ax = plt.subplots(figsize=(10, 5))  
    ax.plot(precios, payoff, color="#1E88E5", linewidth=3)  
    ax.axhline(0, color="black", linewidth=1.5)  
    ax.axvline(precio_actual, color="orange", linestyle="--", label=f"Precio Actual (${precio_actual})")
    ax.fill_between(precios, payoff, 0, where=(payoff >= 0), facecolor='#4CAF50', alpha=0.4, label="Ganancia")  
    ax.fill_between(precios, payoff, 0, where=(payoff < 0), facecolor='#F44336', alpha=0.4, label="Pérdida")  
      
    ax.set_title(titulo, fontsize=14, fontweight='bold')  
    ax.set_xlabel(x_label)  
    ax.set_ylabel(y_label)  
    ax.legend()  
    ax.grid(alpha=0.3)  
    return fig  
  
# ==========================================
# BARRA LATERAL (MENÚ)
# ==========================================
st.sidebar.title("📖 Índice del Manual")  
capitulo = st.sidebar.radio("Navega por los capítulos:", [  
    "1. Introducción 'APB' (Conceptos)",  
    "2. Comprar Derechos (Calls y Puts)",  
    "3. Vender Obligaciones (El Riesgo)",  
    "4. Estrategias: Spreads (Direccionales)",  
    "5. Estrategias: Volatilidad (Conos y Cunas)",  
    "6. Estrategias Avanzadas (Mariposa y Túnel)"  
])
st.sidebar.info("💡 Todos los capítulos operativos usan datos en tiempo real de Yahoo Finance.")

# ==========================================
# CAPÍTULO 1: INTRODUCCIÓN APB
# ==========================================
if capitulo == "1. Introducción 'APB' (Conceptos)":  
    st.title("Capítulo 1: ¿Qué son las Opciones?")  
    st.markdown("""  
    Una opción NO es una acción. Es un CONTRATO que te da el DERECHO a comprar o vender algo a un precio fijo en el futuro.
    
    ### 🏠 El CALL (Como señar un departamento)  
    Querés comprar un depto que vale **$100.000** pero no tenés la plata hoy. Creés que va a subir.  
    Vas a la inmobiliaria y dejás una seña de **$5.000 (PRIMA)** para congelar el precio en **$100.000 (STRIKE)** por un año.  
    *   Si sube a $150.000: Lo comprás a $100k, le restás tu seña, ¡Ganaste $45.000!  
    *   Si baja a $80.000: No lo comprás. Tu pérdida máxima fue solo la seña de $5.000.  
      
    ### 🚗 El PUT (Como el seguro del auto)  
    Tenés un auto de **$20.000** y querés asegurarlo.  
    Pagás **$1.000 (PRIMA)** por mes. Si se destruye, la aseguradora te paga los **$20.000 (STRIKE)**.  
    *   Si chocás (el precio del auto cae a $0): El seguro te salva y cobrás los $20.000.  
    *   Si no chocás: Perdiste los $1.000 del seguro, pero dormiste tranquilo.  
    """)  
  
# ==========================================
# CAPÍTULOS 2 y 3: BÁSICOS
# ==========================================
elif capitulo in ["2. Comprar Derechos (Calls y Puts)", "3. Vender Obligaciones (El Riesgo)"]:  
    st.title(capitulo)  
    ticker = st.text_input("Ticker bursátil (Ej: AAPL, SPY):", "AAPL")  
    precio_actual = obtener_precio_actual(ticker)
    
    if precio_actual:  
        st.info(f"💵 Precio actual de **{ticker}**: **USD {precio_actual}**")  
          
        tipo = st.selectbox("Operación:", ["CALL", "PUT"])  
          
        col1, col2 = st.columns(2)  
        with col1:  
            strike = st.number_input("Strike:", value=float(precio_actual))  
        with col2:  
            prima = st.number_input("Prima:", value=round(precio_actual*0.05, 2))  
              
        precios = np.linspace(precio_actual * 0.5, precio_actual * 1.5, 200)  
          
        if capitulo.startswith("2"):  
            # Compras  
            if tipo == "CALL":  
                payoff = np.maximum(precios - strike, 0) - prima  
                st.write("**Idea:** Pagás la seña hoy. Si vuela, ganancias infinitas. Si cae, perdes solo la seña.")  
            else:  
                payoff = np.maximum(strike - precios, 0) - prima  
                st.write("**Idea:** Comprás un seguro. Proteges tu cartera de caídas severas.")  
        else:  
            # Ventas  
            if tipo == "CALL":  
                payoff = np.minimum(strike - precios, 0) + prima  
                st.write("**Idea (Riesgoso):** Cobrás la seña. Si sube mucho, te obligan a vender barato.")  
            else:  
                payoff = np.minimum(precios - strike, 0) + prima  
                st.write("**Idea:** Sos la aseguradora. Cobrás por esperar a que la acción caiga para comprarla.")  
  
        fig = graficar_payoff(precios, payoff, precio_actual, f"{capitulo[3:10]} {tipo} - {ticker}", "Precio Futuro", "Payoff")  
        st.pyplot(fig)  
  
# ==========================================
# CAPÍTULO 4: SPREADS
# ==========================================
elif capitulo == "4. Estrategias: Spreads (Direccionales)":  
    st.title("Capítulo 4: Spreads (Reduciendo el costo)")  
    st.write("Combinamos la compra y venta de opciones para abaratar costos a cambio de limitar la ganancia máxima.")
    ticker = st.text_input("Ticker (Ej: NVDA):", "NVDA")  
    precio_actual = obtener_precio_actual(ticker)  
      
    if precio_actual:  
        st.info(f"💵 Precio actual de **{ticker}**: **USD {precio_actual}**")  
        tipo_spread = st.radio("Tipo de Spread:", ["Bull Call Spread (Alcista)", "Bear Put Spread (Bajista)"])  
          
        col1, col2 = st.columns(2)  
        if "Bull" in tipo_spread:  
            with col1:  
                st.write("1. Compramos un CALL (Strike Bajo)")  
                strike_compra = st.number_input("Strike Comprado:", value=float(precio_actual))  
                prima_pagada = st.number_input("Prima Pagada:", value=round(precio_actual*0.06, 2))  
            with col2:  
                st.write("2. Vendemos un CALL (Strike Alto)")  
                strike_venta = st.number_input("Strike Vendido:", value=float(precio_actual*1.10))  
                prima_cobrada = st.number_input("Prima Cobrada:", value=round(precio_actual*0.02, 2))  
                  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(precios - strike_compra, 0) - prima_pagada) + (np.minimum(strike_venta - precios, 0) + prima_cobrada)  
        else:  
            with col1:  
                st.write("1. Compramos un PUT (Strike Alto)")  
                strike_compra = st.number_input("Strike Comprado:", value=float(precio_actual))  
                prima_pagada = st.number_input("Prima Pagada:", value=round(precio_actual*0.06, 2))  
            with col2:  
                st.write("2. Vendemos un PUT (Strike Bajo)")  
                strike_venta = st.number_input("Strike Vendido:", value=float(precio_actual*0.90))  
                prima_cobrada = st.number_input("Prima Cobrada:", value=round(precio_actual*0.02, 2))  
                  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(strike_compra - precios, 0) - prima_pagada) + (np.minimum(precios - strike_venta, 0) + prima_cobrada)  
  
        st.warning(f"**Costo y Riesgo Máximo:** Solo arriesgas la diferencia neta de primas: USD {prima_pagada - prima_cobrada:.2f}")  
        fig = graficar_payoff(precios, payoff, precio_actual, f"{tipo_spread} sobre {ticker}", "Precio Futuro", "Payoff")  
        st.pyplot(fig)  
  
# ==========================================
# CAPÍTULO 5: VOLATILIDAD
# ==========================================
elif capitulo == "5. Estrategias: Volatilidad (Conos y Cunas)":  
    st.title("Capítulo 5: Volatilidad Pura")  
    st.write("No sabés si la acción va a subir o bajar, solo sabés que va a explotar (ej: balance de ganancias).")
    ticker = st.text_input("Ticker (Ej: META, TSLA):", "TSLA")  
    precio_actual = obtener_precio_actual(ticker)  
      
    if precio_actual:  
        st.info(f"💵 Precio actual de **{ticker}**: **USD {precio_actual}**")  
        tipo_vol = st.radio("Estrategia:", ["Cono Comprado / Straddle (Mismo Strike)", "Cuna Comprada / Strangle (Strikes Distintos, más barato)"])  
          
        if "Cono" in tipo_vol:  
            strike = st.number_input("Strike Único:", value=float(precio_actual))  
            prima_c = st.number_input("Prima Call:", value=round(precio_actual*0.05, 2))  
            prima_p = st.number_input("Prima Put:", value=round(precio_actual*0.05, 2))  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(precios - strike, 0) - prima_c) + (np.maximum(strike - precios, 0) - prima_p)  
        else:  
            col1, col2 = st.columns(2)  
            with col1:  
                strike_p = st.number_input("Strike PUT (Más bajo):", value=float(precio_actual*0.95))  
                prima_p = st.number_input("Prima Put:", value=round(precio_actual*0.02, 2))  
            with col2:  
                strike_c = st.number_input("Strike CALL (Más alto):", value=float(precio_actual*1.05))  
                prima_c = st.number_input("Prima Call:", value=round(precio_actual*0.02, 2))  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(precios - strike_c, 0) - prima_c) + (np.maximum(strike_p - precios, 0) - prima_p)  
  
        st.warning(f"**Costo Total:** USD {prima_c + prima_p:.2f}. Necesitás un movimiento violento para recuperar esto.")  
        fig = graficar_payoff(precios, payoff, precio_actual, f"{tipo_vol} - {ticker}", "Precio Futuro", "Payoff")  
        st.pyplot(fig)  
  
# ==========================================
# CAPÍTULO 6: ESTRATEGIAS AVANZADAS
# ==========================================
elif capitulo == "6. Estrategias Avanzadas (Mariposa y Túnel)":  
    st.title("Capítulo 6: Sintonía Fina y Protección Total")
    ticker = st.text_input("Ticker (Ej: GGAL, YPF):", "YPF")  
    precio_actual = obtener_precio_actual(ticker)  
      
    if precio_actual:  
        st.info(f"💵 Precio actual de **{ticker}**: **USD {precio_actual}**")  
        estrategia = st.radio("Elegir Estrategia:", ["Mariposa Comprada (Butterfly)", "Túnel Protector (Collar)"])  
          
        precios = np.linspace(precio_actual * 0.6, precio_actual * 1.4, 200)  
  
        if "Mariposa" in estrategia:  
            st.markdown("**Mariposa:** Apuestas a que la acción **NO se va a mover**. Combinas 4 contratos con 3 strikes.")  
            col1, col2, col3 = st.columns(3)  
            with col1:  
                s_bajo = st.number_input("Strike Bajo (Comprás 1):", value=float(precio_actual*0.9))  
                p_bajo = st.number_input("Prima Pagada:", value=round(precio_actual*0.08, 2))  
            with col2:  
                s_medio = st.number_input("Strike Medio (Vendés 2):", value=float(precio_actual))  
                p_medio = st.number_input("Prima Cobrada (x2):", value=round(precio_actual*0.03, 2))  
            with col3:  
                s_alto = st.number_input("Strike Alto (Comprás 1):", value=float(precio_actual*1.1))  
                p_alto = st.number_input("Prima Pagada 2:", value=round(precio_actual*0.01, 2))  
              
            payoff = (np.maximum(precios - s_bajo, 0) - p_bajo) + (2 * (np.minimum(s_medio - precios, 0) + p_medio)) + (np.maximum(precios - s_alto, 0) - p_alto)  
              
        else:  
            st.markdown("**Túnel (Collar):** Ya tenés acciones de la empresa. Querés asegurarlas contra una caída comprando un PUT, pero para pagar ese seguro, vendés un CALL (cediendo las ganancias extremas).")  
            col1, col2 = st.columns(2)  
            with col1:  
                s_put = st.number_input("Strike PUT Comprado (Piso):", value=float(precio_actual*0.90))  
                p_put = st.number_input("Costo del Seguro (Put):", value=round(precio_actual*0.03, 2))  
            with col2:  
                s_call = st.number_input("Strike CALL Vendido (Techo):", value=float(precio_actual*1.10))  
                p_call = st.number_input("Ingreso por Venta (Call):", value=round(precio_actual*0.03, 2))  
              
            # Payoff incluye: Las acciones que ya tenés (precio futuro - precio actual) + el Put comprado + el Call vendido.  
            payoff_acciones = precios - precio_actual  
            payoff_put = np.maximum(s_put - precios, 0) - p_put  
            payoff_call = np.minimum(s_call - precios, 0) + p_call  
            payoff = payoff_acciones + payoff_put + payoff_call  
  
        fig = graficar_payoff(precios, payoff, precio_actual, f"{estrategia} - {ticker}", "Precio Futuro", "Payoff Total")  
        st.pyplot(fig)  
