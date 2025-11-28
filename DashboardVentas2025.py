import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title('Análisis de Ventas y Profitability')

# --- 1. Load Data ---
st.header('1. Carga de Datos')
file_path = 'SalidaFinal.xlsx'

try:
    df = pd.read_excel(file_path)
    st.success(f'Archivo {file_path} cargado exitosamente.')
    st.subheader('Primeras 5 filas del DataFrame:')
    st.dataframe(df.head())
    st.subheader('Tipos de datos de las columnas:')
    st.dataframe(df.dtypes)
except Exception as e:
    st.error(f'Error al cargar el archivo Excel: {e}. Asegúrate de que la ruta sea correcta y el archivo esté accesible.')
    st.stop() # Stop the app if data loading fails

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("📊 Product Performance Analysis")

# ---- Cargar Excel ----
file_path = "SalidaFinal.xlsx"

try:
    df = pd.read_excel(file_path)
    st.success(f"Archivo {file_path} cargado exitosamente.")
except Exception as e:
    st.error(f"Error al cargar archivo: {e}")
    st.stop()

# -------------------------------------------------------------------
# SIDEBAR: FILTROS
# -------------------------------------------------------------------
st.sidebar.header("Filters")

regiones = ["Todas"] + sorted(df["Region"].dropna().unique().tolist())
estados = ["Todas"] + sorted(df["State"].dropna().unique().tolist())

filtro_region = st.sidebar.selectbox("Select Region", regiones)
filtro_estado = st.sidebar.selectbox("Select State", estados)

mostrar_df = st.sidebar.checkbox("Show Filtered Data")

# -------------------------------------------------------------------
# APLICAR FILTROS
# -------------------------------------------------------------------
df_filtrado = df.copy()

if filtro_region != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Region"] == filtro_region]

if filtro_estado != "Todas":
    df_filtrado = df_filtrado[df_filtrado["State"] == filtro_estado]

# -------------------------------------------------------------------
# MOSTRAR TABLA SI EL CHECKBOX ESTÁ ACTIVADO
# -------------------------------------------------------------------
st.subheader("Filtered Data")

if mostrar_df:
    st.dataframe(df_filtrado, use_container_width=True)

# -------------------------------------------------------------------
# GRÁFICA TOP 5 PRODUCTOS MÁS VENDIDOS
# -------------------------------------------------------------------
if len(df_filtrado) > 0:

    top5 = (
        df_filtrado.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )


    top5["Product Name"] = top5["Product Name"].astype(str)

    titulo = f"Top 5 Best-Selling Products ({filtro_region}, {filtro_estado})"

 grafica = (
    alt.Chart(top5)
    .mark_bar(color="#4B8BFF")
    .encode(
        x=alt.X(col_producto, sort="-y", title="Product Name"),
        y=alt.Y(col_sales, title="Total Sales"),
        tooltip=[col_producto, col_sales]
    )
    .properties(
        width=750,
        height=450,
        title=titulo
    )
)


    st.altair_chart(grafica, use_container_width=True)

else:
    st.warning("No hay datos con los filtros seleccionados.")

    
# --- 2. Top 5 Best-Selling Products by Sub-Category ---
st.header('2. Top 5 Sub-Categorías Más Vendidas')
# Group by 'Sub-Category' and sum 'Sales' to find best-selling products, then take the top 5
top_5_products = df.groupby('Sub-Category')['Sales'].sum().nlargest(5).reset_index()

# Create an interactive bar chart using plotly.express
fig_sub_category_sales = px.bar(top_5_products, x='Sales', y='Sub-Category',
             title='Top 5 Sub-Categorías Más Vendidas (Plotly Express)',
             labels={'Sales': 'Total Ventas', 'Sub-Category': 'Sub-Categoría'})

st.plotly_chart(fig_sub_category_sales, use_container_width=True)

# --- 3. Top 5 Best-Selling Products by Name ---
st.header('3. Top 5 Productos Más Vendidos por Nombre')
# Group by 'Product Name' and sum 'Sales' to find best-selling products, then take the top 5
top_5_product_names = df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()

# Create an interactive bar chart using plotly.express
fig_product_names_sales = px.bar(top_5_product_names, x='Sales', y='Product Name',
             title='Top 5 Productos Más Vendidos por Nombre (Plotly Express)',
             labels={'Sales': 'Total Ventas', 'Product Name': 'Nombre del Producto'})

st.plotly_chart(fig_product_names_sales, use_container_width=True)

# --- 4. Sales and Profit Details for Top 5 Best-Selling Products ---
st.header('4. Detalles de Ventas y Profit para los Top 5 Productos Más Vendidos')
# Get the list of top 5 product names
top_5_product_names_list = top_5_product_names['Product Name'].tolist()

# Filter the original DataFrame to include only these top 5 products
df_top_5_products_detail = df[df['Product Name'].isin(top_5_product_names_list)]

# Group by 'Product Name' and sum 'Sales' and 'Profit'
top_5_products_sales_profit = df_top_5_products_detail.groupby('Product Name')[['Sales', 'Profit']].sum().reset_index()

# Sort by Sales to ensure the order is consistent with best-selling
top_5_products_sales_profit = top_5_products_sales_profit.sort_values(by='Sales', ascending=False)

st.subheader('Tabla de Ventas y Profit de los Top 5 Productos Más Vendidos:')
st.dataframe(top_5_products_sales_profit)

# --- 6. Top 5 Most Profitable Products (with formatted names) ---
st.header('6. Top 5 Productos Más Rentables')
# Group by 'Product Name' and sum 'Profit' to find products with highest profit, then take the top 5
top_5_products_by_profit = df.groupby('Product Name')['Profit'].sum().nlargest(5).reset_index()

# Make a copy to avoid modifying the original DataFrame
top_5_products_by_profit_formatted = top_5_products_by_profit.copy()

# Function to split long product names into two lines for better display
def split_name_into_two_lines(name):
    words = name.split(' ')
    if len(words) > 3:
        # Try to find a good split point, e.g., in the middle
        mid_point = len(words) // 2
        return ' '.join(words[:mid_point]) + '<br>' + ' '.join(words[mid_point:])
    return name

# Apply the function to the 'Product Name' column
top_5_products_by_profit_formatted['Product Name Formatted'] = top_5_products_by_profit_formatted['Product Name'].apply(split_name_into_two_lines)

# Create an interactive bar chart using plotly.express with formatted names
fig_top_profit_products_formatted = px.bar(top_5_products_by_profit_formatted,
                                             x='Profit',
                                             y='Product Name Formatted',
                                             title='Top 5 Productos Más Rentables (Plotly Express)',
                                             labels={'Profit': 'Total Profit', 'Product Name Formatted': 'Nombre del Producto'})

st.plotly_chart(fig_top_profit_products_formatted, use_container_width=True)
