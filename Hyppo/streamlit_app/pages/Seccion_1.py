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

    col1, col2 = st.columns([1, 3])

    with col1:
        def create_multiselect_filter(df, column_name, filter_label):
            column_options = df[column_name].unique()
            selected_values = st.multiselect(
                label=filter_label,
                options=column_options,
                default=column_options[0]
            )
            return selected_values

        with st.container(height=450):
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
                
                # Cálculos de métricas generales con los datos filtrados
                ingresos_totales = filtered_data_orders['total_value'].sum()
                ordenes_totales = filtered_data_orders['order_id'].nunique()
                aov = ingresos_totales / ordenes_totales
                tasa_cumplimiento = (filtered_data_orders['skus_entregados'].sum() / filtered_data_orders['skus_pedidos'].sum()) * 100

                # Métricas por cliente
                tasa_conversion = (filtered_data_orders['customer_id'].nunique() / df_BD_signups['customer_id'].nunique()) * 100
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
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Ingresos Totales", f"${ingresos_totales:,.2f}", 
                                help="Suma de 'total_value' para las órdenes filtradas.")
                    col2.metric("Órdenes Totales", f"{ordenes_totales}", 
                                help="Número de órdenes únicas ('order_id').")
                    col3.metric("AOV", f"${aov:,.2f}", 
                                help="Ingresos Totales / Órdenes Totales.")
                    col4.metric("Tasa de Cumplimiento", f"{tasa_cumplimiento:.2f}%", 
                            help="(Skus Entregados / Skus Pedidos) * 100.")

                # Contenedor: Métricas por cliente
                with st.container():
                    st.header("Performance a nivel cliente")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%", 
                                help="(Número de clientes únicos con ordenes / Número de registros únicos) * 100.")
                    col2.metric("LTV Promedio", f"${ltv_por_cliente:,.2f}", 
                                help="Promedio de 'total_value' por cliente.")
                    col3.metric("Tasa de Retención", f"{tasa_retencion:.2f}%", 
                            help="(Clientes que realizaron más de 1 orden / Total de clientes únicos) * 100.")
                    col4.metric("Tasa de Churn", f"{tasa_churn:.2f}%", 
                            help="100 - Tasa de Retención.")

                
                # Hago ala agregación por valor para armar el gráfico
                agg_data = (
                    filtered_data_orders.groupby("order_date_formatted", as_index=False)
                    .agg({"skus_pedidos": "sum", "skus_entregados": "sum", "items_pedidos": "sum", "items_entregados": "sum"})
                )
            
                melted_df = pd.melt(agg_data, id_vars=["order_date_formatted"], 
                                value_vars=["skus_pedidos", "skus_entregados", "items_pedidos", "items_entregados"], 
                                var_name="variable", value_name="value"
                )
                
                selection = alt.selection_multi(fields=['variable'], bind='legend')

                melted_df['variable'] = melted_df['variable'].replace({
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
                        y=alt.Y("value:Q"),
                        color=alt.Color('variable:N', title='Variable', legend=alt.Legend(
                                                orient='bottom',
                                                title=None,
                                                direction='horizontal',
                                                legendX=0,
                                                legendY=0
                                            )
                                        ),
                        tooltip=["order_date_formatted:T", "value:Q", "variable:N"],
                        opacity=alt.condition(selection, alt.value(1), alt.value(0)) 
                    )
                    .add_selection(selection)
                )

                # Visualización del gráfico
                st.altair_chart(chart, use_container_width=True)

except URLError as e:
    st.error(
        f"**This demo requires internet access.**\nConnection error: {e.reason}"
    )
    
    # TODO: métricas a agregar
    # Gráfico que compare los items pedidos con los items entregados y filtrar por channel, por categoria y por tipo de orden. 
    # También filtrar por fecha para ver los KPI de totales. 
    # Ver que pongo de las tabs para ver si agrego por Market, por Eats o todo junto y demás. 