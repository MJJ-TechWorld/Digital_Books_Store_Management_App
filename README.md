````markdown
# ***📚✨ My BooksKart — Digital Books Store Management App***

> ***🎯 A Streamlit-based Digital Books Store Management System for managing book catalogs, inventory, customer orders, billing, employees, authentication, business operations, and store records through an interactive web interface.***

---

# ***🚀🌐 LIVE APPLICATION***

## ***🔥 Try My BooksKart Online***

### 👉 [📚 OPEN MY BOOKSKART — LIVE APPLICATION](https://my-bookskart.streamlit.app/)

***Experience My BooksKart directly from your browser.***

---

# ***💻📂 GITHUB REPOSITORY***

### 👉 [⭐ VIEW MY BOOKSKART SOURCE CODE ON GITHUB](https://github.com/MJJ-TechWorld/My_BooksKart_App)

***Explore the complete source code, project structure, implementation, and development files.***

---

# ***🌟 FEATURES***

## ***🛍️ Customer Store***

My BooksKart provides a complete browser-based bookstore storefront where customers can browse books, search the catalog, manage their cart, and place orders without creating an account.

- 📚 ***Book Catalog & Browsing***
- 🔎 ***Book Search***
- 🏷️ ***Genre-Based Browsing***
- 📖 ***Book Information***
- 🛒 ***Shopping Cart***
- ➕ ***Add Books to Cart***
- ➖ ***Modify Cart Quantities***
- 🧹 ***Remove Items from Cart***
- 💰 ***Automatic Cart Total Calculation***
- 📦 ***Customer Checkout***
- 💳 ***Cash-on-Delivery Payment***
- 🧾 ***Automatic Invoice Generation***
- 📄 ***Downloadable PDF Invoice***
- 🆔 ***Automatic Order ID Generation***
- 📊 ***Automatic Inventory Deduction***
- 📝 ***Complete Order Records***

---

## ***📦 Inventory Management***

The inventory system allows authorized employees to monitor, maintain, receive, and update book stock.

### ***📊 Stock Classification***

| ***Stock Quantity*** | ***Status*** |
|---:|---|
| `0` | 🔴 ***Out of Stock*** |
| `1–2` | 🟠 ***Low Stock*** |
| `>2` | 🟢 ***Healthy Stock*** |

### ***🔧 Inventory Operations***

- 📊 ***View Inventory***
- 🔎 ***Search Inventory***
- 📥 ***Restock Books***
- ➕ ***Add Book Copies***
- 🆕 ***Add New Books***
- 🏷️ ***Create New Genres***
- 💰 ***Update Book Pricing***
- 📦 ***Monitor Stock Levels***
- 🚨 ***Identify Out-of-Stock Books***
- 📝 ***Record Inventory Operations***

### ***📥 Quick Restocking***

When a book reaches zero stock, the Stock Clerk can use the ***📥 Restock*** action.

The system automatically opens ***Inventory Receiving*** with the exact selected book pre-selected for receiving.

---

# ***👤 CUSTOMER CHECKOUT***

Customers can enter structured delivery information during checkout.

### ***📋 Customer Details***

- 👤 ***Full Name***
- 📱 ***Phone Number***
- 🏠 ***Flat / House / Building***
- 🛣️ ***Street / Area***
- 📍 ***Landmark***
- 🏙️ ***City***
- 🗺️ ***State***
- 📮 ***PIN Code***

The customer and delivery information is associated with the order and maintained in the store records.

---

# ***🇮🇳 CASCADING INDIAN ADDRESS SYSTEM***

My BooksKart provides a guided Indian address-selection workflow:

```text
🗺️ State
   ↓
📍 District
   ↓
🏙️ City
   ↓
📮 PIN Code
````

Each selection is used to determine the available options for the next level.

### ***📍 Address Selection Flow***

```text
Select State
     ↓
Districts for Selected State
     ↓
Cities for Selected District
     ↓
PIN Codes for Selected City
```

The address system is designed to provide a structured and guided checkout experience.

The application can use the ***Google Gemini API*** for address-related processing and maintain an address cache to reduce repeated processing.

---

# ***🧾 BILLING & INVOICE SYSTEM***

After successful order placement, My BooksKart generates a structured retail-style invoice.

### ***📄 Invoice Includes***

* 🏢 ***MY BOOKSKART***
* 📚 ***Digital Books Store***
* 🧾 ***Invoice / Bill Information***
* 🆔 ***Order ID***
* 📅 ***Order Date***
* 👤 ***Customer Information***
* 📍 ***Delivery Address***
* 📚 ***Purchased Books***
* 🔢 ***Quantity***
* 💰 ***Unit Price***
* 💵 ***Line Total***
* 📊 ***Order Summary***
* 💳 ***Payment Method***
* 📦 ***Order Status***
* 🧮 ***Grand Total***
* 🏷️ ***MJJ-TechWorld Branding***

Invoices can be displayed within the application and generated as downloadable PDF documents.

---

# ***🛒 COMPLETE ORDER PROCESSING***

My BooksKart supports multiple books in a single transaction.

```text
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
```

---

# ***👨‍💼 EMPLOYEE MANAGEMENT***

Employee management is available through the authorized Director portal.

## ***🪪 AUTOMATIC EMPLOYEE IDs***

Employee IDs are generated automatically by the system.

Example:

```text
EMP101
EMP102
EMP103
EMP104
```

The Director does not manually enter an Employee ID when creating an employee.

The system checks the existing employee records and generates the next appropriate numeric Employee ID.

---

# ***🏢 DESIGNATION-BASED ACCESS***

My BooksKart currently supports two employee designations:

| ***Designation***    | ***Internal Access*** |
| -------------------- | --------------------- |
| 📦 ***Stock Clerk*** | `s`                   |
| 🏢 ***Director***    | `d`                   |

The internal access values are handled by the backend and are not required to be entered by employees.

The application determines access automatically from the employee's designation.

---

# ***🔐 AUTHENTICATION SYSTEM***

The application provides authenticated employee portals with designation-based access control.

## ***📦 STOCK CLERK PORTAL***

Stock Clerk operations include:

* 📚 ***Catalog Management***
* 📦 ***Inventory Management***
* 📥 ***Inventory Receiving***
* ➕ ***Adding Book Copies***
* 🆕 ***Adding Books***
* 🏷️ ***Genre Management***
* 💰 ***Pricing Operations***
* 📝 ***Activity Monitoring***
* 🚨 ***Out-of-Stock Monitoring***
* 📥 ***Quick Restocking***

---

## ***🏢 DIRECTOR PORTAL***

Director operations include:

* 📊 ***Business Dashboard***
* 💰 ***Revenue Monitoring***
* 📈 ***Profit & Expense Records***
* 📦 ***Inventory Overview***
* 👨‍💼 ***Employee Management***
* 🔐 ***Access Management***
* 📝 ***Activity Logs***
* 📚 ***Catalog Management***
* 💰 ***Pricing Management***
* 📊 ***Store Records***
* 💸 ***Expense Management***

---

# ***🔑 DEFAULT ACCOUNT***

My BooksKart initializes a default Director employee account when required.

| ***Field***            | ***Value***    |
| ---------------------- | -------------- |
| 👤 ***Employee ID***   | `EMP101`       |
| 👤 ***Username***      | `user@`        |
| 🔑 ***Password***      | `12345678`     |
| 🏢 ***Designation***   | ***Director*** |
| 🔐 ***Stored Access*** | `d`            |

### ***🔓 Default Portal Access***

The default credentials can be used to access both available employee portals:

* 🏢 ***Director Portal***
* 📦 ***Stock Clerk Portal***

The selected employee portal determines the requested session role for the default credentials.

---

# ***📊 BUSINESS MANAGEMENT***

The Director portal provides centralized information about bookstore operations.

### ***📈 Business Records***

* 💰 ***Revenue***
* 📊 ***Sales Records***
* 📦 ***Inventory Status***
* 💸 ***Expenses***
* 📈 ***Profit Information***
* 🧾 ***Order Records***
* 👨‍💼 ***Employee Records***
* 📝 ***Activity Logs***
* 📚 ***Catalog Information***
* 💰 ***Pricing Information***

---

# ***📝 ACTIVITY LOGGING***

Important application operations are recorded through the activity logging system.

### ***📋 Logged Operations Can Include***

* 🔐 ***Employee Login***
* 👨‍💼 ***Employee Creation***
* 📚 ***Book Creation***
* 📦 ***Inventory Updates***
* 📥 ***Restocking***
* 🛒 ***Order Placement***
* 🧾 ***Sales Processing***
* 💰 ***Pricing Updates***
* 🏷️ ***Genre Creation***
* 🔧 ***Store Operations***
* 💸 ***Expense Recording***

Activity information is maintained in:

```text
Activity_Log.txt
```

---

# ***💾 FILE-BASED DATA STORAGE***

My BooksKart uses structured file-based storage rather than a traditional SQL database.

| ***File***              | ***Purpose***                              |
| ----------------------- | ------------------------------------------ |
| 📚 `BOOKS_DATA.xlsx`    | ***Book catalog and inventory data***      |
| 🧾 `STORE_RECORDS.xlsx` | ***Customer, order and sales records***    |
| 👨‍💼 `EMPLOYEES.csv`   | ***Employee information and credentials*** |
| 💰 `EXPENSES.csv`       | ***Store expense records***                |
| 📝 `Activity_Log.txt`   | ***Application activity logs***            |
| 🏷️ `GENRES.txt`        | ***Available book genres***                |
| 🔐 `CREDENTIAL.txt`     | ***Credential-related system data***       |
| 📍 `ADDRESS_CACHE.json` | ***Address-selection cache***              |

Required runtime files can be initialized automatically by the application.

## ***🗄️ NO SQL DATABASE REQUIRED***

The core application uses:

* 📊 ***Excel***
* 📄 ***CSV***
* 📝 ***TXT***
* 🔧 ***JSON***

***No SQLite database is required for the core application storage.***

---

# ***📊 STORE RECORDS***

Completed orders are stored with structured customer, order, and book information.

Typical records include:

* 🆔 ***Order ID***
* 📅 ***Order Date***
* 👤 ***Customer Name***
* 📱 ***Customer Phone***
* 🏠 ***Delivery Address***
* 📍 ***City / State / PIN***
* 📚 ***Book Information***
* 🔢 ***Quantity***
* 💰 ***Unit Price***
* 💵 ***Total Amount***
* 💳 ***Payment Method***
* 📦 ***Order Status***

Records are maintained in:

```text
STORE_RECORDS.xlsx
```

Each purchased book can be associated with its corresponding order and customer information.

---

# ***📚 BOOK CATALOG MANAGEMENT***

Authorized employees can maintain the bookstore catalog through the application.

### ***📖 Catalog Operations***

* 🔎 ***Search Existing Books***
* 📖 ***View Book Information***
* ➕ ***Add Additional Copies***
* 🆕 ***Add New Books***
* 🏷️ ***Create New Genres***
* 💰 ***Maintain Pricing***
* 📦 ***Monitor Inventory***
* 🚨 ***Identify Unavailable Books***

---

# ***🛍️ STOREFRONT WORKFLOW***

```text
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
```

---

# ***👨‍💼 EMPLOYEE RECORDS***

Employee records can contain:

* 🪪 ***Employee ID***
* 👤 ***Full Name***
* 📱 ***Phone***
* 📧 ***Email***
* 🔐 ***Username***
* 🔑 ***Password***
* 🏢 ***Designation***
* 📅 ***Joining Date***
* 🟢 ***Account Status***

Employee IDs are generated automatically by the system.

---

# ***🛡️ ACCESS CONTROL STRUCTURE***

```text
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
```

---

# ***📥 INVENTORY RECEIVING WORKFLOW***

```text
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
```

---

# ***🏗️ APPLICATION ARCHITECTURE***

```text
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
         💳 COD           💰 Pricing       📝 Logs
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

# ***🔄 CUSTOMER WORKFLOW***

```text
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
```

---

# ***🔄 EMPLOYEE WORKFLOW***

```text
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
```

---

# ***🧩 MAIN APPLICATION SECTIONS***

### ***🛍️ Customer***

***Customer storefront, catalog, search, cart, checkout, COD ordering and invoice generation.***

### ***📦 Stock Clerk***

***Inventory, receiving, restocking, catalog operations, genres, pricing and activity monitoring.***

### ***🏢 Director***

***Business dashboard, employee management, access management, inventory, catalog, pricing, expenses, records and activity logs.***

### ***🧾 Orders***

***Customer orders, sales records, inventory synchronization and invoice generation.***

### ***📊 Business Operations***

***Revenue, expenses, profit information, inventory information and operational records.***

---

# ***🛠️ TECHNOLOGIES USED***

## ***🐍 Core Technology***

* ***Python***

## ***🌐 Web Application***

* ***Streamlit***

## ***📊 Data Management***

* ***OpenPyXL***
* ***CSV***
* ***JSON***
* ***TXT***

## ***🧾 Document Generation***

* ***ReportLab***

## ***🤖 Address Processing***

* ***Google Gemini API***

---

# ***📁 PROJECT STRUCTURE***

```text
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
```

---

# ***⚙️ REQUIREMENTS***

* 🐍 ***Python 3.x***
* 📦 ***Required packages listed in `requirements.txt`***
* 🌐 ***Internet connection for API-assisted address functionality***

### ***📦 Install Dependencies***

```bash
pip install -r requirements.txt
```

---

# ***🚀 RUN LOCALLY***

## ***1️⃣ Clone the Repository***

```bash
git clone https://github.com/MJJ-TechWorld/My_BooksKart_App.git
```

## ***2️⃣ Enter the Project Directory***

```bash
cd My_BooksKart_App
```

## ***3️⃣ Install Dependencies***

```bash
pip install -r requirements.txt
```

## ***4️⃣ Start the Application***

```bash
streamlit run main.py
```

## ***5️⃣ Open the Local Application***

Streamlit will provide a local address similar to:

```text
http://localhost:8501
```

---

# ***🔐 CONFIGURATION***

If API-assisted address functionality is enabled, configure the required ***Gemini API key*** through the supported environment or Streamlit secrets configuration.

> ⚠️ ***Never commit private API credentials to the GitHub repository.***

---

# ***📌 SYSTEM HIGHLIGHTS***

### ***🛒 Integrated Customer Store***

Customers can ***browse books, search the catalog, manage their cart, enter delivery information, place COD orders, and receive invoices*** through one integrated workflow.

### ***📦 Inventory Synchronization***

Completed purchases automatically ***reduce available stock***, while inventory receiving increases available stock.

### ***📥 Guided Restocking***

Out-of-stock books provide a direct ***Restock*** action that automatically selects the exact book in Inventory Receiving.

### ***🧾 Automated Billing***

Orders are converted into structured invoices containing ***customer, book, pricing, payment, delivery and order information***.

### ***👨‍💼 Two-Level Employee Access***

The system currently supports ***Stock Clerk and Director*** designations.

### ***🪪 Automatic Employee IDs***

Employee IDs are generated automatically from existing employee records.

### ***🔐 Default Employee Credentials***

The default `user@` / `12345678` credentials can be used for both available employee portal selections.

### ***📊 Operational Records***

Customer orders, employee information, inventory changes, expenses and activity records are maintained through structured files.

### ***📍 Cascading Address Selection***

***State → District → City → PIN*** selection provides a guided Indian address-entry process.

### ***🧾 Retail-Style PDF Invoices***

The invoice system generates a structured PDF bill branded as ***MY BOOKSKART — Digital Books Store***.

### ***🗃️ Runtime File Initialization***

Required application data files can be initialized automatically when required.

### ***🌐 Web-Based Application***

The application is built with ***Streamlit*** and can be accessed through a web browser.

---

# ***🎯 PROJECT PURPOSE***

**My BooksKart** demonstrates how ***Python and Streamlit*** can be used to build a practical digital bookstore management platform using file-based storage.

The project combines:

* 📚 ***Book Catalog Management***
* 🛒 ***Customer Shopping***
* 📦 ***Inventory Management***
* 📥 ***Inventory Receiving***
* 🧾 ***Billing & Invoicing***
* 👨‍💼 ***Employee Management***
* 🔐 ***Authentication***
* 🛡️ ***Designation-Based Access***
* 📊 ***Business Records***
* 💸 ***Expense Management***
* 📝 ***Activity Logging***
* 💾 ***File-Based Data Management***
* 🇮🇳 ***Indian Address Processing***
* 🤖 ***Gemini-Assisted Address Functionality***
* 🌐 ***Streamlit Web Application***

---

# ***🌐 ACCESS MY BOOKSKART***

## ***🚀 LIVE APPLICATION***

### 👉 [📚 OPEN MY BOOKSKART](https://my-bookskart.streamlit.app/)

***Browse Books • Manage Inventory • Process Orders • Generate Invoices***

---

# ***💻 GITHUB REPOSITORY***

### 👉 [📂 VIEW MY BOOKSKART SOURCE CODE ON GITHUB](https://github.com/MJJ-TechWorld/My_BooksKart_App)

---

# ***👨‍💻 AUTHOR***

## ***MJJ-TechWorld***

🇮🇳 ***Made in India***

***Built with Python + Streamlit for digital bookstore operations and management.***

---

# ***⭐ SUPPORT THE PROJECT***

If you find ***My BooksKart*** useful:

⭐ ***Star the repository***
🍴 ***Fork the project***
💡 ***Explore the source code***
🚀 ***Try the live application***

---

# ***📚 MY BOOKSKART***

> ***Browse. Manage. Order. Track.***

### ***🐍 Built with Python | 🌐 Powered by Streamlit | 📚 Designed for Digital Book Store Management***

```
```
