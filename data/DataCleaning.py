import pandas as pd

# הרחבת ההגדרות להצגה מלאה של עמודות
pd.set_option('display.max_columns', None)  # מציג את כל העמודות
pd.set_option('display.width', 1000)        # מרחיב את רוחב ההדפסה
pd.set_option('display.max_colwidth', None) # מציג את כל תוכן התא

df = pd.read_csv('flight_prices_extended.csv')
print(df.head(10))

columns = ["origin", "destination", "year", "month", "hour", "part_of_day", "day_of_week", "is_weekend",
           "is_summer", "is_holiday", "days_before_departure", "price"]

cleaned_data = pd.DataFrame(columns=columns)
print(cleaned_data)


df['search_datetime'] = pd.to_datetime(df['search_datetime'])
df['year'] = df['search_datetime'].dt.year
df['month'] = df['search_datetime'].dt.month
df['hour'] = df['search_datetime'].dt.hour

# part of day embedded by [1:morning, 2:noon, 3:afternoon, 4:evening, 5:night, 6:midNight]
def part_of_day(hour):
    if 5 <= hour < 12:
        return 1  # morning
    elif 12 <= hour <= 16:
        return 2  # noon
    elif 16 < hour <= 19:
        return 3  # afternoon
    elif 19 < hour <= 22:
        return 4  # evening
    elif hour >= 22 or hour <= 2:
        return 5  # night
    elif 2 < hour < 5:
        return 6  # midnight

df['part_of_day'] = df['hour'].apply(part_of_day)
df['day_of_week'] = df['search_datetime'].dt.dayofweek

def is_weekend(day):
    return 1 if day in [5, 6] else 0

df['is_weekend'] = df['day_of_week'].apply(is_weekend)

def is_summer(month):
    return 1 if month in [6, 7, 8] else 0
df['is_summer'] = df['month'].apply(is_summer)

import holidays
israel_holidays = holidays.country_holidays('IL')
df['is_holiday'] = df['search_datetime'].dt.date.apply(lambda date: int(date in israel_holidays))

# הסרה של כל תו שהוא לא ספרה או פסיק או נקודה
df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).astype(float)

cleaned_data = df[columns].copy()
cleaned_data.to_csv('cleaned_data.csv', index=False)

print(cleaned_data.head(15))
