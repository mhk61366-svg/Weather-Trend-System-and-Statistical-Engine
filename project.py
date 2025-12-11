import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    def hottest_countries(self):
        if self.stats_obj is not None:
            # Bar chart of top 5 hottest countries against avg temperature
            avg_temperature = self.stats_obj.average_temp()
            hottest = avg_temperature.sort_values(ascending=False).head(5)
            bar_graph = plt.bar(hottest.index,hottest.values)
            plt.xlabel("Country")
            plt.ylabel("average temprature")
            plt.title("Top 5 Hottest Countries")
            plt.show()
        else:
            print("DataFrame not found !!!")

    def coldest_countries(self):
        if self.stats_obj is not None:
            # Bar chart of top 5 coldest countries against avg temperature
            avg_temperature = self.stats_obj.average_temp()
            coldest = avg_temperature.sort_values(ascending=True).head(5)
            bar_graph = plt.bar(coldest.index,coldest.values)
            plt.title("Top 5 Coldest Countries")
            plt.xlabel("Country")
            plt.ylabel("average temprature")
            plt.show()
        else:
            print("DataFrame not found !!!")


    def sd_country(self):
        if self.stats_obj is not None:
            sd_temperature = self.stats_obj.sd_temp()
            bar_graph = plt.bar(sd_temperature.index,sd_temperature.values)
            plt.xlabel("Country")
            plt.ylabel("Standard Deviation")
            plt.title("Standard Deviation vs Country Bar Graph")
            plt.show()
        else:
            print("DataFrame not found !!!")


    def avg_temp_graph(self):
        if self.stats_obj is not None:
            # user enters a country name and function shows the graph of avg-temp/time
            x = input("Enter country name to view its graph")
            selected_country = self.stats_obj.weather_data[self.stats_obj.weather_data["Country"] == x]
            if selected_country.empty:
                print("Country not found!")
                return

            graph = plt.plot(selected_country["dt"],selected_country["AverageTemperature"])
            plt.xlabel("Date")
            plt.ylabel("Average Temperature")
            plt.title(f"Temperature Trend of {x}")
            plt.show()
        else:
            print("DataFrame not found !!!")

    def scatter_plot_graph(self):
        if self.stats_obj is not None:
            # Take only one row per country (with lat/long)
            unique_countries = self.stats_obj.weather_data.groupby("Country").first().reset_index()
            avg_temp = self.stats_obj.average_temp().reset_index()
            avg_temp.columns = ["Country", "AvgTemp"]

            # Merge latitude/longitude + avg temperature into one dataframe
            merged = pd.merge(unique_countries, avg_temp, on="Country", how="inner")
            if merged is not None:
                plt.figure(figsize=(10, 6))

                plt.scatter(merged["Longitude"],merged["Latitude"],c = merged["AvgTemp"],cmap="coolwarm",alpha=0.7)
                plt.colorbar(label = "Average Temperature")
                plt.xlabel("Longitude")
                plt.ylabel("Latitude")
                plt.title("Scatter Plot of Latitude vs Longitude (Colored by Avg Temp)")
                plt.show()
            else:
                print("Could not plot graph")
        else:
            print("DataFrame not found !!!")

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
    report = Weather_Report()
    
    # Load and prepare data
    report.stats_DataFrame.load_data()
    report.stats_DataFrame.clean_data()
    report.stats_DataFrame.convert_date()

    while True:
        print("\n---------- WEATHER ANALYSIS MENU ----------")
        print("1. Statistical Analysis")
        print("2. Graphical Analysis")
        print("3. Weather Report")
        print("4. Exit")
        try:
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                statistical_analysis_menu(report)
            elif choice == "2":
                graphical_analysis_menu(report)
            elif choice == "3":
                weather_report_menu(report)
            elif choice == "4":
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Enter 1-4.")
        except:
            print("Wrong Input")

# Statistical Analysis Submenu
def statistical_analysis_menu(report):
    while True:
        print("\n--- STATISTICAL ANALYSIS ---")
        print("a. Average Temperature")
        print("b. Average Uncertainty")
        print("c. Standard Deviation")
        print("d. Variance Temperature")
        print("e. Back to Main Menu")

        choice = input("Enter your choice (a-e): ").lower()

        if choice == "a":
            print(report.stats_DataFrame.average_temp())
        elif choice == "b":
            print(report.stats_DataFrame.avg_uncertainity())
        elif choice == "c":
            print(report.stats_DataFrame.sd_temp())
        elif choice == "d":
            print(report.stats_DataFrame.variance_temp())
        elif choice == "e":
            break
        else:
            print("Invalid choice. Enter a-e.")

# Graphical Analysis Submenu
def graphical_analysis_menu(report):
    graphs = Weather_Visualizer()
    graphs.stats_obj.load_data()
    graphs.stats_obj.clean_data()
    graphs.stats_obj.convert_date()

    while True:
        print("\n--- GRAPHICAL ANALYSIS ---")
        print("a. Global Temperature Trend over Time")
        print("b. Average Temperature (Bar Graph)")
        print("c. Standard Deviation (Bar Graph)")
        print("d. Hotspots Map using Latitude and Temperature")
        print("e. Back to Main Menu")
        try:
            choice = input("Enter your choice (a-e): ").lower()

            if choice == "a":
                # Line plot: average global temperature over months
                graphs.avg_temp_graph()

            elif choice == "b":
                # top 5 hottest/coldest average
                print("Average Temprature for Top 5 hottest countries Bar graph ")
                graphs.hottest_countries()
                print("Average Temprature for Top 5 coldest countries Bar graph ")
                graphs.coldest_countries()

            elif choice == "c":
                # Standard deviation bar graph
                graphs.sd_country()

            elif choice == "d":
                # Hotspots map
                graphs.scatter_plot_graph()
            elif choice == "e":
                break
            else:
                print("Invalid choice. Enter a-e.")
        except:
            print("Invalid Input Error !!!")
            


# Weather Report Submenu
def weather_report_menu(report):
    while True:
        print("\n--- WEATHER REPORT ---")
        print("a. Top 5 Hottest country")
        print("b. Top 5 Coldest country")
        print("c. Hottest month in each country")
        print("d. Coldest month in each country")
        print("e. Back to Main Menu")

        choice = input("Enter your choice (a-e): ").lower()

        if choice == "a":
            print(report.top_5_hottest())
        elif choice == "b":
            print(report.top_5_coldest())
        elif choice == "c":
            print(report.hottest_month_each_country())
        elif choice == "d":
            print(report.coldest_month_each_country())
        elif choice == "e":
            break
        else:
            print("Invalid choice. Enter a-e.")


# Run the program
if __name__ == "__main__":
    main_menu()
    
