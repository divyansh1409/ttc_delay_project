import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation

df = pd.read_csv("cleaned_ttc_bus_delay_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
weekly_data = df.groupby(["Week", "Route"]).size().reset_index(name="DelayCount")

# Get top 10 routes overall
top_routes = weekly_data.groupby("Route")["DelayCount"].sum().nlargest(10).index
weekly_data = weekly_data[weekly_data["Route"].isin(top_routes)]
pivot_df = weekly_data.pivot(index="Week", columns="Route", values="DelayCount").fillna(0).cumsum()

fig, ax = plt.subplots(figsize=(10, 6))

def update(frame):
    ax.clear()
    data = pivot_df.iloc[frame].sort_values(ascending=False).head(10)
    ax.barh(data.index, data.values, color="skyblue")
    ax.set_xlim(0, data.max() + 10)
    ax.set_title(f"TTC Route Delay Race - Week of {pivot_df.index[frame].strftime('%b %d')}")
    ax.set_xlabel("Cumulative Delays")
    ax.set_ylabel("Route")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

ani = animation.FuncAnimation(fig, update, frames=len(pivot_df), repeat=False, interval=500)

ani.save("bar_chart_race_routes.gif", writer="pillow")
print("Saved animated GIF as bar_chart_race_routes.gif")
