import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from urllib.error import URLError

# Configuración de la página
st.set_page_config(
    page_title="Sección 1", 
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
st.markdown("# Sección 1")
st.write(
    """El negocio y el ciclo de vida del cliente."""
)

@st.cache_data
def load_data():
    try:
        # Cargar datasets desde archivos CSV
        # Transacciones del período 2023 y 2024 hasta octubre
        df_bd_orders = pd.read_csv('pages/bd_orders - bq-results-20241024-134337-1729777484801.csv')

        # Convertir la columna de fechas a datetime
        df_bd_orders['order_date_formatted'] = pd.to_datetime(df_bd_orders['order_date_formatted'], errors='coerce')
        
        # Base de datos de descargas de la app desde Diciembre 2022 en adelante
        df_BD_signups = pd.read_csv('pages/BD_signups - results-20241024-105624.csv')
        
        # Convertir la columna de fechas a datetime
        df_BD_signups['fecha_registro_formatted'] = pd.to_datetime(df_BD_signups['fecha_registro_formatted'], errors='coerce')

        return df_bd_orders, df_BD_signups
    
    except FileNotFoundError as e:
        st.error(f"No se encontró el archivo: {e.filename}")
        return pd.DataFrame()

try:
    df_bd_orders, df_BD_signups = load_data()

    first_year = df_bd_orders["order_date_formatted"].min()
    last_year = df_bd_orders["order_date_formatted"].max()

    col1, col2 = st.columns([1, 3.8])

    with col1:
        def create_multiselect_filter(df, column_name, filter_label):
            column_options = df[column_name].unique()
            # Agregar la opción "Todos" al inicio
            column_options_with_all = ["Todos"] + list(column_options)
            selected_values = st.multiselect(
                label=filter_label,
                options=column_options_with_all,
                default=column_options_with_all[0]
            )
            if "Todos" in selected_values:
                return column_options
            else:
                return selected_values


        st.markdown('<h1 style="font-size: 30px; font-weight: bold; text-align:left;">Filtros</h1>', unsafe_allow_html=True)

        start_date, end_date = st.date_input("Order date", [first_year,last_year])
        selected_channel = create_multiselect_filter(df_bd_orders, "channel", "Channel")
        selected_category = create_multiselect_filter(df_bd_orders, "categoria", "Categoria")
        selected_tipo_orden = create_multiselect_filter(df_bd_orders, "tipo_orden", "Tipo orden")   
  
    with col2: 
           
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
            
        if start_date == first_year and end_date == last_year:
            data = df_bd_orders # Mostrar todos los datos
        else:
            # Filtrar los datos por el rango de fechas seleccionado
            data = df_bd_orders[(df_bd_orders["order_date_formatted"] >= start_date) & (df_bd_orders["order_date_formatted"] <= end_date)]
            
        filtered_data_orders = data[
                (data["channel"].isin(selected_channel)) &
                (data["categoria"].isin(selected_category)) &
                (data["tipo_orden"].isin(selected_tipo_orden)) 
            ]

        if filtered_data_orders.empty:
            st.warning("No data available for the selected date range. Showing all available data instead.")
        else:
            if "order_date_formatted" in filtered_data_orders.columns:
                
                def crear_grafico_metrica(data, columna_metrica, nombre_metrica, color_linea,
                                          columna_metrica2=None, nombre_metrica2=None, color_linea2=None, 
                                          columna_metrica3=None, nombre_metrica3=None, color_linea3=None
                                          ):
                    """
                    Función para crear un gráfico de línea para una métrica específica.
                    
                    Parameters:
                    - data: dataframe con los datos.
                    - columna_metrica: nombre de la columna de la métrica que quieres graficar.
                    - nombre_metrica: nombre que se mostrará en el gráfico y la leyenda.
                    - color_linea: color que se usará para la línea del gráfico.
                    - columna_metrica2 (opcional): nombre de la segunda columna de la métrica.
                    - nombre_metrica2 (opcional): nombre para la leyenda de la segunda métrica.
                    - color_linea2 (opcional): color para la segunda línea.
                    - columna_metrica3 (opcional): nombre de la tercera columna de la métrica.
                    - nombre_metrica3 (opcional): nombre para la leyenda de la tercera métrica.
                    - color_linea3 (opcional): color para la tercera línea.
                    
                    Returns:
                    - Un gráfico de línea de Altair.
                    """
                    
                    # Crear lista para las columnas y nombres
                    columnas_metrica = [columna_metrica, columna_metrica2, columna_metrica3]
                    nombres_metrica = [nombre_metrica, nombre_metrica2, nombre_metrica3]
                    colores_linea = [color_linea, color_linea2, color_linea3]
                    
                    # Filtrar las métricas que no son None
                    columnas_metrica = [col for col in columnas_metrica if col is not None]
                    nombres_metrica = [nom for nom in nombres_metrica if nom is not None]
                    colores_linea = [color for color in colores_linea if color is not None]
                    
                    # Preparar los datos en formato largo para graficar
                    agg_data_long = data.melt(id_vars=['order_date_formatted'], 
                                            value_vars=[columna_metrica], 
                                            var_name='Variable', 
                                            value_name='Valor')
                    
                    # Reemplazar los nombres de las variables con los nombres proporcionados
                    for i, col in enumerate(columnas_metrica):
                        agg_data_long['Variable'] = agg_data_long['Variable'].replace({col: nombres_metrica[i]})
                    
                    selection = alt.selection_multi(fields=['Variable'], bind='legend')
                    
                    agg_data_long['Variable'] = agg_data_long['Variable'].replace({
                        columna_metrica: nombre_metrica
                    })
                    
                    chart = (
                        alt.Chart(agg_data_long)
                        .mark_line(color=color_linea)
                        .encode(
                            x=alt.X("order_date_formatted:T", title="Order date"),
                            y=alt.Y("Valor:Q"),
                            # color=alt.Color('Variable:N', 
                            #                 scale=alt.Scale(domain=nombres_metrica, range=colores_linea), 
                            #                 title='Métricas'),
                            tooltip=[
                                alt.Tooltip("order_date_formatted:T", title='Order date'),
                                alt.Tooltip("Valor:Q", format=',.2f'),
                                "Variable:N"
                            ],
                            opacity=alt.condition(selection, alt.value(1), alt.value(0)) 
                        )
                        .add_selection(selection)
                    )
                    
                    return chart
                
                # Cálculos de métricas generales con los datos filtrados
                ingresos_totales = filtered_data_orders['total_value'].sum()
                ordenes_totales = filtered_data_orders['order_id'].nunique()
                aov = ingresos_totales / ordenes_totales
                tasa_cumplimiento_sku = (filtered_data_orders['skus_entregados'].sum() / filtered_data_orders['skus_pedidos'].sum()) * 100
                tasa_cumplimiento_item = (filtered_data_orders['items_entregados'].sum() / filtered_data_orders['items_pedidos'].sum()) * 100

                st.header("Performance general del negocio")
                # Crear tabs para KPIs y visualizaciones
                KPIs, visualziaciones = st.tabs([
                    "KPIs", 
                    "Comportamiento en el tiempo"
                    ])
                
                with KPIs:
                    # Contenedor: Métricas generales
                    with st.container():
                        col1, col2, col3 = st.columns([1.2, 1, 1])
                        col1.metric("Ingresos Totales", f"${ingresos_totales:,.2f}", 
                                    help="Suma del valor total de las órdenes.")
                        col2.metric("Órdenes Totales", f"{ordenes_totales:,.0f}", 
                                    help="Cantidad de órdenes totales.")
                        col3.metric("AOV (Average Order Value)", f"${aov:,.2f}", 
                                    help="Ingresos Totales / Órdenes Totales.")
                        
                        col1, col2, col3 = st.columns([1.2, 1, 1])
                        col1.metric("Tasa de Cumplimiento por SKU", f"{tasa_cumplimiento_sku:.2f}%", 
                                help="(Skus Entregados / Skus Pedidos) * 100.")
                        col2.metric("Tasa de Cumplimiento por Item", f"{tasa_cumplimiento_item:.2f}%", 
                                help="(Items Entregados / Items Pedidos) * 100.")

                with visualziaciones:
                    # Crear tabs para cada métrica
                    ingresos_totales, ordenes_totales, aov, tasa_sku, tasa_item = st.tabs([
                        "Ingresos Totales", 
                        "Órdenes Totales", 
                        "AOV (Average Order Value)",
                        "Tasa de Cuplimiento por SKU",
                        "Tasa de Cumplimiento pot Item"
                        ])
                        
                    # Grafico cada métrica a lo largo del tiempo
                    agg_data_metrics = (
                        filtered_data_orders.groupby("order_date_formatted", as_index=False)
                        .agg({
                            "total_value": "sum",  # Ingresos totales
                            "order_id": "nunique",  # Órdenes totales
                            "skus_entregados": "sum",
                            "skus_pedidos": "sum",
                            "items_pedidos": "sum",
                            "items_entregados": "sum"
                        })
                    )

                    # Renombrar columnas para mayor claridad
                    agg_data_metrics.rename(columns={
                        "total_value": "ingresos_totales", 
                        "order_id": "ordenes_totales"}, 
                    inplace=True)

                    # Calcular AOV (Average Order Value) como ingresos totales / órdenes totales
                    agg_data_metrics["AOV"] = agg_data_metrics["ingresos_totales"] / agg_data_metrics["ordenes_totales"]
                
                    # Calcular la tasa de cumplimiento por SKU 
                    agg_data_metrics["Tasa_sku"] = (agg_data_metrics['skus_entregados'] / agg_data_metrics['skus_pedidos']) * 100
                    
                    # Calcular la tasa de cumplimiento por Item 
                    agg_data_metrics["Tasa_item"] = (agg_data_metrics['items_entregados'] / agg_data_metrics['items_pedidos']) * 100
                
                    # Graficar en cada tab
                    with ingresos_totales:
                        st.altair_chart(crear_grafico_metrica(
                            agg_data_metrics, 
                            "ingresos_totales", 
                            "Ingresos Totales",
                            "#60B7AC"
                            ), use_container_width=True)

                    with ordenes_totales:
                        st.altair_chart(crear_grafico_metrica(
                            agg_data_metrics, 
                            "ordenes_totales", 
                            "Órdenes Totales",
                            "pink"
                            ), use_container_width=True)

                    with aov:
                        st.altair_chart(crear_grafico_metrica(
                            agg_data_metrics, 
                            "AOV", 
                            "Average Order Value",
                            "blue"
                            ), use_container_width=True)

                    with tasa_sku:
                        st.altair_chart(crear_grafico_metrica(
                            agg_data_metrics, 
                            "Tasa_sku", 
                            "Tasa de Cumplimiento por SKU",
                            "#8A2BE2",
                            ), use_container_width=True)

                    with tasa_item:
                        st.altair_chart(crear_grafico_metrica(
                            agg_data_metrics, 
                            "Tasa_item", 
                            "Tasa de Cumplimiento por Item",
                            "green"
                            ), use_container_width=True)

                # Métricas por cliente
                # Filtrar los customer_id en filtered_data_orders que están en df_BD_signups
                filtered_data_orders_registered  = filtered_data_orders[filtered_data_orders['customer_id'].isin(df_BD_signups['customer_id'])]
                
                # Tendría que pone acá de los customer_id que se encuentran en el filtro cuáles de los totales 
                # que se registraron ahi (para que no me de mayor al 100%)
                tasa_conversion = (filtered_data_orders_registered ['customer_id'].nunique() / df_BD_signups['customer_id'].nunique()) * 100
                ltv_por_cliente = filtered_data_orders.groupby('customer_id')['total_value'].sum().mean()
                frecuencia_compra_periodo = filtered_data_orders.groupby('customer_id')['order_id'].count().mean()

                # Métricas de retención
                clientes_retenidos = filtered_data_orders.groupby('customer_id')['order_id'].count().loc[lambda x: x > 1].count()
                tasa_retencion = (clientes_retenidos / filtered_data_orders['customer_id'].nunique()) * 100
                tasa_churn = 100 - tasa_retencion

                st.header("Performance a nivel cliente")                    
                KPIs, visualziaciones = st.tabs([
                    "KPIs", 
                    "Distribución de KPIs"
                    ])
                
                with KPIs:
                    # Contenedor: Métricas por cliente
                    with st.container():

                        col1, col2, col3 = st.columns([1.2, 1, 1])
                        col1.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%", 
                                    help="(Número de clientes únicos con ordenes / Número de registros únicos) * 100.")
                        col2.metric("Lifetime Value Promedio", f"${ltv_por_cliente:,.2f}", 
                                    help="Promedio del valor total por cliente.")
                        col3.metric("Frecuencia de compra Promedio", f"{frecuencia_compra_periodo:,.0f}", 
                                    help="Promedio de la frencuencia de compra por cliente en un periodo dado.")                    
                        
                        col1, col2, col3 = st.columns([1.2, 1, 1])
                        col1.metric("Tasa de Retención", f"{tasa_retencion:.2f}%", 
                                help="(Clientes que realizaron más de 1 orden / Total de clientes únicos) * 100.")
                        col2.metric("Tasa de Churn", f"{tasa_churn:.2f}%", 
                                help="100 - Tasa de Retención.")
    
                # Histogrma de frecuencia de compra.
                frecuencia_compra_cliente = filtered_data_orders.groupby('customer_id')['order_id'].count().reset_index()
                # Renombrar la columna para mayor claridad
                frecuencia_compra_cliente.rename(columns={'order_id': 'frecuencia_compra'}, inplace=True)
                
                # st.dataframe(frecuencia_compra_cliente.sort_values(by='frecuencia_compra', ascending=False))
                
                with visualziaciones:
                    histogram_frecuencia= (
                        alt.Chart(frecuencia_compra_cliente)
                        .mark_bar()
                        .encode(
                            x=alt.X('frecuencia_compra:Q', bin=alt.Bin(maxbins=40), title='Frecuencia de Compra (número de compras)'),
                            y=alt.Y('count()', title='Número de clientes'),
                            tooltip=['frecuencia_compra:Q', 'count():Q']
                        )
                        .properties(
                            width=600,
                            height=280,
                            title='Distribución de la Frecuencia de Compra por Cliente'
                        )
                    )
                    
                    # Mostrar el gráfico en Streamlit
                    st.altair_chart(histogram_frecuencia, use_container_width=True)  
                
                 
                # Hago a la agregación por valor para armar el gráfico
                agg_data = (
                    filtered_data_orders.groupby("order_date_formatted", as_index=False)
                    .agg({"skus_pedidos": "sum", "skus_entregados": "sum", "items_pedidos": "sum", "items_entregados": "sum"})
                )
            
                melted_df = pd.melt(agg_data, id_vars=["order_date_formatted"], 
                                value_vars=["skus_pedidos", "skus_entregados", "items_pedidos", "items_entregados"], 
                                var_name="Variable", value_name="Valor"
                )
                
                selection = alt.selection_multi(fields=['Variable'], bind='legend')

                melted_df['Variable'] = melted_df['Variable'].replace({
                    'skus_pedidos': 'SKUs Pedidos',  
                    'skus_entregados': 'SKUs Entregados',
                    'items_pedidos': 'Items Pedidos',
                    'items_entregados': 'Items Entregados'
                })

                chart = (
                    alt.Chart(melted_df)
                    .mark_line()
                    .encode(
                        x=alt.X("order_date_formatted:T", title="Order date"),
                        y=alt.Y("Valor:Q"),
                        color=alt.Color('Variable:N', title='Variable', legend=alt.Legend(
                                                orient='bottom',
                                                title=None,
                                                direction='horizontal',
                                                legendX=0,
                                                legendY=0
                                            )
                                        ),
                        tooltip=[
                            alt.Tooltip("order_date_formatted:T", title='Order date'),
                            alt.Tooltip("Valor:Q", format=',.2f'),
                            "Variable:N"],
                        opacity=alt.condition(selection, alt.value(1), alt.value(0)) 
                    )
                    .add_selection(selection)
                )

                # Visualización del gráfico
                # st.altair_chart(chart, use_container_width=True)
    
    st.header("Ciclo de Vida de los clientes")
    st.markdown("#### Activación (antes de primera compra)")
    
    # Filtrar los customer_id en filtered_data_orders que están en df_BD_signups (necesito que al menos esten registrados)
    # Con esto si por ejemplo los que hicieron pedidos son A, B, E y los que se encuentran registrados son A, B, C; 
    # me va filtrar A, B; C sería un id que se registró pero que no hizo ninguna orden en ese periodo. 
    filtered_data_orders_registered  = filtered_data_orders[filtered_data_orders['customer_id'].isin(df_BD_signups['customer_id'])]
    
    # Filtrar los customer_id registrados pero que no hicieron un pedido.
    # Con el ejemplo anterior me quedaría solo C. 
    registrados_sin_pedido = df_BD_signups[~df_BD_signups['customer_id'].isin(filtered_data_orders_registered['customer_id'])]
    
    # Número de clientes registrados que no hicieron pedido
    numero_registrados_sin_pedido = registrados_sin_pedido['customer_id'].nunique()

    # Total de clientes registrados
    total_registrados = df_BD_signups['customer_id'].nunique()

    # Es 1-Tasa Activación
    # Proporción de clientes registrados que no realizaron pedidos
    porcentaje_sin_pedido = (numero_registrados_sin_pedido / total_registrados) * 100
    
    # Acá tengo que pensar en los id que estan en registros pero que no estan en singups. 
    # Tasa de conversión es lo mismo que tasa de activación. Lo podría pensar en un cierto periodo de tiempo. 
    tasa_activacion = (filtered_data_orders_registered ['customer_id'].nunique() / df_BD_signups['customer_id'].nunique()) * 100
    
    # Tiempo hasta la priemra compra (TTFP). 
    # Encontrar la primera compra de cada cliente (mínima fecha de compra) de los que estan registrados.
    first_purchase_date = filtered_data_orders_registered.groupby('customer_id')['order_date_formatted'].min().reset_index()
    first_purchase_date.rename(columns={'order_date_formatted': 'first_purchase_date'}, inplace=True)

    # Unir el DataFrame original con la fecha de la primera compra
    df_complete = pd.merge(df_BD_signups, first_purchase_date, on='customer_id', how='left')

    # Calcular el tiempo hasta la primera compra (en días)
    df_complete['time_to_first_purchase'] = (df_complete['first_purchase_date'] - df_complete['fecha_registro_formatted']).dt.days

    # Obtener el tiempo hasta la primera compra para cada cliente 
    # Porque algunos cliente spudieron no haber hechos pedidos entonces aca daría infinito
    time_to_first_purchase = df_complete[['customer_id', 'time_to_first_purchase']].drop_duplicates()

    # POR ALGÚN MOTIVO HAY FECHAS NEGATIVAS
    # st.dataframe(time_to_first_purchase[time_to_first_purchase['time_to_first_purchase']<0])
    
    # Me quedo con los valores positivos para que no sesgue los resultados
    # Calcular estadísticas generales
    average_time_to_first_purchase = time_to_first_purchase[time_to_first_purchase['time_to_first_purchase']>=0]["time_to_first_purchase"].mean()

    # Histograma de tiempo hasta la priemra compra. 
    # Filtrar valores válidos para TTFP
    valid_time_to_first_purchase = df_complete['time_to_first_purchase'].dropna()

    # Crear el DataFrame para Altair
    ttfp_data = pd.DataFrame({'time_to_first_purchase': valid_time_to_first_purchase})

    # Crear el histograma
    histogram = (
        alt.Chart(ttfp_data[ttfp_data["time_to_first_purchase"]>=0])
        .mark_bar()
        .encode(
            x=alt.X('time_to_first_purchase:Q', bin=alt.Bin(maxbins=60), title='Tiempo hasta la primera compra (días)'),
            y=alt.Y('count()', title='Cantidad de clientes'),
            tooltip=['count()']
        )
        .properties(
            width=600,
            height=280,
            title='Distribución del Tiempo Hasta la Primera Compra'
        )
    )
        
    # Contenedor: Métricas por cliente
    with st.container():
        col1, col2, col3 = st.columns([0.5, 0.5, 2])
        col1.metric("Tasa de Activación", f"{tasa_activacion:.2f}%", 
                    help="(Número de clientes que realizó un pedido / Número de registros únicos) * 100.")
        col1.write(f"N° Clientes Registrados Sin Pedido: {numero_registrados_sin_pedido}")
        col1.write(f"De un total de: {total_registrados}")
        col2.metric("Time to First Purchase", f"{average_time_to_first_purchase:,.2f} días", 
                    help="Promedio de la diferencia entre la fecha de registro y fecha de la primera compra")
        col3.altair_chart(histogram, use_container_width=True)  # Mostrar el gráfico en Streamlit


    # Clientes en ciclo temprano de los que estan registrados
    # Filtrar clientes en ciclo de vida temprano (<= 90 días o <= 3 compras)
    clientes_ciclo_temprano_ordenes = filtered_data_orders_registered.groupby('customer_id').filter(lambda x: len(x) <= 3)
    num_clientes_ciclo_temprano_ordenes = clientes_ciclo_temprano_ordenes['customer_id'].nunique()
    
    clientes_ciclo_temprano_dias = filtered_data_orders_registered.groupby('customer_id').filter(lambda x: (x['order_date_formatted'].max() - x['order_date_formatted'].min()).days <= 90)
    num_clientes_ciclo_temprano_dias = clientes_ciclo_temprano_dias['customer_id'].nunique()
    
    st.markdown("#### Ciclo de vida temprano")
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        col1.markdown("Hasta las primeras 3 órdenes.")
        col1.metric("N° Clientes en ciclo temprano", f"{num_clientes_ciclo_temprano_ordenes}")
        col1.write(f"N° Clientes registrados con al menos 1 pedido: {total_registrados-numero_registrados_sin_pedido}")
        col2.markdown("Primeros 30-90 días desde la primera compra.")
        col2.metric("N° Clientes en ciclo temprano", f"{num_clientes_ciclo_temprano_dias}")
    
    
    # Clientes maduros (más de 3 transacciones)
    clientes_ciclo_maduro = filtered_data_orders_registered.groupby('customer_id').filter(lambda x: len(x) > 3)
    num_clientes_ciclo_maduro = clientes_ciclo_maduro['customer_id'].nunique()
    
    st.markdown("#### Madurez del cliente")
    st.metric("Clientes maduros", f"{num_clientes_ciclo_maduro}",
              help="Más de 3 transacciones")

except URLError as e:
    st.error(
        f"**This demo requires internet access.**\nConnection error: {e.reason}"
    )