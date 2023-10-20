import streamlit as st
import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import os
import mysql.connector as sql
import plotly.express as px
import requests

st.set_page_config(
    page_title="Phonepe Pulse Dashboard",
    page_icon="👋",
)

# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [20.5937, 78.9629],
#     columns=['lat', 'lon'])
data_base_path = "./Data/data/aggregated/transaction/country/india/state/"
#Aggregated data
aggr_transactions_list = os.listdir(data_base_path)
mydb = sql.connect(host="127.0.0.1",
                   user="root",
                   password="root",
                   database= "research",
                   port = "3306"
                  )
mycursor = mydb.cursor(buffered=True)
geojsonurl = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
with st.sidebar:
    selected = st.selectbox("Select the menu",["Home","Top Charts","Explore Data"])

if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users ")

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    statsnames = pd.read_csv(r'.\\Data\\Statenames.csv')
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
        ToppersLimit = st.slider("Topper Limit", min_value=3, max_value=statsnames.size)
    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([3,3,3],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select STATE, sum(TRANS_COUNT) as Total_Transactions_Count, sum(AMOUNT) as Total from PHONEPE_AGGREGATED_TRANS where year = {Year} and quarter = {Quarter} group by state order by Total desc limit {ToppersLimit}")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top ' + str(ToppersLimit),
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select DISTRICT , sum(TRANS_COUNT) as Total_Count, sum(AMOUNT) as Total from PHONEPE_MAP_TRANSACTIONS where year = {Year} and quarter = {Quarter} group by district order by Total desc limit {ToppersLimit}")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount']).drop(index=0)

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top ' + str(ToppersLimit),
                             color_discrete_sequence=px.colors.sequential.Turbo,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        
        with col3:
            st.markdown("### :violet[Transaction Details]")
            mycursor.execute(f"select STATE, sum(TRANS_COUNT), sum(AMOUNT) from PHONEPE_AGGREGATED_TRANS where year = {Year} and quarter = {Quarter} group by state limit {ToppersLimit}")
            df = pd.DataFrame(mycursor.fetchall(),columns=['State','Transaction Count', 'Amount'])
            #df1 = df.iloc[1:]
            #df1 = df.drop(index=df.index[0], axis=0, inplace=True)
            print("**"*20)
           
            fig = px.bar(df, x = 'State', y= "Transaction Count",    
                             title='All States Transactions',
                             #color_discrete_map=px.colors.sequential.Agsunset
                            
                             )
            
            st.plotly_chart(fig,use_container_width=True)
    if Type == "Users":
        col1,col2,col3 = st.columns([2,2,2],gap="small")
        
        with col1:
            st.markdown("### :red[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select BRANDS, sum(TRANS_COUNT) as Total_Count, avg(PERCENT)*100 as Avg_Percentage from PHONEPE_AGGREGATED_USERS where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top ' + str(ToppersLimit),
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select DISTRICT, sum(REGISTERED_USERS) as Total_Users,sum(APP_OPENS) as App_opens from PHONEPE_MAP_USERS where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','App_opens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.scatter(df,
                         title='Top ' + str(ToppersLimit),
                         x="District",
                         y="Total_Users",
                         color='District',
                         )
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :blue[District]")
            mycursor.execute(f"select DISTRICT as Districts, sum(REGISTERED_USERS) as Total_Users from TOP_USERS where year = {Year} and quarter = {Quarter} group by DISTRICT order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Districts', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Districts',
                         title='Top ' + str(ToppersLimit),
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
         
        
if selected == "Explore Data":
    
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2,col3,col4 = st.columns([2,2,2,1],gap="small")
    
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :green[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(TRANS_COUNT) as Total_Transactions, sum(amount) as Total_amount from PHONEPE_MAP_TRANSACTIONS where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'.\\Data\\Statenames.csv')
            df1.State = df2
            fig = px.choropleth(df1,geojson=geojsonurl,
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset',)

            fig.update_geos(fitbounds="locations", visible=False) 
            st.plotly_chart(fig)
            
        with col2:
            st.markdown("## :green[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(TRANS_COUNT) as Total_Transactions, sum(amount) as Total_amount from PHONEPE_MAP_TRANSACTIONS where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            
            df2 = pd.read_csv(r'.\\Data\\Statenames.csv')
            df1.State = df2
            fig1 = px.scatter(df1,x='Total_Transactions', y='Total_amount', color='Total_amount', color_continuous_scale='sunset')
            #fig1.update_geos(fitbounds="locations", visible=False)
            
            st.plotly_chart(fig1)
        with col3:
            st.markdown("## :blue[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(TRANS_COUNT) as Total_Transactions, sum(amount) as Total_amount from PHONEPE_MAP_TRANSACTIONS where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'.\\Data\\Statenames.csv')
            df1.State = df2
            fig1 = px.area(df1,x='Total_Transactions',y='Total_amount',color='Total_amount')
            #fig1.update_geos(fitbounds="locations", visible=False)
            
            st.plotly_chart(fig1)
        with col4:
            st.markdown("## :green[Insights on a State - Transactions]")
            states_list = ["Andaman-&-Nicobar","Andhra-Pradesh","Arunachal-Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","adra-and-Nagar-Haveli-and-Daman-and-Diu","Delhi","Goa","Gujarat","Haryana","Himachal-Pradesh","Jammu-&-Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya-Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil-Nadu","Telangana","Tripura","Uttar-Pradesh","Uttarakhand","West-Bengal"]
            df2 = pd.read_csv(r'.\\Data\\Statenames.csv')
            selected_state = st.selectbox(options=states_list,label="Select the state")
            selected_state = selected_state.lower()
            mycursor.execute(f"select sum(amount) as amount, quarter,year from PHONEPE_AGGREGATED_TRANS where state = '{selected_state}' and year = {Year} group by quarter, year")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['amount', 'quarter', 'year'])
                        
            fig1 = px.area(df1,x='quarter',y='amount',color='quarter')
            st.plotly_chart(fig1)


    Year = st.slider("Year", min_value=2018, max_value=2022)
    if Type == "Users":
        col1,col2,col3 = st.columns(3,gap="large")
        
        with col1:
            st.markdown("## Total Transactions in Quarters ##")
            
            mycursor.execute(f"select quarter, sum(AMOUNT) as amount, sum(TRANS_COUNT) as transactions from TOP_TRANSACTIONS where year= {Year} group by quarter")
            df1 = pd.DataFrame(mycursor.fetchall(),columns=['Quarter','amount','transactions'])
            fig = px.histogram(df1,x='Quarter',y='amount')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("## Users Registration ##")
            
            mycursor.execute(f"select state as state, QUARTER as quarter,  sum(REGISTERED_USERS) as users,district as district  from top_users where year = {Year} group by state, quarter, year;")
            df1 = pd.DataFrame(mycursor.fetchall(),columns=['state','quarter','users','district'])
            fig = px.bar(df1,y='quarter',x='users')
            df2 = pd.read_csv(r'.\\Data\\Statenames.csv')
            df1.state = df2
            fig = px.choropleth(df1,geojson=geojsonurl,
                      featureidkey='properties.ST_NM',
                      locations='state',
                      color='state',
                      color_continuous_scale= 'sunset')
            fig.update_geos(fitbounds="locations", visible=False) 
            st.plotly_chart(fig)
        