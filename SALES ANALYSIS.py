#!/usr/bin/env python
# coding: utf-8

# # SALES ANALYSIS

# ### Import necessary libraries

# In[ ]:


import pandas as pd 
import os
import matplotlib.pyplot as plt


# ### Merge data from each month into one CSV

# In[3]:


folder_path = 'C:/salesdata'
file_list = os.listdir(folder_path)


# In[4]:


dfs = []
for file_name in file_list:
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        dfs.append(df)


# In[5]:


df1 = pd.concat(dfs, ignore_index=True)


# In[6]:


df1


# # DATA CLEANING 

# ### CHECKING NULLS 

# In[12]:


df1.isnull().sum()


# In[7]:


df1.dropna(inplace = True)


# ### CHECKING DUPLICATES ROWS

# In[9]:


df1.duplicated().sum()


# In[10]:


df1.drop_duplicates(inplace = True)


# In[11]:


df1.describe()


# In[12]:


df1.info()


# In[13]:


df1.columns


# In[14]:


df1.columns = df1.columns.str.replace(' ', '_')


# ### CHANGE DATATYPE 

# In[15]:


df1['Order_Date'] = pd.to_datetime(df1['Order_Date'],errors='coerce')
df1['Price_Each'] = pd.to_numeric(df1['Price_Each'],errors='coerce')
df1['Quantity_Ordered'] = pd.to_numeric(df1['Quantity_Ordered'],errors='coerce')


# In[16]:


df1.info()


# In[17]:


df1.dropna(inplace = True)


# In[220]:


df1.info()


# ### ADD COLUMNS 

# In[18]:


df1['sale'] = df1['Quantity_Ordered'] * df1['Price_Each']


# In[19]:


df1['Month'] = df1['Order_Date'].dt.month


# In[20]:


df1['City'] = df1['Purchase_Address'].str.split(',').str[1]


# In[46]:


df1['Order_Time'] = df1['Order_Date'].dt.hour


# In[107]:


df1


# # Data Exploration!

# ###  Question 1: What was the best month for sales? How much was earned that month?

# In[22]:


df1.groupby('Month')[['sale']].sum().sort_values(by='sale',ascending = False).reset_index()


# In[77]:


x = range(1,13)
sales = df1.groupby('Month')[['sale']].sum()
plt.bar(x,sales['sale'],color = 'y')
plt.xticks(x)
plt.ylabel('Sales in million USD ($)')
plt.xlabel('Month number')
plt.show()


# ### Question 2: What city sold the most product?

# In[43]:


df1.groupby('City')[['Order_ID']].count().sort_values(by='Order_ID',ascending = False).rename(columns = {'Order_ID': 'Total_Product'})


# In[53]:


results2 = df1.groupby('City')[['Order_ID']].count().rename(columns = {'Order_ID': 'Total_Product'})
cities = results2.index
plt.bar(cities,results2['Total_Product'])
plt.xticks(cities,rotation='vertical',size=8)
plt.ylabel('Number of Products')
plt.xlabel('Cities')
plt.show()


# ### Question 3: What time should we display advertisemens to maximize the likelihood of customer’s buying product?

# In[48]:


df1.groupby('Order_Time')[['Order_ID']].count().sort_values(by='Order_ID',ascending= True).rename(columns = {'Order_ID': 'Total_Product'})


# In[54]:


order = df1.groupby('Order_Time')[['Order_ID']].count().rename(columns = {'Order_ID': 'Total_Product'})
x = order.index
plt.plot(x,order['Total_Product'])
plt.xticks(x)
plt.ylabel('Number of Products')
plt.xlabel('Day Hour')
plt.grid()
plt.show()


# ### Question 4: What products are most often sold together?

# In[145]:


df1['Order_ID'].nunique()


# In[167]:


temp_df1 = df1[df1['Order_ID'].duplicated(keep = False)]


# In[183]:


temp_df1['grouped'] = temp_df1.groupby('Order_ID')['Product'].transform(lambda x: ','.join(x))


# In[184]:


df2 = temp_df1.drop_duplicates(subset=['Order_ID','grouped'])


# In[186]:


df2.groupby('grouped')['Product'].count().reset_index().sort_values(by='Product',ascending = False).rename(columns={'Product':'sold'})


# ### Question 5: What product sold the most? 

# In[194]:


df1.groupby('Product')['sale'].sum().reset_index().sort_values(by='sale',ascending = False)


# In[75]:


results3 = df1.groupby('Product')['sale'].sum().reset_index()
Products = results3['Product']
plt.bar(Products,results3['sale'],color = 'g')
plt.ylabel('Sales in million USD ($)')
plt.xlabel('Product)')
plt.xticks(Products,rotation='vertical',size=8)
plt.show()


# ### Question 6: What are the total profits and total sales per quarter?

# In[83]:


df1['quarter'] = df1['Month'].apply(lambda x: 'Q1' if x in [1,2,3] else 'Q2' if x in [4,5,6] else 'Q3' if x in [7,8,9] else 'Q4')


# In[91]:


quarter_data = df1.groupby('quarter')[['sale']].sum().reset_index().sort_values(by='sale',ascending = False)
total_sales = df1['sale'].sum()


# In[96]:


quarter_data['percentage'] = round((quarter_data['sale'] / total_sales) * 100 , 2)


# In[103]:


x = quarter_data['quarter']
y = quarter_data['sale'] 
plt.pie(y, labels=x, autopct='%1.1f%%')
plt.title('Sales Distribution by Quarter')
plt.show()

