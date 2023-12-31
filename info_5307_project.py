# -*- coding: utf-8 -*-
"""INFO_5307_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-cuMrpUYU-iz3-hkhHWV8nXOPxcijTRG

**Step 1:**
* Using Pandas for data manipulation and Plotly Express for visualization, both
crucial tools for data analysis in Python.
* This will enable us to handle the dataset and create insightful visualizations to tackle Walmart's inventory management issues.
"""

import pandas as pd
from datetime import datetime
import plotly.express as px
import pandas as pd

"""**Step 2:**
* Reading a CSV file named 'walmart.csv' using Pandas and then reducing the dataset to the first 50,000 rows before saving it as 'walmart_trim.csv'.
* Trimming the dataset might be a practical approach to start analyzing a smaller subset for faster processing or to focus on specific portions of the data. This step helped streamline the exploratory analysis by working with a manageable subset.
"""

data = pd.read_csv('walmart.csv',encoding= 'latin-1')
data = data[:50000]
data.to_csv('walmart_trim.csv',index= False)

#printing columns/features from the dataset
print(data.columns)

"""**Step 3:**
* Mapping the numerical store IDs to their corresponding store names, converting the 'Date' column to a datetime format, and then deriving additional features like 'day_of_week', 'month', and 'year' from the date.
* This transformation is quite helpful as it allows for better analysis based on specific time-related trends such as sales patterns across different days, months, and years. Understanding the temporal aspects of sales data is crucial for inventory management, especially in recognizing seasonal variations and periodic trends.
"""

store_mapping = {1: 'Store_1', 2: 'Store_2', 3: 'Store_3',4:'Store_4',5:'Store_5',6:'Store_6',None: 'Null'}  # Add more mappings as needed
data['Store'] = data['Store'].map(store_mapping)
data['Date'] = pd.to_datetime(data['Date'])
data['day_of_week'] = data['Date'].dt.strftime('%A')
data['month'] = data['Date'].dt.month_name()
data['year'] = data['Date'].dt.year

"""**Step 4:**
* Performed some significant data cleaning steps.
* Tried to refine the dataset by filtering rows based on specific criteria, such as selecting the top modes of shipping, regions, and states that have higher occurrences.
* Additionally,handled missing or erroneous values in the 'unit_price', 'sales', and 'Dept' columns by converting them to numeric types, dropping NaN values, and ensuring data consistency by converting 'sales' to float and 'Dept' to string type.

* Cleaning the data is a crucial step in preparing it for analysis. By removing irrelevant or inconsistent entries and ensuring data integrity, you're setting the foundation for more accurate and reliable insights into Walmart's inventory management.
"""

print('Data Before Cleaning: {}'.format(len(data)))
# Data Cleaning
clean_data = data[data['ship_mode'].isin(list(data['ship_mode'].value_counts().keys())[:3])]
clean_data = clean_data[clean_data['region'].isin(list(data['region'].value_counts().keys())[:4])]
clean_data = clean_data[clean_data['state'].isin(list(data['state'].value_counts().keys())[:50])] # considering top 40 states
numeric_column = pd.to_numeric(clean_data['unit_price'], errors='coerce')
clean_data = clean_data[numeric_column.notna()]
numeric_column2 = pd.to_numeric(clean_data['sales'], errors='coerce')
clean_data = clean_data[numeric_column2.notna()]
clean_data = clean_data[clean_data['Dept']!='nan']
clean_data.dropna(subset=['Dept'], inplace=True)
clean_data['sales'] = clean_data['sales'].astype(float)
clean_data['Dept'] = clean_data['Dept'].astype(str)
print('Data After Cleaning: {}'.format(len(clean_data)))

"""**Step 5:**
* Selected specific columns relevant to inventory management and created a subset named 'inventory_data'. Truncating the 'product_name' column to the first 25 characters could facilitate easier analysis and visualization. Additionally, isolated data for the years 2011 and 2012 in the 'yearly_data' subset, possibly for analyzing trends or patterns over these years.

* By narrowing down to essential columns and focusing on specific years, I'm aiming for more targeted insights into inventory-related trends and sales patterns during those periods. This refined dataset will likely streamline the subsequent exploratory analysis for inventory management solutions
"""

inventory_related_columns = ['Date','Dept', 'Weekly_Sales', 'product_container', 'product_name', 'product_sub_category', 'sales', 'ship_date', 'ship_mode', 'unit_price','Store','day_of_week','month','year','state','region','zip_code','profit', 'MarkDown1']
inventory_data = clean_data[inventory_related_columns]
inventory_data['product_name'] = inventory_data['product_name'].str.slice(0, 25)
yearly_data = inventory_data[(inventory_data['year']==2012)|(inventory_data['year']==2011)] # for monthly usage purpose
inventory_data.head()

"""**Step 6:**
* The below code inventory_data.shape aims to display the dimensions of the 'inventory_data' DataFrame.
* This command will provide the number of rows and columns present in the dataset, offering a quick overview of the size and structure of the selected inventory-related columns.
"""

inventory_data.shape

"""# ***Exploratory Data Analysis and Visualization***
### **What are the Top-selling 15 Products by Count in Walmart's Sales Data?**
* The bar chart below showcases the top 20 products by count, indicating the frequency of sales for each product.
* This analysis provides crucial insights into the most frequently sold products at Walmart.


"""

product_counts = inventory_data['product_name'].value_counts().head(15)

fig = px.bar(product_counts, x=product_counts.index, y=product_counts.values,
labels={'x': 'Product Name', 'y': 'Count'},
title='Product Level Analysis'
)

fig.update_layout(xaxis_title_text='Product Name', yaxis_title_text='Count')
fig.show()

"""###**Which product categories consistently exhibit high sales, indicating a need for increased inventory stocking to maximize revenue?**"""

# Calculating total sales per product sub-category
sales_by_subcategory = inventory_data.groupby('product_sub_category')['sales'].sum().sort_values(ascending=False)

# Selecting top 10 product sub-categories by sales
top_10_subcategories = sales_by_subcategory.head(10)

# Creating a pie chart to visualize sales by product sub-category
fig = px.pie(names=top_10_subcategories.index, values=top_10_subcategories.values,
             title='Top 10 Product Sub-Categories by Sales')
fig.show()

"""### **How Do Profits Vary Across Different Product categories at Walmart?**
*  The line graph depicts the total profits amassed from sales in various product subcategories.
*  Analyzing profits per subcategory offers insights into the revenue generation potential of different product categories.
"""

inventory_data['profit'] = inventory_data['profit'].astype(float)
category_profit_counts = inventory_data.groupby(['product_sub_category']).agg({'profit':'sum'}).reset_index()
px.line(category_profit_counts,x='product_sub_category',y='profit',markers=True,title= 'Product Categories and Profitability')

"""###**How Does Sales Volume Vary Across Different Shipping Modes Throughout the Year at Walmart?**
*  The scatter plot showcases the sales count for various shipping modes across different months of the year.
*  This analysis illuminates how the volume of sales via different shipping modes fluctuates monthly.
*  Understanding these variations aids in optimizing shipping strategies and resource allocation.
"""

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
yearly_data['month'] = pd.Categorical(yearly_data['month'], categories=month_order, ordered=True)
shipping_month_counts = yearly_data.groupby(['month','ship_mode']).agg({'sales':'count'}).reset_index()
shipping_month_counts.columns = ['month','ship_mode','count']
fig = px.scatter(shipping_month_counts, x="month", y="count", color="ship_mode",
                 size='count',title= 'Shipping Mode vs Month Analysis')
fig.show()

"""### **Which product categories generate highest profits across different stores at Walmart?**
*  The grouped bar chart represents the total sales volume for different product categories across each store.
*  This analysis provides insights into the sales distribution across stores for various product categories.
*  Understanding these variations helps Walmart identify stores performing exceptionally well or needing improvement in specific product categories.
"""

store_counts = inventory_data.groupby(['Store','product_sub_category']).agg({'profit':'sum'}).reset_index()
store_counts.columns = ['Store','product_sub_category','sales']
fig = px.bar(store_counts, x="Store", y="sales", color="product_sub_category", title="Profits generated by different Product Categories across Stores", barmode='group')
fig.show()

"""### **How Do Monthly Sales Vary Across Different Stores Throughout the Year at Walmart?**

*  The line plot visualizes the total sales trends for each store across different months of the year.
*  This analysis highlights the variations in sales performance over time for individual stores.
*  Understanding monthly sales patterns aids in identifying seasonal trends, pinpointing months of higher or lower sales for each store.
"""

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
yearly_data['month'] = pd.Categorical(yearly_data['month'], categories=month_order, ordered=True)
yearly_data['sales']= yearly_data['sales'].astype(float)
store_month_counts = yearly_data.groupby(['Store','month']).agg({'sales':'sum'}).reset_index()
store_month_counts.columns = ['Store','month','count']
fig = px.line(store_month_counts, x="month", y="count", color="Store",category_orders={'month': month_order},markers = True,title= 'Store-level Monthly Sales Analysis')
fig.update_traces(textposition="bottom right")
fig.show()

"""### **How Does Profits Vary Across Different Departments in different states at Walmart?**
*  The scatter plot showcases total profits generated by department across various states.
*  Different states exhibit varying preferences for specific departments.
*  Understanding which departments perform better in particular states assists in regional inventory management strategies.
"""

inventory_data['profit'] = inventory_data['profit'].astype(float)
inventory_data['Dept'] = inventory_data['Dept'].astype(str)
state_dept = inventory_data.groupby(['state','Dept']).agg({'profit':'sum'}).reset_index()
fig = px.scatter(state_dept, x="state", y="profit", color="Dept",title='State-Departmental Analysis by Profits')
fig.show()

"""###**How can we identify popular products across different regions to optimize inventory?**

* By analyzing the sales data across various regions, we've identified the top-selling products.
*  Understanding these preferences can help in tailoring inventory allocation.
*  I've pinpointed the most sought-after product categories. Prioritizing these categories in inventory stocking could enhance sales and customer satisfaction.



"""

region_category_sales = inventory_data.groupby(['region', 'product_sub_category']).agg({'sales': 'sum'}).reset_index()
top_regions = region_category_sales.groupby('region')['sales'].sum().nlargest(5).index
top_categories = region_category_sales.groupby('product_sub_category')['sales'].sum().nlargest(10).index

filtered_data = region_category_sales[region_category_sales['region'].isin(top_regions) & region_category_sales['product_sub_category'].isin(top_categories)]

fig = px.bar(filtered_data, x="region", y="sales", color="product_sub_category", title="Regional-level Sale Analysis by Product Categories", barmode='group')
fig.show()