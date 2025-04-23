import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from collections import Counter
df = pd.read_csv("cleaned_ttc_bus_delay_data.csv")

# Use only most frequent 30 locations to reduce geocoding time
top_locations = df['Location'].value_counts().nlargest(30).index
df_filtered = df[df['Location'].isin(top_locations)].copy()

location_summary = df_filtered.groupby("Location").agg({
    "Min Delay": "mean",
    "Incident": lambda x: Counter(x).most_common(1)[0][0]
}).reset_index()

geolocator = Nominatim(user_agent="ttc_delay_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

location_summary["geocode"] = location_summary["Location"].apply(geocode)
location_summary["lat"] = location_summary["geocode"].apply(lambda loc: loc.latitude if loc else None)
location_summary["lon"] = location_summary["geocode"].apply(lambda loc: loc.longitude if loc else None)

location_summary = location_summary.dropna(subset=["lat", "lon"])

map_ttc = folium.Map(location=[43.651070, -79.347015], zoom_start=11)

for _, row in location_summary.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=row["Min Delay"] / 2,  # scale bubble size
        popup=f"{row['Location']}<br>Avg Delay: {row['Min Delay']:.1f} mins<br>Top Incident: {row['Incident']}",
        color="blue",
        fill=True,
        fill_color="crimson" if row["Incident"] == "Security" else "orange",
        fill_opacity=0.7
    ).add_to(map_ttc)

map_ttc.save("ttc_delay_map.html")
print("Map saved to ttc_delay_map.html")
