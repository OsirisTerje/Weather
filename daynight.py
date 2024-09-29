import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Point, Hourly
from datetime import datetime, time

# Dictionary with cities and their coordinates (latitude, longitude)
cities = {
    1: ("Oslo", Point(59.9139, 10.7522)),
    2: ("Paris", Point(48.8566, 2.3522)),
    3: ("New York", Point(40.7128, -74.0060)),
    4: ("Brisbane", Point(-27.4698, 153.0251)),
    5: ("Sydney", Point(-33.8688, 151.2093)),
    6: ("Stockholm", Point(59.3293, 18.0686)),
    7: ("Kiev", Point(50.4501, 30.5234))
}

# Display the list of cities
print("Select a city:")
for key, (city_name, _) in cities.items():
    print(f"{key}. {city_name}")

# Get user input for city selection
selection = int(input("Enter the number of the city: "))

# Check if selection is valid
if selection not in cities:
    print("Invalid selection. Exiting.")
    exit()

# Get the selected city and its location
city_name, location = cities[selection]
print(f"You selected: {city_name}")

# Define the time period (for the last year for simplicity)
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)  # Last 1 year of data

# Get the hourly data for the selected city
data = Hourly(location, start, end)
data = data.fetch()

# Check if data is empty
if data.empty:
    print(f"No data available for {city_name}.")
    exit()

# Add hour and month columns
data['hour'] = data.index.hour
data['month'] = data.index.month

# Define day (6 AM to 6 PM) and night (6 PM to 6 AM) timeframes
daytime = data.between_time(time(6, 0), time(18, 0))
nighttime = data.between_time(time(18, 0), time(6, 0))

# Group by month and calculate average for day and night temperatures
daytime_avg = daytime.groupby('month')['temp'].mean()
nighttime_avg = nighttime.groupby('month')['temp'].mean()

# Plot the results
plt.figure(figsize=(10, 6))

# Plot daytime temperatures
plt.plot(daytime_avg.index, daytime_avg.values, label='Daytime Avg Temp', color='orange')

# Plot nighttime temperatures
plt.plot(nighttime_avg.index, nighttime_avg.values, label='Nighttime Avg Temp', color='blue')

# Formatting the graph
plt.title(f'Daytime and Nighttime Average Temperatures in {city_name} (Last Year)')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
