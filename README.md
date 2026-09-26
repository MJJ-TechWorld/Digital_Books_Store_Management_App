# 📚✨ BooksKart — Digital Books Store Management App

> 🎯 **A Streamlit-based Digital Books Store Management System for managing book catalogs, inventory, customer orders, billing, employees, authentication, business operations, and store records through an interactive web interface.**

---

# 🚀🌐 Live Application

## 🔥 Try BooksKart Online

### 👉 **[📚 OPEN BOOKSKART — LIVE APPLICATION](https://my-bookskart.streamlit.app/)**

Experience the complete BooksKart application directly from your browser.

---

# 💻📂 GitHub Repository

### 👉 **[⭐ VIEW BOOKSKART SOURCE CODE ON GITHUB](https://github.com/MJJ-TechWorld/Digital_Books_Store_Management_App)**

Explore the complete source code, project structure, implementation, and development files.

---

# 🌟 Features

## 🛍️ Customer Store

- 📚 **Book Catalog & Browsing**
- 🔎 **Book Search**
- 🏷️ **Genre-Based Browsing**
- 📖 **Book Information**
- 🛒 **Shopping Cart**
- ➕ **Add Books to Cart**
- ➖ **Modify Cart Quantities**
- 🧹 **Remove Items from Cart**
- 💰 **Automatic Cart Total Calculation**
- 📦 **Customer Checkout**
- 💳 **Cash-on-Delivery Payment**
- 🧾 **Automatic Invoice Generation**
- 📄 **Downloadable PDF Invoice**
- 🆔 **Automatic Order ID Generation**
- 📊 **Automatic Inventory Update**
- 📝 **Complete Order Records**

---

## 📦 Inventory Management

BooksKart provides structured inventory management for monitoring and maintaining book stock.

### 📊 Stock Classification

| Stock Quantity | Status |
|---:|---|
| `0` | 🔴 Out of Stock |
| `1–2` | 🟠 Low Stock |
| `>2` | 🟢 Healthy Stock |

### 🔧 Inventory Operations

- 📊 **View Inventory**
- 🔎 **Search Inventory**
- 📥 **Restock Books**
- ➕ **Add Book Copies**
- 🆕 **Add New Books**
- 🏷️ **Create New Genres**
- 💰 **Update Book Pricing**
- 📦 **Monitor Stock Levels**
- 🚨 **Identify Out-of-Stock Books**
- 📝 **Record Inventory Operations**

---

# 👤 Customer Checkout

The customer checkout workflow collects structured delivery information.

### 📋 Customer Details

- 👤 **Full Name**
- 📱 **Phone Number**
- 🏠 **Flat / House / Building**
- 🛣️ **Street / Area**
- 📍 **Landmark**
- 🏙️ **City**
- 🗺️ **State**
- 📮 **PIN Code**

The information is associated with the order and maintained in the store records.

---

# 🇮🇳 Cascading Indian Address System

BooksKart provides a structured location-selection workflow:

```text
🗺️ State
   ↓
📍 District
   ↓
🏙️ City
   ↓
📮 PIN Code
````

The available options are filtered according to the selected location, providing a guided address-entry process.

---

# 🧾 Billing & Invoice System

BooksKart generates structured invoices after successful order placement.

### 📄 Invoice Information

* 🏢 **Store Information**
* 🆔 **Order ID**
* 📅 **Order Date**
* 👤 **Customer Information**
* 📍 **Delivery Address**
* 📚 **Purchased Books**
* 🔢 **Quantity**
* 💰 **Unit Price**
* 💵 **Line Total**
* 📊 **Order Summary**
* 💳 **Payment Method**
* ✅ **Order Status**
* 🧮 **Grand Total**

Invoices can be displayed within the application and generated as downloadable PDF documents.

---

# 🛒 Order Processing

BooksKart supports multiple books in a single transaction.

```text
📚 Select Books
      ↓
🛒 Add to Cart
      ↓
🔢 Set Quantities
      ↓
📊 Calculate Total
      ↓
📍 Enter Customer Details
      ↓
💳 Cash on Delivery
      ↓
✅ Place Order
      ↓
🆔 Generate Order ID
      ↓
📦 Update Inventory
      ↓
💾 Save Store Records
      ↓
🧾 Generate Invoice
      ↓
📄 Download PDF
```

---

# 👨‍💼 Employee Management

BooksKart provides structured employee management for store operations.

### 🪪 Automatic Employee IDs

Employee IDs are generated automatically by the system.

Example:

```text
EMP101
EMP102
EMP103
EMP104
```

Employees do not need to manually enter their Employee ID during registration.

---

# 🏢 Designation-Based Access

BooksKart uses designation-based access control.

### Available Designations

* 📦 **Store Clerk**
* 📋 **Inventory Manager**
* 💼 **Sales Executive**
* 👔 **Assistant Manager**
* 🏢 **Director**

The selected designation is used by the backend to determine the corresponding application access.

Backend access values are handled internally and are not required from employees.

---

# 🔐 Authentication System

The application provides authenticated employee portals.

## 📦 Store Clerk Portal

Store Clerk operations can include:

* 📚 Catalog Management
* 📦 Inventory Management
* 📥 Stock Receiving
* ➕ Adding Book Copies
* 🆕 Adding Books
* 🏷️ Genre Management
* 📝 Activity Monitoring

---

## 🏢 Director Portal

Director operations include:

* 📊 Business Dashboard
* 💰 Revenue Monitoring
* 📈 Profit & Expense Records
* 📦 Inventory Overview
* 👨‍💼 Employee Management
* 🔐 Access Management
* 📝 Activity Logs
* 📚 Catalog Management
* 💰 Pricing Management
* 📊 Store Records

---

# 🔑 Default Account

BooksKart provides a default account for initial employee portal access.

| Field           | Value      |
| --------------- | ---------- |
| 👤 **Username** | `user@`    |
| 🔑 **Password** | `12345678` |

The default account can be used for the available employee portals.

---

# 📊 Business Management

The Director portal provides centralized operational information.

### 📈 Business Records

* 💰 **Revenue**
* 📊 **Sales Records**
* 📦 **Inventory Status**
* 💸 **Expenses**
* 📈 **Profit Information**
* 🧾 **Order Records**
* 👨‍💼 **Employee Records**
* 📝 **Activity Logs**

These records provide structured information for monitoring bookstore operations.

---

# 📝 Activity Logging

Important application operations are recorded through the activity logging system.

### Logged Operations Can Include

* 🔐 Employee Login
* 👨‍💼 Employee Creation
* 📚 Book Creation
* 📦 Inventory Updates
* 📥 Restocking
* 🛒 Order Placement
* 🧾 Sales Processing
* 💰 Pricing Updates
* 🏷️ Genre Creation
* 🔧 Store Operations

Activity information is maintained in:

```text
Activity_Log.txt
```

---

# 💾 Data Storage

BooksKart uses structured file-based storage for application data.

| File                    | Purpose                              |
| ----------------------- | ------------------------------------ |
| 📚 `BOOKS_DATA.xlsx`    | Book catalog and inventory data      |
| 🧾 `STORE_RECORDS.xlsx` | Customer, order and sales records    |
| 👨‍💼 `EMPLOYEES.csv`   | Employee information and credentials |
| 💰 `EXPENSES.csv`       | Store expense records                |
| 📝 `Activity_Log.txt`   | Application activity logs            |
| 🏷️ `GENRES.txt`        | Available book genres                |
| 🔐 `CREDENTIAL.txt`     | Credential-related system data       |
| 📍 `ADDRESS_CACHE.json` | Address-selection cache              |

Required runtime files can be initialized automatically by the application.

---

# 🛠️ Technologies Used

## 🐍 Core Technology

* **Python**

## 🌐 Web Application

* **Streamlit**

## 📊 Data Management

* **OpenPyXL**
* **CSV**
* **JSON**
* **TXT**

## 🧾 Document Generation

* **ReportLab**

## 🤖 Address Processing

* **Google Gemini API**

---

# 🏗️ Application Architecture

```text
                         📚 BOOKSKART
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        🛍️ CUSTOMER      👨‍💼 EMPLOYEE      🏢 DIRECTOR
              │               │               │
              ▼               ▼               ▼
         📚 Catalog       📦 Inventory     📊 Dashboard
         🛒 Cart          📥 Receiving     👨‍💼 Employees
         🧾 Checkout      📚 Catalog       📈 Business
         💳 COD           🏷️ Genres       📝 Logs
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                     💾 FILE-BASED STORAGE
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      📊 Excel              📄 CSV              📝 TXT/JSON
```

---

# 🔄 Customer Workflow

```text
🚀 Open BooksKart
        │
        ▼
👤 Select Customer
        │
        ▼
📚 Browse / Search Books
        │
        ▼
🛒 Add Books to Cart
        │
        ▼
🧾 Review Cart
        │
        ▼
📍 Enter Delivery Details
        │
        ▼
💳 Select Cash on Delivery
        │
        ▼
✅ Place Order
        │
        ▼
🆔 Generate Order ID
        │
        ▼
📦 Update Inventory
        │
        ▼
💾 Save Store Records
        │
        ▼
🧾 Generate Invoice
        │
        ▼
📄 Download PDF
```

---

# 🔄 Employee Workflow

```text
🚀 Open BooksKart
        │
        ▼
👨‍💼 Select Employee Portal
        │
        ▼
🔐 Employee Login
        │
        ▼
🛡️ Access Determined
        │
        ▼
📊 Open Authorized Dashboard
        │
        ├── 📦 Inventory
        ├── 📥 Receiving
        ├── 📚 Catalog
        ├── 🏷️ Genres
        ├── 👨‍💼 Employees
        ├── 📈 Business Records
        └── 📝 Activity Logs
```

---

# 📥 Inventory Receiving Workflow

```text
🚨 Out-of-Stock Book
        ↓
📥 Restock
        ↓
📚 Exact Book Selected
        ↓
🔢 Enter Quantity
        ↓
✅ Confirm Receiving
        ↓
📦 Inventory Updated
        ↓
📝 Activity Recorded
```

---

# 📚 Book Catalog Management

Authorized employees can maintain the bookstore catalog through the application.

### Catalog Operations

* 🔎 Search existing books
* 📖 View book information
* ➕ Add additional copies
* 🆕 Add new books
* 🏷️ Create new genres
* 💰 Maintain pricing
* 📦 Monitor inventory
* 🚨 Identify unavailable books

---

# 🛍️ Storefront Workflow

```text
📚 Browse Catalog
       ↓
🔎 Search Books
       ↓
📖 Select Book
       ↓
🛒 Add to Cart
       ↓
🧾 Review Order
       ↓
📍 Delivery Information
       ↓
💳 COD
       ↓
✅ Confirm Purchase
```

---

# 👨‍💼 Employee Records

Employee records can contain:

* 🪪 Employee ID
* 👤 Full Name
* 📱 Phone
* 📧 Email
* 🔐 Username
* 🔑 Password
* 🏢 Designation
* 📅 Joining Date
* 🟢 Account Status

Employee IDs are generated automatically by the system.

---

# 🛡️ Access Control Structure

```text
🏢 Director
    │
    ├── 📊 Business Management
    ├── 👨‍💼 Employee Management
    ├── 📦 Inventory
    ├── 📚 Catalog
    └── 📝 Activity Logs

📦 Store Clerk
    │
    ├── 📦 Inventory
    ├── 📥 Receiving
    ├── 📚 Catalog Operations
    └── 🏷️ Genre Management

📋 Inventory Manager
    │
    └── 📦 Inventory Operations

💼 Sales Executive
    │
    └── 🛒 Sales Operations

👔 Assistant Manager
    │
    └── 🔧 Authorized Store Operations
```

---

# 📁 Project Structure

```text
Digital_Books_Store_Management_App/
│
├── 📄 main.py
├── 📄 function_utils.py
├── 📚 BOOKS_DATA.xlsx
├── 📊 STORE_RECORDS.xlsx
├── 👨‍💼 EMPLOYEES.csv
├── 💰 EXPENSES.csv
├── 📝 Activity_Log.txt
├── 🏷️ GENRES.txt
├── 🔐 CREDENTIAL.txt
├── 📍 ADDRESS_CACHE.json
├── 📄 requirements.txt
├── 🚫 .gitignore
└── 📖 README.md
```

---

# ⚙️ Requirements

* 🐍 **Python 3.x**
* 📦 Required packages listed in `requirements.txt`
* 🌐 Internet connection for API-assisted address functionality

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# 🚀 Run Locally

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/MJJ-TechWorld/Digital_Books_Store_Management_App.git
```

## 2️⃣ Enter the Project Directory

```bash
cd Digital_Books_Store_Management_App
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Start the Application

```bash
streamlit run main.py
```

## 5️⃣ Open the Local Application

Streamlit will provide a local address similar to:

```text
http://localhost:8501
```

---

# 🔐 Configuration

If API-assisted address functionality is enabled, configure the required Gemini API credential through the supported environment or Streamlit secrets configuration.

Do not commit private API credentials to the GitHub repository.

---

# 📊 Store Records

Completed orders can be recorded with structured customer, order, and book information.

Typical records include:

* 🆔 Order ID
* 📅 Order Date
* 👤 Customer Name
* 📱 Customer Phone
* 📍 Delivery Address
* 📚 Book Information
* 🔢 Quantity
* 💰 Unit Price
* 💵 Total Amount
* 💳 Payment Method
* 📦 Order Status

Records are maintained in:

```text
STORE_RECORDS.xlsx
```

---

# 📌 System Highlights

### 🛒 Integrated Customer Store

Customers can browse books, search the catalog, manage their cart, enter delivery information, place COD orders, and receive invoices through an integrated workflow.

### 📦 Inventory Synchronization

Completed purchases automatically reduce available stock, while receiving operations increase inventory quantities.

### 🧾 Automated Billing

Orders are converted into structured invoices containing customer, book, pricing, payment, and delivery information.

### 👨‍💼 Designation-Based Access

Employee permissions are determined automatically from the selected designation.

### 📊 Operational Records

Customer orders, employee information, inventory changes, expenses, and activity records are maintained through structured files.

### 📍 Structured Address Workflow

State, district, city, and PIN selection provides a guided address-entry system.

### 🌐 Web-Based Application

The application is built with Streamlit and can be accessed directly through a web browser.

---

# 🎯 Project Purpose

BooksKart demonstrates how Python and Streamlit can be used to implement a practical digital bookstore management platform.

The project combines:

* 📚 Book Catalog Management
* 🛒 Customer Shopping
* 📦 Inventory Management
* 🧾 Billing & Invoicing
* 👨‍💼 Employee Management
* 🔐 Authentication
* 🛡️ Designation-Based Access
* 📊 Business Records
* 📝 Activity Logging
* 💾 File-Based Data Management
* 📍 Address Processing
* 🌐 Web Application Deployment

---

# 🌐 Access BooksKart

## 🚀 **LIVE APPLICATION**

### 👉 **[📚 OPEN BOOKSKART](https://my-bookskart.streamlit.app/)**

**Browse Books • Manage Inventory • Process Orders • Generate Invoices**

---

# 💻 GitHub Repository

### 👉 **[📂 VIEW SOURCE CODE ON GITHUB](https://github.com/MJJ-TechWorld/Digital_Books_Store_Management_App)**

---

# 👨‍💻 Author

## **MJJ-TechWorld**

🇮🇳 **Made in India**

Built with **Python + Streamlit** for digital bookstore operations and management.

---

# ⭐ Support the Project

If you find **BooksKart** useful:

⭐ **Star the repository**
🍴 **Fork the project**
💡 **Explore the source code**
🚀 **Try the live application**

---

# 📚 BooksKart

> **Browse. Manage. Order. Track.**

### 🐍 Built with Python | 🌐 Powered by Streamlit | 📚 Designed for Digital Book Store Management

```
```
