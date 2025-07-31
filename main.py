import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

def show_price_graph(dataframe, destination):
    dataframe['flight_datetime'] = pd.to_datetime(dict(
        year=dataframe.year,
        month=dataframe.month,
        day=dataframe.day_in_month,
        hour=dataframe.hour
    ))

    sorted_df = dataframe.sort_values(by="flight_datetime")
    min_row = sorted_df.loc[sorted_df['predicted price'].idxmin()]

    # פתיחת חלון גדול
    graph_window = tk.Toplevel(root)
    graph_window.title("📈 Flight Price Analysis")
    graph_window.geometry("1400x1000")
    graph_window.configure(bg="#34495e")

    tk.Label(graph_window, text=f"Price Analysis to {destination}",
             font=("Helvetica", 20, "bold"),
             bg="#34495e", fg="#1abc9c").pack(pady=15)

    # תיאור קצר
    tk.Label(graph_window, text=(
        "📊 What You See:\n"
        "• Top Left: Price over time\n"
        "• Top Right: Price vs. days in advance\n"
        "• Bottom Left: Price by part of day\n"
        "• Bottom Right: Price by day of week"
    ), font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1").pack(pady=5)

    # יצירת 4 גרפים ברורים
    fig, axs = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # גרף 1 - Price Over Time (עם 3 טיסות הכי זולות)
    axs[0, 0].scatter(sorted_df['flight_datetime'], sorted_df['predicted price'],
                      color='skyblue', s=40, alpha=0.8, label='Predicted Price')

    # מציאת 3 הטיסות הזולות ביותר
    top_3_cheapest = sorted_df.nsmallest(3, 'predicted price')

    # הוספת כוכבים ותוויות לכל אחת משלוש הטיסות הזולות
    for i, row in top_3_cheapest.iterrows():
        axs[0, 0].scatter(row['flight_datetime'], row['predicted price'],
                          color='red', s=120, marker='*')
        axs[0, 0].annotate(f"${row['predicted price']}",
                           (row['flight_datetime'], row['predicted price']),
                           textcoords="offset points", xytext=(0, -15), ha='center',
                           fontsize=10, color='red', fontweight='bold')

    axs[0, 0].set_title("Price Over Time", fontsize=14)
    axs[0, 0].set_xlabel("Date", fontsize=12)
    axs[0, 0].set_ylabel("Price ($)", fontsize=12)
    axs[0, 0].tick_params(axis='x', rotation=30)
    axs[0, 0].legend()
    axs[0, 0].grid(True, linestyle='--', alpha=0.5)

    # גרף 2 - מחיר לעומת ימים מראש
    axs[0, 1].scatter(sorted_df['days_before_departure'], sorted_df['predicted price'],
                     alpha=0.6, color='orange')
    axs[0, 1].set_title("Price vs. Days Before Departure", fontsize=14)
    axs[0, 1].set_xlabel("Days Before", fontsize=12)
    axs[0, 1].set_ylabel("Price ($)", fontsize=12)
    axs[0, 1].grid(True)

    # גרף 3 - מחיר לפי חלק ביום
    part_labels = ['Early\nNight', 'Morning', 'Noon', 'Afternoon', 'Evening', 'Late\nNight']
    axs[1, 0].boxplot([sorted_df[sorted_df['part_of_day'] == i]['predicted price'] for i in range(1, 7)],
                     labels=part_labels)
    axs[1, 0].set_title("Price by Part of Day", fontsize=14)
    axs[1, 0].set_xlabel("Part of Day", fontsize=12)
    axs[1, 0].set_ylabel("Price ($)", fontsize=12)

    # גרף 4 - מחיר לפי יום בשבוע
    day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    axs[1, 1].boxplot([sorted_df[sorted_df['day_of_week'] == i]['predicted price'] for i in range(7)],
                      labels=day_labels)
    axs[1, 1].set_title("Price by Day of Week", fontsize=14)
    axs[1, 1].set_xlabel("Day", fontsize=12)
    axs[1, 1].set_ylabel("Price ($)", fontsize=12)

    # הצגת הגרפים
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


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

def find_best_dates():
    try:
        destination = destination_entry.get().strip().upper()
        start_date = datetime.strptime(start_date_entry.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end_date_entry.get(), "%Y-%m-%d")

        if start_date > end_date:
            raise ValueError("Start date must be before end date.")

        num_samples = 2000
        data_generator = features_generator_by_time(
            start_date_entry.get(), end_date_entry.get(),
            destination, num_samples)

        predicted_prices = model.predict(data_generator)
        data_generator['predicted price'] = predicted_prices.round(2)

        top_3 = data_generator.sort_values(by='predicted price').head(3)

        # === חלון חדש להצגת תוצאות ===
        result_window = tk.Toplevel(root)
        result_window.title("🛫 Cheapest Flights")
        result_window.configure(bg="#34495e")
        result_window.geometry("600x550")

        tk.Label(result_window, text="Top 3 Cheapest Flights", font=("Helvetica", 18, "bold"),
                 bg="#34495e", fg="#1abc9c").pack(pady=15)

        for index, row in top_3.iterrows():
            flight_date = datetime(int(row['year']), int(row['month']), int(row['day_in_month']))
            date_str = flight_date.strftime('%A, %d %B %Y')
            time_str = f"{int(row['hour']):02d}:00"

            details = (
                f"🗓️ Date: {date_str}\n"
                f"🕐 Time: {time_str}\n"
                f"📍 Destination: {destination}\n"
                f"📊 Predicted Price: ${row['predicted price']}\n"
                f"🧩 Info: {'Weekend' if row['is_weekend'] else 'Weekday'}, "
                f"{'Summer' if row['is_summer'] else 'Not summer'}, "
                f"{'Holiday' if row['is_holiday'] else 'Regular day'}\n"
                f"📅 Days Before Departure: {int(row['days_before_departure'])}"
            )

            frame = tk.Frame(result_window, bg="#2c3e50", bd=2, relief="groove")
            frame.pack(fill="x", padx=20, pady=10)

            label = tk.Label(frame, text=details, font=("Helvetica", 13), justify="left",
                             bg="#2c3e50", fg="#ecf0f1", anchor="w")
            label.pack(fill="both", padx=10, pady=10)
        show_price_graph(data_generator, destination)


    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input:\n{e}")

search_button = tk.Button(root, text="🔍 Find Best Dates", font=("Helvetica", 16, "bold"),
                          bg="#1abc9c", fg="black", activebackground="#16a085",
                          padx=20, pady=10, command=find_best_dates)
search_button.pack(pady=20)

# ===== הפעלת הממשק =====
root.mainloop()
