#DIVYANSH AGRAWAL
#Ahnaf Shahriyar Chowdhury

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

df = pd.read_csv('cleaned_ttc_bus_delay_data.csv')

#data statistics
route_delay = df.groupby('Route')['Min Delay'].sum().reset_index()
top10_routes = route_delay.sort_values(by='Min Delay', ascending=False).head(10)
summary_stats = top10_routes['Min Delay'].describe().round(2)
print(summary_stats)

#data distribution
plt.figure(figsize=(12, 6))
plt.hist(df['Min Delay'], bins=15, color='blue', alpha=0.7)
plt.title('Distribution of Total Delays Across Routes')
plt.xlabel('Total Min Delay (Minutes)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


#data statistics
Q1_delay = df['Min Delay'].quantile(0.25)
Q3_delay = df['Min Delay'].quantile(0.75)
IQR_delay = Q3_delay - Q1_delay
Q1_gap = df['Min Gap'].quantile(0.25)
Q3_gap = df['Min Gap'].quantile(0.75)
IQR_gap = Q3_gap - Q1_gap
lower_bound_delay = Q1_delay - 1.5 * IQR_delay
upper_bound_delay = Q3_delay + 1.5 * IQR_delay

lower_bound_gap = Q1_gap - 1.5 * IQR_gap
upper_bound_gap = Q3_gap + 1.5 * IQR_gap
df_cleaned = df[(df['Min Delay'] >= lower_bound_delay) & (df['Min Delay'] <= upper_bound_delay)]
df_cleaned = df_cleaned[(df_cleaned['Min Gap'] >= lower_bound_gap) & (df_cleaned['Min Gap'] <= upper_bound_gap)]
summary_stats_delay = df_cleaned['Min Delay'].describe()
summary_stats_gap = df_cleaned['Min Gap'].describe()

print("Summary Statistics for Min Delay:")
print(summary_stats_delay)
print("\nSummary Statistics for Min Gap:")
print(summary_stats_gap)


# data statistics
incident_delay_stats = df.groupby('Incident')['Min Delay'].describe().round(2)
print(incident_delay_stats)

#data distribution
plt.figure(figsize=(14, 8))
for incident in df['Incident'].unique():
    subset = df[df['Incident'] == incident]
    plt.hist(subset['Min Delay'], bins=20, alpha=0.5, label=incident)
plt.title('Histogram of Delays by Incident Type', fontsize=16)
plt.xlabel('Min Delay (Minutes)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(title='Incident Types')

plt.tight_layout()
plt.show()

#data statistics
summary_stats = df['Min Delay'].describe().round(2)
print(summary_stats)

#data distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Min Delay'], bins=20, color='blue', alpha=0.7)
plt.title('Distribution of Delays (Min Delay)')
plt.xlabel('Min Delay (Minutes)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()


#data statistics
top_locations = df['Location'].value_counts().nlargest(30).index
df_filtered = df[df['Location'].isin(top_locations)].copy()

location_summary = df_filtered.groupby("Location").agg({
    "Min Delay": "mean",
    "Incident": lambda x: Counter(x).most_common(1)[0][0]
}).reset_index()
location_summary_stats = location_summary['Min Delay'].describe().round(2)
print(location_summary_stats)

#data distribution
plt.figure(figsize=(10, 6))
plt.hist(location_summary['Min Delay'], bins=15, color='blue', alpha=0.7)
plt.title('Distribution of Min Delay Across Locations')
plt.xlabel('Min Delay (Minutes)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()


#data statistics
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
weekly_data = df.groupby(["Week", "Route"]).size().reset_index(name="DelayCount")
delay_count_stats = weekly_data['DelayCount'].describe().round(2)
print(delay_count_stats)

#data distribution
plt.figure(figsize=(10, 6))
plt.hist(weekly_data['DelayCount'], bins=15, color='lightblue', edgecolor='black')
plt.title('Distribution of Delay Counts Across Routes (Weekly)')
plt.xlabel('Number of Delays')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()


#data statistics
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
df["Direction"] = df["Direction"].astype("category")
sample_df = df[["Min Delay", "Min Gap", "Hour", "Direction"]].dropna().sample(1000, random_state=42)
numerical_stats = sample_df[['Min Delay', 'Min Gap', 'Hour']].describe().round(2)
print(numerical_stats)
