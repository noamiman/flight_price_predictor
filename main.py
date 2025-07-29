import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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

# ===== כפתור חיפוש =====
def find_best_dates():
    try:
        destination = destination_entry.get().strip().upper()
        start_date = datetime.strptime(start_date_entry.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end_date_entry.get(), "%Y-%m-%d")

        if start_date > end_date:
            raise ValueError("Start date must be before end date.")

        # כאן תכניס את הקריאה למודל והחישוב
        # לדוגמה:
        # best_options = model.get_best_dates(destination, start_date, end_date)

        # הדמיה לתוצאה:
        best_options = [
            ("2025-08-04", 179),
            ("2025-08-12", 190),
            ("2025-08-23", 200)
        ]

        # הצגת התוצאה
        text = f"Best dates to book flight to {destination}:\n\n"
        for date, price in best_options:
            text += f"🗓 {date} — ${price}\n"

        result_label.config(text=text)

    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input:\n{e}")

search_button = tk.Button(root, text="🔍 Find Best Dates", font=("Helvetica", 16, "bold"),
                          bg="#1abc9c", fg="black", activebackground="#16a085",
                          padx=20, pady=10, command=find_best_dates)
search_button.pack(pady=20)

# ===== הפעלת הממשק =====
root.mainloop()
