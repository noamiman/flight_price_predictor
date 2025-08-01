import pandas as pd
import numpy as np

# Generate sample data
np.random.seed(42)
num_samples = 1500

# Generate random dates within 6 months before the flight date
departure_date = pd.Timestamp("2025-09-01")
search_dates = pd.to_datetime(
    np.random.choice(pd.date_range(departure_date - pd.Timedelta(days=180), departure_date - pd.Timedelta(days=1), freq='H'), size=num_samples)
)

# Table Base
df = pd.DataFrame()
df['search_datetime'] = search_dates
df['origin'] = "TLV"
destinations = ['LON', 'NYC', 'PAR', 'BER', 'AMS', 'BCN', 'ROM', 'ATH', 'BKK', 'DXB']
df['destination'] = np.random.choice(destinations, size=num_samples)
df['days_before_departure'] = (departure_date - df['search_datetime']).dt.days
df['hour_of_day'] = df['search_datetime'].dt.hour
df['day_of_week'] = df['search_datetime'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['is_summer'] = df['search_datetime'].dt.month.isin([6, 7, 8]).astype(int)
df['is_holiday'] = df['search_datetime'].isin([
    pd.Timestamp("2025-04-17"),
    pd.Timestamp("2025-05-06"),
    pd.Timestamp("2025-09-01")
]).astype(int)

# Typical price increase in the morning and evening, decrease at night
hour_price_modifier = df['hour_of_day'].apply(
    lambda h: 15 if 7 <= h <= 10 else (10 if 17 <= h <= 20 else (-10 if 0 <= h <= 5 else 0))
)

# Calculate price including all factors
base_price = 300
price = (
    base_price
    + (90 - df['days_before_departure']) * 0.8
    + df['is_weekend'] * 20
    + df['is_summer'] * 25
    + df['is_holiday'] * 40
    + hour_price_modifier
    + np.random.normal(0, 12, size=num_samples)
)
df['price'] = price.round(2).astype(str) + " USD"

# Sort by date
df.sort_values('search_datetime', inplace=True)

# Save to file
csv_path = '/Users/noamiman/PycharmProjects/flight_price_predictor/data/flight_prices_extended.csv'
df.to_csv(csv_path, index=False)

print(df.dtypes)

