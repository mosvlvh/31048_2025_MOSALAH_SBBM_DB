# 31048_2025_MOSALAH_SBBM_DB

# 🩸 Smart Blood Bank Management (SBBM-DB)

A comprehensive, database-driven **Blood Bank Management System** built with **Python (Tkinter GUI)** and powered by an **Oracle SQL & PL/SQL Database**. This system streamlines the registration of blood donors, manages real-time blood unit inventory, and processes clinical lab tests safely using advanced transactional controls and database programming.

---

## Key Features

- **👤 Smart Donor Registration**: Register new blood donors with biological data and track eligibility based on their last donation dates.
- **🩸 Real-Time Inventory Control**: Track blood bags, automated expiration dates (42-day lifespan), and blood groups.
- **🧪 Automated Lab Testing**: Validate blood bag safety metrics (HIV, Hepatitis B, Hepatitis C, Syphilis) using secure backend triggers and packages.
- **🛡️ Secure Transaction Control**: Full database consistency using `COMMIT` and `ROLLBACK` commands.

---

## 📊 System Architecture & Design

### 1. Entity-Relationship Diagram (ERD)
The database schema consists of several structured tables (Donors, Blood Units, Lab Tests, Dispatches, Hospitals, etc.) normalized to ensure minimal redundancy and strict referential integrity.
*(Refer to `image_7e39fe.png` or your uploaded ERD diagram in the repository)*

### 2. Business Process Swimlane Diagram
A comprehensive Swimlane diagram maps out the business logic flow from the donor registration desk, lab testing division, all the way to hospital distribution.

---

## 🛠️ Database Schema & PL/SQL Components

The backend architecture is highly optimized using Oracle PL/SQL concepts:

### 📦 1. Blood Bank Package (`BLOOD_BANK_PKG`)
Encapsulates key business actions into a reusable modular package:
- **`Check_Donor_Eligibility` (Function)**: Automatically computes whether a donor is medical-eligible to donate (at least 56 days required since the last donation).
- **`Process_Lab_Test` (Procedure)**: Takes specific lab results and dynamically updates the blood unit status to `Available` or marks it as `Discarded` (if unsafe results are found).

### 🔍 2. Explicit Cursors (`Explicit_Cursor.sql`)
A dedicated reporting cursor that loops through the inventory, filters out infected or unsafe blood units, and displays detailed records for disposal.

### ⚡ 3. Database Triggers
Active automated triggers to enforce strict validation rules before insert/update operations occur on critical transactional tables.

---

## 🖥️ Graphical User Interface (Python GUI)

The front-end is developed using **Python's Tkinter library** and the **python-oracledb** modern driver:

| Tab Name | Main Function | Backend Interaction |
| :--- | :--- | :--- |
| **👤 Donors** | Registration of new donors | Performs validation, checks eligibility, and executes `INSERT INTO donors`. |
| **🩸 Blood Bags** | Adding newly collected units | Generates barcodes, links to valid donor IDs, and records `Collection_Date`. |
| **🧪 Lab Testing** | Recording infection profiles | Calls `BLOOD_BANK_PKG.Process_Lab_Test` to update status instantly. |

---

## 📂 Project Structure

```text
├── app.py                      # Main Python Tkinter Application Code
├── BLOOD_BANK_PKG_SPEC_BODY.sql # Oracle PL/SQL Package Specification and Body
├── Explicit_Cursor.sql         # SQL script to test Explicit Cursor reports
├── DDL_DML_Schema.sql          # Complete DB Tables Creation and Initial Inserts
├── README.md                   # Project Documentation (This file)
└── assets/                     # Screenshots, ERD, and Swimlane Diagrams

⚙️ Installation & Setup
Prerequisites

    Python 3.x

    Oracle Database (19c/21c/Free Edition)

    python-oracledb library installed:
    Bash

    pip install oracledb

Backend Execution (SQL Developer)

    Execute the tables script (DDL_DML_Schema.sql) to set up tables.

    Compile the PL/SQL Package (BLOOD_BANK_PKG_SPEC_BODY.sql).

    Compile the database triggers.

Frontend Run

    Update database connection credentials inside the app.py script:
    Python

    DB_USER = "Your_Oracle_Username"
    DB_PASSWORD = "Your_Password"

    Launch the application:
    Bash

    python app.py

👥 Contributors & Academic Purpose

Developed for academic assessment in Database Management Systems (PL/SQL & Database Programming).

    Developer: Salah

    Course: SQL & PL/SQL Programming Phase VI


