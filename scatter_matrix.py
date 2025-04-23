import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_ttc_bus_delay_data.csv")
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
df["Direction"] = df["Direction"].astype("category")

sample_df = df[["Min Delay", "Min Gap", "Hour", "Direction"]].dropna().sample(1000, random_state=42)

sns.pairplot(sample_df, hue="Direction", diag_kind="hist", palette="Set2")
plt.suptitle("Scatter Matrix: Min Delay, Gap, Hour, Direction", y=1.02)
plt.tight_layout()
plt.show()
