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
        # Cargar datasets desde archivos Excel
        # Transacciones del período 2023 y 2024 hasta octubre
        df_bd_orders = pd.read_excel('C:/Users/solange.moreyra/Desktop/Sol/Solange-Moreyra-Repository/hyppo/bd_orders.xlsx', engine='openpyxl')

        # Base de datos de descargas de la app desde Diciembre 2022 en adelante
        df_BD_signups = pd.read_excel('C:/Users/solange.moreyra/Desktop/Sol/Solange-Moreyra-Repository/hyppo/BD_signups.xlsx', engine='openpyxl')

        return df_bd_orders, df_BD_signups
    
    except FileNotFoundError as e:
        st.error(f"No se encontró el archivo: {e.filename}")
        return pd.DataFrame()

try:
    df_bd_orders, df_BD_signups = load_data()
    
    # st.title("Visualización del dataframe")
    # st.dataframe(df_bd_orders)
    # st.dataframe(df_BD_signups)

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

        # with st.container(height=450):
        st.markdown('<h1 style="font-size: 30px; font-weight: bold; text-align:left;">Filtros</h1>', unsafe_allow_html=True)
        
        # st.markdown('<div class="filter-title">Geographic</div>', unsafe_allow_html=True)
        start_date, end_date = st.date_input("Order date", [first_year, last_year])
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
                
                def crear_grafico_metrica(data, columna_metrica, nombre_metrica, color_linea):
                    """
                    Función para crear un gráfico de línea para una métrica específica.
                    
                    Parameters:
                    - data: dataframe con los datos.
                    - columna_metrica: nombre de la columna de la métrica que quieres graficar.
                    - nombre_metrica: nombre que se mostrará en el gráfico y la leyenda.
                    - color_linea: color que se usará para la línea del gráfico.
                    
                    Returns:
                    - Un gráfico de línea de Altair.
                    """
                    
                    # Preparar los datos en formato largo para graficar
                    agg_data_long = data.melt(id_vars=['order_date_formatted'], 
                                            value_vars=[columna_metrica], 
                                            var_name='Variable', 
                                            value_name='Valor')
                    
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

                # Métricas por cliente
                
                # Filtrar los customer_id en filtered_data_orders que no están en df_BD_signups
                unregistered_customers = filtered_data_orders[~filtered_data_orders['customer_id'].isin(df_BD_signups['customer_id'])]
                # Tendría que pone acá de los customer_id que se encuentran en el filtro cuáles de los totales que se registraron ahi (para que no me de mayor al 100%)
                tasa_conversion = (unregistered_customers['customer_id'].nunique() / df_BD_signups['customer_id'].nunique()) * 100
                ltv_por_cliente = filtered_data_orders.groupby('customer_id')['total_value'].sum().mean()

                # Métricas de retención
                clientes_retenidos = filtered_data_orders.groupby('customer_id')['order_id'].count().loc[lambda x: x > 1].count()
                tasa_retencion = (clientes_retenidos / filtered_data_orders['customer_id'].nunique()) * 100
                tasa_churn = 100 - tasa_retencion

                # Streamlit UI
                # st.title("Tablero de Métricas del Negocio")
                # st.markdown("Visualización de las métricas clave para analizar la performance general y a nivel cliente.")

                # Contenedor: Métricas generales
                with st.container():
                    st.header("Performance general del negocio")
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

                # Crear tabs para cada métrica
                ingresos_totales, ordenes_totales, aov, tasa_sku, tasa_item = st.tabs([
                    "Ingresos Totales", 
                    "Órdenes Totales", 
                    "AOV(Average Order Value)",
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
                        "#8A2BE2"
                        ), use_container_width=True)

                with tasa_sku:
                    st.altair_chart(crear_grafico_metrica(
                        agg_data_metrics, 
                        "Tasa_sku", 
                        "Tasa de Cumplimiento por SKU",
                        "#8A2BE2"
                        ), use_container_width=True)

                with tasa_item:
                    st.altair_chart(crear_grafico_metrica(
                        agg_data_metrics, 
                        "Tasa_item", 
                        "Tasa de Cumplimiento por Item",
                        "#8A2BE2"
                        ), use_container_width=True)
                       
                # Contenedor: Métricas por cliente
                with st.container():
                    st.header("Performance a nivel cliente")
                    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
                    col1.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%", 
                                help="(Número de clientes únicos con ordenes / Número de registros únicos) * 100.")
                    col2.metric("Lifetime Value Promedio", f"${ltv_por_cliente:,.2f}", 
                                help="Promedio del valor total por cliente.")
                    col3.metric("Tasa de Retención", f"{tasa_retencion:.2f}%", 
                            help="(Clientes que realizaron más de 1 orden / Total de clientes únicos) * 100.")
                    col4.metric("Tasa de Churn", f"{tasa_churn:.2f}%", 
                            help="100 - Tasa de Retención.")
                
 
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
                st.altair_chart(chart, use_container_width=True)
    
    st.header("Ciclo de Vida de los clientes")
    st.markdown("#### Activación (antes de primera compra)")
    st.markdown("#### Ciclo de vida temprano")
    st.markdown("#### Madurez del cliente")
    

except URLError as e:
    st.error(
        f"**This demo requires internet access.**\nConnection error: {e.reason}"
    )
    
    # TODO: métricas a agregar
    # Gráfico que compare los items pedidos con los items entregados y filtrar por channel, por categoria y por tipo de orden. 
    # También filtrar por fecha para ver los KPI de totales. 
    # Ver que pongo de las tabs para ver si agrego por Market, por Eats o todo junto y demás. 
    # Hacer un select box o diferentes tabs donde se peude elegir que tipo de métrica se quiere evaluar a lo largo del tiempo. 
    # Agregar una opción en el drodown que sea All, LISTO
    # Cuáles SKUs tienen mayor tasa de cumplimiento que otros, LISTO 
    # Cantidad de SKUs pedidos en promedio
    # Revisar por qu da mas del 100% la tasa de conversion, LISTO
    # Frecuencia de compra, 