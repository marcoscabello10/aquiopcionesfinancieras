# Simulador Interactivo de Opciones Financieras

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)

Un simulador web interactivo construido con Streamlit para explicar de manera sencilla, "A Prueba de Boludos" (APB), cómo funcionan las opciones financieras. Ideal para asesores financieros que buscan educar a sus clientes utilizando analogías de la vida real.

## 🚀 Características

*   **Tono "APB"**: Explicaciones sin jerga técnica, utilizando analogías comprensibles (ej. "señar un departamento" para los CALLs, "seguro del auto" para los PUTs).
*   **Datos en Tiempo Real**: Integración con `yfinance` para obtener los precios reales de las acciones al momento de la simulación.
*   **Gráficos Interactivos**: Gráficos de ganancias y pérdidas (Payoffs) generados con `matplotlib`, mostrando zonas de ganancia en verde y pérdidas en rojo.
*   **Múltiples Estrategias**:
    *   Compra/Venta simple (Calls y Puts)
    *   Spreads (Bull Call Spread, Bear Put Spread)
    *   Volatilidad (Conos y Cunas)
    *   Estrategias Avanzadas (Mariposas y Túneles)

## 🛠️ Instalación Local

Si deseas ejecutar este proyecto en tu propia computadora, sigue estos pasos:

1.  Clona este repositorio o descarga los archivos.
2.  (Opcional pero recomendado) Crea un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate # En Windows usa: venv\Scripts\activate
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Ejecuta la aplicación:
    ```bash
    streamlit run app.py
    ```

## 🌐 Despliegue (Hosting Gratuito)

Este proyecto está diseñado para ser desplegado de forma gratuita utilizando **Streamlit Community Cloud**. 
Simplemente sube este repositorio a tu cuenta de GitHub, dirígete a [share.streamlit.io](https://share.streamlit.io/), y enlaza el repositorio. ¡Tu aplicación estará en vivo en minutos!

## 📚 Librerías Utilizadas

*   [Streamlit](https://streamlit.io/) - Para la interfaz web interactiva.
*   [Matplotlib](https://matplotlib.org/) - Para la visualización de los gráficos de payoff.
*   [yfinance](https://pypi.org/project/yfinance/) - Para la descarga de datos de mercado de Yahoo Finance.
*   [NumPy](https://numpy.org/) - Para cálculos matemáticos y vectores.
