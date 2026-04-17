import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

class load_data_set:
    def __init__(self):
        self.weather_data = None

    def load_data(self, file_path="D:\BS AI\python semester project\GlobalLandTemperaturesByCity.csv"):
        self.weather_data = pd.read_csv(file_path)
        return self.weather_data

    def clean_data(self):
        if self.weather_data is not None:
            self.weather_data = self.weather_data.dropna() # Corrected: use self.weather_data
            self.weather_data = self.weather_data.drop_duplicates() # Corrected: use self.weather_data
        else:
            print("No DataFrame found")

        return self.weather_data

    def convert_date(self):
        if self.weather_data is not None:
            self.weather_data['dt'] = pd.to_datetime(self.weather_data['dt'])
            self.weather_data["Month"] = self.weather_data["dt"].dt.month
            self.weather_data["Year"] = self.weather_data["dt"].dt.year
            self.weather_data["YearMonth"] = self.weather_data["dt"].dt.to_period("M")
        else:
            print("No DataFrame found")
        return self.weather_data


class Statistical_Engine(load_data_set):
    def __init__(self):
        super().__init__()

    def average_temp(self):
        if self.weather_data is not None:
            avg_temp = self.weather_data.groupby("Country")["AverageTemperature"].mean()
            # average temprature of a country through a period of 2 years
            return avg_temp
        else:
            print("No DataFrame found")    

    def avg_uncertainity(self):
        if self.weather_data is not None:
            avg_uncert = self.weather_data.groupby("Country")["AverageTemperatureUncertainty"].mean()
            #  average temprature of a country through a period of 2 years
            return avg_uncert
        else:
            print("No DataFrame found")  

    def sd_temp(self):
        if self.weather_data is not None:
            standard_deviation = self.weather_data.groupby("Country")["AverageTemperature"].std()
            # standard deviation of mean-monthly recorded temprature throughout 2 years
            return standard_deviation
        else:
            print("No DataFrame found")
    
    def variance_temp(self):
        if self.weather_data is not None:
            var_temp = self.weather_data.groupby("Country")["AverageTemperature"].var()
            # variance of mean-monthly recorded temprature throughout 2 years
            return var_temp
        else:
            print("No DataFrame found")

class Weather_Visualizer:
    def __init__(self) -> None:
        self.stats_obj = Statistical_Engine()

    def hottest_countries(self,ax,error_messege):
        if self.stats_obj is not None:
            # Bar chart of top 5 hottest countries against avg temperature
            avg_temperature = self.stats_obj.average_temp()
            hottest = avg_temperature.sort_values(ascending=False).head(5)
            ax.clear()
            ax.bar(hottest.index,hottest.values)
            ax.set_xlabel("Country")
            ax.set_ylabel("average temprature")
            ax.set_title("Top 5 Hottest Countries")
        else:
            error_messege.config(text="DataFrame Not Found")

    def coldest_countries(self, ax, error_message):
        if self.stats_obj is not None:
            # Bar chart of top 5 coldest countries against avg temperature
            avg_temperature = self.stats_obj.average_temp()
            coldest = avg_temperature.sort_values(ascending=True).head(5)
            ax.clear()
            ax.bar(coldest.index,coldest.values)
            ax.set_title("Top 5 Coldest Countries")
            ax.set_xlabel("Country")
            ax.set_ylabel("average temprature")
        
        else:
            error_message.config(text="DataFrame not found")


    def sd_country(self, ax, error_message):
        if self.stats_obj is not None:
            sd_temperature = self.stats_obj.sd_temp()

            if sd_temperature is None or sd_temperature.empty:
                error_message.config(text="❌ Sufficient Data not available")
                ax.clear()
                return

            # TAKE TOP 10 standard deviation countries only
            top_sd = sd_temperature.sort_values(ascending=False).head(10)

            ax.clear()
            ax.bar(top_sd.index,top_sd.values)
            ax.set_xlabel("Country")
            ax.set_ylabel("Standard Deviation")
            ax.set_title("Top 10 Countries with Highest Temperature Standard Deviation")
            ax.tick_params(axis= 'x', rotation=45)
            error_message.config(text="")
        
        else:
            error_message.config(text="DataFrame Not Found")


    def avg_temp_graph(self, ax, error_messege, country):
        if self.stats_obj is not None:
            # user enters a country name and function shows the graph of avg-temp/time
            x = country.get().strip().lower()
            selected_country = self.stats_obj.weather_data[self.stats_obj.weather_data["Country"].str.lower()== x]
            if selected_country.empty:
                error_messege.config(text="❌ Country not found!")
                ax.clear()
                return
            
            monthly_avg = selected_country.groupby("YearMonth")["AverageTemperature"].mean()
            ax.clear()
            ax.plot(monthly_avg.index.astype(str), monthly_avg.values, marker = 'o')
            ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
            ax.tick_params(axis='x', rotation= 45)
            ax.set_title(f"Temperature Trend of {x}")
            error_messege.config(text="")
        else:
            error_messege.config(text= "DataFrame Not Found")

    def scatter_plot_graph(self, ax, error_messege):
        if self.stats_obj is not None:
            unique_countries = self.stats_obj.weather_data.groupby("Country").first().reset_index()
            avg_temp = self.stats_obj.average_temp().reset_index()
            avg_temp.columns = ["Country", "AvgTemp"]

            merged = pd.merge(unique_countries, avg_temp, on="Country", how="inner")
            merged = merged[["Longitude", "Latitude", "AvgTemp"]].dropna()

            # --- FIX: Parse directional strings like "57.05N", "10.33E" ---
            def parse_coord(val):
                val = str(val).strip()
                if val[-1] in ('S', 'W'):
                    return -float(val[:-1])
                elif val[-1] in ('N', 'E'):
                    return float(val[:-1])
                else:
                    try:
                        return float(val)
                    except:
                        return float('nan')

            merged["Longitude"] = merged["Longitude"].apply(parse_coord)
            merged["Latitude"]  = merged["Latitude"].apply(parse_coord)
            merged["AvgTemp"]   = pd.to_numeric(merged["AvgTemp"], errors='coerce')
            merged = merged.dropna()
            # --------------------------------------------------------------

            if merged.empty:
                error_messege.config(text="❌ No valid numeric data to plot")
                ax.clear()
                return

            ax.clear()

            if len(ax.figure.axes) > 1:
                ax.figure.axes[-1].remove()

            hb = ax.hexbin(
                merged["Longitude"],
                merged["Latitude"],
                C=merged["AvgTemp"],
                gridsize=25,
                cmap="coolwarm"
            )

            ax.set_title("Geo Scatter Plot (Avg Temp by Country)")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.figure.colorbar(hb, ax=ax, label="°C")
            ax.relim()
            ax.autoscale_view()
            error_messege.config(text="")
        else:
            error_messege.config(text="❌ DataFrame not found")
            
class Weather_Report:
    def __init__(self) -> None:
        self.stats_DataFrame = Statistical_Engine()

    def top_5_hottest(self):
        if self.stats_DataFrame.weather_data is not None:
            avg_temp = self.stats_DataFrame.average_temp()
            hottest = avg_temp.sort_values(ascending=False).head(5)
            return hottest
        else:
            print("No DataFrame found")
            return None

    def top_5_coldest(self):
        if self.stats_DataFrame.weather_data is not None:
            avg_temp = self.stats_DataFrame.average_temp()
            coldest = avg_temp.sort_values(ascending=True).head(5)
            return coldest
        else:
            print("No DataFrame found")
            return None

    def hottest_month_each_country(self):
        if self.stats_DataFrame.weather_data is None:
            print("No DataFrame found")
            return None
        df = self.stats_DataFrame.weather_data.copy()
        # Monthly mean temperature for each country
        monthly_avg = df.groupby(["Country", "YearMonth"])["AverageTemperature"].mean()
        # Find hottest month for each country
        hottest = monthly_avg.groupby("Country").idxmax()
        hottest = hottest.apply(lambda x: str(x[1]))
        return hottest

    def coldest_month_each_country(self):
        if self.stats_DataFrame.weather_data is None:
            print("No DataFrame found")
            return None
        df = self.stats_DataFrame.weather_data.copy()
        # Monthly mean temperature
        monthly_avg = df.groupby(["Country", "YearMonth"])["AverageTemperature"].mean()
        # Find coldest month for each country
        coldest = monthly_avg.groupby("Country").idxmin()
        coldest = coldest.apply(lambda x: str(x[1]))
        return coldest

    def prediction_summary(self):
        if self.stats_DataFrame.weather_data is None:
            print("No DataFrame found")
            return None

        df = self.stats_DataFrame.weather_data.copy()
        df = df.groupby(["Country", "YearMonth"])["AverageTemperature"].mean().reset_index()
        df["YearMonth"] = df["YearMonth"].astype(str)
        predictions = []

        for country in df["Country"].unique():
            cdf = df[df["Country"] == country].sort_values("YearMonth")
            temps = cdf["AverageTemperature"].values
            n = len(temps)
            # Month indices 0..n-1
            x = np.arange(n)
            y = temps
            # Linear regression
            slope, intercept = np.polyfit(x, y, 1)
            # Predict next 3 months
            for i in range(1, 4):
                pred_temp = slope * (n + i - 1) + intercept
                # Generate month string
                last_period = pd.Period(cdf["YearMonth"].iloc[-1], freq="M")
                pred_period = last_period + i
                predictions.append({
                    "Country": country,
                    "PredictedMonth": str(pred_period),
                    "PredictedTemperature": round(pred_temp, 2)
                })

        return pd.DataFrame(predictions)
    
    
#----------------Menu-------------------#
def main_menu():
    # Create ONE dataset engine for the entire program
    stats = Statistical_Engine()

    stats.load_data()
    stats.clean_data()
    stats.convert_date()
                           
    visualizer = Weather_Visualizer()    # Share this same Dataset with visualizer & report system
    visualizer.stats_obj = stats

    report = Weather_Report()
    report.stats_DataFrame = stats

    while True:
        print("\n---------- WEATHER ANALYSIS MENU ----------")
        print("1. Statistical Analysis")
        print("2. Graphical Analysis")
        print("3. Weather Report")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            statistical_analysis_menu(stats)

        elif choice == "2":
            graphical_analysis_menu(visualizer)

        elif choice == "3":
            weather_report_menu(report)

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Enter 1-4.")


# Statistical Analysis Submenu
def statistical_analysis_menu(stats):
    while True:
        print("\n--- STATISTICAL ANALYSIS ---")
        print("a. Average Temperature")
        print("b. Average Uncertainty")
        print("c. Standard Deviation")
        print("d. Variance Temperature")
        print("e. Back to Main Menu")

        choice = input("Enter your choice (a-e): ").lower()

        if choice == "a":
            print(stats.average_temp())
        elif choice == "b":
            print(stats.avg_uncertainity())
        elif choice == "c":
            print(stats.sd_temp())
        elif choice == "d":
            print(stats.variance_temp())
        elif choice == "e":
            break

# Graphical Analysis Submenu

# Weather Report Submenu


def GUI_graphical_menu():
    stats = Statistical_Engine()
    stats.load_data()
    stats.clean_data()
    stats.convert_date()
    visualizer = Weather_Visualizer()    # Share this same Dataset with visualizer & report system
    visualizer.stats_obj = stats
    report = Weather_Report()
    report.stats_DataFrame = stats

    graphs_menu = tk.Tk()
    graphs_menu.geometry("1280x920")
    graphs_menu.resizable(False, False)
    graphs_menu.title("Graphical Analysis Report")
    graphs_menu.config(bg="#2b2b2b")
    graphs_menu.grid_columnconfigure(0, weight=1)
    graphs_menu.grid_columnconfigure(1, weight=1)

    for i in range(6):
        graphs_menu.grid_columnconfigure(i, pad=10)

    fig = Figure(figsize=(10,6), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=graphs_menu)
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=6, rowspan=2)

    # Get avg temprature Graph 
    def show_graph():
        visualizer.avg_temp_graph(ax, error_message, country)
        canvas.draw()

    # Get Scatter plot graph
    def show_scatter_graph():
        visualizer.scatter_plot_graph(ax, error_message)
        canvas.draw()
       
    # Get Hottest countries Bar graph
    def show_hottest_bargraph():
        visualizer.hottest_countries(ax, error_message)
        canvas.draw()

    # Get Coldest countries Bar graph
    def show_coldest_bargraph():
        visualizer.coldest_countries(ax, error_message)
        canvas.draw()

    # Get Standard Deviation Bar graph
    def show_sd_bargraph():
        visualizer.sd_country(ax, error_message)
        canvas.draw()

    error_message = tk.Label(graphs_menu, text="",fg= 'red', font=("Times new Roman",12))
    error_message.grid(row=3, column=2)
    prompt_country = tk.Label(graphs_menu, fg="Black", text="Enter Country Name", font=("Times new Roman",12))
    prompt_country.grid(row=0,column=0)
    country = tk.Entry(graphs_menu, fg="black",bg="lightblue", font=("Times new Roman",12))
    country.grid(row=1,column=0)
    get_graph = tk.Button(graphs_menu,text="Get Graph", font=("Times new Roman",12), command=show_graph, , fg="white", bg="#3c3f41")
    get_graph.grid(padx=10, pady=5, row=0, column=1)
    btn_scatter = tk.Button(graphs_menu, text="Scatter Plot",font=("Times new Roman",12), command=show_scatter_graph, , fg="white", bg="#3c3f41")
    btn_scatter.grid(row=0 , column=2, padx=10, pady=5)
    btn_hottest_bargraph = tk.Button(graphs_menu, text="Bar graph (hottest countries)", font=("Times new Roman",12), command=show_hottest_bargraph, , fg="white", bg="#3c3f41")
    btn_hottest_bargraph.grid(row=0, column=3, padx=10, pady=5)
    btn_coldest_bargraph = tk.Button(graphs_menu, text="Bar graph (Coldest countries)", font=("Times new Roman",12), command=show_coldest_bargraph, , fg="white", bg="#3c3f41")
    btn_coldest_bargraph.grid(row=0, column=4, padx=10, pady=5)
    btn_sd_graph = tk.Button(graphs_menu, text=" Standard deviation Bar graph", font=("Times new Roman",12), command=show_sd_bargraph, , fg="white", bg="#3c3f41")
    btn_sd_graph.grid(row=0, column=5,padx=10, pady=5)

    graphs_menu.mainloop()

def GUI_report_menu():
    stats = Statistical_Engine()
    stats.load_data()
    stats.clean_data()
    stats.convert_date()

    report = Weather_Report()
    report.stats_DataFrame = stats

    Report_GUI = tk.Tk()
    Report_GUI.geometry("1280x960")
    Report_GUI.resizable(False, False)
    Report_GUI.title("Weather Analysis Report")

    # left frame for buttons
    left_frame = tk.Frame(Report_GUI, width=320, bg="#2b2b2b")
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
    left_frame.pack_propagate(False)
    # right frame for output
    right_frame = tk.Frame(Report_GUI, bg="#1e1e1e")
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(
        left_frame, text="Weather Analysis Report",       # Heading for Buttons Menu
        bg="#2b2b2b", fg="white",
        font=("Arial", 18, "bold"), pady=20
    ).pack(fill=tk.X)

    tk.Frame(left_frame, bg="#555", height=1).pack(fill=tk.X, padx=10)  # Left Frame for Buttons 

    output_title = tk.Label(                                             # Heading for Outputs section
        right_frame, text="Select a report from the menu",
        bg="#1e1e1e", fg="#aaaaaa",
        font=("Arial", 13, "italic"), anchor="w", padx=15, pady=10
    )
    output_title.pack(fill=tk.X)

    text_frame = tk.Frame(right_frame, bg="#1e1e1e")              # Right Frame for Outputs
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_box = tk.Text(
        text_frame,
        font=("Arial", 12),
        bg="#1e1e1e", fg="#d4d4d4",
        relief=tk.FLAT, state=tk.DISABLED,
        yscrollcommand=scrollbar.set,
        padx=10, pady=10
    )
    output_box.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=output_box.yview)

    # formatting Text Inside Output Box
    def show_output(title, content_str):
        output_title.config(text=title)
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, content_str)
        output_box.config(state=tk.DISABLED)

    def format_series_table(series, col1="Country", col2="Avg Temp (°C)"):
        lines = [f"  {col1:<30} {col2}", "  " + "-" * 45]
        for idx, val in series.items():
            lines.append(f"  {str(idx):<30} {val:.2f}")
        return "\n".join(lines)

    def format_month_series(series, col2_header="Month"):
        lines = [f"  {'Country':<30} {col2_header}", "  " + "-" * 45]
        for country, month in series.items():
            lines.append(f"  {str(country):<30} {month}")
        return "\n".join(lines)

    def format_prediction_df(df):
        lines = [f"  {'Country':<30} {'Predicted Month':<18} {'Predicted Temp (°C)'}",
                 "  " + "-" * 65]
        for _, row in df.iterrows():
            lines.append(
                f"  {row['Country']:<30} {row['PredictedMonth']:<18} {row['PredictedTemperature']:.2f}"
            )
        return "\n".join(lines)

    def get_5hottest_countries():
        report_content = report.top_5_hottest()
        if report_content is not None:
            show_output("Top 5 Hottest Countries", format_series_table(report_content))

    def get_5coldest_countries():
        report_content = report.top_5_coldest()
        if report_content is not None:
            show_output("Top 5 Coldest Countries", format_series_table(report_content))

    def hottest_months():
        report_content = report.hottest_month_each_country()
        if report_content is not None:
            show_output("Hottest Month in each Country", format_month_series(report_content))

    def coldest_months():
        report_content = report.coldest_month_each_country()        
        if report_content is not None:
            show_output("Coldest Month in each Country", format_month_series(report_content))

    def get_prediction_summary():
        report_content = report.prediction_summary()
        if  report_content is not None:
            show_output("Prediction Summary (Next 3 Months)", format_prediction_df(report_content))

    hottest5_btn = tk.Button(left_frame, text="Top 5 Hottest Countries", fg="white", bg="#3c3f41", font=("Arial", 13), anchor="w", padx=15, pady=12, relief=tk.FLAT, cursor="hand2", activebackground="#4e5254", activeforeground="white", command=get_5hottest_countries)
    hottest5_btn.pack(fill=tk.X, padx=10, pady=5)
   
    coldest5_btn = tk.Button(left_frame, text="Top 5 Coldest Countries", fg="white", bg="#3c3f41", font=("Arial", 13), anchor="w", padx=15, pady=12, relief=tk.FLAT, cursor="hand2", activebackground="#4e5254", activeforeground="white", command=get_5coldest_countries)
    coldest5_btn.pack(fill=tk.X, padx=10, pady=5)
   
    hot_months_btn = tk.Button(left_frame, text="Hottest Month per Country", fg="white", bg="#3c3f41", font=("Arial", 13), anchor="w", padx=15, pady=12, relief=tk.FLAT, cursor="hand2", activebackground="#4e5254", activeforeground="white", command=hottest_months)
    hot_months_btn.pack(fill=tk.X, padx=10, pady=5)

    cold_months_btn = tk.Button(left_frame, text="Coldest Month per Country", fg="white", bg="#3c3f41", font=("Arial", 13), anchor="w", padx=15, pady=12, relief=tk.FLAT, cursor="hand2", activebackground="#4e5254", activeforeground="white", command=coldest_months)
    cold_months_btn.pack(fill=tk.X, padx=10, pady=5)
 
    prediction_btn = tk.Button(left_frame, text="Prediction Summary", fg="white", bg="#3c3f41", font=("Arial", 13), anchor="w", padx=15, pady=12, relief=tk.FLAT, cursor="hand2", activebackground="#4e5254", activeforeground="white", command=get_prediction_summary)
    prediction_btn.pack(fill=tk.X, padx=10, pady=5)
    

    Report_GUI.mainloop()

GUI_graphical_menu()
# GUI_report_menu()