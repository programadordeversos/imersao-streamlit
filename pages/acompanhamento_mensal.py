import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():

    df = pd.read_excel(r'C:\Users\d0s_sant\Documents\Imersão Dashboard em Python\Dataset\Vendas.xlsx')

    return df

def color_negative(valor):
    color = "red" if valor < 0 else "#79AC78"

    return f'color: {color}'

def main():
    
    st.set_page_config(page_title="Vendas", page_icon="R5_Icon.ico", layout="wide")

    df = carregar_dados()

    MoM = df.groupby(["mes_ano"])["Lucro"].sum().reset_index()
    MoM["LM"] = MoM["Lucro"].shift(1)
    MoM["Variação"] = MoM["Lucro"] - MoM["LM"]
    MoM["Variação%"] = MoM["Variação"] / MoM["LM"] * 100
    MoM["Variação%"] = MoM["Variação%"].map('{:.2f}%'.format)
    MoM["LM"].fillna(0,inplace=True)
    MoM["Variação"].fillna(0,inplace=True)
    MoM["Variação%"] = MoM["Variação%"].replace("nan%","0.00%")

    st.header("Análise Mensal 📆")
    df_styled = MoM.style.format({"LM": "R${:.2f}",
                                  "Lucro": "R${:.2f}",
                                  "Variação": "{:20,.2f}"})\
                .hide(axis="index")\
                .applymap(color_negative, subset=["Variação"]) 

    st.write(df_styled)

if __name__ == "__main__":
    main()