import streamlit as st  
import numpy as np  
import matplotlib.pyplot as plt  
import yfinance as yf

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Manual Interactivo de Opciones - Prof. Firulais", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
@st.cache_data(ttl=3600)
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
    ax.axvline(precio_actual, color="orange", linestyle="--", label=f"Precio Actual (USD {precio_actual})")
    ax.fill_between(precios, payoff, 0, where=(payoff >= 0), facecolor='#4CAF50', alpha=0.4, label="Ganancia (¡Premio!)")  
    ax.fill_between(precios, payoff, 0, where=(payoff < 0), facecolor='#F44336', alpha=0.4, label="Pérdida (¡Guau!)")  
      
    ax.set_title(titulo, fontsize=14, fontweight='bold')  
    ax.set_xlabel(x_label)  
    ax.set_ylabel(y_label)  
    ax.legend()  
    ax.grid(alpha=0.3)  
    return fig  

def cargar_imagen_internet(url, caption, sidebar=False):
    # Streamlit maneja muy bien las URLs externas de forma nativa
    try:
        if sidebar:
            st.sidebar.image(url, caption=caption, use_column_width=True)
        else:
            st.image(url, caption=caption, use_column_width=True)
    except Exception as e:
        # Fallback en caso de que se caiga la URL
        if sidebar:
            st.sidebar.caption(f"*(Imagen no disponible)*")
        else:
            st.caption(f"*(Imagen no disponible)*")

# Diccionario con URLs de imágenes externas confiables (Unsplash / Wikimedia)
URLS_IMAGENES = {
    "profesor": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?q=80&w=800&auto=format&fit=crop", # Perrito lindo/inteligente
    "estudiante": "https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?q=80&w=800&auto=format&fit=crop", # Perrito prestando atencion
    "concepto": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop" # Gráfico/Finanzas
}
  
# ==========================================
# BARRA LATERAL (MENÚ)
# ==========================================
cargar_imagen_internet(URLS_IMAGENES["profesor"], "Prof. Firulais", sidebar=True)

st.sidebar.title("📖 El Manual del Prof. Firulais")  
capitulo = st.sidebar.radio("Navega por las clases:", [  
    "1. Introducción 'APB' (Conceptos)",  
    "2. Comprar Derechos (Calls y Puts)",  
    "3. Vender Obligaciones (El Riesgo)",  
    "4. Estrategias: Spreads (Direccionales)",  
    "5. Estrategias: Volatilidad (Conos y Cunas)",  
    "6. Estrategias Avanzadas (Mariposa y Túnel)"  
])
st.sidebar.info("💡 Guau! Todos los capítulos operativos usan datos fresquitos en tiempo real de Yahoo Finance.")

# ==========================================
# CAPÍTULO 1: INTRODUCCIÓN APB
# ==========================================
if capitulo == "1. Introducción 'APB' (Conceptos)":  
    st.title("Capítulo 1: ¿Qué son las Opciones? ¡Te lo explico con huesos!")  
    
    col1, col2 = st.columns([1, 2])
    with col1:
        cargar_imagen_internet(URLS_IMAGENES["estudiante"], "Vos tratando de entender opciones")
    with col2:
        st.markdown("""
        ¡Hola! Soy el **Profesor Firulais**. Hoy te voy a enseñar qué es una **Opción Financiera**.  
        No te asustes, no es física cuántica. En términos "A Prueba de Boludos" (APB):
        
        Una opción **NO es una acción**. Es un **CONTRATO** que te da el **DERECHO** (no la obligación) de comprar o vender algo a un precio fijo en el futuro. 
        """)
        
    st.divider()

    st.header("🏠 El CALL (Como señar un departamento)")  
    st.markdown("""  
    Imaginate que querés comprar un depto que vale **USD 100.000** pero no tenés toda la plata hoy. Sin embargo, estás seguro de que el precio va a subir.  
    Vas a la inmobiliaria y le decís: "Te dejo una seña de **USD 5.000 (a esto le llamamos PRIMA)** para que me congeles el precio en **USD 100.000 (a esto le llamamos STRIKE)** por un año".  
    
    ¿Qué pasa en un año?
    *   📈 **Si el depto sube a USD 150.000:** ¡Golazo! Lo comprás a USD 100k, le restás tu seña, ¡Ganaste USD 45.000 limpios!  
    *   📉 **Si el depto baja a USD 80.000:** Obvio que no lo comprás a USD 100k. Te vas corriendo, perdiste tu seña de USD 5.000, pero ¡zafaste de perder mucho más! Tu pérdida máxima está limitada a la seña.
    """)  
      
    st.divider()

    st.header("🚗 El PUT (Como pagar el seguro del auto)")  
    st.markdown("""  
    Tenés un auto hermoso que vale **USD 20.000** y querés asegurarlo para dormir tranquilo (como un perrito en su cucha).  
    Pagás **USD 1.000 (la PRIMA)** por mes. Si el auto se destruye, la aseguradora te tiene que pagar los **USD 20.000 (el STRIKE)**.  
    
    ¿Qué pasa después?
    *   💥 **Si chocás (el precio del auto cae a USD 0):** El seguro te salva las papas y cobrás los USD 20.000.  
    *   😌 **Si no chocás:** "Perdiste" los USD 1.000 del seguro, pero tu auto sigue intacto y dormiste tranquilo todo el mes. ¡Es un buen trato!
    """)
    
    cargar_imagen_internet(URLS_IMAGENES["concepto"], "Mercado y Opciones")
  
# ==========================================
# CAPÍTULOS 2 y 3: BÁSICOS
# ==========================================
elif capitulo in ["2. Comprar Derechos (Calls y Puts)", "3. Vender Obligaciones (El Riesgo)"]:  
    st.title(f"🐶 {capitulo}")  
    st.markdown("¡Vamos a jugar con datos reales! Decime, ¿qué empresa estamos mirando hoy?")
    
    ticker = st.text_input("Escribí el Ticker (Ej: AAPL para Apple, SPY para S&P 500):", "AAPL")  
    precio_actual = obtener_precio_actual(ticker)
    
    if precio_actual:  
        st.success(f"🦴 ¡Lo encontré! El precio actual de **{ticker}** es: **USD {precio_actual}**")  
          
        tipo = st.selectbox("¿Qué contrato querés armar?", ["CALL (Seña por depto)", "PUT (Seguro de auto)"])  
        tipo_base = "CALL" if "CALL" in tipo else "PUT"
          
        col1, col2 = st.columns(2)  
        with col1:  
            strike = st.number_input("Precio Congelado (Strike):", value=float(precio_actual))  
        with col2:  
            prima = st.number_input("Costo del contrato (Prima):", value=round(precio_actual*0.05, 2))  
              
        precios = np.linspace(precio_actual * 0.5, precio_actual * 1.5, 200)  
          
        st.divider()
        if capitulo.startswith("2"):  
            st.subheader("Estás COMPRANDO (Tenés el Derecho)")
            # Compras  
            if tipo_base == "CALL":  
                payoff = np.maximum(precios - strike, 0) - prima  
                st.info(f"💡 **Idea del Prof. Firulais:** Pagás USD {prima:.2f} hoy. Si {ticker} vuela hacia la luna por encima de USD {strike:.2f}, tus ganancias no tienen límite. Si se desploma, lo peor que te pasa es que perdés tu seña de USD {prima:.2f}.")  
            else:  
                payoff = np.maximum(strike - precios, 0) - prima  
                st.info(f"💡 **Idea del Prof. Firulais:** Comprás un seguro para tu inversión por USD {prima:.2f}. Protegés tus acciones de {ticker} si caen por debajo de USD {strike:.2f}.")  
        else:  
            st.subheader("Estás VENDIENDO (Asumís la Obligación)")
            # Ventas  
            if tipo_base == "CALL":  
                payoff = np.minimum(strike - precios, 0) + prima  
                st.error(f"⚠️ **¡Cuidado! Idea Riesgosa:** Cobrás USD {prima:.2f} hoy. Pero si {ticker} sube muchísimo, ¡te obligan a vender barato a USD {strike:.2f}! (Pérdidas infinitas, ¡guau!)")  
            else:  
                payoff = np.minimum(precios - strike, 0) + prima  
                st.warning(f"⚠️ **Idea:** Acá vos sos la Aseguradora. Cobrás USD {prima:.2f} y esperás que {ticker} NO caiga, porque si cae por debajo de USD {strike:.2f}, te obligan a comprarla cara.")  
  
        fig = graficar_payoff(precios, payoff, precio_actual, f"{capitulo[3:10]} {tipo_base} - {ticker}", "Precio Futuro", "Tu Dinero (Payoff)")  
        st.pyplot(fig)  

# ==========================================
# CAPÍTULO 4: SPREADS
# ==========================================
elif capitulo == "4. Estrategias: Spreads (Direccionales)":  
    st.title("Capítulo 4: Spreads (Haciendo la cuenta más barata)")  
    st.markdown("""
    **Profesor Firulais dice:** "A veces la prima (el seguro o la seña) es muy cara. Para que nos cueste menos, podemos **comprar y vender al mismo tiempo** diferentes opciones. ¡Achicamos el costo, pero ojo, también limitamos nuestra ganancia máxima!"
    """)
    ticker = st.text_input("Ticker (Ej: NVDA):", "NVDA")  
    precio_actual = obtener_precio_actual(ticker)  
      
    if precio_actual:  
        st.success(f"🦴 Precio actual de **{ticker}**: **USD {precio_actual}**")  
        tipo_spread = st.radio("¿Para dónde creés que va el mercado?", ["Bull Call Spread (Creo que sube 📈)", "Bear Put Spread (Creo que baja 📉)"])  
          
        st.divider()
        col1, col2 = st.columns(2)  
        if "Bull" in tipo_spread:  
            with col1:  
                st.markdown("### 1. Compramos un CALL (La Seña)")
                st.caption("(Queremos el derecho a comprar)")
                strike_compra = st.number_input("Strike Comprado:", value=float(precio_actual))  
                prima_pagada = st.number_input("Prima Pagada (Nos cuesta):", value=round(precio_actual*0.06, 2))  
            with col2:  
                st.markdown("### 2. Vendemos un CALL (Sub-alquilamos)")
                st.caption("(Obligación de vender si sube mucho)")
                strike_venta = st.number_input("Strike Vendido (Más alto):", value=float(precio_actual*1.10))  
                prima_cobrada = st.number_input("Prima Cobrada (Nos entra plata):", value=round(precio_actual*0.02, 2))  
                  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(precios - strike_compra, 0) - prima_pagada) + (np.minimum(strike_venta - precios, 0) + prima_cobrada)
            
            st.info(f"""
            🐶 **Ejemplo del Profe:** Como **{ticker}** vale **USD {precio_actual}**, armamos esta estrategia alcista.
            - Pagás USD {prima_pagada} por un CALL base {strike_compra}, pero para que te salga más barato...
            - Vendés un CALL base {strike_venta} y cobrás USD {prima_cobrada}.
            - En total de tu bolsillo salen solo **USD {prima_pagada - prima_cobrada:.2f}** (Este es tu riesgo máximo absoluto).
            - **Tu objetivo:** Que {ticker} suba por encima de USD {strike_venta}, pero a partir de ahí ya no ganas más, tu ganancia está topeada.
            """)
        else:  
            with col1:  
                st.markdown("### 1. Compramos un PUT (El Seguro)")
                strike_compra = st.number_input("Strike Comprado:", value=float(precio_actual))  
                prima_pagada = st.number_input("Prima Pagada (Nos cuesta):", value=round(precio_actual*0.06, 2))  
            with col2:  
                st.markdown("### 2. Vendemos un PUT (Aseguramos a otro)")
                strike_venta = st.number_input("Strike Vendido (Más bajo):", value=float(precio_actual*0.90))  
                prima_cobrada = st.number_input("Prima Cobrada (Nos entra plata):", value=round(precio_actual*0.02, 2))  
                  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(strike_compra - precios, 0) - prima_pagada) + (np.minimum(precios - strike_venta, 0) + prima_cobrada)  
            
            st.info(f"""
            🐶 **Ejemplo del Profe:** Como **{ticker}** vale **USD {precio_actual}**, y creés que va a caer.
            - Pagás USD {prima_pagada} por un PUT base {strike_compra}.
            - Para abaratar, vendés un PUT base más bajo (USD {strike_venta}) y cobrás USD {prima_cobrada}.
            - Tu costo final es solo **USD {prima_pagada - prima_cobrada:.2f}** (Tu riesgo máximo).
            - **Tu objetivo:** Que la acción se desplome, pero ojo, tu ganancia máxima se frena si cae por debajo de USD {strike_venta}.
            """)

        fig = graficar_payoff(precios, payoff, precio_actual, f"{tipo_spread} sobre {ticker}", "Precio Futuro", "Tu Dinero (Payoff)")  
        st.pyplot(fig)  
  
# ==========================================
# CAPÍTULO 5: VOLATILIDAD
# ==========================================
elif capitulo == "5. Estrategias: Volatilidad (Conos y Cunas)":  
    st.title("Capítulo 5: Volatilidad Pura (¡Cuando el mercado se vuelve loco!)")  
    st.markdown("""
    **Profesor Firulais dice:** "Imaginate que mañana una empresa dice cuánto ganó en el año (Balance). Vos no sabés si la noticia será buena o mala, pero sabés que la acción **VA A EXPLOTAR** para algún lado. ¡Acá ganamos si se mueve rápido!"
    """)
    ticker = st.text_input("Ticker (Ej: META, TSLA):", "TSLA")  
    precio_actual = obtener_precio_actual(ticker)  
      
    if precio_actual:  
        st.success(f"🦴 Precio actual de **{ticker}**: **USD {precio_actual}**")  
        tipo_vol = st.radio("Estrategia para atrapar el movimiento:", ["Cono (Straddle) - Compro ambos en el MISMO strike", "Cuna (Strangle) - Compro separados, me sale más barato"])  
          
        st.divider()
        if "Cono" in tipo_vol:  
            st.markdown("### Cono: Misma Base")
            strike = st.number_input("Strike Único (El centro de la explosión):", value=float(precio_actual))  
            col1, col2 = st.columns(2)
            with col1:
                prima_c = st.number_input("Prima Call (Pagás por si sube):", value=round(precio_actual*0.05, 2))  
            with col2:
                prima_p = st.number_input("Prima Put (Pagás por si baja):", value=round(precio_actual*0.05, 2))  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(precios - strike, 0) - prima_c) + (np.maximum(strike - precios, 0) - prima_p)  
            
            st.warning(f"""
            🐶 **Ejemplo del Profe:** **{ticker}** está en **USD {precio_actual}**.  
            Estás comprando tanto el derecho a comprar (Call) como a vender (Put) al mismo precio (USD {strike}).
            Tu costo total es altísimo: **USD {prima_c + prima_p:.2f}**. 
            **Recomendación:** Solo hacé esto si creés que mañana sale una noticia enorme de {ticker} que va a hacer que el precio suba por encima de USD {strike + prima_c + prima_p:.2f} o baje por debajo de USD {strike - (prima_c + prima_p):.2f}. ¡Si se queda quieto, perdés todo!
            """)
        else:  
            st.markdown("### Cuna: Bases Separadas")
            col1, col2 = st.columns(2)  
            with col1:  
                strike_p = st.number_input("Strike PUT (Más bajo - Si cae):", value=float(precio_actual*0.95))  
                prima_p = st.number_input("Prima Put:", value=round(precio_actual*0.02, 2))  
            with col2:  
                strike_c = st.number_input("Strike CALL (Más alto - Si sube):", value=float(precio_actual*1.05))  
                prima_c = st.number_input("Prima Call:", value=round(precio_actual*0.02, 2))  
            precios = np.linspace(precio_actual * 0.7, precio_actual * 1.3, 200)  
            payoff = (np.maximum(precios - strike_c, 0) - prima_c) + (np.maximum(strike_p - precios, 0) - prima_p)  
            
            st.info(f"""
            🐶 **Ejemplo del Profe:** Para no gastar tanto, separamos las bases.  
            En vez de pagar una fortuna, pagás un total de **USD {prima_c + prima_p:.2f}**. 
            **Recomendación:** Es más barato, pero ahora **{ticker}** tiene que moverse mucho más fuerte para que empieces a ganar. Tiene que dispararse arriba de USD {strike_c} o desplomarse debajo de USD {strike_p}. Si el precio de {ticker} se queda en el medio (entre USD {strike_p} y USD {strike_c}), perdés la inversión.
            """)

        fig = graficar_payoff(precios, payoff, precio_actual, f"{tipo_vol[:15]} - {ticker}", "Precio Futuro", "Tu Dinero (Payoff)")  
        st.pyplot(fig)  
  
# ==========================================
# CAPÍTULO 6: ESTRATEGIAS AVANZADAS
# ==========================================
elif capitulo == "6. Estrategias Avanzadas (Mariposa y Túnel)":  
    st.title("Capítulo 6: Estrategias de Perro Viejo 🐶 (Mariposa y Túnel)")
    st.markdown("Ya dominás lo básico, vamos con jugadas de protección y sintonía fina.")
    ticker = st.text_input("Ticker (Ej: GGAL, YPF):", "YPF")  
    precio_actual = obtener_precio_actual(ticker)  
      
    if precio_actual:  
        st.success(f"🦴 Precio actual de **{ticker}**: **USD {precio_actual}**")  
        estrategia = st.radio("Elegir Estrategia:", ["Mariposa (Creo que NO se va a mover nada)", "Túnel / Collar (Tengo las acciones y las quiero proteger sin gastar tanto)"])  
          
        precios = np.linspace(precio_actual * 0.6, precio_actual * 1.4, 200)  
  
        st.divider()
        if "Mariposa" in estrategia:  
            st.markdown("### 🦋 La Mariposa")
            st.markdown("Acá apostamos a que la acción se va a quedar quietita. Para ganar, combinamos varias opciones para armar una 'carpa'.")  
            col1, col2, col3 = st.columns(3)  
            with col1:  
                s_bajo = st.number_input("Strike Bajo (Comprás 1):", value=float(precio_actual*0.9))  
                p_bajo = st.number_input("Prima Pagada 1:", value=round(precio_actual*0.08, 2))  
            with col2:  
                s_medio = st.number_input("Strike Medio (Vendés 2):", value=float(precio_actual))  
                p_medio = st.number_input("Prima Cobrada (x2):", value=round(precio_actual*0.03, 2))  
            with col3:  
                s_alto = st.number_input("Strike Alto (Comprás 1):", value=float(precio_actual*1.1))  
                p_alto = st.number_input("Prima Pagada 2:", value=round(precio_actual*0.01, 2))  
              
            payoff = (np.maximum(precios - s_bajo, 0) - p_bajo) + (2 * (np.minimum(s_medio - precios, 0) + p_medio)) + (np.maximum(precios - s_alto, 0) - p_alto)  
            
            st.info(f"""
            🐶 **Ejemplo del Profe:** Esta es mi favorita para mercados aburridos.  
            Si creés que **{ticker}** se va a quedar clavado en **USD {precio_actual}**, armás esta carpa. Al vender dos opciones en el medio, financiás la compra de las de las puntas.
            Tu riesgo está limitadísimo a la poca plata neta que pongas, ¡y ganás el premio mayor si el día de vencimiento la acción cierra justo en USD {s_medio}!
            """)
        else:  
            st.markdown("### 🛡️ El Túnel Protector (Collar)")
            st.markdown("**Profesor Firulais explica:** Ya tenés acciones en tu portafolio. Las querés asegurar contra una caída comprando un PUT (Seguro de auto). Pero como es caro, vendés un CALL (cediendo las ganancias locas si sube mucho) para que te financie el seguro. ¡Quedás atrapado en un túnel seguro!")  
            col1, col2 = st.columns(2)  
            with col1:  
                s_put = st.number_input("Strike PUT Comprado (El piso que querés):", value=float(precio_actual*0.90))  
                p_put = st.number_input("Costo del Seguro (Pagás):", value=round(precio_actual*0.03, 2))  
            with col2:  
                s_call = st.number_input("Strike CALL Vendido (El techo que cedés):", value=float(precio_actual*1.10))  
                p_call = st.number_input("Ingreso por Venta (Cobrás):", value=round(precio_actual*0.03, 2))  
              
            payoff_acciones = precios - precio_actual  
            payoff_put = np.maximum(s_put - precios, 0) - p_put  
            payoff_call = np.minimum(s_call - precios, 0) + p_call  
            payoff = payoff_acciones + payoff_put + payoff_call  
            
            st.success(f"""
            🐶 **Ejemplo del Profe:** ¡Jugada maestra de protección! 
            Vos tenés acciones de **{ticker}** compradas a **USD {precio_actual}**. 
            Si se viene una crisis, comprás un seguro (PUT) en USD {s_put}. Para no pagarlo de tu bolsillo, vendés un techo (CALL) en USD {s_call}.
            **Resultado:** No importa si hay un crash mundial, nunca venderás tus {ticker} por debajo de USD {s_put}. El único costo de esta seguridad total es que, si {ticker} sube a USD 200, te obligan a vender en USD {s_call} (ganás bien, pero cedés la suba infinita).
            """)

        fig = graficar_payoff(precios, payoff, precio_actual, f"{estrategia[:15]} - {ticker}", "Precio Futuro", "Tu Dinero Total (Payoff)")  
        st.pyplot(fig)
