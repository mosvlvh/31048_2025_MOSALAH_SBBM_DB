import tkinter as tk
from tkinter import messagebox, ttk
import oracledb
from datetime import datetime, timedelta

# ==========================================
# ⚙️ Database Connection Settings
# ==========================================
DB_USER = "U310482025_SALAH_SBB_DB"
DB_PASSWORD = "Oracle1234"
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SERVICE = "FREEPDB1"

dsn_string = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

def get_db_connection():
    # Establishes a database connection using modern python-oracledb client
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn_string)

# ==========================================
# 💾 1. Register Donor Function
# ==========================================
def register_donor():
    d_id = entry_donor_id.get().strip()
    f_name = entry_first_name.get().strip()
    l_name = entry_last_name.get().strip()
    gender = var_gender.get()
    b_date_str = entry_birth_date.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    last_don_str = entry_last_donation.get().strip() # Fetches the new Last Donation Date field

    if not d_id or not f_name or not l_name or not b_date_str:
        messagebox.showwarning("Warning", "Please fill in all required fields!")
        return

    try:
        birth_date = datetime.strptime(b_date_str, "%Y-%m-%d")

        # Check if Last Donation Date is provided, otherwise set as None (NULL)
        last_donation_date = None
        if last_don_str:
            last_donation_date = datetime.strptime(last_don_str, "%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert donor data including the new Last_Donation_Date column
        query = """
            INSERT INTO donors (donor_id, first_name, last_name, gender, birth_date, phone, email, last_donation_date)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """
        cursor.execute(query, [d_id, f_name, l_name, gender, birth_date, phone, email, last_donation_date])
        conn.commit()
        messagebox.showinfo("Success", f"Donor {f_name} {l_name} registered successfully!")

        # Reset entry fields after successful insertion
        entry_donor_id.delete(0, tk.END)
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_birth_date.delete(0, tk.END)
        entry_birth_date.insert(0, "1995-08-22")
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_last_donation.delete(0, tk.END) # Clear the last donation entry

        cursor.close()
        conn.close()
    except ValueError:
        messagebox.showerror("Format Error", "Dates must be in YYYY-MM-DD format!")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to register donor:\n{str(e)}")

# ==========================================
# 💾 2. Add Blood Bag Function
# ==========================================
def add_blood_bag():
    barcode = entry_bag_barcode.get().strip()
    donor_id = entry_bag_donor_id.get().strip()
    bg = var_bag_bg.get()

    if not barcode or not donor_id:
        messagebox.showwarning("Warning", "Please fill in Barcode and Donor ID!")
        return

    col_date = datetime.now()
    exp_date = col_date + timedelta(days=42)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new blood unit linked to a valid Donor ID
        query = """
            INSERT INTO blood_units (unit_barcode_id, donor_id, blood_group, collection_date, expiration_date, status)
            VALUES (:1, :2, :3, :4, :5, 'Available')
        """
        cursor.execute(query, [barcode, donor_id, bg, col_date, exp_date])
        conn.commit()
        messagebox.showinfo("Success", f"Blood Bag {barcode} added and linked to Donor {donor_id}!")

        entry_bag_barcode.delete(0, tk.END)
        entry_bag_donor_id.delete(0, tk.END)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to add blood bag:\n{str(e)}")

# ==========================================
# 💾 3. Submit Lab Test Function
# ==========================================
def submit_lab_test():
    barcode = entry_lab_barcode.get().strip()
    hiv = var_hiv.get()
    hep_b = var_hepb.get()
    hep_c = var_hepc.get()
    syphilis = var_syphilis.get()

    if not barcode:
        messagebox.showwarning("Warning", "Please enter the Blood Bag Barcode!")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Calling stored procedure from BLOOD_BANK_PKG to process the test logic
        cursor.callproc("BLOOD_BANK_PKG.Process_Lab_Test", [barcode, hiv, hep_b, hep_c, syphilis])
        conn.commit()

        messagebox.showinfo("Success", f"Blood bag {barcode} has been successfully processed & updated!")

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Lab Error", f"Action Rejected:\n{str(e)}")


# ==========================================
# 🎨 User Interface (GUI Layout)
# ==========================================
root = tk.Tk()
root.title("Smart Blood Bank Management System")
root.geometry("480x620") # Slightly increased height to comfortably accommodate the new field
root.configure(bg="#f5f6fa")

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#f5f6fa")
style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[12, 6])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab_donor = tk.Frame(notebook, bg="#f5f6fa")
tab_bag = tk.Frame(notebook, bg="#f5f6fa")
tab_lab = tk.Frame(notebook, bg="#f5f6fa")

notebook.add(tab_donor, text=" 👤 Donors ")
notebook.add(tab_bag, text=" 🩸 Blood Bags ")
notebook.add(tab_lab, text=" 🧪 Lab Testing ")

blood_groups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]

# ------------------------------------------
# 👤 Donors Tab Fields (With Last Donation Date Added)
# ------------------------------------------
tk.Label(tab_donor, text="Register New Donor", font=("Arial", 13, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(pady=5)

fields = [
    ("Donor ID (Required):", "donor_id"),
    ("First Name (Required):", "first_name"),
    ("Last Name (Required):", "last_name"),
    ("Birth Date (YYYY-MM-DD):", "birth_date"),
    ("Phone Number:", "phone"),
    ("Email:", "email"),
    ("Last Donation Date (YYYY-MM-DD) [Optional]:", "last_donation") # New Label text
]

entries = {}
for label_text, field_name in fields:
    tk.Label(tab_donor, text=label_text, font=("Arial", 9), bg="#f5f6fa").pack(pady=1)
    entry = tk.Entry(tab_donor, font=("Arial", 10), justify="center", width=28)
    entry.pack(pady=2)
    entries[field_name] = entry

entry_donor_id = entries["donor_id"]
entry_first_name = entries["first_name"]
entry_last_name = entries["last_name"]
entry_birth_date = entries["birth_date"]
entry_birth_date.insert(0, "1995-08-22")
entry_phone = entries["phone"]
entry_email = entries["email"]
entry_last_donation = entries["last_donation"] # New reference to entry field

tk.Label(tab_donor, text="Gender:", font=("Arial", 9), bg="#f5f6fa").pack(pady=1)
var_gender = tk.StringVar(value="M")
tk.OptionMenu(tab_donor, var_gender, "M", "F").pack(pady=2)

btn_reg_donor = tk.Button(tab_donor, text="Register Donor", command=register_donor, bg="#2980b9", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5)
btn_reg_donor.pack(pady=10)


# ------------------------------------------
# 🩸 Blood Bags Tab Fields
# ------------------------------------------
tk.Label(tab_bag, text="Add New Blood Bag to Inventory", font=("Arial", 13, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(pady=15)

tk.Label(tab_bag, text="Blood Bag Barcode (ID):", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
entry_bag_barcode = tk.Entry(tab_bag, font=("Arial", 11), justify="center", width=25)
entry_bag_barcode.pack(pady=5)

tk.Label(tab_bag, text="Donor ID (Must exist in Donors):", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
entry_bag_donor_id = tk.Entry(tab_bag, font=("Arial", 11), justify="center", width=25)
entry_bag_donor_id.pack(pady=5)

tk.Label(tab_bag, text="Blood Group for this Bag:", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
var_bag_bg = tk.StringVar(value="O+")
tk.OptionMenu(tab_bag, var_bag_bg, *blood_groups).pack(pady=5)

btn_add_bag = tk.Button(tab_bag, text="Add Blood Bag", command=add_blood_bag, bg="#8e44ad", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5)
btn_add_bag.pack(pady=35)


# ------------------------------------------
# 🧪 Lab Testing Tab Fields
# ------------------------------------------
tk.Label(tab_lab, text="Blood Lab Testing Portal", font=("Arial", 13, "bold"), bg="#f5f6fa", fg="#c0392b").pack(pady=15)

tk.Label(tab_lab, text="Blood Bag Barcode:", font=("Arial", 10, "bold"), bg="#f5f6fa", fg="#2c3e50").pack()
entry_lab_barcode = tk.Entry(tab_lab, font=("Arial", 11), justify="center", width=22)
entry_lab_barcode.pack(pady=5)

options = ["Negative", "Positive"]

tk.Label(tab_lab, text="HIV Result:", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
var_hiv = tk.StringVar(value="Negative")
tk.OptionMenu(tab_lab, var_hiv, *options).pack()

tk.Label(tab_lab, text="Hepatitis B Result:", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
var_hepb = tk.StringVar(value="Negative")
tk.OptionMenu(tab_lab, var_hepb, *options).pack()

tk.Label(tab_lab, text="Hepatitis C Result:", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
var_hepc = tk.StringVar(value="Negative")
tk.OptionMenu(tab_lab, var_hepc, *options).pack()

tk.Label(tab_lab, text="Syphilis Result:", font=("Arial", 10), bg="#f5f6fa").pack(pady=2)
var_syphilis = tk.StringVar(value="Negative")
tk.OptionMenu(tab_lab, var_syphilis, *options).pack()

btn_save_test = tk.Button(tab_lab, text="Submit & Update Database", command=submit_lab_test, bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5)
btn_save_test.pack(pady=20)

root.mainloop()
