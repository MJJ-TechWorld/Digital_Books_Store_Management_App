import csv
import io
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BASE_DIR = Path(__file__).resolve().parent
BOOK_DATA_PATH = BASE_DIR / "BOOKS_DATA.xlsx"
STORE_DATA_PATH = BASE_DIR / "STORE_RECORDS.xlsx"
CREDT_DATA_PATH = BASE_DIR / "CREDENTIAL.txt"
EMPLS_DATA_PATH = BASE_DIR / "EMPLOYEES.csv"
LOG_DATA_PATH = BASE_DIR / "Activity_Log.txt"
GENRES_PATH = BASE_DIR / "GENRES.txt"
EXPENSES_PATH = BASE_DIR / "EXPENSES.csv"
ADDRESS_CACHE_PATH = BASE_DIR / "ADDRESS_CACHE.json"
GEMINI_MODEL = "gemini-3.5-flash-lite"

STORE_HEADERS = [
    "Order ID", "Order Date", "Customer Name", "Phone", "Flat/House/Building",
    "Street/Area", "Landmark", "City", "District", "State", "PIN Code",
    "Payment Method", "Book ID", "Book Name", "Author", "Genre", "Quantity",
    "Unit Price", "Unit Cost", "Line Total", "Line Profit", "Order Total", "Order Profit"
]

EMPLOYEE_HEADERS = [
    "Employee ID", "Full Name", "Phone", "Email", "Username", "Password",
    "Designation", "Access", "Status", "Joined On"
]

EXPENSE_HEADERS = ["Date", "Category", "Description", "Amount", "Recorded By"]


def clean_text(value):
    text = "" if value is None else str(value).strip()
    return re.sub(r"\s+", " ", text)


def title_case_text(value):
    text = clean_text(value)
    if not text:
        return ""
    return " ".join(part.capitalize() for part in text.split(" "))


def clean_address(value):
    text = clean_text(value)
    if not text:
        return ""
    replacements = {
        "flat no": "Flat No", "flat": "Flat", "house no": "House No", "house": "House",
        "building": "Building", "bldg": "Bldg", "road": "Road", "street": "Street",
        "area": "Area", "lane": "Lane", "sector": "Sector", "block": "Block"
    }
    words = []
    for word in text.split(" "):
        key = word.lower().rstrip(",")
        words.append(replacements.get(key, word.capitalize()))
    return " ".join(words)


def ensure_runtime_files():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if not BOOK_DATA_PATH.exists():
        wb = Workbook()
        ws = wb.active
        ws.title = "GENERAL"
        ws.append(["Sr No", "DDC Code", "Book Name", "Author Name", "Language", "Published Date", "Wholesale Price", "Market Price (INR)", "Profit Margin", "Quantities Available"])
        wb.save(BOOK_DATA_PATH)
    if not STORE_DATA_PATH.exists():
        wb = Workbook()
        ws = wb.active
        ws.title = "Orders"
        ws.append(STORE_HEADERS)
        wb.save(STORE_DATA_PATH)
    if not EMPLS_DATA_PATH.exists() or EMPLS_DATA_PATH.stat().st_size == 0:
        with open(EMPLS_DATA_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(EMPLOYEE_HEADERS)
            writer.writerow(["EMP101", "Store Clerk", "", "", "user@", "12345678", "Store Clerk", "sd", "Active", datetime.now().strftime("%Y-%m-%d")])
    if not CREDT_DATA_PATH.exists():
        CREDT_DATA_PATH.write_text("EMPLOYEE ACCOUNT CREDENTIALS ARE STORED IN EMPLOYEES.CSV\n", encoding="utf-8")
    if not LOG_DATA_PATH.exists():
        LOG_DATA_PATH.write_text("", encoding="utf-8")
    if not GENRES_PATH.exists():
        genres = []
        try:
            genres = get_genres()
        except Exception:
            genres = []
        GENRES_PATH.write_text("\n".join(genres), encoding="utf-8")
    if not EXPENSES_PATH.exists():
        with open(EXPENSES_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(EXPENSE_HEADERS)
    if not ADDRESS_CACHE_PATH.exists():
        ADDRESS_CACHE_PATH.write_text("{}", encoding="utf-8")


def _header_map(headers):
    return {clean_text(h).lower(): i for i, h in enumerate(headers)}


def load_books():
    ensure_runtime_files()
    books = []
    wb = load_workbook(BOOK_DATA_PATH, data_only=False)
    for sheet in wb.worksheets:
        if sheet.max_row < 2:
            continue
        headers = [clean_text(c.value) for c in sheet[1]]
        mapping = _header_map(headers)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(v is not None and str(v).strip() for v in row):
                continue
            book_id = row[mapping.get("ddc code", 1)] if len(row) > mapping.get("ddc code", 1) else ""
            title = row[mapping.get("book name", 2)] if len(row) > mapping.get("book name", 2) else ""
            if not title:
                continue
            author = row[mapping.get("author name", 3)] if len(row) > mapping.get("author name", 3) else ""
            genre = sheet.title.split("--")[0].strip()
            wholesale = row[mapping.get("wholesale price", 6)] if len(row) > mapping.get("wholesale price", 6) else 0
            market = row[mapping.get("market price (inr)", 7)] if len(row) > mapping.get("market price (inr)", 7) else 0
            stock = row[mapping.get("quantities available", 9)] if len(row) > mapping.get("quantities available", 9) else 0
            language = row[mapping.get("language", 4)] if len(row) > mapping.get("language", 4) else ""
            published = row[mapping.get("published date", 5)] if len(row) > mapping.get("published date", 5) else ""
            profit = row[mapping.get("profit margin", 8)] if len(row) > mapping.get("profit margin", 8) else 0
            books.append({
                "id": clean_text(book_id), "title": clean_text(title), "author": clean_text(author),
                "genre": clean_text(genre), "language": clean_text(language), "published": clean_text(published),
                "cost": to_float(wholesale), "price": to_float(market), "profit": to_float(profit),
                "stock": to_int(stock), "sheet": sheet.title
            })
    return books


def save_book_stock(book_id, new_stock):
    wb = load_workbook(BOOK_DATA_PATH)
    for ws in wb.worksheets:
        headers = [clean_text(c.value).lower() for c in ws[1]]
        if "ddc code" not in headers or "quantities available" not in headers:
            continue
        id_col = headers.index("ddc code") + 1
        stock_col = headers.index("quantities available") + 1
        for r in range(2, ws.max_row + 1):
            if clean_text(ws.cell(r, id_col).value) == clean_text(book_id):
                ws.cell(r, stock_col).value = max(0, int(new_stock))
                wb.save(BOOK_DATA_PATH)
                return True
    return False


def change_book_stock(book_id, delta):
    for book in load_books():
        if book["id"] == book_id:
            new_stock = max(0, book["stock"] + int(delta))
            if save_book_stock(book_id, new_stock):
                return new_stock
    return None


def get_genres():
    ensure_runtime_files()
    genres = []
    try:
        wb = load_workbook(BOOK_DATA_PATH, read_only=True, data_only=True)
        for name in wb.sheetnames:
            value = clean_text(name.split("--")[0])
            if value and value not in genres:
                genres.append(value)
    except Exception:
        pass
    if GENRES_PATH.exists():
        for line in GENRES_PATH.read_text(encoding="utf-8").splitlines():
            value = clean_text(line)
            if value and value not in genres:
                genres.append(value)
    return sorted(genres)


def add_genre(genre):
    genre = title_case_text(genre)
    if not genre:
        return False
    genres = get_genres()
    if genre.lower() in {g.lower() for g in genres}:
        return False
    with open(GENRES_PATH, "a", encoding="utf-8") as f:
        f.write(("" if GENRES_PATH.stat().st_size == 0 else "\n") + genre)
    return True


def load_employees():
    ensure_runtime_files()
    with open(EMPLS_DATA_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    result = []
    for raw in rows:
        row = {clean_text(k): clean_text(v) for k, v in raw.items() if k is not None}
        row["Access"] = row.get("Access", "").lower()
        result.append(row)
    return result


def generate_employee_id():
    max_id = 100
    for row in load_employees():
        match = re.search(r"(\d+)", row.get("Employee ID", ""))
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"EMP{max_id + 1}"


def create_employee(full_name, phone, email, username, password, designation):
    access = "sd" if designation == "Store Clerk" else "csp"
    employee_id = generate_employee_id()
    with open(EMPLS_DATA_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([employee_id, title_case_text(full_name), clean_text(phone), clean_text(email), clean_text(username), clean_text(password), designation, access, "Active", datetime.now().strftime("%Y-%m-%d")])
    return employee_id


def authenticate_employee(username, password):
    username = clean_text(username)
    password = clean_text(password)
    for row in load_employees():
        if row.get("Username") == username and row.get("Password") == password and row.get("Status", "Active").lower() == "active":
            return row
    return None


def append_activity(employee, action, details=""):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = employee.get("Full Name", "System") if isinstance(employee, dict) else clean_text(employee)
    with open(LOG_DATA_PATH, "a", encoding="utf-8") as f:
        f.write(f"{stamp} | {name} | {action} | {clean_text(details)}\n")


def read_activity(limit=100):
    ensure_runtime_files()
    lines = [x.strip() for x in LOG_DATA_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
    return list(reversed(lines[-limit:]))


def load_expenses():
    ensure_runtime_files()
    with open(EXPENSES_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_expense(category, description, amount, recorded_by):
    with open(EXPENSES_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d"), clean_text(category), clean_text(description), float(amount), clean_text(recorded_by)])


def append_order_records(order, items):
    ensure_runtime_files()
    wb = load_workbook(STORE_DATA_PATH)
    ws = wb.active
    if ws.max_row == 1 and not ws.cell(1, 1).value:
        ws.append(STORE_HEADERS)
    for item in items:
        ws.append([
            order["order_id"], order["date"], order["customer_name"], order["phone"], order["flat"], order["street"],
            order["landmark"], order["city"], order["district"], order["state"], order["pin"], "Cash on Delivery",
            item["id"], item["title"], item["author"], item["genre"], item["quantity"], item["unit_price"],
            item["unit_cost"], item["line_total"], item["line_profit"], order["total"], order["profit"]
        ])
    wb.save(STORE_DATA_PATH)


def generate_order_id():
    return "ORD" + datetime.now().strftime("%Y%m%d%H%M%S") + str(abs(hash(os.urandom(8))) % 1000).zfill(3)


def to_int(value):
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def to_float(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def money(value):
    return f"₹{to_float(value):,.2f}"


def stock_status(stock):
    stock = to_int(stock)
    if stock == 0:
        return "Out of Stock"
    if stock <= 2:
        return "Low Stock"
    return "Healthy"


def build_invoice_html(order, items):
    rows = "".join(
        f"<tr><td>{i+1}</td><td>{item['title']}</td><td>{item['quantity']}</td><td>{money(item['unit_price'])}</td><td>{money(item['line_total'])}</td></tr>"
        for i, item in enumerate(items)
    )
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>{order['order_id']}</title><style>body{{font-family:Arial,sans-serif;margin:40px;color:#1f2937}}h1{{margin-bottom:4px}}.muted{{color:#64748b}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:20px 0}}table{{width:100%;border-collapse:collapse;margin-top:20px}}th,td{{border:1px solid #dbe3ec;padding:10px;text-align:left}}th{{background:#eef4ff}}.total{{text-align:right;font-size:20px;font-weight:700;margin-top:20px}}</style></head><body><h1>Book Store Invoice</h1><div class='muted'>Order ID: {order['order_id']} · {order['date']}</div><div class='grid'><div><b>Customer</b><br>{order['customer_name']}<br>{order['phone']}</div><div><b>Delivery Address</b><br>{order['flat']}<br>{order['street']}<br>{order['landmark']}<br>{order['city']}, {order['district']}<br>{order['state']} - {order['pin']}</div></div><table><thead><tr><th>#</th><th>Book</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr></thead><tbody>{rows}</tbody></table><div class='total'>Total: {money(order['total'])}</div><p>Payment: Cash on Delivery</p><p>Thank you for your order.</p></body></html>"""


def build_invoice_pdf(order, items):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("invoice_title", parent=styles["Title"], fontSize=22, leading=26, textColor=colors.HexColor("#173B7A"))
    body = ParagraphStyle("invoice_body", parent=styles["BodyText"], fontSize=9, leading=13)
    story = [Paragraph("Book Store Invoice", title), Paragraph(f"Order ID: {order['order_id']}<br/>Date: {order['date']}", body), Spacer(1, 8)]
    address = f"{order['flat']}<br/>{order['street']}<br/>{order['landmark']}<br/>{order['city']}, {order['district']}<br/>{order['state']} - {order['pin']}"
    info = Table([[Paragraph(f"<b>Customer</b><br/>{order['customer_name']}<br/>{order['phone']}", body), Paragraph(f"<b>Delivery Address</b><br/>{address}", body)]], colWidths=[85*mm, 85*mm])
    info.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")), ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("PADDING", (0,0), (-1,-1), 8)]))
    story += [info, Spacer(1, 12)]
    data = [["#", "Book", "Qty", "Unit Price", "Total"]]
    for i, item in enumerate(items, 1):
        data.append([str(i), item["title"], str(item["quantity"]), money(item["unit_price"]), money(item["line_total"])])
    table = Table(data, colWidths=[10*mm, 82*mm, 15*mm, 30*mm, 30*mm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#173B7A")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")), ("PADDING", (0,0), (-1,-1), 6), ("ALIGN", (2,1), (-1,-1), "RIGHT")]))
    story += [table, Spacer(1, 12), Paragraph(f"<b>Total: {money(order['total'])}</b><br/>Payment: Cash on Delivery", body)]
    doc.build(story)
    return buffer.getvalue()


def _cache_load():
    try:
        return json.loads(ADDRESS_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _cache_save(data):
    ADDRESS_CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _cache_key(kind, state="", district="", city=""):
    return "|".join([kind, clean_text(state), clean_text(district), clean_text(city)]).lower()


def gemini_address_options(api_key, kind, state="", district="", city=""):
    ensure_runtime_files()
    cache = _cache_load()
    key = _cache_key(kind, state, district, city)
    if key in cache and isinstance(cache[key], list):
        return cache[key]
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    if kind == "states":
        prompt = "Return a JSON array containing the official names of all Indian states and union territories. Return only JSON array strings."
    elif kind == "districts":
        prompt = f"Return a JSON array containing all districts of the Indian state or union territory named {state}. Return only JSON array strings."
    elif kind == "cities":
        prompt = f"Return a JSON array containing cities and major towns/localities used for postal addressing in {district}, {state}, India. Return only JSON array strings."
    else:
        prompt = f"Return a JSON array of valid India Post PIN codes associated with {city}, {district}, {state}, India. Return only six-digit PIN code strings. Do not invent values; if uncertain, omit them."
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0, "maxOutputTokens": 4096}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={urllib.parse.quote(api_key)}"
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API error {exc.code}: {detail[:300]}")
    except Exception as exc:
        raise RuntimeError(f"Address service unavailable: {exc}")
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        values = json.loads(text)
    except Exception as exc:
        raise RuntimeError(f"Invalid address response: {exc}")
    if not isinstance(values, list):
        raise RuntimeError("Address response was not a list.")
    if kind == "pins":
        cleaned = sorted({str(v).strip() for v in values if re.fullmatch(r"\d{6}", str(v).strip())})
    else:
        cleaned = sorted({clean_text(v) for v in values if clean_text(v)})
    cache[key] = cleaned
    _cache_save(cache)
    return cleaned
