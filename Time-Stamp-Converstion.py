import pandas as pd
from datetime import datetime

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Load your data
df = pd.read_csv("#CSV downloaded from Extracting-Duration.py")  # replace with your actual file

# Convert timestamp columns to datetime
df['EVENT_TIMESTAMP'] = pd.to_datetime(df['EVENT_TIMESTAMP'])
df['OFF_TIMESTAMP'] = pd.to_datetime(df['OFF_TIMESTAMP'])

# Extract date and hour for grouping
df['DATE'] = df['EVENT_TIMESTAMP'].dt.date
df['HOUR'] = df['EVENT_TIMESTAMP'].dt.hour

# Create an hour interval label (e.g. 14:00–15:00)
df['HOUR_INTERVAL'] = df['HOUR'].apply(lambda h: f"{h:02d}:00–{(h+1)%24:02d}:00")

# Group by USER_ID, DATE, HOUR_INTERVAL
grouped = df.groupby(['USER_ID', 'DATE', 'HOUR_INTERVAL']).agg(
    EVENTS_COUNT=('EVENT_TIMESTAMP', 'count'),
    TOTAL_DURATION=('DURATION', 'sum')
).reset_index()

# (Optional) Fill missing hour bins with 0s for each user/date
users = df['USER_ID'].unique()
dates = df['DATE'].unique()
hours = [f"{h:02d}:00–{(h+1)%24:02d}:00" for h in range(24)]
full_index = pd.MultiIndex.from_product([users, dates, hours], names=['USER_ID', 'DATE', 'HOUR_INTERVAL'])

# Reindex to ensure all combinations exist
grouped = grouped.set_index(['USER_ID', 'DATE', 'HOUR_INTERVAL']).reindex(full_index, fill_value=0).reset_index()

# Filter for specific time intervals ("01:00–02:00" and "02:00–03:00")
filtered_df = grouped[grouped['HOUR_INTERVAL'].isin(['01:00–02:00', '02:00–03:00'])]

# Reset the index of the filtered dataframe and remove any extra indexing
filtered_df = filtered_df.reset_index(drop=True)

# Save the filtered result to a new CSV file
filtered_df.to_csv(#location.csv", index=False)


