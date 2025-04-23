#DIVYANSH AGRAWAL
#Ahnaf Shahriyar Chowdhury

import pandas as pd

#to check the datatype of each column
df = pd.read_csv('ttc-bus-delay-data-2024.csv')  
print(df.dtypes) 

#to count the number of missing values in each column
missing_values = df.isnull().sum() 
print(missing_values)

# to fill the missing values for 'Direction' and 'Route' columns with 'Unknown'
df['Direction'] = df['Direction'].fillna('Unknown')
df['Route'] = df['Route'].fillna('Unknown')


# to count the number of duplicate rows
num_duplicates = df.duplicated().sum()
print(num_duplicates)

# to remove duplicate rows and update the dataframe in df_cleaned
df_cleaned = df.drop_duplicates()
print(df_cleaned.head())

# to save the cleaned dataframe to a new Excel file
df_cleaned.to_csv('cleaned_ttc_bus_delay_data.csv', index=False)

#to count the number of missing values in each column
df2=pd.read_excel('cleaned_ttc_bus_delay_data.xlsx')
missing_values2 = df2.isnull().sum() 
print(missing_values2)

num_duplicates2 = df2.duplicated().sum()
print(num_duplicates2)
