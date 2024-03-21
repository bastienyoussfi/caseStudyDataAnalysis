import pandas as pd
import matplotlib.pyplot as plt

# Let's first read the different tables
rentals = pd.read_csv("Dataset/rentals_table.csv")
customers = pd.read_csv("Dataset/customers_table.csv")
trailers = pd.read_csv("Dataset/trailers_table.csv")

# ----------------------------------------------------------------------------- #

# Here is the query using groupby to count trailers for each make
trailer_count_per_company = trailers.groupby('make').size().reset_index(name='available_trailer_count')

# print(trailer_count_per_company)

# ----------------------------------------------------------------------------- #

# Compute the distribution of trailer capacities
bin_size = 50

capacity_distribution = trailers.groupby(pd.cut(trailers['capacity'], range(0, int(trailers['capacity'].max()) + bin_size, bin_size)), observed=False)['capacity'].count().reset_index(name='bin_capacity')
capacity_distribution.columns = ['capacity', 'count']

# Sort the distribution by capacity
capacity_distribution = capacity_distribution.sort_values(by='capacity')

# print(capacity_distribution)

# ----------------------------------------------------------------------------- #

# Calculate the average duration of trailer rentals
average_trailer_duration = rentals['duration'].mean()

# print(average_trailer_duration)

# ----------------------------------------------------------------------------- #

# Calculate the count of rentals for each trailer
rentals_count = rentals['trailer_id'].value_counts().reset_index()
rentals_count.columns = ['trailer_id', 'rental_count']

# Sort the rentals count in descending order
rentals_count = rentals_count.sort_values(by='rental_count', ascending=False)

# Select the top three most rented trailers
top_three_rented = rentals_count.head(3)

# print(top_three_rented)

# ----------------------------------------------------------------------------- #

# Count the occurrences of each trailer make
make_distribution = trailers['make'].value_counts()

# Plotting the distribution of trailer makes
plt.figure(figsize=(10, 6))
make_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution of Trailer Makes')
plt.xlabel('Trailer Make')
plt.ylabel('Count')
plt.tight_layout()
# plt.show()

# ----------------------------------------------------------------------------- #

# Plotting the distribution of rental durations
plt.hist(rentals['duration'], color='skyblue')
plt.title('Distribution of Rental Durations')
plt.xlabel('Duration')
plt.ylabel('Frequency')
plt.tight_layout()
# plt.show()

# ----------------------------------------------------------------------------- #

# Group by 'trailer_id' and find the minimum rental date and maximum return date for each trailer
first_renting_date = rentals.groupby('trailer_id')['rental_date'].min().reset_index()
last_return_date = rentals.groupby('trailer_id')['return_date'].max().reset_index()

rental_duration = [0] * 10
rentals['rental_date'] = pd.to_datetime(rentals['rental_date'])
rentals['return_date'] = pd.to_datetime(rentals['return_date'])

# Calculate the rental period for each rental
rentals['rental_period'] = rentals['return_date'] - rentals['rental_date']

# Sum the rental periods to get the total rental duration
total_rental_duration_per_trailer = rentals.groupby('trailer_id')['rental_period'].sum()

# print("Total Rental Duration:", total_rental_duration_per_trailer)

# ----------------------------------------------------------------------------- #

# Merge rental data with customer data based on 'customer_id'
merge = pd.merge(rentals, customers, on='customer_id', how='inner')

# Group by customer industry and calculate the count of rentals for each industry
rental_demand_trends = merge.groupby('industry').size().reset_index(name='rental_count')

# print(rental_demand_trends)

# ----------------------------------------------------------------------------- #

# For this question we'll consider the first 10 trailers

# ----------------------------------------------------------------------------- #

# Convert 'start_time' to datetime objects and extract month and year
rentals['start_time'] = pd.to_datetime(rentals['rental_date'])
rentals['rental_month'] = rentals['rental_date'].dt.month
rentals['rental_year'] = rentals['rental_date'].dt.year

# Let's then merge the rentals data with the customers data in order to have both time and locations
merge = pd.merge(rentals, customers, on='customer_id', how='inner')

# Let's then group by location
demand_based_on_location = merge.groupby(['country', 'rental_year', 'rental_month']).size().reset_index(name='Rental count')

# print(demand_based_on_location.sort_values(by=['rental_year', 'rental_month']))

# ----------------------------------------------------------------------------- #

# Let's merge the customers and rentals data to see which customers have the most profitable rentals
merge = pd.merge(rentals, customers, on="customer_id", how="inner")

# Let's then group by industry and sum both the rentals duration and the total price
total_price = merge.groupby(['industry'])['rental_price_eur'].sum().reset_index(name='Total price')
total_rental_duration_per_industry = merge.groupby(['industry'])['duration'].sum().reset_index(name='Total rental duration')

# Then, let's check how profitable are each industry's rentals by diving the two columns
prof = pd.DataFrame()
prof['industry'] = total_price['industry']
prof['profitability'] = total_price['Total price'].div(total_rental_duration_per_industry['Total rental duration'])

print(prof)

# We see that the Manufacturing industry has the most profitable rentals as their ratio is the lowest