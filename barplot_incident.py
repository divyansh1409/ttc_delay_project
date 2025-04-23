import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_ttc_bus_delay_data.csv')
incident_delay = df.groupby('Incident')['Min Delay'].sum().reset_index()
incident_delay = incident_delay.sort_values(by='Min Delay', ascending=False)
colors = plt.cm.Paired(range(len(incident_delay)))

plt.figure(figsize=(14, 6))
bars = plt.bar(incident_delay['Incident'], incident_delay['Min Delay'], color=colors)
plt.title('Total Delays by Incident Type', fontsize=16)
plt.xlabel('Incident Type', fontsize=12)
plt.ylabel('Total Min Delay (Minutes)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
