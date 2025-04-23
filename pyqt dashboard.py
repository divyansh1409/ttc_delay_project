import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox,
    QPushButton, QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import folium
from collections import Counter
import webbrowser
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def generate_and_open_folium_map(df):
    top_locations = df['Location'].value_counts().loc[lambda x: x > 5].nlargest(30).index
    df_filtered = df[df['Location'].isin(top_locations)].copy()

    location_summary = df_filtered.groupby("Location").agg({
        "Min Delay": "mean",
        "Incident": lambda x: Counter(x.dropna()).most_common(1)[0][0]
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
            radius=max(row["Min Delay"] / 2, 3),
            popup=f"{row['Location']}<br>Avg Delay: {row['Min Delay']:.1f} mins<br>Top Incident: {row['Incident']}",
            color="blue",
            fill=True,
            fill_color="crimson" if row["Incident"] == "Security" else "orange",
            fill_opacity=0.7
        ).add_to(map_ttc)

    map_path = "ttc_delay_map.html"
    map_ttc.save(map_path)
    webbrowser.open(map_path)

class TTCFullDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TTC Delay Analysis Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        self.df = None
        self.canvas = FigureCanvas(plt.Figure())
        self.status_label = QLabel("No file loaded.")

        self.dropdown = QComboBox()
        self.dropdown.addItems([
            "Select visualization",
            "1. Total Delay by Incident",
            "2. Top 10 Routes - Bar Plot",
            "3. Min Delay vs Min Gap - Scatter Plot",
            "4. Delay by Route and Incident - Stacked Bar",
            "5. Top 10 Routes - Heatmap",
            "6. Scatter Matrix - Delay, Gap, Hour, Direction",
            "7. Animated Bar Chart Race (Snapshot)",
            "8. Geospatial Bubble Plot (Static)"
        ])
        self.dropdown.currentTextChanged.connect(self.update_plot)
        self.load_button = QPushButton("Load Dataset")
        self.load_button.clicked.connect(self.load_data)

        self.save_button = QPushButton("Save Plot")
        self.save_button.clicked.connect(self.save_plot)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("TTC Delay Visualizations"))
        layout.addWidget(self.load_button)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.canvas)
        self.map_button = QPushButton("Open Interactive Folium Map")
        self.map_button.clicked.connect(self.open_map)
        layout.addWidget(self.map_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.df = pd.read_csv(file_path)
                else:
                    self.df = pd.read_excel(file_path)

                self.df["Hour"] = pd.to_datetime(self.df["Time"], format="%H:%M").dt.hour
                self.df["Date"] = pd.to_datetime(self.df["Date"])
                self.df["Week"] = self.df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
                self.df["Direction"] = self.df["Direction"].astype("category")
                self.status_label.setText(f"Loaded: {file_path}")
                self.update_plot(self.dropdown.currentText())
            except Exception as e:
                self.status_label.setText(f"Failed to load file: {str(e)}")

    def update_plot(self, choice):
        if self.df is None or choice == "Select visualization":
            return

        self.canvas.figure.clear()

        if choice == "6. Scatter Matrix - Delay, Gap, Hour, Direction":
            sample_df = self.df[["Min Delay", "Min Gap", "Hour", "Direction"]].dropna().sample(1000)
            sns.pairplot(sample_df, hue="Direction", diag_kind="hist", palette="Set2")
            plt.suptitle("Scatter Matrix: Delay, Gap, Hour, Direction", y=1.02)
            plt.show()
            return

        ax = self.canvas.figure.add_subplot(111)

        if choice == "1. Total Delay by Incident":
            data = self.df.groupby("Incident")["Min Delay"].sum().reset_index().sort_values(by="Min Delay", ascending=False)
            ax.bar(data["Incident"], data["Min Delay"], color=plt.cm.Paired(range(len(data))))
            ax.set_title("Total Delays by Incident Type")
            ax.set_xlabel("Incident")
            ax.set_ylabel("Total Min Delay")
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        elif choice == "2. Top 10 Routes - Bar Plot":
            data = self.df.groupby("Route")["Min Delay"].sum().nlargest(10).reset_index()
            sns.barplot(x="Route", y="Min Delay", data=data, ax=ax)
            ax.set_title("Top 10 Routes with Most Delays")
            ax.set_xlabel("Route")
            ax.set_ylabel("Total Min Delay")

        elif choice == "3. Min Delay vs Min Gap - Scatter Plot":
            df_filtered = self.df.copy()
            for col in ["Min Delay", "Min Gap"]:
                q1, q3 = df_filtered[col].quantile([0.25, 0.75])
                iqr = q3 - q1
                df_filtered = df_filtered[(df_filtered[col] >= q1 - 1.5 * iqr) & (df_filtered[col] <= q3 + 1.5 * iqr)]
            sns.scatterplot(data=df_filtered, x="Min Delay", y="Min Gap", ax=ax)
            ax.set_title("Min Delay vs Min Gap")
            ax.set_xlabel("Min Delay")
            ax.set_ylabel("Min Gap")

        elif choice == "4. Delay by Route and Incident - Stacked Bar":
            grouped = self.df.groupby(["Route", "Incident"])["Min Delay"].sum().unstack().fillna(0)
            top_routes = grouped.sum(axis=1).sort_values(ascending=False).head(10).index
            grouped.loc[top_routes].plot(kind="bar", stacked=True, ax=ax, colormap="Set3")
            ax.set_title("Delays by Route and Incident Type (Top 10 Routes)")
            ax.set_xlabel("Route")
            ax.set_ylabel("Total Min Delay")
            ax.legend(title="Incident", bbox_to_anchor=(1.05, 1), loc="upper left")

        elif choice == "5. Top 10 Routes - Heatmap":
            data = self.df.groupby("Route")["Min Delay"].sum().nlargest(10).to_frame().T
            sns.heatmap(data, cmap="YlOrRd", annot=True, fmt=".0f", ax=ax, cbar_kws={"label": "Total Delay"})
            ax.set_title("Top 10 Routes - Delay Heatmap")
            ax.set_ylabel("")
            ax.set_xlabel("Route")

        elif choice == "7. Animated Bar Chart Race (Snapshot)":
            grouped = self.df.groupby(["Week", "Route"]).size().reset_index(name="DelayCount")
            top_routes = grouped.groupby("Route")["DelayCount"].sum().nlargest(10).index
            grouped = grouped[grouped["Route"].isin(top_routes)]
            pivot = grouped.pivot(index="Week", columns="Route", values="DelayCount").fillna(0).cumsum()
            snapshot = pivot.iloc[0].sort_values(ascending=False).head(10)
            ax.barh(snapshot.index.astype(str), snapshot.values, color="skyblue")
            ax.set_title(f"TTC Route Delay Race (Snapshot: {pivot.index[0].strftime('%b %d')})")
            ax.set_xlabel("Cumulative Delays")
            ax.set_ylabel("Route")

        elif choice == "8. Geospatial Bubble Plot (Static)":
            top_locs = self.df["Location"].value_counts().nlargest(10).index
            filtered = self.df[self.df["Location"].isin(top_locs)]
            loc_summary = filtered.groupby("Location").agg({
                "Min Delay": "mean",
                "Incident": lambda x: Counter(x).most_common(1)[0][0]
            }).reset_index()
            ax.barh(loc_summary["Location"], loc_summary["Min Delay"],
                    color=["crimson" if inc == "Security" else "orange" for inc in loc_summary["Incident"]])
            ax.set_title("Avg Delay by Location (Top 10)")
            ax.set_xlabel("Average Delay")
            ax.set_ylabel("Location")

        self.canvas.draw()

    def save_plot(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;PDF Files (*.pdf)")
        if file_path:
            self.canvas.figure.savefig(file_path)
            self.status_label.setText(f"Saved to: {file_path}")
    def open_map(self):
        if self.df is not None:
            generate_and_open_folium_map(self.df)
        else:
            self.status_label.setText("Please load the dataset first.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TTCFullDashboard()
    window.show()
    sys.exit(app.exec_())
