import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from urllib.error import URLError

# Configuración de la página
st.set_page_config(
    page_title="Sección 2", 
    page_icon="❤️",
    layout="wide"
    )

# Establecer fondo de la página y estilos personalizados
st.markdown(
    """
    <style>
    body {
        margin: 0;
    }
    .block-container {
        background-color: transparent;
    }
    .sidebar .sidebar-content {
        background-color: transparent;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 10px;
        background-color: #FFFFFF;
        width: 100%;
    }
    .header img {
        width: 120px;
        height: 40px;
        top: 15.83px;
        left: 81px;
        gap: 12px;
        opacity: 1;
        transform: rotate(0deg);
        margin-right: 0px;
    }
    .header .line {
        width: 32.6px;
        height: 0px;
        border: 0.91px solid #000000;
        top: 16px;
        left: 155px;
        opacity: 1;
        transform: rotate(-90deg);
        margin-right: 0px;
    }
    .header .title {
        font-family: 'Inter', sans-serif;
        font-size: 13.94px;
        font-weight: 400;
        line-height: 17.42px;
        text-align: left;
        text-underline-position: from-font;
        text-decoration-skip-ink: none;
    }
    .filter-container {
        background-color: transparent;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .filter-title {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
    <div class="header">
        <img src="https://i.postimg.cc/y8FYQLdJ/Hyppo-sin-fondo.png" alt="Hyppo Logo">
        <div class="line"></div>
        <div class="title">Let's Size Up</div>
    </div>
    """, unsafe_allow_html=True
)

# Descripción
st.markdown("# Sección 2")
st.write(
    """Estrategia de marketing."""
)

@st.cache_data
def load_data():
    try:
        # Cargar datasets desde archivos CSV
        # Campañas de envíos automatizados de comunicaciones que tuvo prendida 
        # el cliente durante Q3 2024 con un detalle de los envíos realizados

        df_BD_campaigns_Q3 = pd.read_csv('pages/bd_campaigns_q3 - bq-results-20241024-214424-1729806389970.csv')

        # Transacciones del período 2023 y 2024 hasta octubre
        df_bd_orders = pd.read_csv('pages/bd_orders - bq-results-20241024-134337-1729777484801.csv')
        
        # Convertir la columna de fechas a datetime
        df_bd_orders['order_date_formatted'] = pd.to_datetime(df_bd_orders['order_date_formatted'], errors='coerce')
        
        # Base de datos de descargas de la app desde Diciembre 2022 en adelante
        df_BD_signups = pd.read_csv('pages/BD_signups - results-20241024-105624.csv')
        
        # Convertir la columna de fechas a datetime
        df_BD_signups['fecha_registro_formatted'] = pd.to_datetime(df_BD_signups['fecha_registro_formatted'], errors='coerce')

        return df_BD_campaigns_Q3, df_bd_orders, df_BD_signups
    
    except FileNotFoundError as e:
        st.error(f"No se encontró el archivo: {e.filename}")
        return pd.DataFrame()

try:
    df_BD_campaigns_Q3, df_bd_orders, df_BD_signups= load_data()
    
    # st.title("Visualización del dataframe")
    # st.dataframe(df_BD_campaigns_Q3)

    # first_year = df_bd_orders["order_date_formatted"].min()
    # last_year = df_bd_orders["order_date_formatted"].max()

    # col1, col2 = st.columns([1, 3.8])

    # with col1:
        # def create_multiselect_filter(df, column_name, filter_label, dependent_values=None, dependent_column=None):
        #     """
        #     Crea un filtro multiselect con soporte para valores dependientes.
        #     """
        #     # Filtrar las opciones si hay un valor dependiente
        #     if dependent_values is not None and dependent_column is not None:
        #         filtered_df = df[df[dependent_column].isin(dependent_values)]
        #         column_options = filtered_df[column_name].unique()
        #     else:
        #         column_options = df[column_name].unique()
            
            
        #     # Agregar la opción "Todos" al inicio
        #     column_options_with_all = ["Todos"] + list(column_options)
        #     selected_values = st.multiselect(
        #         label=filter_label,
        #         options=column_options_with_all,
        #         default=column_options_with_all[0]
        #     )
        #     if "Todos" in selected_values:
        #         return column_options
        #     else:
        #         return selected_values

        # # with st.container(height=450):
        # st.markdown('<h1 style="font-size: 30px; font-weight: bold; text-align:left;">Filtros</h1>', unsafe_allow_html=True)
        
        # # st.markdown('<div class="filter-title">Geographic</div>', unsafe_allow_html=True)
        # start_date, end_date = st.date_input("Order date", [first_year, last_year])
        # selected_channel = create_multiselect_filter(df_bd_orders, "channel", "Channel")
        # selected_category = create_multiselect_filter(df_bd_orders, "categoria", "Categoria")
        # selected_tipo_orden = create_multiselect_filter(df_bd_orders, "tipo_orden", "Tipo orden") 
        # selected_campaign_name = create_multiselect_filter(df_BD_campaigns_Q3, "campaign_name", "Nombre de campaña")   
        # selected_metric = create_multiselect_filter(df_BD_campaigns_Q3, "metric", "Métrica")
        
        # # Muestro solamene la opciones disponibles para subject según el campaing_name que elijo
        # selected_subject = create_multiselect_filter(
        #     df=df_BD_campaigns_Q3, 
        #     column_name="subject", 
        #     filter_label="Subject",
        #     dependent_values=selected_campaign_name,
        #     dependent_column="campaign_name"
        # )
    
    # with col2: 
    # Cuentas por campaña
    st.header("Tasa de conversión de campañas y Tasa de clics (Clicks-Through Rate)")
    # Filtrar las métricas necesarias
    metrics_to_count = ['delivered', 'opened', 'clicked']

    # Crear una tabla con las cantidades agrupadas
    grouped_campaigns = df_BD_campaigns_Q3[df_BD_campaigns_Q3['metric'].isin(metrics_to_count)].groupby(
        ['campaign_name', 'metric']
    )['metric'].count().unstack(fill_value=0).reset_index()

    # Asegurar que las columnas estén en el orden correcto
    grouped_campaigns = grouped_campaigns.rename_axis(None, axis=1)
    grouped_campaigns.columns.name = None

    # Calcular métricas
    grouped_campaigns['Conversion rate (%)'] = (grouped_campaigns['opened'] /(grouped_campaigns['opened'] + grouped_campaigns['delivered'])) * 100
    grouped_campaigns['CTR (%)'] = (grouped_campaigns['clicked'] / (grouped_campaigns['clicked'] + grouped_campaigns['opened'] + grouped_campaigns['delivered'])) * 100

    # Redondear métricas para mayor claridad
    grouped_campaigns['Conversion rate (%)'] = grouped_campaigns['Conversion rate (%)'].round(2)
    grouped_campaigns['CTR (%)'] = grouped_campaigns['CTR (%)'].round(2)

    # Mostrar el DataFrame resultante en Streamlit
    st.dataframe(grouped_campaigns)
    
# Tasa de rebote
    st.header("Tasa de rebote (Bounce Rate)")
    # Normalizar las fechas
    df_BD_campaigns_Q3['created_at'] = pd.to_datetime(df_BD_campaigns_Q3['created_at']).dt.date
    df_BD_signups['fecha_registro_formatted'] = pd.to_datetime(df_BD_signups['fecha_registro_formatted']).dt.date

    # Obtener los usuarios registrados y las campañas
    df_signups = df_BD_signups[['customer_id', 'fecha_registro_formatted']].copy()
    df_campaigns = df_BD_campaigns_Q3[['campaign_name', 'customer_id', 'created_at']].copy()

    # Agrupar usuarios registrados por campaña
    usuarios_registrados_por_campaña = df_campaigns.groupby('campaign_name')['customer_id'].unique().reset_index()
    usuarios_registrados_por_campaña = usuarios_registrados_por_campaña.rename(columns={'customer_id': 'usuarios_enviados'})

    # Unir campañas con usuarios registrados
    usuarios_registrados_por_campaña['usuarios_registrados'] = usuarios_registrados_por_campaña['campaign_name'].apply(
        lambda campaña: df_signups['customer_id'].unique()
    )

    # Calcular usuarios rebotados por campaña
    usuarios_registrados_por_campaña['Usuarios Rebotados'] = usuarios_registrados_por_campaña.apply(
        lambda row: len(set(row['usuarios_registrados']) - set(row['usuarios_enviados'])),
        axis=1
    )

    # Calcular métricas por campaña
    usuarios_registrados_por_campaña['Total Registrados'] = usuarios_registrados_por_campaña['usuarios_registrados'].apply(len)
    usuarios_registrados_por_campaña['Bounce Rate'] = (
        (usuarios_registrados_por_campaña['Usuarios Rebotados'] / usuarios_registrados_por_campaña['Total Registrados']) * 100
    ).round(2)

    # Seleccionar columnas relevantes para mostrar
    resultados_bounce_rate = usuarios_registrados_por_campaña[['campaign_name', 'Total Registrados', 'Usuarios Rebotados', 'Bounce Rate']]

    # Mostrar resultados en Streamlit
    st.dataframe(resultados_bounce_rate)

# Proemdio de compras
    st.header("Promedio de compras")

    # Filtrar las campañas donde el metric es 'clicked'
    df_campaigns_clicked = df_BD_campaigns_Q3[df_BD_campaigns_Q3['metric'] == 'clicked']

    # Convertir las fechas a formato datetime para realizar comparaciones
    df_campaigns_clicked['created_at'] = pd.to_datetime(df_campaigns_clicked['created_at'])
    df_bd_orders['order_date_formatted'] = pd.to_datetime(df_bd_orders['order_date_formatted'])

    # Hacer el join entre las campañas y las órdenes, considerando que el cliente hizo una compra después de hacer clic en la campaña
    df_joined = pd.merge(df_campaigns_clicked, df_bd_orders, on='customer_id')

    # Filtrar solo las compras que ocurrieron después de que el cliente clickeó la campaña
    df_filtered = df_joined[df_joined['order_date_formatted'] > df_joined['created_at']]

    # Contar cuántas compras realizó cada usuario por campaña
    df_user_purchases = df_filtered.groupby(['campaign_name', 'customer_id']).size().reset_index(name='Promedio de Compras')

    # Calcular el promedio de compras por usuario por campaña
    df_average_purchases = df_user_purchases.groupby('campaign_name')['Promedio de Compras'].mean().reset_index()

    # Mostrar el DataFrame resultante con el promedio de compras por campaña
    st.dataframe(df_average_purchases)
    
# Ganancia promedio
    st.header("Valor promedio")

    # Filtrar las campañas donde el metric es 'clicked'
    df_campaigns_clicked = df_BD_campaigns_Q3[df_BD_campaigns_Q3['metric'] == 'clicked']

    # Convertir las fechas a formato datetime para realizar comparaciones
    df_campaigns_clicked['created_at'] = pd.to_datetime(df_campaigns_clicked['created_at'])
    df_bd_orders['order_date_formatted'] = pd.to_datetime(df_bd_orders['order_date_formatted'])

    # Hacer el join entre las campañas y las órdenes, considerando que el cliente hizo una compra después de hacer clic en la campaña
    df_joined = pd.merge(df_campaigns_clicked, df_bd_orders, on='customer_id')

    # Filtrar solo las compras que ocurrieron después de que el cliente clickeó la campaña
    df_filtered = df_joined[df_joined['order_date_formatted'] > df_joined['created_at']]

    # Sumar el total_value de cada compra por usuario y campaña
    df_user_value = df_filtered.groupby(['campaign_name', 'customer_id'])['total_value'].sum().reset_index(name='Valor Promedio')

    # Calcular el promedio de total_value por usuario por campaña
    df_average_value = df_user_value.groupby('campaign_name')['Valor Promedio'].mean().reset_index()

    # Mostrar el DataFrame resultante con el promedio de total_value por campaña
    st.dataframe(df_average_value)

# Desempeño por tipo de usuario
    st.header("Desempeño por tipo de usuario (Tasas de Recompra y Activación por campaña)")

    # Filtrar las campañas donde el metric es 'clicked'
    df_campaigns_clicked = df_BD_campaigns_Q3[df_BD_campaigns_Q3['metric'] == 'clicked']

    # Convertir las fechas a formato datetime para realizar comparaciones
    df_campaigns_clicked['created_at'] = pd.to_datetime(df_campaigns_clicked['created_at'])
    df_bd_orders['order_date_formatted'] = pd.to_datetime(df_bd_orders['order_date_formatted'])

    # Hacer el join entre las campañas y las órdenes, considerando que el cliente hizo una compra después de hacer clic en la campaña
    df_joined = pd.merge(df_campaigns_clicked, df_bd_orders, on='customer_id')

    # Filtrar solo las compras que ocurrieron después de que el cliente clickeó la campaña
    df_filtered = df_joined[df_joined['order_date_formatted'] > df_joined['created_at']]

    # **Tasa de Recompra**:
    # Agrupar por campaña y cliente, y contar las compras posteriores
    df_recompra = df_filtered.groupby(['campaign_name', 'customer_id'])['order_date_formatted'].count().reset_index(name='compras_totales')

    # Filtrar usuarios que hicieron más de una compra
    df_recompra = df_recompra[df_recompra['compras_totales'] > 1]

    # Calcular la tasa de recompra (usuarios que compraron más de una vez / usuarios totales)
    df_recompra_rate = df_recompra.groupby('campaign_name')['compras_totales'].count().reset_index(name='usuarios_recompra')
    df_total_users = df_filtered.groupby('campaign_name')['customer_id'].nunique().reset_index(name='usuarios_totales')

    df_recompra_rate = pd.merge(df_recompra_rate, df_total_users, on='campaign_name')
    df_recompra_rate['Tasa_Recompra'] = (df_recompra_rate['usuarios_recompra'] / df_recompra_rate['usuarios_totales']) * 100

    # **Tasa de Activación**:
    # Para calcular la tasa de activación, identificamos a los usuarios que compraron por primera vez debido a la campaña
    df_first_purchase = df_filtered.groupby('customer_id')['order_date_formatted'].min().reset_index(name='first_purchase')
    df_first_purchase = pd.merge(df_filtered, df_first_purchase, on='customer_id')

    # Filtrar para los usuarios cuya primera compra fue después de la campaña (usuarios nuevos activados)
    df_new_users = df_first_purchase[df_first_purchase['first_purchase'] == df_first_purchase['order_date_formatted']]

    # Calcular la tasa de activación (usuarios nuevos que realizaron compras debido a la campaña)
    df_activation_rate = df_new_users.groupby('campaign_name')['customer_id'].nunique().reset_index(name='usuarios_activados')
    df_campaigns_count = df_campaigns_clicked.groupby('campaign_name')['customer_id'].nunique().reset_index(name='usuarios_totales_campaña')

    df_activation_rate = pd.merge(df_activation_rate, df_campaigns_count, on='campaign_name')
    df_activation_rate['Tasa_Activacion'] = (df_activation_rate['usuarios_activados'] / df_activation_rate['usuarios_totales_campaña']) * 100

    # **Unir resultados en un solo DataFrame**:
    df_result = pd.merge(df_recompra_rate[['campaign_name', 'Tasa_Recompra']], df_activation_rate[['campaign_name', 'Tasa_Activacion']], on='campaign_name', how='outer')

    # Mostrar el DataFrame resultante
    st.dataframe(df_result)

# Cantidad por campaña y métrica
    st.header("Agrupación por campaña y métrica")
    grouped_data = df_BD_campaigns_Q3.groupby(['campaign_name', 'metric']).size().reset_index(name='count')
    # Mostrar el resultado
    st.dataframe(grouped_data)
    
    # st.write("Visualización: Conteo por Campaign Name y Metric")
    # bar_chart = alt.Chart(grouped_data).mark_bar().encode(
    #     x=alt.X('campaign_name:N', title='Campaign Name', sort='-y'),  # Campañas en el eje X
    #     y=alt.Y('count:Q', title='Conteo'),  # Conteo en el eje Y
    #     color='metric:N',  # Diferenciar por color las métricas
    #     column='metric:N',  # Crear columnas separadas por métrica
    #     tooltip=['campaign_name', 'metric', 'count']  # Información al pasar el mouse
    # ).properties(
    #     width=200,  # Ancho de cada gráfico por métrica
    #     height=400,  # Altura del gráfico
    #     title='Conteo por Campaign Name y Metric'
    # )

    # # Mostrar el gráfico en Streamlit
    # st.altair_chart(bar_chart, use_container_width=True)
    
except URLError as e:
    st.error(
        f"**This demo requires internet access.**\nConnection error: {e.reason}"
    )