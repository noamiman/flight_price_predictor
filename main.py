import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
import pandas as pd
import joblib

model, feature_columns = joblib.load('src/flight_price_model.pkl')
pd.set_option('display.max_columns', None)  # הצג את כל העמודות
pd.set_option('display.max_rows', None)     # הצג את כל השורות
# ===== יצירת חלון =====
root = tk.Tk()
root.title("Flight Price Predictor")
root.geometry("600x500")
root.configure(bg="#2c3e50")

# ===== כותרת =====
title = tk.Label(root, text="✈️ Flight Price Optimizer", font=("Helvetica", 24, "bold"), fg="#1abc9c", bg="#2c3e50")
title.pack(pady=30)

# ===== מסגרת קלטים =====
form = tk.Frame(root, bg="#2c3e50")
form.pack(pady=10)

# ===== יעד =====
tk.Label(form, text="Destination:", font=("Helvetica", 16), fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=0, sticky="e", pady=10, padx=10)
destination_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
destination_entry.grid(row=0, column=1, padx=10)

# ===== תאריך התחלה =====
tk.Label(form, text="Start Date (YYYY-MM-DD):", font=("Helvetica", 16), fg="#ecf0f1", bg="#2c3e50").grid(row=1, column=0, sticky="e", pady=10, padx=10)
start_date_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
start_date_entry.grid(row=1, column=1, padx=10)

# ===== תאריך סיום =====
tk.Label(form, text="End Date (YYYY-MM-DD):", font=("Helvetica", 16), fg="#ecf0f1", bg="#2c3e50").grid(row=2, column=0, sticky="e", pady=10, padx=10)
end_date_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
end_date_entry.grid(row=2, column=1, padx=10)

# ===== תוצאות =====
result_label = tk.Label(root, text="", font=("Helvetica", 16), fg="#f1c40f", bg="#2c3e50", justify="left")
result_label.pack(pady=20)


def features_generator_by_time(startTime, endTime, destination, num_samples):
    destinations = ['LON', 'NYC', 'PAR', 'BER', 'AMS', 'BCN', 'ROM', 'ATH', 'BKK', 'DXB']
    destination_map = {
        destination: i for i, destination in enumerate(destinations)
    }

    start_time_DT = datetime.strptime(startTime, "%Y-%m-%d")
    end_time_DT = datetime.strptime(endTime, "%Y-%m-%d")
    delta = end_time_DT - start_time_DT

    columns = ["year", "month", "day_in_month", "hour", "part_of_day", "day_of_week",
               "is_weekend", "is_summer", "is_holiday", "days_before_departure", "destination_encoded"]
    df = pd.DataFrame(columns=columns)
    for i in range(num_samples):
        des_num = destination_map[destination]
        random_date_range = random.randint(0, delta.days)
        random_date = start_time_DT + timedelta(days=random_date_range)
        year = random_date.year
        month = random_date.month
        day = random_date.day
        hour = random.randint(0, 23)
        part_of_day = random.randint(1, 6)
        day_of_week = random.randint(0, 6)
        is_weekend = random.randint(0, 1)
        is_summer = random.randint(0, 1)
        is_holiday = random.randint(0, 1)
        days_before_departure = random.randint(1, 180)

        df_new_row = pd.DataFrame([{
            "year": year,
            "month": month,
            "day_in_month": day,
            "hour": hour,
            "part_of_day": part_of_day,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "is_summer": is_summer,
            "is_holiday": is_holiday,
            "days_before_departure": days_before_departure,
            "destination_encoded": des_num

        }])
        df = pd.concat([df, df_new_row], ignore_index=True)
    return df

# ===== כפתור חיפוש =====
def find_best_dates():
    try:
        destination = destination_entry.get().strip().upper()
        start_date = datetime.strptime(start_date_entry.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end_date_entry.get(), "%Y-%m-%d")

        if start_date > end_date:
            raise ValueError("Start date must be before end date.")
        num_samples = 100
        data_generator = features_generator_by_time(start_date_entry.get(), end_date_entry.get(),
                                                    destination, num_samples)
        predicted_prices = model.predict(data_generator)
        data_generator['predicted price'] = predicted_prices.round(2)
        top_3_cheapest = data_generator.sort_values(by='predicted price').head(3)
        print(top_3_cheapest)
    #columns[destination:[0-9],year[2025],month[1-12],hour[0-23],part_of_day[1-6],
        # day_of_week[1-7],is_weekend[1/0],is_summer[1/0],
        # is_holiday[1/0],days_before_departure[1-180]]
    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input:\n{e}")


search_button = tk.Button(root, text="🔍 Find Best Dates", font=("Helvetica", 16, "bold"),
                          bg="#1abc9c", fg="black", activebackground="#16a085",
                          padx=20, pady=10, command=find_best_dates)
search_button.pack(pady=20)

# ===== הפעלת הממשק =====
root.mainloop()
