import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Point, Monthly
from datetime import datetime

# Define the location for Oslo (latitude, longitude)
oslo = Point(59.9139, 10.7522)

# Define the time period (last 5 years)
years = 5
end_year = datetime.now().year
start_year = end_year - years
start = datetime(start_year, 1, 1)
end = datetime(end_year, 12, 31)

# Get the data for each year
data = Monthly(oslo, start, end)
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
plt.title('Monthly Average Temperature in Oslo (Last 5 Years)')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Year')
plt.grid(True)

# Show the plot
plt.show()
