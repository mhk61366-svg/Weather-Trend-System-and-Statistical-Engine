import pandas as pd

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
            self.weather_data['dt'] = pd.to_datetime(self.weather_data['dt'], format='%d/%m/%Y')
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

weather_set = Statistical_Engine()
weather_set.load_data()
print("Data Frame Dimensions before cleaning: ")
print(weather_set.weather_data.shape)
weather_set.clean_data()
print("Data Frame Dimensions after cleaning: ")
# print shape of the attribute weather_data of Object weather set
print(weather_set.weather_data.shape)

weather_set.convert_data()
print(weather_set.weather_data.head())  # check if date conversions went well

print(weather_set.average_temp())