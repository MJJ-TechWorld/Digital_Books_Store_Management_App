from __future__ import annotations

import html
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from function_utils import *

st.set_page_config(page_title="Digital Books Store", page_icon="📚", layout="wide", initial_sidebar_state="expanded")
create_imp_files()


def money(value: float) -> str:
    return f"₹{float(value):,.2f}"


def page_bg(kind: str = "store") -> None:
    backgrounds = {
        "store": "linear-gradient(135deg,#eef2ff,#fff7ed 55%,#fdf2f8)",
        "checkout": "linear-gradient(135deg,#eff6ff,#ecfdf5 55%,#f8fafc)",
        "staff": "linear-gradient(135deg,#ecfeff,#eff6ff 55%,#f0fdf4)",
        "director": "linear-gradient(135deg,#eef2ff,#faf5ff 55%,#fff7ed)",
    }
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"]{{background:{backgrounds.get(kind, backgrounds['store'])};}}
    [data-testid="stHeader"]{{background:transparent;}}
    .block-container{{max-width:1450px;padding-top:1rem;padding-bottom:4rem;}}
    .hero{{padding:34px 38px;border-radius:28px;background:linear-gradient(110deg,#172554,#312e81 58%,#6d28d9);color:white;box-shadow:0 20px 55px rgba(30,41,59,.15);margin-bottom:24px;}}
    .hero h1{{font-size:clamp(2rem,4vw,3.6rem);margin:0 0 8px;font-weight:850;letter-spacing:-1px;}}
    .hero p{{margin:0;color:#dbeafe;font-size:1.02rem;max-width:900px;line-height:1.6;}}
    .section-title{{font-size:1.55rem;font-weight:850;color:#172554;margin:24px 0 12px;}}
    .product{{background:rgba(255,255,255,.94);border:1px solid #e2e8f0;border-radius:22px;padding:18px;box-shadow:0 10px 30px rgba(15,23,42,.06);height:100%;}}
    .product h3{{margin:10px 0 4px;color:#172554;font-size:1.08rem;line-height:1.3;}}
    .pill{{display:inline-block;padding:5px 10px;border-radius:999px;background:#eef2ff;color:#4338ca;font-weight:800;font-size:.72rem;}}
    .price{{font-size:1.25rem;font-weight:850;color:#6d28d9;margin-top:8px;}}
    .stock-good{{color:#15803d;font-weight:750;font-size:.84rem;}}
    .stock-low{{color:#b45309;font-weight:750;font-size:.84rem;}}
    .stock-out{{color:#b91c1c;font-weight:750;font-size:.84rem;}}
    .muted{{color:#64748b;font-size:.88rem;}}
    .metric-card{{background:rgba(255,255,255,.9);border:1px solid #e2e8f0;border-radius:20px;padding:18px;box-shadow:0 8px 25px rgba(15,23,42,.05);}}
    .checkout-card{{background:white;border:1px solid #e2e8f0;border-radius:20px;padding:22px;box-shadow:0 12px 32px rgba(15,23,42,.06);}}
    .success-box{{background:#ecfdf5;border:1px solid #86efac;border-radius:22px;padding:22px;}}
    .log-card{{background:white;border-left:5px solid #4f46e5;border-radius:14px;padding:13px 16px;margin:8px 0;box-shadow:0 7px 20px rgba(15,23,42,.06);}}
    .log-action{{font-weight:800;color:#312e81;}}
    .log-meta{{color:#64748b;font-size:.82rem;margin-top:4px;}}
    div.stButton>button{{border-radius:12px;font-weight:800;min-height:2.65rem;}}
    .stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"]{{border-radius:12px!important;}}
    </style>
    """, unsafe_allow_html=True)


def hero(title: str, subtitle: str, emoji: str = "📚") -> None:
    st.markdown(f'<div class="hero"><h1>{emoji} {html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>', unsafe_allow_html=True)


def init_state() -> None:
    defaults = {"role": None, "employee": None, "cart": {}, "checkout_done": None, "nav": "Home", "catalog_page": 1}
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def logout() -> None:
    employee = st.session_state.get("employee")
    if employee:
        log_activity(employee, "Logout", "Director" if st.session_state.get("role") == "p" else "Store Clerk")
    st.session_state.role = None
    st.session_state.employee = None
    st.session_state.nav = "Home"
    st.session_state.cart = {}
    st.session_state.checkout_done = None
    st.rerun()


def landing() -> None:
    page_bg("store")
    hero("Digital Books Store", "Choose your experience and continue to a purpose-built workspace.", "📚")
    st.markdown('<div class="section-title">How would you like to continue?</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3, gap="large")
    with a:
        st.markdown('<div class="metric-card"><h2>🛍️ Customer Storefront</h2><p>Explore the catalog, build your cart and place a Cash-on-Delivery order with a complete delivery address.</p></div>', unsafe_allow_html=True)
        if st.button("Enter Storefront →", key="landing_customer", type="primary", use_container_width=True):
            st.session_state.role = "customer"
            st.session_state.nav = "Storefront"
            st.session_state.catalog_page = 1
            st.rerun()
    with b:
        st.markdown('<div class="metric-card"><h2>👨‍💼 Store Clerk</h2><p>Manage incoming stock, catalog books, genres and pricing from one focused operations workspace.</p></div>', unsafe_allow_html=True)
        if st.button("Open Clerk Portal →", key="landing_staff", use_container_width=True):
            st.session_state.role = "staff_login"
            st.rerun()
    with c:
        st.markdown('<div class="metric-card"><h2>👑 Director</h2><p>Monitor business performance, manage Store Clerk accounts and review operational activity.</p></div>', unsafe_allow_html=True)
        if st.button("Open Director Portal →", key="landing_director", use_container_width=True):
            st.session_state.role = "director_login"
            st.rerun()


def customer_sidebar() -> None:
    with st.sidebar:
        st.markdown("# 📚 Digital Books Store")
        st.metric("Cart", f"{sum(st.session_state.cart.values())} item(s)")
        choices = ["Storefront", "Cart"]
        if st.session_state.cart:
            choices.append("Checkout")
        if st.session_state.get("checkout_done"):
            choices.append("Order Confirmation")
        current = st.session_state.get("nav", "Storefront")
        if current not in choices:
            current = "Storefront"
        nav = st.radio("Shop", choices, index=choices.index(current), key="customer_nav")
        st.session_state.nav = nav
        st.divider()
        if st.button("← Exit storefront", key="customer_exit", use_container_width=True):
            st.session_state.role = None
            st.session_state.nav = "Home"
            st.session_state.cart = {}
            st.rerun()


def customer_home() -> None:
    page_bg("store")
    hero("Your next great read is waiting.", "Discover books, compare prices and add your favourites to a live shopping cart.", "📚")
    books = read_books()
    a, b, c, d = st.columns(4)
    a.metric("Catalog", f"{len(books)} books")
    b.metric("Collections", len(get_genres()))
    c.metric("Languages", len(get_languages()))
    d.metric("In-stock titles", sum(book["stock"] > 0 for book in books))
    storefront_catalog()


def storefront_catalog() -> None:
    st.markdown('<div class="section-title">Explore the catalog</div>', unsafe_allow_html=True)
    q = st.text_input("Search", placeholder="Search title, author, genre or product code", key="catalog_search")
    a, b, c, d = st.columns([1.4, 1, 1, 1])
    genre = a.selectbox("Collection", ["All"] + get_genres(), key="catalog_genre")
    language = b.selectbox("Language", ["All"] + get_languages(), key="catalog_language")
    available = c.checkbox("Only available", value=True, key="catalog_available")
    sort = d.selectbox("Sort", ["Featured", "Price: Low to High", "Price: High to Low", "Title A-Z"], key="catalog_sort")
    books = search_books(q, genre, language, available)
    if sort == "Price: Low to High":
        books.sort(key=lambda book: book["price"])
    elif sort == "Price: High to Low":
        books.sort(key=lambda book: book["price"], reverse=True)
    elif sort == "Title A-Z":
        books.sort(key=lambda book: book["name"].lower())
    st.caption(f"{len(books)} products found · {sum(st.session_state.cart.values())} item(s) in cart")
    if not books:
        st.info("No matching products. Try another search or filter.")
        return
    per_page = 12
    pages = max(1, (len(books) + per_page - 1) // per_page)
    page = min(max(int(st.session_state.catalog_page), 1), pages)
    visible = books[(page - 1) * per_page: page * per_page]
    for row_start in range(0, len(visible), 4):
        cols = st.columns(4, gap="medium")
        for col, book in zip(cols, visible[row_start:row_start + 4]):
            with col:
                stock_class = "stock-good" if book["stock"] > 2 else "stock-low" if book["stock"] > 0 else "stock-out"
                stock_text = f"In stock · {book['stock']} left" if book["stock"] > 0 else "Currently unavailable"
                st.markdown(f'<div class="product"><span class="pill">{html.escape(book["genre"])}</span><h3>{html.escape(book["name"])}</h3><div class="muted">by {html.escape(book["author"])}</div><div class="muted">{html.escape(book["language"])} · Code {html.escape(book["code"])}</div><div class="price">{money(book["price"])}</div><div class="{stock_class}">{stock_text}</div></div>', unsafe_allow_html=True)
                if book["stock"] > 0:
                    max_qty = min(book["stock"], 99)
                    current = min(max(int(st.session_state.cart.get(book["code"], 1)), 1), max_qty)
                    qty = st.number_input("Quantity", 1, max_qty, current, key=f"qty_{book['code']}")
                    if st.button("🛒 Add to cart", key=f"add_{book['code']}", type="primary", use_container_width=True):
                        st.session_state.cart[book["code"]] = int(qty)
                        st.toast(f"{book['name']} added to cart", icon="🛒")
                        st.rerun()
                else:
                    st.button("Out of stock", key=f"out_{book['code']}", disabled=True, use_container_width=True)
    if pages > 1:
        p1, p2, p3 = st.columns([1, 2, 1])
        if page > 1 and p1.button("← Previous", key="catalog_previous", use_container_width=True):
            st.session_state.catalog_page = page - 1
            st.rerun()
        p2.markdown(f"<div style='text-align:center;padding:9px;font-weight:800'>Page {page} of {pages}</div>", unsafe_allow_html=True)
        if page < pages and p3.button("Next →", key="catalog_next", use_container_width=True):
            st.session_state.catalog_page = page + 1
            st.rerun()


def customer_cart() -> None:
    page_bg("checkout")
    hero("Shopping cart", "Review quantities and totals before moving to delivery details.", "🛒")
    if not st.session_state.cart:
        st.info("Your cart is empty. Return to the storefront to add books.")
        return
    books = {book["code"]: book for book in read_books()}
    total = 0.0
    for code in list(st.session_state.cart):
        book = books.get(code)
        if not book:
            st.session_state.cart.pop(code, None)
            continue
        c1, c2, c3, c4 = st.columns([4, 1.2, 1.3, 1])
        c1.markdown(f"**{html.escape(book['name'])}**  \n{html.escape(book['author'])} · {money(book['price'])}")
        max_qty = max(1, book["stock"])
        qty = c2.number_input("Qty", 1, max_qty, min(int(st.session_state.cart[code]), max_qty), key=f"cart_qty_{code}")
        st.session_state.cart[code] = int(qty)
        line_total = book["price"] * int(qty)
        total += line_total
        c3.markdown(f"**{money(line_total)}**")
        if c4.button("Remove", key=f"remove_{code}"):
            st.session_state.cart.pop(code, None)
            st.rerun()
        st.divider()
    st.markdown(f"## Order total: {money(total)}")
    if st.button("Proceed to secure checkout →", type="primary", use_container_width=True, key="proceed_checkout"):
        st.session_state.nav = "Checkout"
        st.rerun()


def checkout() -> None:
    page_bg("checkout")
    hero("Secure checkout", "Complete the delivery details and place your Cash-on-Delivery order.", "🚚")
    if not st.session_state.cart:
        st.warning("Your cart is empty.")
        return
    with st.form("checkout_form"):
        st.markdown('<div class="checkout-card">', unsafe_allow_html=True)
        st.markdown("### Contact information")
        a, b = st.columns(2)
        name = a.text_input("Full name *")
        phone = b.text_input("Mobile number *", max_chars=10)
        st.markdown("### Delivery address")
        a, b = st.columns(2)
        house = a.text_input("Flat / House / Building *")
        street = b.text_input("Street / Area *")
        a, b = st.columns(2)
        landmark = a.text_input("Landmark", placeholder="Optional")
        city = b.text_input("City *")
        a, b = st.columns(2)
        state = a.text_input("State *")
        pin = b.text_input("PIN code *", max_chars=6)
        st.markdown("### Payment")
        st.radio("Payment method", ["Cash on Delivery"], index=0, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Place COD order", type="primary", use_container_width=True)
    if submitted:
        if not name.strip() or not phone.isdigit() or len(phone) != 10 or not house.strip() or not street.strip() or not city.strip() or not state.strip() or not pin.isdigit() or len(pin) != 6:
            st.error("Please complete all required fields. Enter a valid 10-digit mobile number and 6-digit PIN code.")
            return
        customer = {"name": name.strip(), "phone": phone.strip(), "house": house.strip(), "street": street.strip(), "landmark": landmark.strip(), "city": city.strip(), "state": state.strip(), "pin": pin.strip()}
        ok, result, items, total = place_order(customer, dict(st.session_state.cart))
        if not ok:
            st.error(result)
            return
        invoice_html = generate_invoice_html(result, customer, items, total)
        invoice_pdf = generate_invoice_pdf(result, customer, items, total)
        st.session_state.checkout_done = {"order_id": result, "items": items, "total": total, "customer": customer, "invoice_html": invoice_html, "invoice_pdf": invoice_pdf}
        st.session_state.cart = {}
        st.session_state.nav = "Order Confirmation"
        st.rerun()


def order_confirmation() -> None:
    page_bg("checkout")
    data = st.session_state.get("checkout_done")
    if not data:
        st.info("No recent order found.")
        return
    if "invoice_html" not in data:
        data["invoice_html"] = generate_invoice_html(data["order_id"], data["customer"], data["items"], data["total"])
    if "invoice_pdf" not in data:
        data["invoice_pdf"] = generate_invoice_pdf(data["order_id"], data["customer"], data["items"], data["total"])
        st.session_state.checkout_done = data
    st.markdown('<div class="success-box"><h2>🎉 Order placed successfully</h2><p>Your order has been recorded and the requested stock has been reserved.</p></div>', unsafe_allow_html=True)
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Order ID", data["order_id"])
    b.metric("Order total", money(data["total"]))
    c.metric("Payment", "Cash on Delivery")
    st.markdown("### Invoice")
    st.components.v1.html(data["invoice_html"], height=720, scrolling=True)
    d1, d2 = st.columns(2)
    d1.download_button("⬇️ Download PDF invoice", data=data["invoice_pdf"], file_name=f"{data['order_id']}.pdf", mime="application/pdf", use_container_width=True, key="download_pdf_invoice")
    d2.download_button("⬇️ Download printable HTML", data=data["invoice_html"], file_name=f"{data['order_id']}.html", mime="text/html", use_container_width=True, key="download_html_invoice")
    if st.button("Continue shopping", type="primary", use_container_width=True, key="continue_shopping"):
        st.session_state.checkout_done = None
        st.session_state.nav = "Storefront"
        st.rerun()


def login_page(access: str) -> None:
    kind = "director" if access == "p" else "staff"
    page_bg(kind)
    title = "Director Command Center" if access == "p" else "Store Clerk Workspace"
    hero(title, "Sign in with the credentials recorded in EMPLOYEES.csv.", "👑" if access == "p" else "👨‍💼")
    with st.form(f"login_form_{access}"):
        username = st.text_input("Username", key=f"login_username_{access}")
        password = st.text_input("Password", type="password", key=f"login_password_{access}")
        submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)
    if submitted:
        employee = authenticate(username, password, access)
        if employee:
            st.session_state.employee = employee
            st.session_state.role = "p" if access == "p" else "staff"
            st.session_state.nav = "Dashboard"
            log_activity(employee, "Login", "Director" if access == "p" else "Store Clerk")
            st.rerun()
        else:
            st.error("Incorrect username, password, or access level.")
    if st.button("← Back", key=f"login_back_{access}", use_container_width=True):
        st.session_state.role = None
        st.session_state.nav = "Home"
        st.rerun()


def staff_sidebar(kind: str) -> None:
    employee = st.session_state.get("employee") or {}
    with st.sidebar:
        st.markdown("# 📚 Digital Books Store")
        st.success(f"Signed in as\n**{employee.get('First Name', '')} {employee.get('Last Name', '')}**")
        if kind == "staff":
            choices = ["Dashboard", "Inventory Receiving", "Catalog Administration", "Pricing Desk"]
            label = "Store Clerk Workspace"
        else:
            choices = ["Dashboard", "Employee Management", "Activity Audit"]
            label = "Director Workspace"
        current = st.session_state.get("nav", "Dashboard")
        if current not in choices:
            current = "Dashboard"
        nav = st.radio(label, choices, index=choices.index(current), key=f"workspace_nav_{kind}")
        st.session_state.nav = nav
        st.divider()
        if st.button("↩ Logout", key=f"workspace_logout_{kind}", use_container_width=True):
            logout()


def staff_dashboard() -> None:
    page_bg("staff")
    hero("Store Clerk Workspace", "Keep stock, catalog information and pricing accurate with fast operational tools.", "📦")
    books = read_books()
    low = [book for book in books if 0 < book["stock"] <= 2]
    out = [book for book in books if book["stock"] == 0]
    a, b, c, d = st.columns(4)
    a.metric("Catalog", len(books))
    b.metric("Units in stock", sum(book["stock"] for book in books))
    c.metric("Low stock", len(low))
    d.metric("Out of stock", len(out))
    st.markdown("### Inventory overview")
    df = pd.DataFrame([{"Code": book["code"], "Book": book["name"], "Genre": book["genre"], "Price": money(book["price"]), "Stock": book["stock"]} for book in books])
    st.dataframe(df, use_container_width=True, hide_index=True)


def add_stock_ui() -> None:
    page_bg("staff")
    hero("Inventory receiving", "Record incoming copies and the purchase expense in one operation.", "📥")
    books = read_books()
    codes = [book["code"] for book in books]
    if not codes:
        st.warning("No books found.")
        return
    code = st.selectbox("Select book", codes, format_func=lambda value: f"{value} · {find_book(value)['name']}", key="stock_book_select")
    book = find_book(code)
    a, b = st.columns(2)
    a.metric("Current stock", book["stock"])
    b.metric("Wholesale cost", money(book["wholesale"]))
    with st.form("stock_receiving_form"):
        quantity = st.number_input("Copies received", 1, 100000, 1)
        cost = st.number_input("Unit purchase cost (INR)", 0.0, 100000.0, float(book["wholesale"]), step=1.0)
        if st.form_submit_button("Add copies", type="primary", use_container_width=True):
            ok, message = add_stock(code, int(quantity), float(cost))
            if ok:
                log_activity(st.session_state.employee, f"Received {quantity} copies of {book['name']}", "Store Clerk")
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def catalog_admin_ui() -> None:
    page_bg("staff")
    hero("Catalog administration", "Add new titles and create collections without leaving the workspace.", "🗂️")
    tab1, tab2 = st.tabs(["Add new book", "Create genre"])
    with tab1:
        genres = get_genres()
        if not genres:
            st.info("Create a genre first.")
        else:
            with st.form("new_book_form"):
                a, b = st.columns(2)
                code = a.text_input("Unique product code *")
                name = b.text_input("Book title *")
                a, b = st.columns(2)
                author = a.text_input("Author *")
                language = b.text_input("Language *", value="English")
                a, b = st.columns(2)
                published = a.text_input("Published date", value="01-01-2026")
                genre = b.selectbox("Genre *", genres)
                a, b, c = st.columns(3)
                wholesale = a.number_input("Wholesale price", 0.0, 100000.0, 100.0)
                price = b.number_input("Market price", 0.0, 100000.0, 150.0)
                stock = c.number_input("Opening stock", 0, 100000, 0)
                if st.form_submit_button("Add book", type="primary", use_container_width=True):
                    ok, message = add_new_book({"code": code, "name": name, "author": author, "language": language, "published": published, "genre": genre, "wholesale": wholesale, "price": price, "stock": stock})
                    if ok:
                        log_activity(st.session_state.employee, f"Added book {name}", "Store Clerk")
                        st.success(message)
                    else:
                        st.error(message)
    with tab2:
        with st.form("new_genre_form"):
            name = st.text_input("New genre name")
            if st.form_submit_button("Create genre", type="primary", use_container_width=True):
                ok, message = add_new_genre(name)
                if ok:
                    log_activity(st.session_state.employee, f"Created genre {name}", "Store Clerk")
                    st.success(message)
                else:
                    st.error(message)


def pricing_ui() -> None:
    page_bg("staff")
    hero("Pricing desk", "Review market price, wholesale cost and margin across the catalog.", "💰")
    books = read_books()
    df = pd.DataFrame([{"Code": book["code"], "Book": book["name"], "Wholesale": money(book["wholesale"]), "Market Price": money(book["price"]), "Margin": money(book["margin"])} for book in books])
    st.dataframe(df, use_container_width=True, hide_index=True)


def director_dashboard() -> None:
    page_bg("director")
    hero("Director Command Center", "Monitor revenue, profitability, inventory and operational performance at a glance.", "👑")
    summary = sales_summary()
    a, b, c, d, e = st.columns(5)
    a.metric("Revenue", money(summary["revenue"]))
    b.metric("Gross profit", money(summary["profit"]))
    c.metric("Units sold", int(summary["units"]))
    d.metric("Orders", int(summary["orders"]))
    e.metric("Inventory expense", money(summary["expenses"]))
    books = read_books()
    low = sum(1 for book in books if 0 < book["stock"] <= 2)
    out = sum(1 for book in books if book["stock"] == 0)
    x, y = st.columns(2)
    x.metric("Low-stock SKUs", low)
    y.metric("Out-of-stock SKUs", out)
    orders = load_orders()
    if not orders:
        st.info("No customer orders have been recorded yet.")
        return
    df = pd.DataFrame(orders)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Item Total (INR)"] = pd.to_numeric(df["Item Total (INR)"], errors="coerce").fillna(0)
    daily = df.dropna(subset=["Order Date"]).groupby(df.dropna(subset=["Order Date"])["Order Date"].dt.date)["Item Total (INR)"].sum()
    st.markdown("### Revenue trend")
    st.line_chart(daily)
    st.markdown("### Recent customer orders")
    st.dataframe(df.tail(20), use_container_width=True, hide_index=True)


def employee_management() -> None:
    page_bg("director")
    hero("Employee management", "Create Store Clerk accounts directly. No OTP or secondary registration step.", "👥")
    with st.form("employee_add_form"):
        a, b = st.columns(2)
        empid = a.text_input("Employee ID *")
        first = b.text_input("First name *")
        a, b = st.columns(2)
        last = a.text_input("Last name *")
        phone = b.text_input("Phone number *", max_chars=10)
        a, b = st.columns(2)
        username = a.text_input("Username *")
        password = b.text_input("Password *", type="password")
        if st.form_submit_button("Create Store Clerk account", type="primary", use_container_width=True):
            rows = read_employees()
            duplicate = any(row.get("EMP ID", "").lower() == empid.lower() or row.get("Username", "").lower() == username.lower() for row in rows)
            if duplicate:
                st.error("Employee ID or username already exists.")
            elif not empid.strip() or not first.strip() or not last.strip() or not phone.isdigit() or len(phone) != 10 or not username.strip() or not password:
                st.error("Please complete all fields and use a valid 10-digit phone number.")
            else:
                rows.append({"EMP ID": empid.strip(), "First Name": first.strip(), "Last Name": last.strip(), "Phone Number": phone, "Username": username.strip(), "Password": password, "Access": "s"})
                write_employees(rows)
                log_activity(st.session_state.employee, f"Created Store Clerk account {username.strip()}", "Director")
                st.success("Store Clerk account created successfully.")
                st.rerun()
    rows = read_employees()
    if rows:
        display = pd.DataFrame(rows).drop(columns=["Password"], errors="ignore")
        st.markdown("### Current workforce")
        st.dataframe(display, use_container_width=True, hide_index=True)


def logs_ui() -> None:
    page_bg("director")
    hero("Activity audit", "A readable operational timeline of employee logins, logouts and store actions.", "📜")
    logs = list(reversed(get_activity_logs()))
    if not logs:
        st.info("No activity has been recorded yet.")
        return
    for index, log in enumerate(logs):
        st.markdown(f'<div class="log-card"><div><span class="log-action">{html.escape(log["Action"])}</span> · {html.escape(log["Employee"])}</div><div class="log-meta">Employee ID: {html.escape(log["Employee ID"])} · Workspace: {html.escape(log["Workspace"])} · {html.escape(log["Time"])}</div></div>', unsafe_allow_html=True)


def app() -> None:
    init_state()
    role = st.session_state.role
    if role is None:
        landing()
        return
    if role == "customer":
        customer_sidebar()
        nav = st.session_state.nav
        if nav == "Storefront":
            customer_home()
        elif nav == "Cart":
            customer_cart()
        elif nav == "Checkout":
            checkout()
        elif nav == "Order Confirmation":
            order_confirmation()
        return
    if role == "staff_login":
        login_page("s")
        return
    if role == "director_login":
        login_page("p")
        return
    if role == "staff":
        staff_sidebar("staff")
        pages = {"Dashboard": staff_dashboard, "Inventory Receiving": add_stock_ui, "Catalog Administration": catalog_admin_ui, "Pricing Desk": pricing_ui}
        pages.get(st.session_state.nav, staff_dashboard)()
        return
    if role == "p":
        staff_sidebar("director")
        pages = {"Dashboard": director_dashboard, "Employee Management": employee_management, "Activity Audit": logs_ui}
        pages.get(st.session_state.nav, director_dashboard)()
        return


if __name__ == "__main__":
    app()
