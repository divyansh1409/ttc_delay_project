import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('cleaned_ttc_bus_delay_data.csv')

# Group by Route and Incident type, summing up Min Delay
route_incident_delay = df.groupby(['Route', 'Incident'])['Min Delay'].sum().unstack().fillna(0)

# Sort by total delay for each route and select the top 10 routes
top_10_routes = route_incident_delay.sum(axis=1).sort_values(ascending=False).head(10).index
top_10_route_incident_delay = route_incident_delay.loc[top_10_routes]

# Create the plot
fig, ax = plt.subplots(figsize=(16, 8))
top_10_route_incident_delay.plot(kind='bar', stacked=True, figsize=(16, 8), colormap='Set3', ax=ax)

# Title and labels
ax.set_title('Total Delays by Route and Incident Type (Top 10 Routes)', fontsize=16)
ax.set_xlabel('Route', fontsize=12)
ax.set_ylabel('Total Min Delay (Minutes)', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

# Move the legend outside the plot
ax.legend(title="Incident Types", loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

# Adjust layout to make space for the legend and prevent extra empty figure
plt.tight_layout()

# Show the plot
plt.show()
