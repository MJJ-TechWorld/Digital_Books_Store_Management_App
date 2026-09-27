📚✨ My BooksKart — Digital Books Store Management App

> 🎯 A Streamlit-based Digital Books Store Management System for managing book catalogs, inventory, customer orders, billing, employees, authentication, business operations, and store records through an interactive web interface.




---

🚀🌐 Live Application

🔥 Try My BooksKart Online

👉 📚 OPEN MY BOOKSKART — LIVE APPLICATION

Experience the complete My BooksKart application directly from your browser.


---

💻📂 GitHub Repository

👉 ⭐ VIEW MY BOOKSKART SOURCE CODE ON GITHUB

Explore the complete source code, project structure, implementation, and development files.


---

🌟 Features

🛍️ Customer Store

My BooksKart provides a browser-based bookstore storefront where customers can purchase books without creating an account.

📚 Book Catalog & Browsing

🔎 Book Search

🏷️ Genre-Based Browsing

📖 Book Information

🛒 Shopping Cart

➕ Add Books to Cart

➖ Modify Cart Quantities

🧹 Remove Items from Cart

💰 Automatic Cart Total Calculation

📦 Customer Checkout

💳 Cash-on-Delivery Payment

🧾 Automatic Invoice Generation

📄 Downloadable PDF Invoice

🆔 Automatic Order ID Generation

📊 Automatic Inventory Deduction

📝 Complete Order Records



---

📦 Inventory Management

The inventory system allows authorized employees to monitor and maintain book stock.

📊 Stock Classification

Stock Quantity	Status

0	🔴 Out of Stock
1–2	🟠 Low Stock
>2	🟢 Healthy Stock


🔧 Inventory Operations

📊 View Inventory

🔎 Search Inventory

📥 Restock Books

➕ Add Book Copies

🆕 Add New Books

🏷️ Create New Genres

💰 Update Book Pricing

📦 Monitor Stock Levels

🚨 Identify Out-of-Stock Books

📝 Record Inventory Operations


📥 Quick Restocking

When a book reaches 0 stock, the Stock Clerk can use the 📥 Restock action from the out-of-stock section.

The system automatically takes the selected book to Inventory Receiving, where the exact book is already selected for receiving.


---

👤 Customer Checkout

Customers can enter structured delivery information during checkout.

📋 Customer Details

👤 Full Name

📱 Phone Number

🏠 Flat / House / Building

🛣️ Street / Area

📍 Landmark

🏙️ City

🗺️ State

📮 PIN Code


The information is associated with the order and stored with the corresponding store records.


---

🇮🇳 Cascading Indian Address System

My BooksKart provides a guided Indian address-selection workflow:

🗺️ State
   ↓
📍 District
   ↓
🏙️ City
   ↓
📮 PIN Code

The selections are dynamically dependent on the previous selection.

For example:

Select State
     ↓
Only districts from that state
     ↓
Only cities from that district
     ↓
PIN codes belonging to that city

This helps reduce incorrect combinations during customer checkout.

The application can use the Google Gemini API for address-related processing while maintaining a local cache to reduce repeated requests.


---

🧾 Billing & Invoice System

After an order is successfully placed, My BooksKart generates a structured retail-style invoice.

📄 Invoice Includes

🏢 MY BOOKSKART

📚 Digital Books Store

🧾 Invoice / Bill Information

🆔 Order ID

📅 Order Date

👤 Customer Information

📍 Delivery Address

📚 Purchased Books

🔢 Quantity

💰 Unit Price

💵 Line Total

📊 Order Summary

💳 Payment Method

📦 Order Status

🧮 Grand Total

🏷️ MJJ-TechWorld Branding


Invoices can be displayed in the application and generated as downloadable PDF documents.


---

🛒 Complete Order Processing

My BooksKart supports multiple books in a single transaction.

📚 Browse Books
      ↓
🔎 Search / Filter
      ↓
🛒 Add Books to Cart
      ↓
🔢 Modify Quantities
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
📦 Deduct Inventory
      ↓
💾 Save Store Records
      ↓
🧾 Generate Invoice
      ↓
📄 Download PDF


---

👨‍💼 Employee Management

Employee management is available through the authorized Director portal.

🪪 Automatic Employee IDs

Employee IDs are generated automatically by the system.

Example:

EMP101
EMP102
EMP103
EMP104

The Director does not manually enter an Employee ID while creating an employee.

The system checks existing employee IDs and generates the next appropriate numeric ID automatically.


---

🏢 Designation-Based Access

The current application uses two designations only:

Designation	Backend Access

📦 Stock Clerk	s
🏢 Director	d


The backend access values are used internally and are not displayed to employees in the application interface.

Employees select their designation, while the corresponding access is determined automatically by the system.


---

🔐 Authentication System

The application provides separate authenticated employee portals.

📦 Stock Clerk Portal

Stock Clerk operations include:

📚 Catalog Management

📦 Inventory Management

📥 Inventory Receiving

➕ Adding Book Copies

🆕 Adding Books

🏷️ Genre Management

💰 Pricing Operations

📝 Activity Monitoring

🚨 Out-of-Stock Monitoring

📥 Quick Restocking



---

🏢 Director Portal

Director operations include:

📊 Business Dashboard

💰 Revenue Monitoring

📈 Profit & Expense Records

📦 Inventory Overview

👨‍💼 Employee Management

🔐 Access Management

📝 Activity Logs

📚 Catalog Management

💰 Pricing Management

📊 Store Records

💸 Expense Management



---

🔑 Default Account

My BooksKart initializes a default Director account when required.

Field	Value

👤 Employee ID	EMP101
👤 Username	user@
🔑 Password	12345678
🏢 Designation	Director
🔐 Access	Director


The default account is intended for initial access to the employee management system.


---

📊 Business Management

The Director portal provides centralized information about bookstore operations.

📈 Business Records

💰 Revenue

📊 Sales Records

📦 Inventory Status

💸 Expenses

📈 Profit Information

🧾 Order Records

👨‍💼 Employee Records

📝 Activity Logs

📚 Catalog Information

💰 Pricing Information



---

📝 Activity Logging

Important application operations are recorded through the activity logging system.

Logged Operations Can Include

🔐 Employee Login

👨‍💼 Employee Creation

📚 Book Creation

📦 Inventory Updates

📥 Restocking

🛒 Order Placement

🧾 Sales Processing

💰 Pricing Updates

🏷️ Genre Creation

🔧 Store Operations


Activity information is maintained in:

Activity_Log.txt


---

💾 File-Based Data Storage

My BooksKart uses structured files instead of a traditional database.

File	Purpose

📚 BOOKS_DATA.xlsx	Book catalog and inventory data
🧾 STORE_RECORDS.xlsx	Customer, order and sales records
👨‍💼 EMPLOYEES.csv	Employee information and credentials
💰 EXPENSES.csv	Store expense records
📝 Activity_Log.txt	Application activity logs
🏷️ GENRES.txt	Available book genres
🔐 CREDENTIAL.txt	Credential-related system data
📍 ADDRESS_CACHE.json	Address-selection cache


Required runtime files can be initialized automatically by the application.

🗄️ No SQL Database Required

The application uses:

📊 Excel

📄 CSV

📝 TXT

🔧 JSON


There is no SQLite or other SQL database dependency for the core application storage.


---

📊 Store Records

Completed orders are stored with structured customer, order, and book information.

Typical records include:

🆔 Order ID

📅 Order Date

👤 Customer Name

📱 Customer Phone

🏠 Delivery Address

📍 City / State / PIN

📚 Book Information

🔢 Quantity

💰 Unit Price

💵 Total Amount

💳 Payment Method

📦 Order Status


Records are maintained in:

STORE_RECORDS.xlsx

Each purchased book can be recorded with the associated order and customer information, allowing sales data to be maintained in a structured format.


---

📚 Book Catalog Management

Authorized employees can maintain the bookstore catalog through the application.

Catalog Operations

🔎 Search existing books

📖 View book information

➕ Add additional copies

🆕 Add new books

🏷️ Create new genres

💰 Maintain pricing

📦 Monitor inventory

🚨 Identify unavailable books



---

🛍️ Storefront Workflow

📚 Browse Catalog
       ↓
🔎 Search Books
       ↓
📖 View Book
       ↓
🛒 Add to Cart
       ↓
🧾 Review Cart
       ↓
📍 Delivery Information
       ↓
💳 Cash on Delivery
       ↓
✅ Confirm Purchase
       ↓
🧾 Invoice


---

👨‍💼 Employee Records

Employee records can contain:

🪪 Employee ID

👤 Full Name

📱 Phone

📧 Email

🔐 Username

🔑 Password

🏢 Designation

📅 Joining Date

🟢 Account Status


Employee IDs are generated automatically by the system.


---

🛡️ Access Control Structure

🏢 Director
    │
    ├── 📊 Business Dashboard
    ├── 👨‍💼 Employee Management
    ├── 📦 Inventory
    ├── 📚 Catalog
    ├── 💰 Pricing
    ├── 💸 Expenses
    ├── 📊 Store Records
    └── 📝 Activity Logs

📦 Stock Clerk
    │
    ├── 📦 Inventory
    ├── 📥 Inventory Receiving
    ├── 📚 Catalog Operations
    ├── 🏷️ Genre Management
    ├── 💰 Pricing Operations
    └── 📝 Activity Monitoring


---

📥 Inventory Receiving Workflow

🚨 Out-of-Stock Book
        ↓
📥 Click Restock
        ↓
📚 Exact Book Automatically Selected
        ↓
🔢 Enter Quantity
        ↓
✅ Confirm Receiving
        ↓
📦 Inventory Updated
        ↓
📝 Activity Recorded


---

🏗️ Application Architecture

📚 MY BOOKSKART
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        🛍️ CUSTOMER      📦 STOCK CLERK    🏢 DIRECTOR
              │               │               │
              ▼               ▼               ▼
         📚 Catalog       📦 Inventory     📊 Dashboard
         🔎 Search        📥 Receiving     👨‍💼 Employees
         🛒 Cart          📚 Catalog       📈 Business
         🧾 Checkout      🏷️ Genres       💸 Expenses
         💳 COD           💰 Pricing      📝 Logs
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                     💾 FILE-BASED STORAGE
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      📊 Excel              📄 CSV              📝 TXT/JSON


---

🔄 Customer Workflow

🚀 Open My BooksKart
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
💳 Cash on Delivery
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


---

🔄 Employee Workflow

🚀 Open My BooksKart
        │
        ▼
👨‍💼 Select Employee Portal
        │
        ▼
🔐 Employee Login
        │
        ▼
🛡️ Access Determined Automatically
        │
        ▼
📊 Open Authorized Dashboard
        │
        ├── 📦 Inventory
        ├── 📥 Receiving
        ├── 📚 Catalog
        ├── 🏷️ Genres
        ├── 💰 Pricing
        ├── 👨‍💼 Employees
        ├── 📈 Business Records
        └── 📝 Activity Logs


---

🧩 Main Application Sections

The application is organized around the following functional areas:

🛍️ Customer

Customer storefront, catalog, search, cart, checkout, COD ordering and invoice generation.

📦 Stock Clerk

Inventory, receiving, restocking, catalog operations, genres, pricing and activity monitoring.

🏢 Director

Business dashboard, employees, access management, inventory, catalog, pricing, expenses, records and activity logs.

🧾 Orders

Customer orders, sales records, inventory synchronization and invoice generation.

📊 Business Operations

Revenue, expenses, profit information, inventory information and operational records.


---

🛠️ Technologies Used

🐍 Core Technology

Python


🌐 Web Application

Streamlit


📊 Data Management

OpenPyXL

CSV

JSON

TXT


🧾 Document Generation

ReportLab


🤖 Address Processing

Google Gemini API



---

📁 Project Structure

My_BooksKart_App/
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


---

⚙️ Requirements

🐍 Python 3.x

📦 Required packages listed in requirements.txt

🌐 Internet connection for API-assisted address functionality


Install the required dependencies:

pip install -r requirements.txt


---

🚀 Run Locally

1️⃣ Clone the Repository

git clone https://github.com/MJJ-TechWorld/My_BooksKart_App.git

2️⃣ Enter the Project Directory

cd My_BooksKart_App

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Start the Application

streamlit run main.py

5️⃣ Open the Local Application

Streamlit will provide a local address similar to:

http://localhost:8501


---

🔐 Configuration

If API-assisted address functionality is enabled, configure the required Gemini API key through the supported environment or Streamlit secrets configuration.

⚠️ Do not commit private API credentials to the GitHub repository.


---

📊 System Highlights

🛒 Customer Store

Customers can browse books, search the catalog, manage their cart, enter delivery information, place COD orders, and receive invoices through an integrated workflow.

📦 Inventory Synchronization

Completed purchases automatically reduce available stock, while inventory receiving increases stock quantities.

📥 Guided Restocking

Out-of-stock books provide a direct restocking action that automatically selects the exact book in the inventory receiving section.

🧾 Automated Billing

Orders are converted into structured invoices containing customer, book, pricing, payment, and delivery information.

👨‍💼 Two-Level Employee Access

The system currently supports Stock Clerk and Director designations, with access determined automatically from the designation.

🪪 Automatic Employee IDs

Employee IDs are generated by checking existing employee records and assigning the next appropriate ID.

📊 Operational Records

Customer orders, employee information, inventory changes, expenses, and activity records are maintained through structured files.

📍 Cascading Address Selection

State → District → City → PIN selection provides a guided Indian address-entry process.

🌐 Web-Based Application

The application is built with Streamlit and can be accessed directly through a web browser.

🧾 Retail-Style PDF Invoices

The invoice system generates a structured PDF bill branded as MY BOOKSKART — Digital Books Store.

🗃️ Automatic Runtime File Initialization

Required Excel, CSV, TXT and JSON files can be created or initialized by the application when needed.


---

🎯 Project Purpose

My BooksKart demonstrates how Python and Streamlit can be used to build a practical digital bookstore management platform without relying on a traditional SQL database.

The project combines:

📚 Book Catalog Management

🛒 Customer Shopping

📦 Inventory Management

📥 Inventory Receiving

🧾 Billing & Invoicing

👨‍💼 Employee Management

🔐 Authentication

🛡️ Designation-Based Access

📊 Business Records

💸 Expense Management

📝 Activity Logging

💾 File-Based Data Management

🇮🇳 Indian Address Processing

🤖 Gemini-Assisted Address Functionality

🌐 Streamlit Web Application



---

🌐 Access My BooksKart

🚀 LIVE APPLICATION

👉 📚 OPEN MY BOOKSKART

Browse Books • Manage Inventory • Process Orders • Generate Invoices


---

💻 GitHub Repository

👉 📂 VIEW MY BOOKSKART SOURCE CODE ON GITHUB


---

👨‍💻 Author

MJJ-TechWorld

🇮🇳 Made in India

Built with Python + Streamlit for digital bookstore operations and management.


---

⭐ Support the Project

If you find My BooksKart useful:

⭐ Star the repository
🍴 Fork the project
💡 Explore the source code
🚀 Try the live application


---

📚 My BooksKart

> Browse. Manage. Order. Track.



🐍 Built with Python | 🌐 Powered by Streamlit | 📚 Designed for Digital Book Store Management
