import os
from datetime import datetime
from pathlib import Path

import streamlit as st

from function_utils import *

BASE_DIR = Path(__file__).resolve().parent
ensure_runtime_files()

st.set_page_config(page_title="Book Store", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#f8fbff 0%,#eef4ff 55%,#f8faff 100%)}
[data-testid="stHeader"]{background:rgba(255,255,255,.72)}
.block-container{padding-top:2rem;padding-bottom:2rem;max-width:1400px}
.hero{padding:32px;border-radius:28px;background:linear-gradient(135deg,#173b7a,#3b82f6);color:white;box-shadow:0 16px 40px rgba(23,59,122,.18);margin-bottom:24px}
.hero h1{font-size:42px;margin:0}.hero p{font-size:16px;opacity:.9}
.card{background:rgba(255,255,255,.9);border:1px solid #dbe6f5;border-radius:22px;padding:20px;box-shadow:0 8px 28px rgba(31,64,104,.08);height:100%}
.metric{background:white;border:1px solid #dbe6f5;border-radius:18px;padding:18px;box-shadow:0 6px 20px rgba(31,64,104,.06)}
.metric .value{font-size:28px;font-weight:800;color:#173b7a}.metric .label{color:#64748b;font-size:13px}
.book-title{font-weight:800;font-size:18px;color:#173b7a}.muted{color:#64748b}.price{font-size:20px;font-weight:800;color:#0f766e}
.footer{margin-top:38px;padding:18px 0;border-top:1px solid #dbe6f5;color:#64748b;text-align:center;font-size:12px}
</style>""", unsafe_allow_html=True)


def gemini_key():
    try:
        value = st.secrets.get("GEMINI_API_KEY", "")
        if value:
            return value
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "").strip()


def footer():
    st.markdown("<div class='footer'>Book Store Management System · Inventory · Orders · Employee Operations · Records</div>", unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)


def metric(label, value):
    st.markdown(f"<div class='metric'><div class='label'>{label}</div><div class='value'>{value}</div></div>", unsafe_allow_html=True)


def set_screen(screen):
    st.session_state.screen = screen
    st.rerun()


def init_state():
    defaults = {
        "screen": "home", "role": None, "employee": None, "cart": {}, "checkout": {},
        "order": None, "invoice_html": None, "invoice_pdf": None, "restock_book_id": None,
        "address_state": "", "address_district": "", "address_city": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def home():
    hero("📚 Book Store", "Select an access area to continue")
    cols = st.columns(3)
    options = [
        ("Customer", "Browse books, manage cart and place an order", "🛍️", "customer"),
        ("Store Clerk", "Inventory, receiving, catalog and store operations", "📦", "clerk_login"),
        ("Director", "Business records, employees, expenses and controls", "📊", "director_login")
    ]
    for col, (title, desc, icon, screen) in zip(cols, options):
        with col:
            st.markdown(f"<div class='card'><div style='font-size:42px'>{icon}</div><h2>{title}</h2><p class='muted'>{desc}</p></div>", unsafe_allow_html=True)
            if st.button(f"Continue as {title}", use_container_width=True, key=f"home_{screen}"):
                set_screen(screen)
    footer()


def customer_store():
    hero("📖 Book Catalogue", "Search the available collection and add books to your cart")
    books = load_books()
    genres = ["All Genres"] + get_genres()
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        query = st.text_input("Search", placeholder="Book name, author or book ID")
    with c2:
        genre = st.selectbox("Genre", genres)
    with c3:
        only_available = st.checkbox("Show available only", value=True)
    filtered = []
    for book in books:
        match = query.lower() in f"{book['title']} {book['author']} {book['id']}".lower()
        genre_match = genre == "All Genres" or book["genre"].lower() == genre.lower()
        stock_match = not only_available or book["stock"] > 0
        if match and genre_match and stock_match:
            filtered.append(book)
    if not filtered:
        st.info("No matching books found.")
    for start in range(0, len(filtered), 4):
        cols = st.columns(4)
        for col, book in zip(cols, filtered[start:start+4]):
            with col:
                st.markdown(f"<div class='card'><div class='book-title'>{book['title']}</div><div class='muted'>{book['author']}</div><div class='muted'>{book['genre']}</div><br><div class='price'>{money(book['price'])}</div><div class='muted'>Stock: {book['stock']} · {stock_status(book['stock'])}</div></div>", unsafe_allow_html=True)
                qty = st.number_input("Quantity", min_value=1, max_value=max(1, book["stock"]), value=1, key=f"qty_{book['id']}", disabled=book["stock"] == 0)
                if st.button("Add to Cart", key=f"add_{book['id']}", use_container_width=True, disabled=book["stock"] == 0):
                    st.session_state.cart[book["id"]] = min(book["stock"], st.session_state.cart.get(book["id"], 0) + qty)
                    st.toast(f"Added {book['title']}")
    st.divider()
    cart_count = sum(st.session_state.cart.values())
    if st.button(f"🛒 Cart · {cart_count} item(s)", use_container_width=True, type="primary"):
        set_screen("cart")
    footer()


def cart_page():
    hero("🛒 Your Cart", "Review quantities before checkout")
    books = {b["id"]: b for b in load_books()}
    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Continue Shopping"):
            set_screen("customer")
        footer()
        return
    total = 0
    for book_id, qty in list(st.session_state.cart.items()):
        book = books.get(book_id)
        if not book:
            st.session_state.cart.pop(book_id, None)
            continue
        line = book["price"] * qty
        total += line
        c1, c2, c3 = st.columns([5, 2, 2])
        c1.write(f"**{book['title']}** · {book['author']}")
        new_qty = c2.number_input("Qty", min_value=1, max_value=max(1, book["stock"]), value=min(qty, max(1, book["stock"])), key=f"cart_qty_{book_id}")
        st.session_state.cart[book_id] = new_qty
        if c3.button("Remove", key=f"remove_{book_id}"):
            st.session_state.cart.pop(book_id, None)
            st.rerun()
        st.caption(f"{money(book['price'])} × {new_qty} = {money(book['price'] * new_qty)}")
    st.markdown(f"### Order Total: {money(total)}")
    c1, c2 = st.columns(2)
    if c1.button("Continue Shopping", use_container_width=True):
        set_screen("customer")
    if c2.button("Proceed to Secure Checkout", type="primary", use_container_width=True):
        set_screen("checkout")
    footer()


def address_selectors():
    key = gemini_key()
    if not key:
        st.error("GEMINI_API_KEY is not configured. Add it to Streamlit Secrets or the environment.")
        return None, None, None, None
    try:
        states = gemini_address_options(key, "states")
    except Exception as exc:
        st.error(str(exc))
        return None, None, None, None
    state = st.selectbox("State / Union Territory", [""] + states, key="address_state_select")
    if state != st.session_state.address_state:
        st.session_state.address_state = state
        st.session_state.address_district = ""
        st.session_state.address_city = ""
    if not state:
        return state, "", "", ""
    districts = gemini_address_options(key, "districts", state=state)
    district = st.selectbox("District", [""] + districts, key="address_district_select")
    if district != st.session_state.address_district:
        st.session_state.address_district = district
        st.session_state.address_city = ""
    if not district:
        return state, district, "", ""
    cities = gemini_address_options(key, "cities", state=state, district=district)
    city = st.selectbox("City / Town", [""] + cities, key="address_city_select")
    if city != st.session_state.address_city:
        st.session_state.address_city = city
    if not city:
        return state, district, city, ""
    pins = gemini_address_options(key, "pins", state=state, district=district, city=city)
    pin = st.selectbox("PIN Code", [""] + pins, key="address_pin_select")
    return state, district, city, pin


def checkout_page():
    hero("🧾 Checkout", "Enter delivery details and confirm Cash on Delivery")
    books = {b["id"]: b for b in load_books()}
    if not st.session_state.cart:
        set_screen("customer")
        return
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number", max_chars=10)
        flat = st.text_input("Flat / House / Building")
        street = st.text_input("Street / Area")
        landmark = st.text_input("Landmark (Optional)")
    with c2:
        state, district, city, pin = address_selectors()
        st.text_input("Payment Method", value="Cash on Delivery", disabled=True)
    submit = st.button("Place Order", type="primary", use_container_width=True)
    if submit:
        name = title_case_text(name)
        phone = clean_text(phone)
        flat = clean_address(flat)
        street = clean_address(street)
        landmark = clean_address(landmark)
        if not name or not phone.isdigit() or len(phone) != 10 or not flat or not street or not state or not district or not city or not pin:
            st.error("Please complete all required customer and address fields.")
            return
        items = []
        total = 0
        profit = 0
        fresh_books = {b["id"]: b for b in load_books()}
        for book_id, qty in st.session_state.cart.items():
            book = fresh_books.get(book_id)
            if not book or book["stock"] < qty:
                st.error(f"Insufficient stock for {book['title'] if book else book_id}.")
                return
            line_total = book["price"] * qty
            line_profit = (book["price"] - book["cost"]) * qty
            total += line_total
            profit += line_profit
            items.append({"id": book["id"], "title": book["title"], "author": book["author"], "genre": book["genre"], "quantity": qty, "unit_price": book["price"], "unit_cost": book["cost"], "line_total": line_total, "line_profit": line_profit})
        order = {"order_id": generate_order_id(), "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "customer_name": name, "phone": phone, "flat": flat, "street": street, "landmark": landmark or "-", "city": city, "district": district, "state": state, "pin": pin, "total": total, "profit": profit}
        for item in items:
            change_book_stock(item["id"], -item["quantity"])
        append_order_records(order, items)
        append_activity({"Full Name": "Customer"}, "Order placed", order["order_id"])
        st.session_state.cart = {}
        st.session_state.order = {"order": order, "items": items}
        st.session_state.invoice_html = build_invoice_html(order, items)
        st.session_state.invoice_pdf = build_invoice_pdf(order, items)
        set_screen("confirmation")
    footer()


def confirmation_page():
    order_data = st.session_state.get("order")
    if not order_data:
        set_screen("customer")
        return
    order = order_data["order"]
    items = order_data["items"]
    hero("✅ Order Confirmed", f"Order {order['order_id']} has been recorded")
    metric("Order Total", money(order["total"]))
    st.markdown(f"**Customer:** {order['customer_name']}<br>**Delivery:** {order['city']}, {order['district']}, {order['state']} - {order['pin']}<br>**Payment:** Cash on Delivery", unsafe_allow_html=True)
    st.markdown("### Items")
    for item in items:
        st.write(f"{item['title']} · {item['quantity']} × {money(item['unit_price'])} = **{money(item['line_total'])}**")
    st.download_button("Download Invoice HTML", st.session_state.invoice_html, file_name=f"{order['order_id']}.html", mime="text/html", use_container_width=True)
    st.download_button("Download Invoice PDF", st.session_state.invoice_pdf, file_name=f"{order['order_id']}.pdf", mime="application/pdf", use_container_width=True)
    if st.button("Back to Store", type="primary", use_container_width=True):
        set_screen("customer")
    footer()


def login_page(role):
    title = "Store Clerk Login" if role == "sd" else "Director Login"
    hero("🔐 " + title, "Enter your employee credentials")
    with st.form(f"login_{role}"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)
    if submit:
        employee = authenticate_employee(username, password)
        if not employee:
            st.error("Invalid username or password.")
        elif role not in employee.get("Access", ""):
            st.error("This account does not have access to this workspace.")
        else:
            st.session_state.employee = employee
            st.session_state.role = role
            append_activity(employee, "Logged in")
            set_screen("clerk" if role == "sd" else "director")
    if st.button("Back"):
        set_screen("home")
    footer()


def logout():
    if st.session_state.employee:
        append_activity(st.session_state.employee, "Logged out")
    st.session_state.employee = None
    st.session_state.role = None
    set_screen("home")


def clerk_dashboard():
    employee = st.session_state.employee
    hero("📦 Store Clerk", f"Signed in as {employee.get('Full Name', employee.get('Username', ''))}")
    books = load_books()
    out = [b for b in books if b["stock"] == 0]
    low = [b for b in books if 0 < b["stock"] <= 2]
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("Books", len(books))
    with c2: metric("Out of Stock", len(out))
    with c3: metric("Low Stock", len(low))
    with c4: metric("Genres", len(get_genres()))
    st.markdown("### Out-of-Stock Books")
    if not out:
        st.success("No books are currently out of stock.")
    for book in out:
        c1, c2, c3 = st.columns([5, 2, 1])
        c1.write(f"**{book['title']}** · {book['author']} · {book['id']}")
        c2.write("Quantity: 0")
        if c3.button("📥 Restock", key=f"restock_{book['id']}"):
            st.session_state.restock_book_id = book["id"]
            set_screen("receiving")
    st.markdown("### Store Operations")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Inventory Receiving", use_container_width=True): set_screen("receiving")
    if c2.button("Catalog", use_container_width=True): set_screen("catalog")
    if c3.button("Genres", use_container_width=True): set_screen("genres")
    if c4.button("Activity Log", use_container_width=True): set_screen("activity")
    if st.button("Log Out", use_container_width=True): logout()
    footer()


def receiving_page():
    hero("📥 Inventory Receiving", "Record newly received copies and update stock")
    books = load_books()
    ids = [b["id"] for b in books]
    current_id = st.session_state.restock_book_id if st.session_state.restock_book_id in ids else ids[0] if ids else ""
    selected = st.selectbox("Book", ids, index=ids.index(current_id) if current_id in ids else 0, format_func=lambda x: next((b["title"] + " · " + x for b in books if b["id"] == x), x)) if ids else ""
    qty = st.number_input("Copies Received", min_value=1, step=1)
    if st.button("Update Stock", type="primary", use_container_width=True) and selected:
        new_stock = change_book_stock(selected, qty)
        book = next(b for b in books if b["id"] == selected)
        append_activity(st.session_state.employee, "Inventory received", f"{book['title']} +{qty}, new stock {new_stock}")
        st.session_state.restock_book_id = None
        st.success(f"Stock updated to {new_stock}.")
        st.rerun()
    if st.button("Back to Dashboard", use_container_width=True): set_screen("clerk")
    footer()


def catalog_page():
    hero("📚 Catalog", "View the current book collection and stock")
    books = load_books()
    for book in books:
        st.write(f"**{book['title']}** · {book['author']} · {book['genre']} · {money(book['price'])} · Stock {book['stock']} · {stock_status(book['stock'])}")
    if st.button("Back to Dashboard"): set_screen("clerk")
    footer()


def genres_page():
    hero("🏷️ Genres", "Manage the genre directory")
    st.write(" · ".join(get_genres()))
    new_genre = st.text_input("Add Genre")
    if st.button("Add Genre", type="primary"):
        if add_genre(new_genre):
            append_activity(st.session_state.employee, "Genre added", new_genre)
            st.success("Genre added.")
            st.rerun()
        st.warning("Genre already exists or is empty.")
    if st.button("Back to Dashboard"): set_screen("clerk")
    footer()


def activity_page(back="clerk"):
    hero("📝 Activity Log", "Recent operational events")
    for line in read_activity(150):
        parts = [p.strip() for p in line.split("|", 3)]
        if len(parts) == 4:
            st.markdown(f"<div class='card' style='margin-bottom:8px;padding:12px'><b>{parts[0]}</b> · {parts[1]}<br><b>{parts[2]}</b> · {parts[3]}</div>", unsafe_allow_html=True)
        else:
            st.write(line)
    if st.button("Back"): set_screen(back)
    footer()


def director_dashboard():
    hero("📊 Director Workspace", f"Signed in as {st.session_state.employee.get('Full Name', st.session_state.employee.get('Username', ''))}")
    books = load_books()
    records = []
    if STORE_DATA_PATH.exists():
        wb = load_workbook(STORE_DATA_PATH, read_only=True, data_only=True)
        ws = wb.active
        headers = [clean_text(x.value) for x in ws[1]]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if any(v is not None for v in row): records.append(dict(zip(headers, row)))
    revenue = sum(to_float(r.get("Line Total")) for r in records)
    profit = sum(to_float(r.get("Line Profit")) for r in records)
    expenses = sum(to_float(r.get("Amount")) for r in load_expenses())
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric("Revenue", money(revenue))
    with c2: metric("Book Profit", money(profit))
    with c3: metric("Expenses", money(expenses))
    with c4: metric("Net", money(profit-expenses))
    c1,c2,c3,c4 = st.columns(4)
    if c1.button("Employees", use_container_width=True): set_screen("employees")
    if c2.button("Expenses", use_container_width=True): set_screen("expenses")
    if c3.button("Catalog", use_container_width=True): set_screen("catalog_director")
    if c4.button("Activity Log", use_container_width=True): set_screen("activity_director")
    if st.button("Log Out", use_container_width=True): logout()
    footer()


def employees_page():
    hero("👥 Employees", "Create and review store employee accounts")
    employees = load_employees()
    for e in employees:
        st.write(f"**{e.get('Employee ID','')}** · {e.get('Full Name','')} · {e.get('Designation','')} · {e.get('Username','')} · {e.get('Status','')}")
    st.divider()
    st.markdown("### Create Employee")
    with st.form("employee_create"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password")
        designation = st.selectbox("Designation", ["Store Clerk", "Director"])
        submit = st.form_submit_button("Create Employee", type="primary")
    if submit:
        if not name or not username or not password:
            st.error("Full Name, Username and Password are required.")
        elif any(e.get("Username", "").lower() == username.lower() for e in employees):
            st.error("Username already exists.")
        else:
            emp_id = create_employee(name, phone, email, username, password, designation)
            append_activity(st.session_state.employee, "Employee created", f"{emp_id} · {designation}")
            st.success(f"Employee created: {emp_id}")
            st.rerun()
    if st.button("Back to Director"): set_screen("director")
    footer()


def expenses_page():
    hero("💳 Expenses", "Record store operating expenses")
    with st.form("expense_form"):
        category = st.text_input("Category")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        submit = st.form_submit_button("Record Expense", type="primary")
    if submit and amount > 0:
        add_expense(category, description, amount, st.session_state.employee.get("Full Name", "Director"))
        append_activity(st.session_state.employee, "Expense recorded", f"{category} · {money(amount)}")
        st.success("Expense recorded.")
    st.markdown("### Recent Expenses")
    for e in reversed(load_expenses()[-30:]):
        st.write(f"{e.get('Date')} · **{e.get('Category')}** · {e.get('Description')} · {money(e.get('Amount'))}")
    if st.button("Back to Director"): set_screen("director")
    footer()


def director_catalog():
    hero("📚 Catalog", "Book prices, costs and stock")
    for b in load_books():
        st.write(f"**{b['title']}** · Cost {money(b['cost'])} · Price {money(b['price'])} · Profit {money(b['profit'])} · Stock {b['stock']}")
    if st.button("Back to Director"): set_screen("director")
    footer()


def route():
    screen = st.session_state.screen
    if screen == "home": home()
    elif screen == "customer": customer_store()
    elif screen == "cart": cart_page()
    elif screen == "checkout": checkout_page()
    elif screen == "confirmation": confirmation_page()
    elif screen == "clerk_login": login_page("sd")
    elif screen == "director_login": login_page("csp")
    elif screen == "clerk": clerk_dashboard()
    elif screen == "receiving": receiving_page()
    elif screen == "catalog": catalog_page()
    elif screen == "genres": genres_page()
    elif screen == "activity": activity_page("clerk")
    elif screen == "director": director_dashboard()
    elif screen == "employees": employees_page()
    elif screen == "expenses": expenses_page()
    elif screen == "catalog_director": director_catalog()
    elif screen == "activity_director": activity_page("director")
    else:
        st.session_state.screen = "home"
        st.rerun()


init_state()
route()
