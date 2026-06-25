# TASK-2-ADEESA-FATIMA
GUI-based Expense Tracker built with Python, tkinter &amp; SQLite — supports add, update, delete, date filtering, and persistent storage of expenses.
#  Expense Tracker — GUI Application

##  Project Description

The **Expense Tracker** is a desktop GUI application built with Python that allows users to record, manage, and filter their daily expenses. It goes beyond a basic terminal script by providing a full graphical interface with a persistent database — meaning all your data is saved even after closing the application.

This project demonstrates a complete real-world workflow: taking user input through a form, storing it in a database, displaying it in a table, and allowing full CRUD operations (Create, Read, Update, Delete) — the same pattern used in professional backend applications.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| `Python 3` | Core programming language |
| `tkinter` | GUI framework (built into Python) |
| `ttk` (from tkinter) | Styled widgets — Combobox, Treeview |
| `sqlite3` | Local database to store expenses permanently |
| `datetime` | Auto-stamping entries with date and time |

---

## Features

- **Add Expense** — Enter description, category, and amount to log a new expense
- **Update Expense** — Select any row and edit its details
- **Delete Expense** — Remove any selected entry from the database
- **Custom Categories** — Choose from preset categories or type your own
- **Date Filter** — Filter expenses between any two dates (YYYY-MM-DD format)
- **Show All** — Reset filter and view all expenses
- **Running Total** — Total spent amount updates automatically at the bottom
- **Persistent Storage** — All data saved in `expenses.db` (SQLite file)

---

##  Project Structure

```
expense_tracker/
│
├── Expense_tracker.py      # Main Python file (entire app in one script)
└── expenses.db             # Auto-created SQLite database (on first run)
```

---

## How to Run

### Requirements
- Python 3.x installed
- No extra libraries needed — all modules are built into Python

### Steps

```bash
# Step 1 — Clone or download the file
# Step 2 — Open terminal in the project folder
# Step 3 — Run the script

python Expense_tracker.py
```

The app window will open. The `expenses.db` database file is created automatically on first run.

---

# Code Description

The code is organized into four main sections:

### 1. Database Setup
```python
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (...)''')
```
Connects to (or creates) an SQLite database on startup. The `expenses` table stores: ID, date, description, category, and amount. `CREATE TABLE IF NOT EXISTS` ensures the table is only created once — safe to run repeatedly.

---

### 2. Core Functions

| Function | What it does |
|---|---|
| `add_expense()` | Reads form fields → validates input → inserts new row into DB → refreshes table |
| `update_expense()` | Takes the selected row's ID → updates its fields in DB with new values from the form |
| `delete_expense()` | Gets selected row's ID → deletes it from DB → refreshes table |
| `update_list()` | Clears the Treeview → re-fetches all rows from DB → displays them + calculates total |
| `apply_date_filter()` | Validates date format → calls `update_list()` with date range for SQL WHERE clause |
| `on_select()` | Fires when user clicks a row → loads that row's data back into the input form for editing |
| `clear_fields()` | Resets all input fields to empty after add/update/delete |

---

### 3. GUI Layout

The interface is built using `tkinter` widgets arranged in three sections:

```
┌─────────────────────────────────────────────────┐
│  Input Frame                                    │
│  [Description] [Category ▼] [Amount] [Add]      |
│                             [Update] [Delete]   │
├─────────────────────────────────────────────────┤
│  Filter Frame                                   │
│  From: [____] To: [____] [Apply] [Show All]     │
├─────────────────────────────────────────────────┤
│  Treeview Table                                 │
│  ID | Date | Description | Category | Amount    │
│  1  | ...  | ...         | Food     | 150.00    │
│  2  | ...  | ...         | Other    | 200.00    │
├─────────────────────────────────────────────────┤
│  Total: ₨350.00                                 │
└─────────────────────────────────────────────────┘
```

---

### 4. Database Queries Used

```python
# Insert new expense
INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)

# Fetch all expenses
SELECT id, date, description, category, amount FROM expenses ORDER BY date DESC

# Fetch with date filter
SELECT ... WHERE date BETWEEN ? AND ? ORDER BY date DESC

# Update selected expense
UPDATE expenses SET description=?, category=?, amount=? WHERE id=?

# Delete selected expense
DELETE FROM expenses WHERE id=?
```

---

## 🔄 How It Works — Step by Step

1. **App starts** → connects to `expenses.db` → creates table if not exists → loads all existing expenses into the table

2. **User adds expense** → fills Description, selects Category, enters Amount → clicks **Add** → data is validated → inserted into database → table refreshes automatically

3. **User edits expense** → clicks any row in the table → fields auto-fill with that row's data → user makes changes → clicks **Update** → database is updated

4. **User deletes expense** → clicks any row → clicks **Delete** → row removed from database → table refreshes

5. **User filters by date** → enters From and To dates → clicks **Apply Filter** → SQL WHERE clause filters results → only matching rows shown → total updates accordingly

6. **Total calculation** → every time `update_list()` runs, it loops through all visible rows and adds up the Amount column → displays live total at the bottom

---

##  Error Handling

| Situation | How it is handled |
|---|---|
| Amount is not a number | `try/except ValueError` → shows error popup |
| Description or category is empty | `if not desc or not cat` check → shows error popup |
| Invalid date format in filter | `datetime.strptime()` validation → shows error popup |
| No row selected for delete/update | `tree.focus()` check → shows error popup |

---

##  Key Concepts Demonstrated

- **IPO Model** — Input (form fields) → Process (SQL queries + validation) → Output (Treeview table + total)
- **CRUD Operations** — Full Create, Read, Update, Delete using SQLite
- **Event-Driven Programming** — GUI buttons and `<<TreeviewSelect>>` events trigger functions
- **Persistent Storage** — Data survives app restarts via SQLite database
- **Defensive Coding** — All user inputs validated before touching the database
- **Separation of Concerns** — Each function has one specific responsibility

---

##  Sample Output

```
Session opened → expenses.db connected
Entry added   : "Lunch" | Food | ₨150.00  → 2026-06-25 13:45:00
Entry added   : "Bus"   | Transport | ₨30.00  → 2026-06-25 14:00:00
Total displayed at bottom: ₨180.00
```

