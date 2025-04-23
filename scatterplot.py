import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('cleaned_ttc_bus_delay_data.csv')

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

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Min Delay', y='Min Gap', data=df_cleaned, color='blue')
plt.title('Min Delay vs. Min Gap')
plt.xlabel('Min Delay (Minutes)')
plt.ylabel('Min Gap (Minutes)')
plt.tight_layout()
plt.show()

