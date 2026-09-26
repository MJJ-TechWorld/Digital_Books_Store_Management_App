Yes, I understand now. You want **ONE single continuous Markdown code block**, so you can click copy **once** and paste the entire README into GitHub. Nothing should be split into separate blocks.

````markdown
# 📚✨ BooksKart — Digital Books Store Management App

> 🎯 **A Streamlit-based Digital Books Store Management System for managing book catalogs, inventory, customer orders, billing, employees, authentication, business operations, and store records through an interactive web interface.**

---

# 🚀🌐 Live Application

## 🔥 Try BooksKart Online

### 👉 [📚 OPEN BOOKSKART — LIVE APPLICATION](https://my-bookskart.streamlit.app/)

Experience the BooksKart digital bookstore directly from your browser.

---

# 💻📂 GitHub Repository

### 👉 [⭐ VIEW BOOKSKART SOURCE CODE ON GITHUB](https://github.com/MJJ-TechWorld/Digital_Books_Store_Management_App)

Explore the complete source code, project structure, implementation, and development files.

---

# 🌟 Features

- 📚 **Digital Book Catalog**
- 🔎 **Book Search**
- 🏷️ **Genre-Based Browsing**
- 📖 **Book Information**
- 🛒 **Shopping Cart**
- ➕ **Add Books to Cart**
- ➖ **Modify Cart Quantities**
- 🧹 **Remove Cart Items**
- 💰 **Automatic Cart Total Calculation**
- 📦 **Customer Checkout**
- 💳 **Cash-on-Delivery Payment**
- 🧾 **Automated Billing**
- 📄 **Downloadable PDF Invoices**
- 🆔 **Automatic Order ID Generation**
- 📊 **Automatic Inventory Updates**
- 📝 **Complete Order Records**
- 📦 **Inventory Management**
- 📥 **Book Restocking**
- ➕ **Add Book Copies**
- 🆕 **Add New Books**
- 🏷️ **Create New Genres**
- 💰 **Book Pricing Management**
- 🚨 **Out-of-Stock Detection**
- 👨‍💼 **Employee Management**
- 🪪 **Automatic Employee ID Generation**
- 🔐 **Employee Authentication**
- 🛡️ **Designation-Based Access Control**
- 📊 **Business Dashboard**
- 💰 **Revenue & Expense Management**
- 📈 **Profit Information**
- 📝 **Activity Logging**
- 🇮🇳 **Cascading Indian Address Selection**
- 💾 **Excel, CSV, TXT & JSON Data Storage**
- 🌐 **Streamlit Web Interface**
- 📄 **PDF Document Generation**

---

# 🛍️ Customer Store

BooksKart provides an interactive customer storefront for browsing and purchasing books.

### Customer Operations

- 📚 Browse available books
- 🔎 Search books
- 🏷️ Browse by genre
- 📖 View book information
- 🛒 Add books to cart
- 🔢 Modify quantities
- 🧹 Remove books from cart
- 💰 Calculate order totals
- 📍 Enter delivery information
- 💳 Select Cash on Delivery
- ✅ Place orders
- 🧾 Generate invoices
- 📄 Download PDF invoices

---

# 👤 Customer Checkout

The checkout system collects structured customer and delivery information.

### Customer Information

- 👤 **Full Name**
- 📱 **Phone Number**
- 🏠 **Flat / House / Building**
- 🛣️ **Street / Area**
- 📍 **Landmark**
- 🏙️ **City**
- 🗺️ **State**
- 📮 **PIN Code**

The entered information is associated with the order and stored in the store records.

---

# 🇮🇳 Cascading Indian Address System

BooksKart provides a structured address-selection workflow:

**🗺️ State → 📍 District → 🏙️ City → 📮 PIN Code**

The available options are filtered according to the previously selected location, providing a structured method for entering Indian delivery addresses.

---

# 📦 Inventory Management

BooksKart provides inventory controls for monitoring and maintaining book stock.

### 📊 Stock Classification

| Stock Quantity | Status |
|---:|---|
| `0` | 🔴 Out of Stock |
| `1–2` | 🟠 Low Stock |
| `>2` | 🟢 Healthy Stock |

### 🔧 Inventory Operations

- 📊 View inventory
- 🔎 Search inventory
- 📥 Restock books
- ➕ Add book copies
- 🆕 Add new books
- 🏷️ Create new genres
- 💰 Update book pricing
- 📦 Monitor stock levels
- 🚨 Identify unavailable books
- 📝 Record inventory operations

---

# 📥 Inventory Receiving

Out-of-stock books can be routed directly to the inventory receiving workflow.

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
````

---

# 🧾 Billing & Invoice System

BooksKart provides an automated billing and invoice workflow after successful order placement.

### Invoice Includes

* 🏢 Store information
* 🆔 Order ID
* 📅 Order date
* 👤 Customer information
* 📍 Delivery address
* 📚 Purchased books
* 🔢 Quantity
* 💰 Unit price
* 💵 Line total
* 📊 Order summary
* 💳 Payment method
* ✅ Order status
* 🧮 Grand total

Invoices can be displayed in the application and generated as downloadable PDF documents.

---

# 🛒 Order Processing

BooksKart supports multiple books within a single customer transaction.

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

Employee IDs are generated automatically.

Example:

`EMP101` → `EMP102` → `EMP103` → `EMP104`

Employees do not need to manually enter an Employee ID during registration.

---

# 🏢 Designation-Based Access

BooksKart uses human-readable designations for employee management.

### Available Designations

* 📦 **Store Clerk**
* 📋 **Inventory Manager**
* 💼 **Sales Executive**
* 👔 **Assistant Manager**
* 🏢 **Director**

The backend automatically determines the corresponding access permissions from the selected designation.

Backend access values are handled internally and are not required from employees.

---

# 🔐 Authentication System

BooksKart provides authenticated employee portals.

## 📦 Store Clerk Portal

Store Clerk operations can include:

* 📚 Catalog management
* 📦 Inventory management
* 📥 Stock receiving
* ➕ Adding book copies
* 🆕 Adding books
* 🏷️ Genre management
* 📝 Activity monitoring

## 🏢 Director Portal

Director operations include:

* 📊 Business dashboard
* 💰 Revenue monitoring
* 📈 Profit and expense records
* 📦 Inventory overview
* 👨‍💼 Employee management
* 🔐 Access management
* 📝 Activity logs
* 📚 Catalog management
* 💰 Pricing management
* 📊 Store records

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

### Business Records

* 💰 Revenue
* 📊 Sales records
* 📦 Inventory status
* 💸 Expenses
* 📈 Profit information
* 🧾 Order records
* 👨‍💼 Employee records
* 📝 Activity logs

---

# 📝 Activity Logging

Important application operations can be recorded in the activity log.

### Logged Operations Can Include

* 🔐 Employee login
* 👨‍💼 Employee creation
* 📚 Book creation
* 📦 Inventory updates
* 📥 Restocking
* 🛒 Order placement
* 🧾 Sales processing
* 💰 Pricing updates
* 🏷️ Genre creation
* 🔧 Store operations

Activity information is maintained in:

`Activity_Log.txt`

---

# 💾 Data Storage

BooksKart uses structured file-based storage.

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

* 🐍 **Python**
* 🌐 **Streamlit**
* 📊 **OpenPyXL**
* 📄 **ReportLab**
* 📑 **CSV**
* 🗂️ **JSON**
* 📝 **TXT**
* 🤖 **Google Gemini API**

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

# 📚 Book Catalog Management

Authorized employees can maintain the bookstore catalog.

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

# 📊 Store Records

Completed orders can be stored with structured customer, order, and book information.

### Records Can Include

* 🆔 Order ID
* 📅 Order date
* 👤 Customer name
* 📱 Customer phone
* 📍 Delivery address
* 📚 Book information
* 🔢 Quantity
* 💰 Unit price
* 💵 Total amount
* 💳 Payment method
* 📦 Order status

Records are maintained in:

`STORE_RECORDS.xlsx`

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

Install the dependencies using:

```bash
pip install -r requirements.txt
```

---

# 🚀 Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MJJ-TechWorld/Digital_Books_Store_Management_App.git
```

### 2️⃣ Enter the Project Directory

```bash
cd Digital_Books_Store_Management_App
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start the Application

```bash
streamlit run main.py
```

### 5️⃣ Open the Local Application

Streamlit will provide a local address similar to:

`http://localhost:8501`

---

# 🔐 Configuration

If API-assisted address functionality is enabled, configure the required Gemini API credential through the supported environment or Streamlit secrets configuration.

Do not commit private API credentials to the GitHub repository.

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

## 🚀 LIVE APPLICATION

### 👉 [📚 OPEN BOOKSKART](https://my-bookskart.streamlit.app/)

**Browse Books • Manage Inventory • Process Orders • Generate Invoices**

---

# 💻 GitHub Repository

### 👉 [📂 VIEW SOURCE CODE ON GITHUB](https://github.com/MJJ-TechWorld/Digital_Books_Store_Management_App)

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
