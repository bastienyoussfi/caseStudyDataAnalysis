import pandas as pd
import matplotlib.pyplot as plt

# Let's first read the different tables
rentals = pd.read_csv("Dataset/rentals_table.csv")
customers = pd.read_csv("Dataset/customers_table.csv")
trailers = pd.read_csv("Dataset/trailers_table.csv")

# ----------------------------------------------------------------------------- #

# Here is the query using groupby to count trailers for each make
trailer_count_per_company = trailers.groupby('make').size().reset_index(name='available_trailer_count')

print("Here is how many trailers are available per make:\n", trailer_count_per_company, "\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# To compute the distribution of trailer capacities, we first need to choose a bin size, 50 seemed reasonnable
bin_size = 50

# We use the cut function to segment the values into bins and we then use the function count in order to count the values in each bin
capacity_distribution = trailers.groupby(pd.cut(trailers['capacity'], range(0, int(trailers['capacity'].max()) + bin_size, bin_size)), observed=False)['capacity'].count().reset_index(name='bin_capacity')
capacity_distribution.columns = ['capacity', 'count']

# Sort the distribution by capacity
capacity_distribution = capacity_distribution.sort_values(by='capacity')

print("Here is the trailer capacity distribution with a bin_size of ", bin_size, ":\n", capacity_distribution, "\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# We calculate the average duration of trailer rentals with the mean function
average_trailer_duration = rentals['duration'].mean()

print("The average duration of trailer rentals is ", average_trailer_duration, "days.\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# We first calculate the count of rentals for each trailer
rentals_count = rentals['trailer_id'].value_counts().reset_index()
rentals_count.columns = ['trailer_id', 'rental_count']

# We then sort the rentals count in descending order to get the most popular ones
rentals_count = rentals_count.sort_values(by='rental_count', ascending=False)

# Finally we select the top three most rented trailers
top_three_rented = rentals_count.head(3)

print("The 3 most frequently rented trailers are:\n", top_three_rented, "\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# Count the occurrences of each trailer make
make_distribution = trailers['make'].value_counts()

# Plotting the distribution of trailer makes with pyplot
plt.figure(figsize=(10, 6))
make_distribution.plot(kind='bar', color='blue')
plt.title('Distribution of Trailer Makes')
plt.xlabel('Trailer Make')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("./fig1")
plt.close()

# ----------------------------------------------------------------------------- #

# Plotting the distribution of rental durations with pyplot
plt.figure(figsize=(10, 6))
plt.hist(rentals['duration'], color='red')
plt.title('Distribution of Rental Durations')
plt.xlabel('Duration')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("./fig2")

# ----------------------------------------------------------------------------- #

# Group by 'trailer_id' and find the minimum rental date and maximum return date for each trailer
first_renting_date = rentals.groupby('trailer_id')['rental_date'].min().reset_index()
last_return_date = rentals.groupby('trailer_id')['return_date'].max().reset_index()

# Convert the str in order to be able to use operators on them
first_renting_date['rental_date'] = pd.to_datetime(first_renting_date['rental_date'])
last_return_date['return_date'] = pd.to_datetime(last_return_date['return_date'])


# Creating a new dataframe to store our result
usage = pd.DataFrame()
usage['available time'] = last_return_date['return_date']-first_renting_date['rental_date']

# Creating a new dataframe to store the total rental duration of each trailer
rental_duration = [0] * 10
rentals['rental_date'] = pd.to_datetime(rentals['rental_date'])
rentals['return_date'] = pd.to_datetime(rentals['return_date'])

# Calculate the rental period for each rental
rentals['rental_period'] = rentals['return_date'] - rentals['rental_date']

# Sum the rental periods to get the total rental duration
total_rental_duration_per_trailer = rentals.groupby('trailer_id')['rental_period'].sum().reset_index(name='total time')

# Divide the total time the trailers were rented by the total time of life of the trailer
usage['utilization rate'] = total_rental_duration_per_trailer['total time'].div(usage['available time'])

print("Here is the average utilization rate of trailers:\n", usage, "\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# Merge rental data with customer data based on 'customer_id'
merge = pd.merge(rentals, customers, on='customer_id', how='inner')

# Group by customer industry and calculate the count of rentals for each industry
rental_demand_trends = merge.groupby('industry').size().reset_index(name='rental_count')

print("Here are the rental demand trends across different customer industries:\n", rental_demand_trends, "\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# For this question let's consider only the first 10 trailers
current_year = 2024

# Calculate the age of each trailer
age = pd.DataFrame()
age['trailer_age'] = current_year - trailers['year'][:10]

# Merge trailer data with rental data based on 'trailer_id'
merge = pd.merge(rentals, trailers, on='trailer_id', how='inner')

# Analyze the correlation between trailer age and rental duration
correlation = age['trailer_age'].corr(merge['duration'])

print("Here is the correlation coefficient between the age of the trailer and its usage: ", correlation, "\nIt doesn't seem to be correlated.\n-----------------------------------------------------------------------------")

# ----------------------------------------------------------------------------- #

# Let's first convert 'start_time' to datetime objects and extract month and year
rentals['start_time'] = pd.to_datetime(rentals['rental_date'])
rentals['rental_month'] = rentals['rental_date'].dt.month
rentals['rental_year'] = rentals['rental_date'].dt.year

# Let's then merge the rentals data with the customers data in order to have both time and locations
merge = pd.merge(rentals, customers, on='customer_id', how='inner')

# Let's then group by location
demand_based_on_location = merge.groupby(['country', 'rental_year', 'rental_month']).size().reset_index(name='Rental count')

print("Here are the seasonal patterns in rental demand based on customer locations:\n", demand_based_on_location.sort_values(by=['rental_year', 'rental_month']), "\nAfter seeing the results, I do not feel like there is any sort of seasonal patterns in trailer rental.\n-----------------------------------------------------------------------------")

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

print("Here is the profitability of the different industries:\n", prof, "\nWe see that the Manufacturing industry has the most profitable rentals as their ratio is the lowest.\n-----------------------------------------------------------------------------")