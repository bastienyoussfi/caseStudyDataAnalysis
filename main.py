import pandas as pd 

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
capacity_distribution = trailers['capacity'].value_counts().reset_index()
capacity_distribution.columns = ['capacity', 'count']

# Sort the distribution by capacity
capacity_distribution = capacity_distribution.sort_values(by='capacity')

print(capacity_distribution)

# ----------------------------------------------------------------------------- #

# Calculate the average duration of trailer rentals

average_trailer_duration = rentals['duration'].mean()

print(average_trailer_duration)