# -*- coding: utf-8 -*-
"""
Created on Sun May 14 10:04:30 2023

@author: vinee
"""

import pandas as pd
import plotly.express as px
import streamlit as st
#emojis : https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title='India Sales Dashboard',
                   page_icon=":bar_chart:",
                   layout="wide")



# inputExcelFile = input(' Enter Excel file : ')
# sheetName = input('Enter Excel sheet name : ')
# skipRows = int(input('Number of rows skip : '))
# useCols = input ('column range (like A: R) : ')
# nRows = int(input('Number of rows to be processed : '))


inputExcelFile = 'supermarkt_india_sales.xlsx'
sheetName = 'Sales'
skipRows = 0
useCols = 'A:Q'
nRows = 1000

## thsi tag will cache the df and not load all the time

@st.cache
def get_data_from_excel():

    df = pd.read_excel(io = inputExcelFile,
                       engine = 'openpyxl',
                       sheet_name = sheetName,
                       skiprows= skipRows,
                       usecols= useCols,
                       nrows = nRows
                     )  
    # Add 'hour' to df
    df['hour'] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()
                 
#st.dataframe(df)

# IFTHINGSNOTWORK
# Actually after running this command , go to Anaconda promt and change the env
# using conda actiavte [env_name]
# got to location where this file is located and run : streamlit run [app.py]
# if this fails to work then use this command : python -m streamlit run [app.py]


#..... SIDEBAR ...............


st.sidebar.header('Filters...')

city = st.sidebar.multiselect('Select the city', 
                              options = df["City"].unique(),
                              default=df['City'].unique() 
                              )

customer_type = st.sidebar.multiselect('Select the Customer Type', 
                              options = df["Customer_type"].unique(),
                              default=df['Customer_type'].unique() 
                              )

gender = st.sidebar.multiselect('Select the Gender', 
                              options = df["Gender"].unique(),
                              default=df['Gender'].unique() 
                              )






# filters logic

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
    )

#st.dataframe(df_selection)



#............... MAINPAGE >>>>>>>>>>>>>>

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")



# Top KPI's
total_sales = int( df_selection["Total"].sum())
average_rating =  round(df_selection["Rating"].mean(),1)
try:
  star_rating  = ":star:" * int (round(average_rating,0))
except:
  star_rating =   ":star:" * 0

average_sale_by_transaction = round(df_selection["Total"].mean(),2)


left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"INR  {total_sales:,}")


with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
    
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"INR  {average_sale_by_transaction}")
    
st.markdown("...")








# sales by product line [BAR CHART]

sales_by_product_line = (df_selection.groupby(by = ["Product line"])
                         .sum(numeric_only = True)[["Total"]].sort_values(by = "Total"))

fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation="h",
    title="<b> Sales by Product Line</b>",
    color_discrete_sequence=["#0083BB"] * len(sales_by_product_line),
    template="plotly_white"
    )                         


fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis =(dict(showgrid = False))
    )

#st.plotly_chart(fig_product_sales)

# sales by Hour [BAR CHART]

sales_by_hour = (df_selection.groupby(by = ["hour"])
                         .sum(numeric_only = True)[["Total"]]
                         )

fig_hourly_sales = px.bar(
    sales_by_hour,
    y = "Total",
    x = sales_by_hour.index,
    #orientation="h",
    title="<b> Sales by Hour</b>",
    color_discrete_sequence=["#0083BB"] * len(sales_by_hour),
    template="plotly_white"
   
    )                         


fig_hourly_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis =(dict(showgrid = False)),
    xaxis = dict(tickmode="linear")
    )

#st.plotly_chart(fig_hourly_sales)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_hourly_sales,use_container_width=True)

right_column.plotly_chart(fig_product_sales,use_container_width=True)

#hide strealit style
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#use to creare .streamlit folder where streamlit installed and create 
#config.toml file 

