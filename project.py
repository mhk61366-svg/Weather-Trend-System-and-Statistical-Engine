import pandas as pd
import matplotlib.pyplot as plt
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

    def convert_data(self):
        if self.weather_data is not None:
            self.weather_data['dt'] = pd.to_datetime(self.weather_data['dt'])
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


#-----------------------Testing section(proper Menu not made Yet)-----------------------
weather_set = Weather_Visualizer()

# Load data
weather_set.stats_obj.load_data()
print("Data Frame Dimensions before cleaning: ")
print(weather_set.stats_obj.weather_data.shape)

# Clean data
weather_set.stats_obj.clean_data()
print("Data Frame Dimensions after cleaning: ")
print(weather_set.stats_obj.weather_data.shape)

# Convert date column
weather_set.stats_obj.convert_data()
print(weather_set.stats_obj.weather_data.head()) 

# Statistical functions
print(weather_set.stats_obj.average_temp().head())
print(weather_set.stats_obj.avg_uncertainity().head())
print(weather_set.stats_obj.sd_temp().head())
print(weather_set.stats_obj.variance_temp().head())

# Graph
# weather_set.avg_temp_graph()

weather_set.sd_country()
