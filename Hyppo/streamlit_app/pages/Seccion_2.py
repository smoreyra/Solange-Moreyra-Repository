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
        # Cargar datasets desde archivos Excel
        # Campañas de envíos automatizados de comunicaciones que tuvo prendida 
        # el cliente durante Q3 2024 con un detalle de los envíos realizados
        df_BD_campaigns_Q3 = pd.read_excel('C:/Users/solange.moreyra/Desktop/Sol/Solange-Moreyra-Repository/hyppo/bd_campaigns_q3.xlsx', engine='openpyxl')

        # Transacciones del período 2023 y 2024 hasta octubre
        df_bd_orders = pd.read_excel('C:/Users/solange.moreyra/Desktop/Sol/Solange-Moreyra-Repository/hyppo/bd_orders.xlsx', engine='openpyxl')

        # Base de datos de descargas de la app desde Diciembre 2022 en adelante
        df_BD_signups = pd.read_excel('C:/Users/solange.moreyra/Desktop/Sol/Solange-Moreyra-Repository/hyppo/BD_signups.xlsx', engine='openpyxl')

        return df_BD_campaigns_Q3, df_bd_orders, df_BD_signups
    
    except FileNotFoundError as e:
        st.error(f"No se encontró el archivo: {e.filename}")
        return pd.DataFrame()

try:
    df_BD_campaigns_Q3, df_bd_orders, df_BD_signups= load_data()
    
    st.title("Visualización del dataframe")
    st.dataframe(df_BD_campaigns_Q3)

    first_year = df_bd_orders["order_date_formatted"].min()
    last_year = df_bd_orders["order_date_formatted"].max()

    col1, col2 = st.columns([1, 3.8])

    with col1:
        def create_multiselect_filter(df, column_name, filter_label, dependent_values=None, dependent_column=None):
            """
            Crea un filtro multiselect con soporte para valores dependientes.
            """
            # Filtrar las opciones si hay un valor dependiente
            if dependent_values is not None and dependent_column is not None:
                filtered_df = df[df[dependent_column].isin(dependent_values)]
                column_options = filtered_df[column_name].unique()
            else:
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
        selected_campaign_name = create_multiselect_filter(df_BD_campaigns_Q3, "campaign_name", "Nombre de campaña")   
        selected_metric = create_multiselect_filter(df_BD_campaigns_Q3, "metric", "Métrica")
        
        # Muestro solamene la opciones disponibles para subject según el campaing_name que elijo
        selected_subject = create_multiselect_filter(
            df=df_BD_campaigns_Q3, 
            column_name="subject", 
            filter_label="Subject",
            dependent_values=selected_campaign_name,
            dependent_column="campaign_name"
        )
  
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
            # Tasa de entrega de campañas a usuarios únicos
            total_campaigns = df_BD_campaigns_Q3['campaign_id'].nunique()
            delivered_campaigns = df_BD_campaigns_Q3[df_BD_campaigns_Q3['delivery_status'] == 'Delivered']['campaign_id'].nunique()
            tasa_entrega_campaigns = (delivered_campaigns / total_campaigns) * 100

            # Tasa de conversión de campañas
            total_conversions = df_BD_campaigns_Q3['conversions'].sum()
            tasa_conversion_campaigns = (total_conversions / total_campaigns) * 100

            # Promedio de compras por usuario
            avg_purchases_per_user = filtered_data_orders.groupby('customer_id')['order_id'].nunique().mean()

            # Valor total de compras por campaña
            df_campaigns_orders = pd.merge(filtered_data_orders, df_BD_campaigns_Q3, on='campaign_id')
            total_value_by_campaign = df_campaigns_orders.groupby('campaign_id')['total_value'].sum()

            # Segmentación de usuarios por tipo de campaña
            user_campaign_segmentation = df_campaigns_orders.groupby('campaign_type')['customer_id'].nunique()

            # Impacto de los descuentos
            discounted_orders = filtered_data_orders[filtered_data_orders['discounted'] == True]
            discount_impact = discounted_orders['total_value'].sum() / filtered_data_orders['total_value'].sum() * 100

            # Tasa de recompra
            repeat_customers = filtered_data_orders.groupby('customer_id')['order_id'].count().loc[lambda x: x > 1].count()
            tasa_recompra = (repeat_customers / filtered_data_orders['customer_id'].nunique()) * 100

            # Desempeño por tipo de usuario
            performance_by_user_type = filtered_data_orders.groupby('user_type')['total_value'].sum()

            # Tasa de activación
            active_users = df_BD_signups[df_BD_signups['user_status'] == 'Active']
            tasa_activacion = (active_users['customer_id'].nunique() / df_BD_signups['customer_id'].nunique()) * 100

            # Mostrar KPIs
            st.header("KPIs de Marketing")
            col1, col2 = st.columns([1, 1])

            with col1:
                st.metric("Tasa de entrega de campañas", 
                          f"{tasa_entrega_campaigns:.2f}%", 
                          help="Porcentaje de campañas entregadas.")
                st.metric("Tasa de conversión de campañas", 
                          f"{tasa_conversion_campaigns:.2f}%", 
                          help="Porcentaje de conversiones por campaña.")
                st.metric("Promedio de compras por usuario", 
                          f"{avg_purchases_per_user:.2f}", 
                          help="Promedio de compras realizadas por usuario.")
                st.metric("Valor total de compras por campaña", 
                          f"${total_value_by_campaign.sum():,.2f}", 
                          help="Valor total de compras agrupado por campaña.")
                
            with col2:
                st.metric("Segmentación de usuarios por tipo de campaña", 
                          f"{user_campaign_segmentation}", 
                          help="Número de usuarios por tipo de campaña.")
                st.metric("Impacto de los descuentos", 
                          f"{discount_impact:.2f}%", 
                          help="Porcentaje de ventas con descuento.")
                st.metric("Tasa de recompra", 
                          f"{tasa_recompra:.2f}%", 
                          help="Porcentaje de clientes que han comprado más de una vez.")
                st.metric("Desempeño por tipo de usuario", 
                          f"{performance_by_user_type}", 
                          help="Desempeño total de ventas por tipo de usuario.")
                st.metric("Tasa de activación", 
                          f"{tasa_activacion:.2f}%", 
                          help="Porcentaje de usuarios activos.")

                # Hago a la agregación por valor para armar el gráfico
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
    
    st.header("Ciclo de Vida de los clientes")
    st.markdown("#### Activación (antes de primera compra)")
    st.markdown("#### Ciclo de vida temprano")
    st.markdown("#### Madurez del cliente")
    

except URLError as e:
    st.error(
        f"**This demo requires internet access.**\nConnection error: {e.reason}"
    )
    
    # TODO: métricas a agregar
    # 1. Primero entiendo de que se trata el df, acá se ve que también es una app de comida como el ejercicio de la sección 1. 