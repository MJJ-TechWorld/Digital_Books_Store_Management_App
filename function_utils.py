import csv
import re
import html
import uuid
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook, load_workbook

BASE_DIR = Path(__file__).resolve().parent
BOOK_DATA_PATH = BASE_DIR / "BOOKS_DATA.xlsx"
STORE_DATA_PATH = BASE_DIR / "STORE_RECORDS.xlsx"
EMPLS_DATA_PATH = BASE_DIR / "EMPLOYEES.csv"
LOG_DATA_PATH = BASE_DIR / "Activity_Log.txt"
GENRES_DATA_PATH = BASE_DIR / "GENRES.txt"
EXPENSES_DATA_PATH = BASE_DIR / "EXPENSES.csv"
CREDT_DATA_PATH = BASE_DIR / "CREDENTIAL.txt"

BOOK_HEADERS = ["Book ID", "Book Name", "Author Name", "Genre", "Language", "Published Date", "Wholesale Price", "Market Price", "Profit Margin", "Quantities Available"]
EMP_HEADERS = ["Employee ID", "Full Name", "Phone", "Email", "Username", "Password", "Designation", "Access", "Status", "Joined On"]
SALES_HEADERS = ["Order ID", "Order Date", "Customer Name", "Phone", "Flat / House / Building", "Street / Area", "Landmark", "City", "State", "PIN", "Payment Method", "Book ID", "Book Name", "Author", "Genre", "Quantity", "Unit Price", "Cost Price", "Line Total", "Line Profit", "Order Status"]
EXPENSE_HEADERS = ["Expense ID", "Date", "Category", "Description", "Amount"]

ALIASES = {
    "id": ["book id", "book code", "ddc code", "code", "id", "isbn"],
    "name": ["book name", "title", "name", "book"],
    "author": ["author name", "author", "writer"],
    "genre": ["genre", "category", "section"],
    "language": ["language", "lang"],
    "published": ["published date", "publication date", "year", "published"],
    "cost": ["wholesale price", "cost price", "purchase price", "cost"],
    "price": ["market price (inr)", "market price", "selling price", "sale price", "price", "mrp"],
    "profit": ["profit margin", "margin", "profit"],
    "stock": ["quantities available", "quantity", "stock", "copies", "available copies"]
}

def norm(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").strip().lower()).strip()

def clean_name(value):
    return " ".join(str(value or "").strip().split()).title()

def clean_address(value):
    value = " ".join(str(value or "").strip().split())
    if not value:
        return ""
    parts = re.split(r",\s*", value)
    return ", ".join(p.strip().title() for p in parts if p.strip())

def clean_text(value):
    return " ".join(str(value or "").strip().split())

def money(value):
    try:
        return round(float(value or 0), 2)
    except Exception:
        return 0.0

def integer(value):
    try:
        return int(float(value or 0))
    except Exception:
        return 0

def ensure_runtime_files():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if not BOOK_DATA_PATH.exists():
        wb = Workbook()
        ws = wb.active
        ws.title = "BOOKS -- GENERAL"
        ws.append(BOOK_HEADERS)
        wb.save(BOOK_DATA_PATH)
    if not STORE_DATA_PATH.exists():
        wb = Workbook()
        ws = wb.active
        ws.title = "Sales"
        ws.append(SALES_HEADERS)
        wb.create_sheet("Orders")
        wb.save(STORE_DATA_PATH)
    if not EMPLS_DATA_PATH.exists():
        with open(EMPLS_DATA_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(EMP_HEADERS)
    if not LOG_DATA_PATH.exists():
        LOG_DATA_PATH.write_text("BOOK STORE ACTIVITY LOG\n" + "=" * 90 + "\n", encoding="utf-8")
    if not GENRES_DATA_PATH.exists():
        GENRES_DATA_PATH.write_text("General\n", encoding="utf-8")
    if not EXPENSES_DATA_PATH.exists():
        with open(EXPENSES_DATA_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(EXPENSE_HEADERS)
    if not CREDT_DATA_PATH.exists():
        CREDT_DATA_PATH.write_text("Runtime credentials are managed through EMPLOYEES.csv.\n", encoding="utf-8")

def _header_map(headers):
    return {norm(h): i for i, h in enumerate(headers)}

def _find_index(mapping, aliases):
    for alias in aliases:
        if norm(alias) in mapping:
            return mapping[norm(alias)]
    for key, idx in mapping.items():
        for alias in aliases:
            if norm(alias) in key or key in norm(alias):
                return idx
    return None

def load_books():
    ensure_runtime_files()
    wb = load_workbook(BOOK_DATA_PATH, data_only=True)
    books = []
    for ws in wb.worksheets:
        values = list(ws.iter_rows(values_only=True))
        if not values:
            continue
        headers = list(values[0])
        mapping = _header_map(headers)
        for row in values[1:]:
            if not row or not any(v is not None and str(v).strip() for v in row):
                continue
            def get(kind):
                idx = _find_index(mapping, ALIASES[kind])
                return row[idx] if idx is not None and idx < len(row) else ""
            bid = clean_text(get("id"))
            name = clean_text(get("name"))
            if not name:
                continue
            genre = clean_text(get("genre")) or ws.title.split("--")[0].strip().title()
            books.append({
                "id": bid,
                "name": name,
                "author": clean_name(get("author")),
                "genre": genre,
                "language": clean_text(get("language")) or "English",
                "published": clean_text(get("published")),
                "cost": money(get("cost")),
                "price": money(get("price")),
                "profit": money(get("profit")),
                "stock": integer(get("stock")),
                "sheet": ws.title
            })
    used = {b["id"] for b in books if b["id"]}
    seq = 1
    for b in books:
        if not b["id"]:
            while f"BK{seq:04d}" in used:
                seq += 1
            b["id"] = f"BK{seq:04d}"
            used.add(b["id"])
            seq += 1
    return books

def save_books(books):
    wb = Workbook()
    first = True
    groups = {}
    for b in books:
        groups.setdefault(b.get("genre") or "General", []).append(b)
    for genre, rows in groups.items():
        title = re.sub(r"[^A-Za-z0-9 &_-]", "", genre)[:20] or "General"
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title[:31]
        ws.append(BOOK_HEADERS)
        for i, b in enumerate(rows, 1):
            ws.append([b["id"], b["name"], b["author"], b["genre"], b["language"], b["published"], b["cost"], b["price"], b["profit"], b["stock"]])
    if first:
        ws = wb.active
        ws.title = "BOOKS -- GENERAL"
        ws.append(BOOK_HEADERS)
    wb.save(BOOK_DATA_PATH)

def get_book(book_id):
    for b in load_books():
        if b["id"] == book_id:
            return b
    return None

def add_book(book):
    books = load_books()
    books.append(book)
    save_books(books)
    return book

def update_book(book_id, **changes):
    books = load_books()
    found = None
    for b in books:
        if b["id"] == book_id:
            b.update(changes)
            found = b
            break
    if found:
        save_books(books)
    return found

def add_stock(book_id, copies):
    books = load_books()
    for b in books:
        if b["id"] == book_id:
            b["stock"] += integer(copies)
            save_books(books)
            return b
    return None

def reduce_stock(items):
    books = load_books()
    index = {b["id"]: b for b in books}
    for item in items:
        if item["book_id"] not in index or index[item["book_id"]]["stock"] < integer(item["quantity"]):
            return False
    for item in items:
        index[item["book_id"]]["stock"] -= integer(item["quantity"])
    save_books(books)
    return True

def load_employees():
    ensure_runtime_files()
    with open(EMPLS_DATA_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return []
    headers = rows[0]
    result = []
    for row in rows[1:]:
        if not row or not any(str(x).strip() for x in row):
            continue
        row = row + [""] * max(0, len(EMP_HEADERS) - len(row))
        if len(headers) < len(EMP_HEADERS):
            headers = EMP_HEADERS
        result.append(dict(zip(headers, row)))
    return result

def generate_employee_id():
    highest = 100
    for emp in load_employees():
        text = " ".join(str(v) for v in emp.values())
        for n in re.findall(r"EMP\s*0*(\d+)", text.upper()):
            highest = max(highest, int(n))
    return f"EMP{highest + 1}"

def authenticate_employee(username, password):
    username = clean_text(username)
    for emp in load_employees():
        if clean_text(emp.get("Username")) == username and str(emp.get("Password", "")) == str(password):
            access = clean_text(emp.get("Access")).lower()
            designation = clean_text(emp.get("Designation")).lower()
            role = "Director" if access in {"csp", "p", "director", "admin"} or "director" in designation else "Store Clerk"
            emp["role"] = role
            return emp
    return None

def create_employee(full_name, phone, email, username, password, designation="Store Clerk", access="s"):
    employees = load_employees()
    if any(clean_text(e.get("Username")).lower() == clean_text(username).lower() for e in employees):
        raise ValueError("Username already exists.")
    emp_id = generate_employee_id()
    record = {"Employee ID": emp_id, "Full Name": clean_name(full_name), "Phone": clean_text(phone), "Email": clean_text(email).lower(), "Username": clean_text(username), "Password": str(password), "Designation": clean_name(designation), "Access": access, "Status": "Active", "Joined On": datetime.now().strftime("%d-%m-%Y")}
    with open(EMPLS_DATA_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([record[h] for h in EMP_HEADERS])
    return record

def load_genres():
    ensure_runtime_files()
    values = [clean_text(x) for x in GENRES_DATA_PATH.read_text(encoding="utf-8").splitlines() if clean_text(x)]
    values += [b["genre"] for b in load_books() if b["genre"]]
    return sorted(set(values), key=str.lower)

def add_genre(genre):
    genre = clean_name(genre)
    if not genre:
        return False
    genres = load_genres()
    if genre.lower() in {g.lower() for g in genres}:
        return False
    with open(GENRES_DATA_PATH, "a", encoding="utf-8") as f:
        f.write(genre + "\n")
    return True

def log_activity(actor, action, details=""):
    ensure_runtime_files()
    stamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(LOG_DATA_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] | {clean_text(actor)} | {clean_text(action)} | {clean_text(details)}\n")

def load_logs(limit=250):
    ensure_runtime_files()
    lines = LOG_DATA_PATH.read_text(encoding="utf-8").splitlines()
    return [x for x in lines if x.startswith("[")][-limit:][::-1]

def _ensure_sales_sheet(wb):
    if "Sales" not in wb.sheetnames:
        ws = wb.create_sheet("Sales")
        ws.append(SALES_HEADERS)
    return wb["Sales"]

def append_order(order, items):
    ensure_runtime_files()
    wb = load_workbook(STORE_DATA_PATH)
    ws = _ensure_sales_sheet(wb)
    for item in items:
        ws.append([order["order_id"], order["date"], order["customer_name"], order["phone"], order["flat"], order["street"], order["landmark"], order["city"], order["state"], order["pin"], order["payment"], item["book_id"], item["name"], item["author"], item["genre"], item["quantity"], item["unit_price"], item["cost_price"], item["line_total"], item["line_profit"], "Confirmed"])
    if "Orders" not in wb.sheetnames:
        wb.create_sheet("Orders")
    ow = wb["Orders"]
    if ow.max_row == 1 and ow.cell(1,1).value is None:
        ow.append(["Order ID", "Date", "Customer Name", "Phone", "City", "State", "PIN", "Payment", "Items", "Grand Total", "Grand Profit", "Status"])
    elif ow.max_row == 1 and ow.cell(1,1).value != "Order ID":
        pass
    if ow.max_row == 1 and ow.cell(1,1).value is None:
        pass
    if ow.max_row == 1 and ow.cell(1,1).value == "Order ID":
        pass
    ow.append([order["order_id"], order["date"], order["customer_name"], order["phone"], order["city"], order["state"], order["pin"], order["payment"], sum(integer(i["quantity"]) for i in items), order["grand_total"], order["grand_profit"], "Confirmed"])
    wb.save(STORE_DATA_PATH)

def new_order_id():
    return "ORD-" + datetime.now().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:6].upper()

def load_sales():
    ensure_runtime_files()
    wb = load_workbook(STORE_DATA_PATH, data_only=True)
    if "Sales" not in wb.sheetnames:
        return []
    ws = wb["Sales"]
    values = list(ws.values)
    if not values:
        return []
    headers = [str(x) for x in values[0]]
    return [dict(zip(headers, r)) for r in values[1:] if r and any(x is not None for x in r)]

def add_expense(category, description, amount):
    eid = "EXP-" + datetime.now().strftime("%Y%m%d%H%M%S")
    with open(EXPENSES_DATA_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([eid, datetime.now().strftime("%d-%m-%Y"), clean_name(category), clean_text(description), money(amount)])
    return eid

def load_expenses():
    ensure_runtime_files()
    with open(EXPENSES_DATA_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows

def invoice_html(order, items):
    rows = "".join(f"<tr><td>{html.escape(str(i['name']))}</td><td>{html.escape(str(i['book_id']))}</td><td>{i['quantity']}</td><td>₹{i['unit_price']:.2f}</td><td>₹{i['line_total']:.2f}</td></tr>" for i in items)
    address = ", ".join(x for x in [order['flat'], order['street'], order['landmark'], order['city'], order['state'] + " - " + order['pin']] if x)
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{order['order_id']}</title><style>body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#172033;padding:32px}}.invoice{{max-width:900px;margin:auto;background:white;border-radius:22px;padding:36px;box-shadow:0 20px 60px #14213d18}}h1{{margin:0;color:#633cff}}.top{{display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid #e5e7eb;padding-bottom:22px}}table{{width:100%;border-collapse:collapse;margin-top:25px}}th,td{{padding:13px;border-bottom:1px solid #e5e7eb;text-align:left}}th{{background:#f0edff}}.total{{font-size:24px;font-weight:800;text-align:right;margin-top:22px;color:#0f8b6d}}.muted{{color:#667085}}</style></head><body><div class="invoice"><div class="top"><div><h1>BOOKNEST</h1><p class="muted">Premium Book Store · Tax Invoice</p></div><div><b>Order ID</b><br>{order['order_id']}<br><span class="muted">{order['date']}</span></div></div><h3>Customer</h3><p><b>{html.escape(order['customer_name'])}</b><br>{html.escape(order['phone'])}<br>{html.escape(address)}</p><table><tr><th>Book</th><th>Code</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr>{rows}</table><div class="total">Grand Total: ₹{order['grand_total']:.2f}</div><p class="muted">Payment: {order['payment']} · Status: Confirmed</p></div></body></html>'''
