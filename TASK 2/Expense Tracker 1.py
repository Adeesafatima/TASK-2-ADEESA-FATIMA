import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- DB setup ---
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        category TEXT,
        amount REAL
    )
''')
conn.commit()

CATEGORY_OPTIONS = ["Food", "Transport", "Utilities", "Entertainment", "Other"]

# --- Add Expense ---
def add_expense():
    desc = desc_entry.get()
    cat = cat_var.get() if cat_var.get() != "Custom" else custom_cat_entry.get()
    try:
        amt = float(amt_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Amount must be a number.")
        return

    if not desc or not cat:
        messagebox.showerror("Missing data", "Please fill all fields.")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)",
                   (date, desc, cat, amt))
    conn.commit()
    update_list()
    clear_fields()

def clear_fields():
    desc_entry.delete(0, tk.END)
    amt_entry.delete(0, tk.END)
    custom_cat_entry.delete(0, tk.END)
    cat_var.set("Select")

# --- List Update ---
def update_list(from_date=None, to_date=None):
    for row in tree.get_children():
        tree.delete(row)

    query = "SELECT id, date, description, category, amount FROM expenses"
    params = []
    if from_date and to_date:
        query += " WHERE date BETWEEN ? AND ?"
        params = [from_date + " 00:00:00", to_date + " 23:59:59"]
    query += " ORDER BY date DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()

    total = 0
    for row in rows:
        tree.insert('', tk.END, values=row)
        total += row[4]

    total_var.set(f"Total: ₨{total:,.2f}")

# --- Apply Date Filter ---
def apply_date_filter():
    from_date = from_entry.get()
    to_date = to_entry.get()
    try:
        datetime.strptime(from_date, "%Y-%m-%d")
        datetime.strptime(to_date, "%Y-%m-%d")
        update_list(from_date, to_date)
    except ValueError:
        messagebox.showerror("Invalid date", "Use YYYY-MM-DD format.")

# --- Select Row to Edit ---
def on_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    global selected_id
    selected_id = values[0]
    desc_entry.delete(0, tk.END)
    desc_entry.insert(0, values[2])
    amt_entry.delete(0, tk.END)
    amt_entry.insert(0, values[4])
    cat_var.set(values[3])
    custom_cat_entry.delete(0, tk.END)

# --- Delete Selected ---
def delete_expense():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("No selection", "Please select an item to delete.")
        return
    values = tree.item(selected, 'values')
    cursor.execute("DELETE FROM expenses WHERE id = ?", (values[0],))
    conn.commit()
    update_list()
    clear_fields()

# --- Update Selected ---
def update_expense():
    if not selected_id:
        messagebox.showerror("No selection", "Select an item to update.")
        return
    desc = desc_entry.get()
    cat = cat_var.get() if cat_var.get() != "Custom" else custom_cat_entry.get()
    try:
        amt = float(amt_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Amount must be a number.")
        return
    cursor.execute("UPDATE expenses SET description = ?, category = ?, amount = ? WHERE id = ?",
                   (desc, cat, amt, selected_id))
    conn.commit()
    update_list()
    clear_fields()

# --- GUI Setup ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x650")
root.resizable(False, False)

# --- Input Frame ---
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Description").grid(row=0, column=0)
tk.Label(frame, text="Category").grid(row=0, column=1)
tk.Label(frame, text="Amount").grid(row=0, column=2)

desc_entry = tk.Entry(frame, width=25)
amt_entry = tk.Entry(frame, width=15)

desc_entry.grid(row=1, column=0, padx=5)
amt_entry.grid(row=1, column=2, padx=5)

cat_var = tk.StringVar(value="Select")
cat_menu = ttk.Combobox(frame, textvariable=cat_var, values=CATEGORY_OPTIONS + ["Custom"], state="readonly", width=15)
cat_menu.grid(row=1, column=1, padx=5)

custom_cat_entry = tk.Entry(frame, width=15)
custom_cat_entry.grid(row=2, column=1, padx=5)
tk.Label(frame, text="(If 'Custom')").grid(row=3, column=1)

# Buttons
tk.Button(frame, text="Add", command=add_expense).grid(row=1, column=3, padx=10)
tk.Button(frame, text="Update", command=update_expense).grid(row=1, column=4, padx=10)
tk.Button(frame, text="Delete", command=delete_expense).grid(row=1, column=5, padx=10)

# --- Date Filter ---
filter_frame = tk.LabelFrame(root, text="Filter by Date (YYYY-MM-DD)")
filter_frame.pack(pady=10, fill="x", padx=10)

tk.Label(filter_frame, text="From:").grid(row=0, column=0)
from_entry = tk.Entry(filter_frame, width=12)
from_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="To:").grid(row=0, column=2)
to_entry = tk.Entry(filter_frame, width=12)
to_entry.grid(row=0, column=3)

tk.Button(filter_frame, text="Apply Filter", command=apply_date_filter).grid(row=0, column=4, padx=10)
tk.Button(filter_frame, text="Show All", command=lambda: update_list()).grid(row=0, column=5)

# --- Treeview ---
columns = ("ID", "Date", "Description", "Category", "Amount")
tree = ttk.Treeview(root, columns=columns, show='headings', height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140 if col == "Date" else 120, anchor=tk.W if col != "Amount" else tk.E)
tree.pack(pady=10, fill=tk.BOTH, expand=True)
tree.bind('<<TreeviewSelect>>', on_select)

# --- Total Label ---
total_var = tk.StringVar()
tk.Label(root, textvariable=total_var, font=("Arial", 14, "bold")).pack(pady=10)

selected_id = None
update_list()
root.mainloop()
