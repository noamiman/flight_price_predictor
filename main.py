# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import joblib

from utills import generate_features, show_price_graph, analyze_shap_top_cheap

# === Initial Configuration ===
model, feature_columns = joblib.load('src/flight_price_model.pkl')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# === main GUI ===
root = tk.Tk()
root.title("Flight Price Predictor")
root.geometry("600x500")
root.configure(bg="#2c3e50")

# === title ===
tk.Label(root, text="✈️ Flight Price Optimizer", font=("Helvetica", 24, "bold"),
         fg="#1abc9c", bg="#2c3e50").pack(pady=30)

form = tk.Frame(root, bg="#2c3e50")
form.pack(pady=10)

# === User Input Fields ===
tk.Label(form, text="Destination:", font=("Helvetica", 16),
         fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=0, sticky="e", pady=10, padx=10)
destination_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
destination_entry.grid(row=0, column=1, padx=10)

tk.Label(form, text="Start Date (YYYY-MM-DD):", font=("Helvetica", 16),
         fg="#ecf0f1", bg="#2c3e50").grid(row=1, column=0, sticky="e", pady=10, padx=10)
start_date_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
start_date_entry.grid(row=1, column=1, padx=10)

tk.Label(form, text="End Date (YYYY-MM-DD):", font=("Helvetica", 16),
         fg="#ecf0f1", bg="#2c3e50").grid(row=2, column=0, sticky="e", pady=10, padx=10)
end_date_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
end_date_entry.grid(row=2, column=1, padx=10)

tk.Label(form, text="Days Before:", font=("Helvetica", 16),
         fg="#ecf0f1", bg="#2c3e50").grid(row=3, column=0, sticky="e", pady=10, padx=10)
days_before_entry = ttk.Entry(form, font=("Helvetica", 16), width=25)
days_before_entry.grid(row=3, column=1, padx=10)

# === Main Function ===
def find_best_dates():
    try:
        destination = destination_entry.get().strip().upper()
        start_date_str = start_date_entry.get()
        end_date_str = end_date_entry.get()
        days_before = int(days_before_entry.get())

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        if start_date > end_date:
            raise ValueError("Start date must be before end date.")

        delta_days = (end_date - start_date).days
        num_samples = max(200, min(delta_days * 24, 3000))

        df = generate_features(start_date_str, end_date_str, destination, days_before, num_samples)
        df["predicted price"] = model.predict(df).round(2)

        show_price_graph(df, destination, model, feature_columns, root)

    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input:\n{e}")

tk.Button(root, text="🔍 Find Best Dates", font=("Helvetica", 16, "bold"),
          bg="#1abc9c", fg="black", activebackground="#16a085",
          padx=20, pady=10, command=find_best_dates).pack(pady=20)

root.mainloop()
