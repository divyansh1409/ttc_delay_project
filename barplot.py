import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('cleaned_ttc_bus_delay_data.csv')
route_delay = df.groupby('Route')['Min Delay'].sum().reset_index()
top10_routes = route_delay.sort_values(by='Min Delay', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x='Route', y='Min Delay', data=top10_routes)
plt.title('Top 10 Routes with the Most Delays')
plt.xlabel('Route')
plt.ylabel('Total Min Delay (Minutes)')
plt.xticks(rotation=45) 
plt.tight_layout()  
plt.show()




