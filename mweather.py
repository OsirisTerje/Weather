import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Point, Monthly
from datetime import datetime

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

# Define the time period (last 5 years)
years = 5
end_year = datetime.now().year
start_year = end_year - years
start = datetime(start_year, 1, 1)
end = datetime(end_year, 12, 31)

# Get the data for the selected city
data = Monthly(location, start, end)
data = data.fetch()

# Resample data to monthly averages and group by year
data['year'] = data.index.year
data['month'] = data.index.month
monthly_avg = data.groupby(['year', 'month'])['tavg'].mean().unstack(0)

# Plot the graph
plt.figure(figsize=(10, 6))

for year in monthly_avg.columns:
    plt.plot(monthly_avg.index, monthly_avg[year], label=f'{year}')

# Formatting the graph
plt.title(f'Monthly Average Temperature in {city_name} (Last 5 Years)')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Year')
plt.grid(True)

# Show the plot
plt.show()
