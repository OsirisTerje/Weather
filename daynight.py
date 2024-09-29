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
    7: ("Kiev", Point(50.4501, 30.5234)),
    8: ("Luleå", Point(65.5841, 22.1547))  # Added Luleå with its coordinates
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

# Ask the user to specify a year
year = int(input("Enter the year (e.g., 2022): "))
if year < 1970 or year > datetime.now().year:
    print("Invalid year. Please select a valid year between 1970 and the current year.")
    exit()

# Define the time period (for the selected year)
start = datetime(year, 1, 1)
end = datetime(year, 12, 31)

# Get the hourly data for the selected city
data = Hourly(location, start, end)
data = data.fetch()

# Check if data is empty
if data.empty:
    print(f"No data available for {city_name} in {year}.")
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

# Max and Min for daytime
max_day_temp = daytime.groupby('month')['temp'].max()
min_day_temp = daytime.groupby('month')['temp'].min()

# Max and Min for nighttime
max_night_temp = nighttime.groupby('month')['temp'].max()
min_night_temp = nighttime.groupby('month')['temp'].min()

# Calculate the temperature differences between day and night
temp_diff = daytime_avg - nighttime_avg

# Calculate the average, max, and min difference, and the months in which they occur
avg_diff = temp_diff.mean()
max_diff = temp_diff.max()
min_diff = temp_diff.min()
max_diff_month = temp_diff.idxmax()  # Month with max difference
min_diff_month = temp_diff.idxmin()  # Month with min difference

# Month names
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
max_diff_month_name = month_names[max_diff_month - 1]
min_diff_month_name = month_names[min_diff_month - 1]

# Find the months with max/min for day and night
max_day_month = month_names[max_day_temp.idxmax() - 1]
min_day_month = month_names[min_day_temp.idxmin() - 1]
max_night_month = month_names[max_night_temp.idxmax() - 1]
min_night_month = month_names[min_night_temp.idxmin() - 1]

# Plot the results
plt.figure(figsize=(10, 6))

# Plot daytime temperatures
plt.plot(daytime_avg.index, daytime_avg.values, label='Daytime Avg Temp', color='orange')

# Plot nighttime temperatures
plt.plot(nighttime_avg.index, nighttime_avg.values, label='Nighttime Avg Temp', color='blue')

# Formatting the graph
plt.title(f'Daytime and Nighttime Average Temperatures in {city_name} ({year})')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.xticks(ticks=range(1, 13), labels=month_names)
plt.legend()
plt.grid(True)

# Adjust the plot to make space on the right for the text block
plt.subplots_adjust(right=0.75)

# Add text block to the right, outside the graph
plt.text(1.05, 0.5, 
         f'Avg Temp Diff: {avg_diff:.2f}°C\n'
         f'Max Diff: {max_diff:.2f}°C ({max_diff_month_name})\n'
         f'Min Diff: {min_diff:.2f}°C ({min_diff_month_name})\n\n'
         f'Max Day Temp: {max_day_temp.max():.2f}°C ({max_day_month})\n'
         f'Min Day Temp: {min_day_temp.min():.2f}°C ({min_day_month})\n'
         f'Max Night Temp: {max_night_temp.max():.2f}°C ({max_night_month})\n'
         f'Min Night Temp: {min_night_temp.min():.2f}°C ({min_night_month})', 
         fontsize=10, bbox=dict(facecolor='white', alpha=0.5),
         transform=plt.gca().transAxes,  # Position relative to axis
         verticalalignment='center', horizontalalignment='left')  # Align in the center to the right of the graph

# Show the plot
plt.show()
