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

# Add hour, day, and month columns
data['hour'] = data.index.hour
data['month'] = data.index.month
data['day'] = data.index.date

# ---- CORRECTING DAYS AND HOURS WITH PRECIPITATION ----

# Convert the 'day' column back into a DatetimeIndex for easier grouping by month
data['day'] = pd.to_datetime(data['day'])

# Group by day and calculate total precipitation for each day
daily_precip = data.groupby('day')['prcp'].sum()

# Extract the month from the DatetimeIndex and assign it to daily_precip
daily_precip.index = pd.to_datetime(daily_precip.index)

# Group by month and count the number of days with precipitation > 0
days_with_precip = daily_precip.groupby(daily_precip.index.month).apply(lambda x: (x > 0).sum())

# Total precipitation for each month
total_precipitation = data.groupby('month')['prcp'].sum()

# Count the number of hours with precipitation by month
hours_with_precip = data[data['prcp'] > 0].groupby('month')['prcp'].count()

# Number of days with precipitation above half the maximum
max_day_precip = data.groupby('month')['prcp'].max()
half_max_precip = max_day_precip.max() / 2
days_above_half_max_precip = daily_precip.groupby(daily_precip.index.month).apply(lambda x: (x > half_max_precip).sum())

# Max number of continuous days with precipitation above half the maximum
def max_continuous_days_above_threshold(df, threshold):
    df['above_threshold'] = df['prcp'] > threshold
    df['block'] = (df['above_threshold'] != df['above_threshold'].shift()).cumsum()
    max_cont_days = df[df['above_threshold']].groupby(['month', 'block']).size().reset_index(name='count')
    return max_cont_days.groupby('month')['count'].max()

max_cont_days = max_continuous_days_above_threshold(data, half_max_precip)

# ---- PLOTTING THE GRAPH ----

fig, ax2 = plt.subplots(figsize=(10, 6))

# Bar plot for days with precipitation
ax2.bar(days_with_precip.index, days_with_precip.values, label='Days with Precipitation', alpha=0.6, color='skyblue')

# Bar plot for days with precipitation above half the maximum
ax2.bar(days_above_half_max_precip.index, days_above_half_max_precip.values, label='Days > Half Max Precip', alpha=0.6, color='dodgerblue')

# Bar plot for maximum continuous days with precipitation above half the maximum
ax2.bar(max_cont_days.index, max_cont_days.values, label='Max Continuous Days > Half Max Precip', alpha=0.6, color='darkblue')

# Add total precipitation and number of hours labels above each bar
for i in range(1, 13):  # Loop over all months
    if i in total_precipitation.index and i in days_with_precip.index and i in hours_with_precip.index:
        total_precip = total_precipitation[i]
        precip_hours = hours_with_precip[i]
        ax2.text(i, days_with_precip[i] + 0.5, f'{total_precip:.2f} mm, {precip_hours} hrs', ha='center')
    else:
        ax2.text(i, 1, 'No data', ha='center')

# Add number of days as labels on the max continuous days bar plot
for i, v in max_cont_days.items():
    if pd.notna(v):
        ax2.text(i, v + 0.2, str(v), ha='center')

# Formatting the graph
ax2.set_xlabel('Month')
ax2.set_ylabel('Number of Days', color='black')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax2.legend(loc='upper right')
ax2.grid(True)

# Show the graph
plt.tight_layout()
plt.show()
