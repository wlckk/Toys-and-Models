import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import datetime as dt
from dateutil.relativedelta import relativedelta
st.set_page_config(
    page_title="Project Python!",
    page_icon=":smiley:",
    layout="wide",
)
#connection to mysql
connection = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.178.25.157', port = '23456', database = 'toys_and_models', use_pure = True)
#put your querys here and name them "query_FQ1" , for example
query_sales = """
    SELECT YEAR(o.orderDate) AS Sales_Year, 
           MONTH(o.orderDate) AS Sales_Month, 
           SUM(CASE WHEN p.productLine = 'Motorcycles' THEN od.quantityOrdered ELSE 0 END) AS Motorcycles_Sales, 
           SUM(CASE WHEN p.productLine = 'Classic Cars' THEN od.quantityOrdered ELSE 0 END) AS Classic_Cars_Sales, 
           SUM(CASE WHEN p.productLine = 'Trucks and Buses' THEN od.quantityOrdered ELSE 0 END) AS Trucks_Buses_Sales, 
           SUM(CASE WHEN p.productLine = 'Vintage Cars' THEN od.quantityOrdered ELSE 0 END) AS Vintage_Cars_Sales, 
           SUM(CASE WHEN p.productLine = 'Planes' THEN od.quantityOrdered ELSE 0 END) AS Planes_Sales, 
           SUM(CASE WHEN p.productLine = 'Trains' THEN od.quantityOrdered ELSE 0 END) AS Trains_Sales, 
           SUM(CASE WHEN p.productLine = 'Ships' THEN od.quantityOrdered ELSE 0 END) AS Ships_Sales, 
           LAG(SUM(CASE WHEN p.productLine = 'Motorcycles' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Motorcycles_Sales_PY,
           LAG(SUM(CASE WHEN p.productLine = 'Classic Cars' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Ccs_PreviousYear, 
           LAG(SUM(CASE WHEN p.productLine = 'Trucks and Buses' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Trucks_Buses_Sales_PreviousYear, 
           LAG(SUM(CASE WHEN p.productLine = 'Vintage Cars' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Vintage_Cars_Sales_PreviousYear, 
           LAG(SUM(CASE WHEN p.productLine = 'Planes' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Planes_Sales_PreviousYear, 
           LAG(SUM(CASE WHEN p.productLine = 'Trains' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Trains_PreviousYear, 
           LAG(SUM(CASE WHEN p.productLine = 'Ships' THEN od.quantityOrdered ELSE 0 END), 12) OVER (ORDER BY YEAR(o.orderDate), MONTH(o.orderDate)) AS Ships_PreviousYear
    FROM orders o
    JOIN orderdetails od ON o.orderNumber = od.orderNumber
    JOIN products p ON p.productCode = od.productCode
    GROUP BY YEAR(o.orderDate), MONTH(o.orderDate)
    ORDER BY YEAR(o.orderDate), MONTH(o.orderDate);
"""
query_FQ2 = '''Select o.customernumber, o.orderdate, o.ordernumber, sum((od.quantityordered * od.priceeach)) as Order_Value
from orders o
join orderdetails od
	on o.ordernumber = od.ordernumber
group by o.ordernumber
having sum((od.quantityordered * od.priceeach)) not in (select p.amount
from payments p)'''
query_FQ1 = '''WITH my_table AS (
    SELECT SUM(od.quantityOrdered * od.priceEach) AS turnover,
           YEAR(o.orderDate) AS Year,
           country
    FROM products AS p
    JOIN orderdetails AS od ON p.productCode = od.productCode
    JOIN orders AS o ON o.orderNumber = od.orderNumber
    JOIN customers AS c ON o.customerNumber = c.customerNumber 
    WHERE o.orderDate >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)
    GROUP BY Year, country
    ORDER BY country
)

SELECT mt.turnover, 
       mt.Year, 
       mt.country
FROM my_table AS mt
ORDER BY mt.country;'''
query_LQ1 = '''SELECT p.productName, sum(p.quantityInStock) as total_stock
FROM orderdetails od
    JOIN products p
      ON od.productcode = p.productcode
    GROUP BY p.productCode
    ORDER BY sum(od.quantityOrdered) DESC
    LIMIT 5;'''
query_human_res = '''SELECT year, month, x.sellers, monthly_turnover
FROM (SELECT year(o.OrderDate) as year,
			month(o.OrderDate) as month,
			concat(e.firstName, ' ', e.lastname) AS sellers,
            SUM(od.quantityOrdered) AS monthly_turnover,
            row_number() over (partition by year(o.OrderDate), month(o.OrderDate) order by SUM(od.quantityOrdered) desc) as seq
FROM orders as o
JOIN customers as c
ON c.customerNumber=o.customerNumber
JOIN employees as e
ON e.employeeNumber=c.salesRepEmployeeNumber
JOIN orderdetails as od
ON od.orderNumber=o.orderNumber
GROUP BY year(o.OrderDate), month(o.OrderDate), sellers
Order by year(o.OrderDate), month(o.OrderDate)) as x
where x.seq <=2;'''
#define your databases here, follow the same logic, df_FQ1, for example
df_SL = pd.read_sql_query(query_sales, con = connection)
df_FQ2 = pd.read_sql_query(query_FQ2, con = connection)
df_FQ1 = pd.read_sql_query(query_FQ1, con = connection)
df_LQ1 = pd.read_sql_query(query_LQ1, con = connection) 
df_HR = pd.read_sql_query(query_human_res, con = connection)
df_HR['date'] = pd.to_datetime(df_HR[['year', 'month']]. assign(day=1))
df_HR['date'] = pd.to_datetime(df_HR['date']).dt.date
#dont touch these
#with st.sidebar:
#    p = st.button("Presentation")
#    S = st.button("Sales")
#    F = st.button("Finance")
#    L = st.button("Logistics")
#    HR = st.button("Human Resources")
choice = st.sidebar.radio("Select a Topic", ('Sales','Finance','Logistics','Human Resources'))
#if choice == 'Presentation':
#   st.write('This is the presentation')
#uncomment your if after you paste the code and make sure it works
#if p:
if choice == 'Sales':
   st.header("Sales Quest")
   st.subheader("The number of products sold by category and by month, with comparison and rate of change compared to the same month of the previous year")
   year = st.selectbox("Select a Year", df_SL["Sales_Year"].unique())
   filtered_df = df_SL[df_SL["Sales_Year"] == year]
   st.write(filtered_df)
   sales_by_month = filtered_df.groupby("Sales_Month").sum()[["Motorcycles_Sales", "Classic_Cars_Sales", "Trucks_Buses_Sales", "Vintage_Cars_Sales", "Planes_Sales", "Trains_Sales", "Ships_Sales"]]
   st.bar_chart(sales_by_month)
   # Filter the dataset to only include years 2021 and 2022
   filtered_df = df_SL[df_SL["Sales_Year"].isin([2021, 2022])]

# Group the data by year and calculate the total sales for each year
   sales_by_year = filtered_df.groupby("Sales_Year").sum()[["Motorcycles_Sales", "Classic_Cars_Sales", "Trucks_Buses_Sales", "Vintage_Cars_Sales", "Planes_Sales", "Trains_Sales", "Ships_Sales"]]

# Calculate the rate of change between 2021 and 2022
   motorcycles_rate = (sales_by_year.loc[2022, "Motorcycles_Sales"] - sales_by_year.loc[2021, "Motorcycles_Sales"]) / sales_by_year.loc[2021, "Motorcycles_Sales"] * 100
   classic_cars_rate = (sales_by_year.loc[2022, "Classic_Cars_Sales"] - sales_by_year.loc[2021, "Classic_Cars_Sales"]) / sales_by_year.loc[2021, "Classic_Cars_Sales"] * 100
   trucks_buses_rate = (sales_by_year.loc[2022, "Trucks_Buses_Sales"] - sales_by_year.loc[2021, "Trucks_Buses_Sales"]) / sales_by_year.loc[2021, "Trucks_Buses_Sales"] * 100
   vintage_cars_rate = (sales_by_year.loc[2022, "Vintage_Cars_Sales"] - sales_by_year.loc[2021, "Vintage_Cars_Sales"]) / sales_by_year.loc[2021, "Vintage_Cars_Sales"] * 100
   planes_rate = (sales_by_year.loc[2022, "Planes_Sales"] - sales_by_year.loc[2021, "Planes_Sales"]) / sales_by_year.loc[2021, "Planes_Sales"] * 100
   trains_rate = (sales_by_year.loc[2022, "Trains_Sales"] - sales_by_year.loc[2021, "Trains_Sales"]) / sales_by_year.loc[2021, "Trains_Sales"] * 100
   ships_rate = (sales_by_year.loc[2022, "Ships_Sales"] - sales_by_year.loc[2021, "Ships_Sales"]) / sales_by_year.loc[2021, "Ships_Sales"] * 100

# Display the results using Streamlit
   st.write("Sales by Year")
   st.bar_chart(sales_by_year)

   st.write("Rate of Change between 2021 and 2022")
   st.write(f"Motorcycles Sales: {motorcycles_rate:.2f}%")
   st.write(f"Classic Cars Sales: {classic_cars_rate:.2f}%")
   st.write(f"Trucks and Buses Sales: {trucks_buses_rate:.2f}%")
   st.write(f"Vintage Cars Sales: {vintage_cars_rate:.2f}%")
   st.write(f"Planes Sales: {planes_rate:.2f}%")
   st.write(f"Trains Sales: {trains_rate:.2f}%")
   st.write(f"Ships Sales: {ships_rate:.2f}%")
   
if choice == 'Finance':
   df_FQ1_sorted = df_FQ1.sort_values(by='turnover', ascending = False)
   st.header("Finances Quest 1")
   st.subheader("The turnover of the orders of the last two months by country")
   col1, col2 = st.columns(2)
   with col2:
        st.write(df_FQ1_sorted)
   with col1:
        fig, ax = plt.subplots(1,1)
        viz_bar1 = sns.barplot(data = df_FQ1_sorted,
            x = 'country',
            y = 'turnover',
            color="royalblue",
            ax = ax)
        fig.set_tight_layout(True)
        plt.xticks(rotation=45)
        plt.title('Turnover of the orders of the last two months by country')
        st.pyplot((viz_bar1.figure))
   st.header("Finances Quest 2")
   st.subheader("Orders that have not yet been paid")
   df_gb_cn = df_FQ2.groupby('customernumber').sum()
   df_gb_cn = df_gb_cn.reset_index()
   df_sorted = df_gb_cn.sort_values(by='Order_Value', ascending = False)
   df_sorted1 = df_sorted.drop(columns='ordernumber')
   col1, col2 = st.columns(2)
   with col2:
    df_sorted1
   with col1:
    fig, ax = plt.subplots(1,1, figsize = (15,10))
    viz_bar2 = sns.barplot(data=df_sorted,
                          x='customernumber',
                          y='Order_Value',
                          color='royalblue',
                          order=df_sorted["customernumber"],
                          ax = ax)
    fig.set_tight_layout(True)
    plt.xticks(rotation=45)
    plt.xlabel("Customernumber", size=15)
    plt.ylabel("Orders Value", size=15)
    plt.title('Orders that have not yet been paid, total by Client')
    st.pyplot((viz_bar2.figure))
   st.header("Orders that have not yet been paid, Detailed by client and order number")
   df_FQ2
if choice == 'Logistics':
    st.header("Logistics")
    st.subheader("The stock of the 5 most ordered products")
    df_rename = df_LQ1.rename(columns={'productName': 'Product Name', 'total_stock': 'Total Stock'})
    col1, col2 = st.columns(2)
    with col2:
       st.write(" ")
       st.write(" ")
       st.write(" ")
       st.write(" ")
       st.dataframe(df_rename, use_container_width=True)
    with col1:
       fig, ax = plt.subplots(1,1)#figsize=(12,6))
       viz_1 = sns.barplot(data = df_LQ1,
                   x = 'productName',
                   y = 'total_stock', 
                   #palette='tab10',
                   ax=ax)
       fig.set_tight_layout(True)
       plt.title("")
       plt.ylabel("Total Stock")
       plt.xlabel("")
       plt.xticks(rotation=40)
       st.pyplot(viz_1.figure)

if choice == 'Human Resources':
    st.header("Human Resources")
    st.subheader("Top 2 sellers with the highest turnover each month")
    def page_df():
       df_rename = df_HR[['sellers','monthly_turnover','date']].rename(columns={'sellers': 'Sellers', 'monthly_turnover': 'Monthly Turnover', 'date': 'Date'})
       col1, col2 = st.columns(2)
       with col1:
          st.write(" ")
          st.write(" ")
          st.write(" ")
          st.dataframe(df_rename, use_container_width=True)
          #df_pivot_sum = df_HR.pivot_table(values = 'monthly_turnover', index = 'sellers', aggfunc = 'sum')
       with col2:
          df_rel_freq = (df_HR['sellers'].value_counts()/df_HR.shape[0]*100)
          fig, ax = plt.subplots()
          ax = df_rel_freq.plot(kind='pie')
          #ax.pie(df_rel_freq, labels=list(df_HR['sellers'].unique()))
          ax.set_ylabel("")
          #ax.axis(rotation=15)
          st.pyplot(fig)
    def page_plot():
       #st.header("Plot Data")
       col1, col2 = st.columns(2)
       with col2:
          selected_date = st.select_slider('Select date',
                                        options=list(df_HR['date']))
          st.write("The selected date is:", selected_date)
          filtered_data = df_HR[df_HR['date'] == selected_date]
       with col1:
          fig, ax = plt.subplots(1,1)#,figsize=(15,5))
          sns.barplot(data = filtered_data,
                   x = 'sellers',
                   y = 'monthly_turnover', dodge=True)
          plt.title("")
          plt.ylabel("Monthly Turnover")
          plt.xlabel("Sellers")
          st.pyplot(plt.gcf())
    pages = {
       "Preview Data": page_df,
       "Plot Data": page_plot
    }
    selected_page = st.selectbox(
       "Choose Page",
       pages.keys()
    )
    pages[selected_page]()