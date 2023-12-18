import pandas as pd
import streamlit as st
import pyodbc
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import locale

@st.cache_data
def carregar_dados():

    df = pd.read_excel('Vendas.xlsx')

    return df

def main():

    # caminho_imagem = r'C:\Users\d0s_sant\Documents\Imersão Dashboard em Python\Streamlit'+'\\'+'f3.png'

    st.set_page_config(page_title="Vendas", page_icon="R5_Icon.ico")
    st.sidebar.image("f3.png", width=100)
    st.title("Dashboard de Vendas 📊")

    df = carregar_dados()

    ano_filtrado = st.sidebar.selectbox("Filtrar por Ano:", ["Todos", *df["Ano"].unique()])

    if ano_filtrado != "Todos":
        df_filtrado = df[df["Ano"] == ano_filtrado]
    else:
        df_filtrado = df

    total_custo = (df_filtrado["Custo"].sum())
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    total_custo = locale.currency(total_custo, grouping=True)
    # total_custo = total_custo.replace('.',',')
    # total_custo = "R$ " + total_custo[:2] + "." + total_custo[2:5] + "." + total_custo[5:]

    total_lucro = (df_filtrado["Lucro"].sum())
    total_lucro = locale.currency(total_lucro, grouping=True)
    # total_lucro = "R$ " + total_lucro[:2] + "." + total_lucro[2:5] + "." + total_lucro[5:]

    total_clientes = (df_filtrado["ID Cliente"]).nunique()


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Custo",total_custo)
        style_metric_cards(border_left_color="#FF971D")
    
    with col2:
        st.metric("Total Lucro",total_lucro)
        # style_metric_cards()
    
    with col3:
        st.metric("Total Clientes",total_clientes)
        # style_metric_cards()


    st.markdown(
    """"
    <style>
    [data-testid="stMetricValue"]{
        font-size: 18px;
        color: rgba(0,0,0)
    }
    """
    ,
    unsafe_allow_html=True,
    )     


    produtos_vendidos_marca = df_filtrado.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()

    lucro_categoria = df_filtrado.groupby("Categoria")["Lucro"].sum().reset_index()

    lucro_mes_categoria = df_filtrado.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()

    col1, col2 = st.columns(2)

    barras = px.bar(produtos_vendidos_marca, x="Quantidade", y="Marca", orientation="h", 
                 title="Total Produtos Vendidos Por Marca", color_discrete_sequence=["#FF971D"], width=380, height=350, text="Quantidade")
    barras.update_layout(title_x= 0.2)
    barras.update_yaxes(automargin=True)
    col1.plotly_chart(barras, use_container_width=True)

    rosca = px.pie(lucro_categoria, values="Lucro", names="Categoria", title="Lucro Por Categoria",
                 hole=0.64, width=380, height=350, color_discrete_sequence=["#000000", "#FF971D", "#CF7500"])
    rosca.update_layout(title_x= 0.4)
    rosca.update_yaxes(automargin=True)
    col2.plotly_chart(rosca, use_container_width=True, theme="streamlit")


    linhas = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", title="Lucro x Mês x Categoria",
                 color="Categoria", markers=True, color_discrete_sequence=["#000000", "#FF971D", "#CF7500"])
    st.plotly_chart(linhas)

if __name__ == "__main__":
    main()
