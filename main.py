import pandas as pd
import matplotlib.pyplot as plt

# Reading the different tables
rentals = pd.read_csv("Dataset/rentals_table.csv")
customers = pd.read_csv("Dataset/customers_table.csv")
trailers = pd.read_csv("Dataset/trailers_table.csv")

# ----------------------------------------------------------------------------- #

# Query using groupby to count trailers for each make
trailer_count_per_company = trailers.groupby('make').size().reset_index(name='available_trailer_count')

print(trailer_count_per_company)

# ----------------------------------------------------------------------------- #

# Compute the distribution of trailer capacities
bin_size = 50

capacity_distribution = trailers.groupby(pd.cut(trailers['capacity'], range(0, int(trailers['capacity'].max()) + bin_size, bin_size)), observed=False)['capacity'].count().reset_index(name='bin_capacity')
capacity_distribution.columns = ['capacity', 'count']

# Sort the distribution by capacity
capacity_distribution = capacity_distribution.sort_values(by='capacity')

print(capacity_distribution)

# ----------------------------------------------------------------------------- #

# Calculate the average duration of trailer rentals
average_trailer_duration = rentals['duration'].mean()

print(average_trailer_duration)

# ----------------------------------------------------------------------------- #

# Calculate the count of rentals for each trailer
rentals_count = rentals['trailer_id'].value_counts().reset_index()
rentals_count.columns = ['trailer_id', 'rental_count']

# Sort the rentals count in descending order
rentals_count = rentals_count.sort_values(by='rental_count', ascending=False)

# Select the top three most rented trailers
top_three_rented = rentals_count.head(3)

print(top_three_rented)

# ----------------------------------------------------------------------------- #

# Count the occurrences of each trailer make
make_distribution = trailers['make'].value_counts()

# Plotting the distribution of trailer makes
plt.figure(figsize=(10, 6))
make_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution of Trailer Makes')
plt.xlabel('Trailer Make')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------- #

# Plotting the distribution of rental durations
plt.figure(figsize=(10, 6))
plt.hist(rentals['duration'], bins=20, color='skyblue')
plt.title('Distribution of Rental Durations')
plt.xlabel('Duration')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------- #

