# utils.py
import random
import pandas as pd
import matplotlib.pyplot as plt
import shap
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def generate_features(start_date_str, end_date_str, destination, days_before, num_samples):
    from datetime import datetime, timedelta

    destinations = ['LON', 'NYC', 'PAR', 'BER', 'AMS', 'BCN', 'ROM', 'ATH', 'BKK', 'DXB']
    destination_map = {d: i for i, d in enumerate(destinations)}

    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.strptime(end_date_str, "%Y-%m-%d")
    delta = end - start

    rows = []
    for _ in range(num_samples):
        rand_date = start + timedelta(days=random.randint(0, delta.days))
        row = {
            "year": rand_date.year,
            "month": rand_date.month,
            "day_in_month": rand_date.day,
            "hour": random.randint(0, 23),
            "part_of_day": random.randint(1, 6),
            "day_of_week": random.randint(0, 6),
            "is_weekend": random.randint(0, 1),
            "is_summer": random.randint(0, 1),
            "is_holiday": random.randint(0, 1),
            "days_before_departure": random.randint(1, days_before),
            "destination_encoded": destination_map[destination]
        }
        rows.append(row)
    return pd.DataFrame(rows)

def show_price_graph(df, destination, model, feature_columns, parent_window):
    df['flight_datetime'] = pd.to_datetime(dict(
        year=df.year, month=df.month,
        day=df.day_in_month, hour=df.hour
    ))
    sorted_df = df.sort_values(by="flight_datetime")

    window = tk.Toplevel(parent_window)
    window.title("📈 Flight Price Analysis")
    window.geometry("1400x1000")
    window.configure(bg="#34495e")

    tk.Label(window, text=f"Price Analysis to {destination}",
             font=("Helvetica", 20, "bold"),
             bg="#34495e", fg="#1abc9c").pack(pady=15)

    tk.Label(window, text=(
        "📊 What You See:\n"
        "• Top Left: Price over time\n"
        "• Top Right: Price vs. days in advance\n"
        "• Bottom Left: Price by part of day\n"
        "• Bottom Right: Price by day of week"
    ), font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1").pack(pady=5)

    fig, axs = plt.subplots(2, 2, figsize=(16, 10), dpi=100)
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # === גרף 1: Price over time
    axs[0, 0].scatter(sorted_df['flight_datetime'], sorted_df['predicted price'],
                      color='skyblue', s=40, alpha=0.8)
    top_3 = sorted_df.nsmallest(3, 'predicted price')
    for _, row in top_3.iterrows():
        axs[0, 0].scatter(row['flight_datetime'], row['predicted price'],
                          color='red', s=120, marker='*')
        axs[0, 0].annotate(f"${row['predicted price']:.0f}",
                           (row['flight_datetime'], row['predicted price']),
                           textcoords="offset points", xytext=(0, -15), ha='center',
                           fontsize=10, color='red', fontweight='bold')
    axs[0, 0].set_title("Price Over Time")
    axs[0, 0].set_xlabel("Date")
    axs[0, 0].set_ylabel("Price ($)")
    axs[0, 0].tick_params(axis='x', rotation=30)
    axs[0, 0].grid(True, linestyle='--', alpha=0.5)

    # === גרף 2: Price vs. days_before_departure
    axs[0, 1].scatter(sorted_df['days_before_departure'], sorted_df['predicted price'],
                     alpha=0.6, color='orange')
    axs[0, 1].set_title("Price vs. Days Before Departure")
    axs[0, 1].set_xlabel("Days Before")
    axs[0, 1].set_ylabel("Price ($)")
    axs[0, 1].grid(True)

    # === גרף 3: Part of day
    part_labels = ['Early\nNight', 'Morning', 'Noon', 'Afternoon', 'Evening', 'Late\nNight']
    axs[1, 0].boxplot([sorted_df[sorted_df['part_of_day'] == i]['predicted price'] for i in range(1, 7)],
                     labels=part_labels)
    axs[1, 0].set_title("Price by Part of Day")
    axs[1, 0].set_xlabel("Part of Day")
    axs[1, 0].set_ylabel("Price ($)")

    # === גרף 4: Day of week
    day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    axs[1, 1].boxplot([sorted_df[sorted_df['day_of_week'] == i]['predicted price'] for i in range(7)],
                      labels=day_labels)
    axs[1, 1].set_title("Price by Day of Week")
    axs[1, 1].set_xlabel("Day")
    axs[1, 1].set_ylabel("Price ($)")

    # כפתור לניתוח SHAP של 50 הטיסות הכי זולות
    tk.Button(window, text="🧠 Analyze Top 50 Cheapest (SHAP)",
              font=("Helvetica", 12, "bold"), bg="#f39c12", fg="black",
              command=lambda: analyze_shap_top_cheap(model, df, feature_columns, window)
              ).pack(pady=15)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def analyze_shap_top_cheap(model, df, feature_columns, parent_window):
    try:
        top_cheap = df.sort_values(by='predicted price').head(50)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(top_cheap[feature_columns])

        window = tk.Toplevel(parent_window)
        window.title("🔍 SHAP Analysis – Top 50 Cheapest Flights")
        window.geometry("1000x1000")
        window.configure(bg="#2c3e50")

        tk.Label(window, text="SHAP Summary Plot",
                 font=("Helvetica", 16, "bold"),
                 bg="#2c3e50", fg="#1abc9c").pack(pady=10)


        # === Dependence plot
        tk.Label(window, text="SHAP Dependence: days_before_departure vs. is_holiday",
                 font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)

        fig2 = plt.figure(figsize=(10, 5))
        shap.dependence_plot("days_before_departure", shap_values, top_cheap[feature_columns],
                             interaction_index="is_holiday", show=False)


        mode_day = int(top_cheap['day_of_week'].mode()[0])
        mode_hour = int(top_cheap['hour'].mode()[0])
        mode_holiday = int(top_cheap['is_holiday'].mode()[0])
        mode_weekend = int(top_cheap['is_weekend'].mode()[0])
        range_days = (int(top_cheap['days_before_departure'].min()),
                        int(top_cheap['days_before_departure'].max()))

        day_map = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        summary_text = (
            f"🧠 Smart Booking Insight:\n"
            f"📅 Best days before departure: {range_days[0]}–{range_days[1]} days\n"
            f"📆 Preferred day of week: {day_map[mode_day]}\n"
            f"🕒 Preferred hour: Around {mode_hour}:00\n"
            f"🎉 Holiday: {'Yes' if mode_holiday else 'No'}\n"
            f"🛌 Weekend: {'Yes' if mode_weekend else 'No'}"
        )

        tk.Label(window, text=summary_text, font=("Helvetica", 13),
                 justify="left", bg="#2c3e50", fg="#ecf0f1").pack(padx=20, pady=20, fill="x")
        # === Summary plot
        fig1 = plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, top_cheap[feature_columns], show=False)
        canvas1 = FigureCanvasTkAgg(fig1, master=window)
        canvas1.draw()
        canvas1.get_tk_widget().pack(pady=10)

    except Exception as e:
        messagebox.showerror("SHAP Error", f"SHAP analysis failed:\n{e}")
