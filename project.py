import pandas as pd

class load_data_set:
    def __init__(self):
        self.weather_data = None

    def load_data(self, file_path="C:\Users\hp\Dekstop\Weather-Trend-System-and-Statistical\GlobalLandTemperaturesByCity.csv":
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
    
    
    
    
     


#-----------------------Testing section(proper Menu not made Yet)-----------------------
weather_set = Statistical_Engine()
weather_set.load_data()
print("Data Frame Dimensions before cleaning: ")
print(weather_set.weather_data.shape)
weather_set.clean_data()
print("Data Frame Dimensions after cleaning: ")
# print shape of the attribute weather_data of Object weather set
print(weather_set.weather_data.shape)

weather_set.convert_date()
print(weather_set.weather_data.head())  # check if date conversions went well

print(weather_set.average_temp())
print(weather_set.avg_uncertainity())
print(weather_set.sd_temp())
print(weather_set.variance_temp())

# Initialize report
report = Weather_Report()

# Load and prepare data
report.stats_DataFrame.load_data()
report.stats_DataFrame.clean_data()
report.stats_DataFrame.convert_data()

# Show top 5 hottest countries
print("Top 5 Hottest Countries:")
print(report.top_5_hottest())

# Show top 5 coldest countries
print("\nTop 5 Coldest Countries:")
print(report.top_5_coldest())
