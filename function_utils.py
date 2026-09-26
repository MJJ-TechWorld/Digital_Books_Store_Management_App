from __future__ import annotations

import csv
import io
import re
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BASE_DIR = Path(__file__).resolve().parent
BOOK_DATA_PATH = BASE_DIR / "BOOKS_DATA.xlsx"
STORE_DATA_PATH = BASE_DIR / "STORE_RECORDS.xlsx"
EMPLS_DATA_PATH = BASE_DIR / "EMPLOYEES.csv"
LOG_DATA_PATH = BASE_DIR / "Activity_Log.txt"
CREDT_DATA_PATH = BASE_DIR / "CREDENTIAL.txt"

ORDER_HEADERS = [
    "Order ID", "Order Date", "Customer Name", "Phone", "House / Flat",
    "Street / Area", "Landmark", "City", "State", "PIN Code",
    "Payment Method", "Order Status", "Unique Code", "Book Name", "Author",
    "Genre", "Language", "Unit Price (INR)", "Quantity", "Item Total (INR)",
    "Wholesale Cost (INR)", "Item Profit (INR)"
]

EXPENSE_HEADERS = [
    "Entry ID", "Date", "Type", "Unique Code", "Book Name", "Author",
    "Genre", "Unit Cost (INR)", "Quantity", "Total Expense (INR)"
]


def _safe(value: Any, default: str = "") -> str:
    return default if value is None else str(value).strip()


def _now() -> datetime:
    return datetime.now()


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", _safe(value).lower()).strip("-")[:80] or "item"


def _style_header(ws) -> None:
    fill = PatternFill("solid", fgColor="172554")
    font = Font(color="FFFFFF", bold=True)
    side = Side(style="thin", color="CBD5E1")
    for cell in ws[1]:
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(left=side, right=side, top=side, bottom=side)
    ws.freeze_panes = "A2"
    if ws.max_row and ws.max_column:
        ws.auto_filter.ref = ws.dimensions


def _format_sheet(ws) -> None:
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(vertical="center", wrap_text=True)
    _style_header(ws)
    for col in ws.columns:
        letter = col[0].column_letter
        longest = max((len(_safe(c.value)) for c in col[:100]), default=10)
        ws.column_dimensions[letter].width = min(max(longest + 2, 12), 34)


def create_imp_files() -> None:
    if not BOOK_DATA_PATH.exists():
        raise FileNotFoundError("BOOKS_DATA.xlsx was not found.")
    if not EMPLS_DATA_PATH.exists():
        with EMPLS_DATA_PATH.open("w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(["EMP ID", "First Name", "Last Name", "Phone Number", "Username", "Password", "Access"])
    if not CREDT_DATA_PATH.exists():
        CREDT_DATA_PATH.write_text("EMP ID, Code\n", encoding="utf-8")
    if not LOG_DATA_PATH.exists():
        LOG_DATA_PATH.write_text("EMP ID - Name - Session - Action - Time\n", encoding="utf-8")
    if not STORE_DATA_PATH.exists():
        wb = Workbook()
        ws = wb.active
        ws.title = "Order Items"
        ws.append(ORDER_HEADERS)
        expense = wb.create_sheet("Stock Purchases")
        expense.append(EXPENSE_HEADERS)
        for sheet in wb.worksheets:
            _format_sheet(sheet)
        wb.save(STORE_DATA_PATH)
        wb.close()
    else:
        upgrade_store_workbook()


def upgrade_store_workbook() -> None:
    wb = None
    try:
        wb = load_workbook(STORE_DATA_PATH)
        if "Order Items" not in wb.sheetnames:
            ws = wb.create_sheet("Order Items", 0)
            ws.append(ORDER_HEADERS)
        else:
            ws = wb["Order Items"]
            headers = [cell.value for cell in ws[1]]
            if headers != ORDER_HEADERS:
                legacy_name = "Legacy Order Items"
                if legacy_name in wb.sheetnames:
                    del wb[legacy_name]
                ws.title = legacy_name
                fresh = wb.create_sheet("Order Items", 0)
                fresh.append(ORDER_HEADERS)
        if "Stock Purchases" not in wb.sheetnames:
            expense = wb.create_sheet("Stock Purchases")
            expense.append(EXPENSE_HEADERS)
        for sheet in wb.worksheets:
            _format_sheet(sheet)
        wb.save(STORE_DATA_PATH)
    except Exception:
        pass
    finally:
        if wb:
            wb.close()


def read_employees() -> List[Dict[str, str]]:
    with EMPLS_DATA_PATH.open(newline="", encoding="utf-8-sig") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_employees(rows: List[Dict[str, str]]) -> None:
    headers = ["EMP ID", "First Name", "Last Name", "Phone Number", "Username", "Password", "Access"]
    with EMPLS_DATA_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def authenticate(username: str, password: str, access: str) -> Optional[Dict[str, str]]:
    username = username.strip()
    password = password.strip()
    for row in read_employees():
        if row.get("Username", "").strip() != username or row.get("Password", "") != password:
            continue
        if access not in row.get("Access", "").strip().lower():
            continue
        return row
    return None


def log_activity(employee: Optional[Dict[str, str]], action: str, session: str = "Operational") -> None:
    if not employee:
        return
    name = f"{employee.get('First Name', '')} {employee.get('Last Name', '')}".strip()
    timestamp = _now().strftime("%d-%m-%Y %I:%M %p")
    with LOG_DATA_PATH.open("a", encoding="utf-8") as file:
        file.write(f"{employee.get('EMP ID', '')} - {name} - {session} - {action} - {timestamp}\n")


def get_activity_logs() -> List[Dict[str, str]]:
    if not LOG_DATA_PATH.exists():
        return []
    lines = [line.strip() for line in LOG_DATA_PATH.read_text(encoding="utf-8").splitlines() if line.strip()][1:]
    result = []
    for line in lines:
        parts = [part.strip() for part in line.split(" - ")]
        if len(parts) >= 5:
            result.append({"Employee ID": parts[0], "Employee": parts[1], "Workspace": parts[2], "Action": parts[3], "Time": " - ".join(parts[4:])})
        else:
            result.append({"Employee ID": "", "Employee": line, "Workspace": "", "Action": "", "Time": ""})
    return result


def read_books() -> List[Dict[str, Any]]:
    wb = load_workbook(BOOK_DATA_PATH, data_only=True, read_only=True)
    books = []
    for sheet in wb.worksheets:
        genre = sheet.title.split("--")[0].strip() if "--" in sheet.title else sheet.title.strip()
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or len(row) < 10 or not row[1]:
                continue
            try:
                stock = int(row[9] or 0)
            except (TypeError, ValueError):
                stock = 0
            books.append({
                "sr_no": row[0], "code": _safe(row[1]).upper(), "name": _safe(row[2]),
                "author": _safe(row[3]), "language": _safe(row[4]), "published": _safe(row[5]),
                "wholesale": float(row[6] or 0), "price": float(row[7] or 0),
                "margin": float(row[8] or 0), "stock": stock, "genre": genre
            })
    wb.close()
    return books


def search_books(query: str = "", genre: str = "All", language: str = "All", in_stock_only: bool = False) -> List[Dict[str, Any]]:
    q = query.strip().lower()
    result = []
    for book in read_books():
        haystack = " ".join([book["code"], book["name"], book["author"], book["genre"], book["language"]]).lower()
        if q and q not in haystack:
            continue
        if genre != "All" and book["genre"] != genre:
            continue
        if language != "All" and book["language"] != language:
            continue
        if in_stock_only and book["stock"] <= 0:
            continue
        result.append(book)
    return result


def get_genres() -> List[str]:
    return sorted({book["genre"] for book in read_books()})


def get_languages() -> List[str]:
    return sorted({book["language"] for book in read_books() if book["language"]})


def find_book(code: str) -> Optional[Dict[str, Any]]:
    code = code.strip().upper()
    return next((book for book in read_books() if book["code"] == code), None)


def _find_book_row(ws, code: str):
    for row in ws.iter_rows(min_row=2):
        if _safe(row[1].value).upper() == code.upper():
            return row
    return None


def update_stock(code: str, delta: int) -> bool:
    wb = load_workbook(BOOK_DATA_PATH)
    changed = False
    try:
        for ws in wb.worksheets:
            row = _find_book_row(ws, code)
            if row:
                current = int(row[9].value or 0)
                new_value = current + int(delta)
                if new_value < 0:
                    return False
                row[9].value = new_value
                changed = True
                break
        if changed:
            wb.save(BOOK_DATA_PATH)
        return changed
    finally:
        wb.close()


def record_stock_purchase(book: Dict[str, Any], quantity: int, unit_cost: float) -> None:
    wb = load_workbook(STORE_DATA_PATH)
    try:
        ws = wb["Stock Purchases"]
        entry_id = "PUR-" + _now().strftime("%Y%m%d%H%M%S") + secrets.token_hex(2).upper()
        qty = int(quantity)
        cost = float(unit_cost)
        ws.append([entry_id, _now().strftime("%Y-%m-%d %H:%M:%S"), "Inventory Receiving", book["code"], book["name"], book["author"], book["genre"], cost, qty, round(cost * qty, 2)])
        _format_sheet(ws)
        wb.save(STORE_DATA_PATH)
    finally:
        wb.close()


def add_stock(code: str, quantity: int, purchase_cost: Optional[float] = None) -> Tuple[bool, str]:
    book = find_book(code)
    if not book:
        return False, "Book not found."
    if quantity < 1:
        return False, "Quantity must be at least 1."
    cost = float(purchase_cost if purchase_cost is not None else book["wholesale"])
    if not update_stock(code, quantity):
        return False, "Could not update stock."
    try:
        record_stock_purchase(book, quantity, cost)
    except Exception as exc:
        update_stock(code, -quantity)
        return False, f"Stock was not saved because the purchase record failed: {exc}"
    return True, f"Added {quantity} copies of {book['name']}."


def add_new_genre(name: str) -> Tuple[bool, str]:
    name = name.strip()
    if not name:
        return False, "Genre name is required."
    wb = load_workbook(BOOK_DATA_PATH)
    try:
        if any(ws.title.split("--")[0].strip().lower() == name.lower() for ws in wb.worksheets):
            return False, "That genre already exists."
        ws = wb.create_sheet(f"{name}--{_slug(name).upper()[:8]}")
        ws.append(["Sr No", "Unique Code", "Book Name", "Author", "Language", "Published Date", "Wholesale Price", "Market Price", "Margin", "Available Copies"])
        _format_sheet(ws)
        wb.save(BOOK_DATA_PATH)
        return True, f"Genre '{name}' created."
    finally:
        wb.close()


def add_new_book(data: Dict[str, Any]) -> Tuple[bool, str]:
    required = ["code", "name", "author", "language", "published", "genre"]
    if any(not _safe(data.get(key)) for key in required):
        return False, "Please complete all required book fields."
    code = _safe(data["code"]).upper()
    if find_book(code):
        return False, "Unique book code already exists."
    wb = load_workbook(BOOK_DATA_PATH)
    try:
        target = next((ws for ws in wb.worksheets if ws.title.split("--")[0].strip().lower() == _safe(data["genre"]).lower()), None)
        if target is None:
            return False, "Genre sheet not found. Create the genre first."
        wholesale = float(data["wholesale"])
        price = float(data["price"])
        stock = int(data.get("stock", 0))
        if wholesale < 0 or price < 0 or stock < 0:
            return False, "Prices and stock cannot be negative."
        serials = [int(row[0].value) for row in target.iter_rows(min_row=2) if str(row[0].value or "").isdigit()]
        serial = max(serials or [0]) + 1
        target.append([serial, code, _safe(data["name"]), _safe(data["author"]), _safe(data["language"]), _safe(data["published"]), wholesale, price, max(price - wholesale, 0), stock])
        _format_sheet(target)
        wb.save(BOOK_DATA_PATH)
        return True, f"{data['name']} was added to the catalog."
    finally:
        wb.close()


def _ensure_order_sheet(wb):
    if "Order Items" not in wb.sheetnames:
        ws = wb.create_sheet("Order Items", 0)
        ws.append(ORDER_HEADERS)
    return wb["Order Items"]


def place_order(customer: Dict[str, str], cart: Dict[str, int]) -> Tuple[bool, str, List[Dict[str, Any]], float]:
    if not cart:
        return False, "Your cart is empty.", [], 0.0
    books = {book["code"]: book for book in read_books()}
    items = []
    for code, qty in cart.items():
        book = books.get(code.upper())
        qty = int(qty)
        if not book:
            return False, f"Book {code} is no longer available.", [], 0.0
        if qty < 1 or book["stock"] < qty:
            return False, f"Insufficient stock for {book['name']}. Available: {book['stock']}.", [], 0.0
        items.append({**book, "quantity": qty, "item_total": round(book["price"] * qty, 2), "item_profit": round(book["margin"] * qty, 2)})

    order_id = "ORD-" + _now().strftime("%Y%m%d") + "-" + secrets.token_hex(3).upper()
    order_time = _now().strftime("%Y-%m-%d %H:%M:%S")
    total = round(sum(item["item_total"] for item in items), 2)
    changed = []
    for item in items:
        if not update_stock(item["code"], -item["quantity"]):
            for old_code, old_qty in changed:
                update_stock(old_code, old_qty)
            return False, "Stock changed during checkout. Please review your cart.", [], 0.0
        changed.append((item["code"], item["quantity"]))

    wb = None
    try:
        wb = load_workbook(STORE_DATA_PATH)
        ws = _ensure_order_sheet(wb)
        for item in items:
            ws.append([
                order_id, order_time, customer.get("name", ""), customer.get("phone", ""),
                customer.get("house", ""), customer.get("street", ""), customer.get("landmark", ""),
                customer.get("city", ""), customer.get("state", ""), customer.get("pin", ""),
                "Cash on Delivery", "Placed", item["code"], item["name"], item["author"], item["genre"],
                item["language"], item["price"], item["quantity"], item["item_total"],
                item["wholesale"] * item["quantity"], item["item_profit"]
            ])
        _format_sheet(ws)
        wb.save(STORE_DATA_PATH)
    except Exception as exc:
        for old_code, old_qty in changed:
            update_stock(old_code, old_qty)
        return False, f"Could not save the order: {exc}", [], 0.0
    finally:
        if wb:
            wb.close()
    return True, order_id, items, total


def load_orders() -> List[Dict[str, Any]]:
    if not STORE_DATA_PATH.exists():
        return []
    wb = load_workbook(STORE_DATA_PATH, data_only=True, read_only=True)
    try:
        if "Order Items" not in wb.sheetnames:
            return []
        ws = wb["Order Items"]
        rows = list(ws.iter_rows(values_only=True))
        if len(rows) <= 1:
            return []
        headers = list(rows[0])
        return [dict(zip(headers, row)) for row in rows[1:] if any(value is not None for value in row)]
    finally:
        wb.close()


def sales_summary() -> Dict[str, float]:
    orders = load_orders()
    revenue = sum(float(row.get("Item Total (INR)") or 0) for row in orders)
    profit = sum(float(row.get("Item Profit (INR)") or 0) for row in orders)
    units = sum(int(row.get("Quantity") or 0) for row in orders)
    order_ids = {row.get("Order ID") for row in orders if row.get("Order ID")}
    expenses = 0.0
    wb = None
    try:
        wb = load_workbook(STORE_DATA_PATH, data_only=True, read_only=True)
        if "Stock Purchases" in wb.sheetnames:
            ws = wb["Stock Purchases"]
            rows = ws.iter_rows(values_only=True)
            headers = list(next(rows, []))
            index = {header: i for i, header in enumerate(headers)}
            total_index = index.get("Total Expense (INR)")
            if total_index is not None:
                for row in rows:
                    expenses += float(row[total_index] or 0)
    except Exception:
        expenses = 0.0
    finally:
        if wb:
            wb.close()
    return {"revenue": revenue, "profit": profit, "units": units, "orders": len(order_ids), "expenses": expenses}


def generate_invoice_html(order_id: str, customer: Dict[str, str], items: List[Dict[str, Any]], total: float) -> str:
    address = ", ".join(value for value in [customer.get("house"), customer.get("street"), customer.get("landmark"), customer.get("city"), customer.get("state"), customer.get("pin")] if value)
    rows = "".join(
        f"<tr><td>{index}</td><td><strong>{_safe(item['name'])}</strong><br><span>{_safe(item['author'])}</span></td><td>{item['quantity']}</td><td>₹{item['price']:,.2f}</td><td>₹{item['item_total']:,.2f}</td></tr>"
        for index, item in enumerate(items, 1)
    )
    placed = _now().strftime("%d %b %Y, %I:%M %p")
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>{order_id}</title><style>@page{{size:A4;margin:14mm}}body{{font-family:Arial,sans-serif;background:#eef2ff;color:#0f172a;margin:0;padding:28px}}.invoice{{max-width:850px;margin:auto;background:#fff;border-radius:24px;padding:34px;box-shadow:0 18px 60px rgba(15,23,42,.15)}}.top{{display:flex;justify-content:space-between;gap:20px;border-bottom:2px solid #e2e8f0;padding-bottom:20px}}h1{{margin:0;color:#172554}}.muted{{color:#64748b}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:25px 0}}table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;border-bottom:1px solid #e2e8f0;text-align:left}}th{{background:#172554;color:#fff}}.total{{text-align:right;font-size:26px;font-weight:800;margin-top:24px;color:#312e81}}.badge{{display:inline-block;padding:7px 12px;border-radius:999px;background:#dcfce7;color:#166534;font-weight:700}}.print{{border:0;border-radius:10px;padding:11px 16px;background:#312e81;color:white;font-weight:700;cursor:pointer;margin-top:20px}}@media print{{body{{background:white;padding:0}}.invoice{{box-shadow:none;padding:0}}.print{{display:none}}}}</style></head><body><div class='invoice'><div class='top'><div><h1>📚 DIGITAL BOOKS STORE</h1><p class='muted'>Customer Order Invoice</p></div><div style='text-align:right'><strong>Order ID</strong><br>{order_id}<br><span class='badge'>Cash on Delivery</span></div></div><div class='grid'><div><strong>Customer</strong><p>{_safe(customer.get('name'))}<br>{_safe(customer.get('phone'))}</p></div><div><strong>Delivery Address</strong><p>{address}</p></div></div><table><thead><tr><th>#</th><th>Book</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr></thead><tbody>{rows}</tbody></table><div class='total'>Grand Total: ₹{total:,.2f}</div><p class='muted'>Placed: {placed} · Payment due on delivery.</p><button class='print' onclick='window.print()'>Print Invoice</button></div></body></html>"""


def generate_invoice_pdf(order_id: str, customer: Dict[str, str], items: List[Dict[str, Any]], total: float) -> bytes:
    buffer = io.BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm, topMargin=14 * mm, bottomMargin=14 * mm)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=styles["Title"], fontSize=20, textColor=colors.HexColor("#172554"), leading=24)
    small = ParagraphStyle("small", parent=styles["BodyText"], fontSize=9, textColor=colors.HexColor("#64748b"), leading=13)
    right = ParagraphStyle("right", parent=styles["BodyText"], alignment=TA_RIGHT, fontSize=9, leading=13)
    story = [Paragraph("DIGITAL BOOKS STORE", title), Paragraph("Customer Order Invoice", small), Spacer(1, 8)]
    address = ", ".join(value for value in [customer.get("house"), customer.get("street"), customer.get("landmark"), customer.get("city"), customer.get("state"), customer.get("pin")] if value)
    meta = Table([
        [Paragraph(f"<b>Order ID:</b> {order_id}<br/><b>Payment:</b> Cash on Delivery", small), Paragraph(f"<b>Customer:</b> {_safe(customer.get('name'))}<br/><b>Phone:</b> {_safe(customer.get('phone'))}<br/><b>Address:</b> {address}", small)]
    ], colWidths=[85 * mm, 85 * mm])
    meta.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")), ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#e2e8f0")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    story += [meta, Spacer(1, 18)]
    data = [["#", "Book", "Qty", "Unit Price", "Total"]]
    for index, item in enumerate(items, 1):
        data.append([str(index), Paragraph(f"{_safe(item['name'])}<br/><font color='#64748b'>{_safe(item['author'])}</font>", small), str(item["quantity"]), f"₹{item['price']:,.2f}", f"₹{item['item_total']:,.2f}"])
    table = Table(data, colWidths=[10 * mm, 88 * mm, 18 * mm, 28 * mm, 28 * mm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (2, 1), (-1, -1), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story += [table, Spacer(1, 18), Paragraph(f"<b>Grand Total: ₹{total:,.2f}</b>", ParagraphStyle("total", parent=styles["Heading2"], alignment=TA_RIGHT, textColor=colors.HexColor("#312e81"))), Spacer(1, 8), Paragraph("Thank you for shopping with Digital Books Store. Payment is due on delivery.", small)]
    document.build(story)
    return buffer.getvalue()
