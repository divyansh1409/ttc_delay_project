import pandas as pd

df = pd.read_excel('ttc-bus-delay-data-2024.xlsx')  
#print(df.dtypes) #to check the datatype of each column

#missing_values = df.isnull().sum() #to count the number of missing values in each column
#print(missing_values)

df['Direction'] = df['Direction'].fillna('Unknown')
df['Route'] = df['Route'].fillna('Unknown')

missing_values = df.isnull().sum()
#print(missing_values)

num_duplicates = df.duplicated().sum()
#print(num_duplicates)

df_cleaned = df.drop_duplicates()


# to save the cleaned dataframe to a new csv file
#df_cleaned.to_csv('cleaned_ttc_bus_delay_data.csv', index=False)

