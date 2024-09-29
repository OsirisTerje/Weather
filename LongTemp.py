import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from datetime import datetime

# Dictionary with cities and their coordinates (latitude, longitude)
cities = {
    1: ("Oslo", Point(59.9139, 10.7522)),
    2: ("Paris", Point(48.8566, 2.3522)),
    3: ("New York", Point(40.7128, -74.0060)),
    4: ("Brisbane", Point(-27.4698, 153.0251)),
    5: ("Sydney", Point(-33.8688, 151.2093)),
    6: ("Stockholm", Point(59.3293, 18.0686)),
    7: ("Kiev", Point(50.4501, 30.5234)),
    8: ("Luleå", Point(65.5841, 22.1547))  # Luleå coordinates
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

# Ask the user to specify the number of years to average (1 to 10)
years_to_average = int(input("Enter the number of years to average (1-10): "))
if years_to_average < 1 or years_to_average > 10:
    print("Invalid selection. Please choose a number between 1 and 10.")
    exit()

# Define the total span of time (5 times the average span)
total_year_span = 5 * years_to_average

# Get the current year
current_year = datetime.now().year

# Create a list of year ranges for the 5 graphs
year_ranges = [(current_year - (i + 1) * years_to_average, current_year - i * years_to_average) for i in range(5)]

# Define a function to fetch and average data for a range of years
def get_average_data(location, start_year, end_year):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    
    data = Daily(location, start, end)
    data = data.fetch()
    
    # Group by month and calculate the average temperature
    monthly_avg_temp = data.groupby(data.index.month)['tavg'].mean()
    
    return monthly_avg_temp

# Fetch and plot the data for each range
plt.figure(figsize=(10, 6))
for i, (start_year, end_year) in enumerate(year_ranges):
    avg_data = get_average_data(location, start_year, end_year)
    label = f"{start_year}-{end_year} Avg"
    plt.plot(avg_data.index, avg_data.values, label=label)

# Set plot labels and formatting
plt.xlabel('Month')
plt.ylabel('Average Temperature (°C)')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(loc='upper right')
plt.title(f'{city_name} - Average Temperature for {total_year_span} Years')
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
