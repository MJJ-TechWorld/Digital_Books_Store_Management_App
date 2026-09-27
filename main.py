import streamlit as st
from datetime import datetime
from html import escape
from function_utils import *

st.set_page_config(page_title="BooksKart | Store Management", page_icon="📚", layout="wide", initial_sidebar_state="expanded")
ensure_runtime_files()

BG = {
    "landing":"https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1800&q=82",
    "customer":"https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=1800&q=82",
    "clerk":"https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1800&q=82",
    "director":"https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1800&q=82",
    "records":"https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=1800&q=82"
}

st.markdown(f'''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{{--ink:#172033;--muted:#667085;--purple:#6546f5;--cyan:#12b8a6;--orange:#ff8a3d;--red:#e5484d;--card:rgba(255,255,255,.94)}}
html,body,[class*="css"]{{font-family:Inter,sans-serif;color:var(--ink)}}
[data-testid="stAppViewContainer"]{{background:transparent}}[data-testid="stMain"]{{background:transparent}}
[data-testid="stHeader"]{{background:transparent}}
.block-container{{padding-top:1.4rem;max-width:1450px}}
.hero{{padding:42px 46px;border-radius:30px;background:linear-gradient(105deg,rgba(255,255,255,.84),rgba(246,244,255,.68)),url('{BG['landing']}') center/cover;box-shadow:0 20px 70px rgba(20,30,70,.12);border:1px solid #fff;margin-bottom:28px}}
.hero h1{{font-size:clamp(36px,5vw,68px);margin:0;letter-spacing:-2px;color:#241b52;font-weight:800}}.hero p{{font-size:18px;color:#596275;max-width:760px}}
.section-title{{font-size:28px;font-weight:800;color:#251d52;margin:12px 0 18px}}.gradient-text{{background:linear-gradient(90deg,#6546f5,#12a99b,#ff7a3d);-webkit-background-clip:text;background-clip:text;color:transparent}}
.card{{background:var(--card);border:1px solid rgba(100,70,245,.10);border-radius:22px;padding:22px;box-shadow:0 12px 38px rgba(23,32,51,.08);height:100%}}
.metric{{background:linear-gradient(135deg,#fff,#f3f0ff);border:1px solid #e7e1ff;border-radius:20px;padding:20px;box-shadow:0 10px 28px rgba(44,34,100,.07)}}.metric .v{{font-size:30px;font-weight:800;color:#372a8e}}.metric .l{{color:#667085;font-weight:600}}
.book-card{{background:#fff;border:1px solid #e9eaf0;border-radius:20px;padding:20px;box-shadow:0 10px 30px rgba(23,32,51,.07);min-height:230px}}.book-card h3{{color:#241b52;margin-bottom:5px}}.pill{{display:inline-block;padding:6px 11px;border-radius:999px;background:#f0edff;color:#5637d8;font-weight:700;font-size:12px}}
.status-ok{{color:#087f5b;font-weight:800}}.status-low{{color:#b26a00;font-weight:800}}.status-out{{color:#c92a2a;font-weight:800}}
[data-testid="stSidebar"]{{background:linear-gradient(180deg,#15132a,#211c47 58%,#2e2564);color:white}}[data-testid="stSidebar"] *{{color:#fff!important}}
[data-testid="stSidebar"] .stButton>button{{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.14);color:white!important;border-radius:12px}}
.stButton>button{{border-radius:13px;border:0;padding:.62rem 1rem;font-weight:700;box-shadow:0 6px 18px rgba(60,45,150,.12)}}
.stButton>button[kind="primary"]{{background:linear-gradient(90deg,#6546f5,#7a5cf7);color:#fff}}
.stDownloadButton>button{{border-radius:13px;font-weight:700}}
div[data-testid="stForm"]{{background:rgba(255,255,255,.9);border-radius:22px;padding:22px;border:1px solid #e7e8ef}}
</style>''', unsafe_allow_html=True)


def go(page):
    st.session_state.page = page
    st.rerun()

def init():
    defaults = {"page":"landing","role":None,"employee":None,"cart":{},"order":None,"invoice":None,"invoice_pdf":None,"customer":None,"restock_book_code":None}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
init()

def page_bg(kind):
    st.markdown(f'''<style>[data-testid="stAppViewContainer"]{{background:linear-gradient(rgba(248,250,253,.70),rgba(248,250,253,.78)),url('{BG[kind]}') center/cover fixed}}</style>''', unsafe_allow_html=True)

def logout():
    st.session_state.role=None; st.session_state.employee=None; st.session_state.page="landing"; st.session_state.cart={}; st.session_state.order=None; st.session_state.invoice=None; st.rerun()

def sidebar_customer():
    with st.sidebar:
        st.markdown("## 📚 BooksKart")
        st.caption("Customer storefront")
        st.divider()
        if st.button("🏠 Storefront", key="cs_store", use_container_width=True): go("customer")
        if st.button(f"🛒 Cart · {sum(st.session_state.cart.values())}", key="cs_cart", use_container_width=True): go("cart")
        if st.button("🔐 Secure Checkout", key="cs_checkout", use_container_width=True): go("checkout")
        st.divider()
        if st.button("↩ Change Portal", key="cs_logout", use_container_width=True): logout()

def sidebar_staff(role):
    with st.sidebar:
        st.markdown("## 📚 BooksKArt")
        st.caption(f"{role} Workspace")
        st.divider()
        if role=="Store Clerk":
            nav=[("📊 Dashboard","clerk"),("📦 Inventory Receiving","receiving"),("➕ Add Book","addbook"),("🏷️ Genres","genres"),("💰 Pricing","pricing"),("🧾 Activity Log","activity")]
        else:
            nav=[("📊 Executive Dashboard","director"),("👥 Employees","employees"),("📚 Catalog","catalog"),("💰 Pricing","pricing"),("💳 Expenses","expenses"),("🧾 Sales Records","records"),("🧾 Activity Log","activity")]
        for label,target in nav:
            if st.button(label,key=f"nav_{role}_{target}",use_container_width=True): go(target)
        st.divider()
        if st.button("↩ Logout",key=f"logout_{role}",use_container_width=True): logout()

def landing():
    page_bg("landing")
    st.markdown('''<div class="hero"><div class="pill">BOOK STORE MANAGEMENT</div><h1>BOOK<span class="gradient-text">NEST</span></h1><p>Storefront and store operations for customers, store clerks and directors.</p></div>''', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Choose your workspace</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    cards=[("🛍️","Customer","Explore the catalog, build your cart and place a Cash on Delivery order."),("📦","Store Clerk","Manage receiving, stock, books, genres, pricing and daily activity."),("🏢","Director","Monitor business performance, employees, sales, expenses and catalog control.")]
    for col,(icon,title,desc) in zip((c1,c2,c3),cards):
        with col:
            st.markdown(f'<div class="card"><div style="font-size:42px">{icon}</div><h2>{title}</h2><p style="color:#667085;min-height:68px">{desc}</p></div>',unsafe_allow_html=True)
            if st.button(f"Continue as {title}",key=f"role_{title}",type="primary",use_container_width=True):
                if title=="Customer": go("customer")
                else: st.session_state.login_role=title; go("login")

def login():
    page_bg("clerk" if st.session_state.get("login_role")=="Store Clerk" else "director")
    role=st.session_state.get("login_role","Store Clerk")
    st.markdown(f'<div class="hero"><div class="pill">LOGIN</div><h1>{role} <span class="gradient-text">Portal</span></h1><p>Sign in using the credentials maintained in EMPLOYEES.csv.</p></div>',unsafe_allow_html=True)
    _,mid,_=st.columns([1,1.2,1])
    with mid:
        with st.form("login_form"):
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
            if st.form_submit_button("Sign In →",type="primary",use_container_width=True):
                emp=authenticate_employee(username,password)
                if emp and emp["role"]==role:
                    st.session_state.employee=emp; st.session_state.role=role; log_activity(emp.get("Full Name",username),"Logged in",role); go("clerk" if role=="Store Clerk" else "director")
                else: st.error("Invalid credentials or insufficient access.")
        if st.button("← Back",use_container_width=True): go("landing")

def customer():
    page_bg("customer"); sidebar_customer()
    books=load_books(); genres=load_genres()
    st.markdown('<div class="hero"><div class="pill">CUSTOMER</div><h1>Find your next <span class="gradient-text">great read.</span></h1><p>Search the live catalog, filter by genre and add available books directly to your cart.</p></div>',unsafe_allow_html=True)
    a,b,c=st.columns([2,1,1]); search=a.text_input("Search books, authors or codes",key="cust_search"); genre=b.selectbox("Genre",["All Genres"]+genres); availability=c.selectbox("Availability",["All Books","In Stock","Out of Stock"])
    filtered=[x for x in books if (not search or search.lower() in f"{x['name']} {x['author']} {x['id']}".lower()) and (genre=="All Genres" or x['genre']==genre) and (availability=="All Books" or (availability=="In Stock" and x['stock']>0) or (availability=="Out of Stock" and x['stock']==0))]
    st.caption(f"{len(filtered)} books found · {sum(st.session_state.cart.values())} item(s) in cart")
    for start in range(0,len(filtered),3):
        cols=st.columns(3)
        for col,bk in zip(cols,filtered[start:start+3]):
            with col:
                status="Out of Stock" if bk['stock']==0 else ("Low Stock" if bk['stock']<=2 else "Healthy")
                cls="status-out" if bk['stock']==0 else ("status-low" if bk['stock']<=2 else "status-ok")
                st.markdown(f'''<div class="book-card"><span class="pill">{escape(bk['genre'])}</span><h3>{escape(bk['name'])}</h3><p style="color:#667085">{escape(bk['author'])}</p><p><b>₹{bk['price']:.2f}</b> · <span class="{cls}">{status}</span></p><small>{escape(bk['id'])} · {escape(bk['language'])}</small></div>''',unsafe_allow_html=True)
                if st.button("Add to Cart",key=f"add_{bk['id']}",disabled=bk['stock']<=0,use_container_width=True):
                    st.session_state.cart[bk['id']]=min(st.session_state.cart.get(bk['id'],0)+1,bk['stock']); st.toast("Added to cart"); st.rerun()

def cart_page():
    page_bg("customer"); sidebar_customer(); st.markdown('<div class="hero"><div class="pill">YOUR CART</div><h1>Review your <span class="gradient-text">selection.</span></h1></div>',unsafe_allow_html=True)
    if not st.session_state.cart: st.info("Your cart is empty.");
    books={b['id']:b for b in load_books()}; total=0
    for bid,qty in list(st.session_state.cart.items()):
        b=books.get(bid)
        if not b: continue
        line=b['price']*qty; total+=line
        c1,c2,c3,c4=st.columns([3,1,1,1]); c1.markdown(f"**{b['name']}**  \\n{b['author']} · {bid}"); c2.write(f"₹{b['price']:.2f}"); newqty=c3.number_input("Qty",1,min(b['stock'],10),qty,key=f"qty_{bid}");
        if newqty!=qty: st.session_state.cart[bid]=newqty; st.rerun()
        if c4.button("Remove",key=f"rm_{bid}"): del st.session_state.cart[bid]; st.rerun()
    st.markdown(f'<div class="metric"><div class="l">Cart Total</div><div class="v">₹{total:,.2f}</div></div>',unsafe_allow_html=True)
    if st.session_state.cart and st.button("Proceed to Secure Checkout →",type="primary",use_container_width=True): go("checkout")

def checkout():
    page_bg("customer"); sidebar_customer()
    if not st.session_state.cart: go("cart")
    books={b['id']:b for b in load_books()}; total=sum(books[k]['price']*v for k,v in st.session_state.cart.items() if k in books)
    st.markdown('<div class="hero"><div class="pill">CHECKOUT · COD</div><h1>Complete your <span class="gradient-text">delivery.</span></h1><p>Enter customer and delivery details.</p></div>',unsafe_allow_html=True)
    st.markdown("### Customer details")
    a,b=st.columns(2); name=a.text_input("Full Name *",key="checkout_name"); phone=b.text_input("Phone *",max_chars=10,key="checkout_phone")
    st.markdown("### Delivery address")
    a,b=st.columns(2); flat=a.text_input("Flat / House / Building *",key="checkout_flat"); street=b.text_input("Street / Area *",key="checkout_street")
    landmark=st.text_input("Landmark",key="checkout_landmark")
    states=get_indian_states()
    if not states: st.error("Address directory is unavailable. Check GEMINI_API_KEY and try again."); return
    state=st.selectbox("State *",states,key="address_state_live")
    districts=get_indian_districts(state)
    if not districts: st.error(f"No district data was returned for {state}. Please retry."); return
    district=st.selectbox("District *",districts,key=f"address_district_live_{state}")
    cities=get_indian_cities(state,district)
    if not cities: st.error(f"No city data was returned for {district}, {state}. Please retry."); return
    city=st.selectbox("City *",cities,key=f"address_city_live_{state}_{district}")
    pins=get_city_pincodes(state,district,city)
    if not pins: st.error(f"No PIN codes were returned for {city}, {district}, {state}. Please retry."); return
    pin=st.selectbox("PIN *",pins,key=f"address_pin_live_{state}_{district}_{city}")
    st.markdown('<div class="metric"><div class="l">Payment Method</div><div class="v" style="font-size:22px">Cash on Delivery</div></div>',unsafe_allow_html=True)
    if st.button(f"Place Order · ₹{total:,.2f}",type="primary",use_container_width=True):
        if not name or not phone.isdigit() or len(phone)!=10 or not flat or not street or not pin.isdigit() or len(pin)!=6: st.error("Please complete all required fields with valid phone and PIN values."); return
        items=[]
        for bid,qty in st.session_state.cart.items():
            b=books.get(bid)
            if not b or b['stock']<qty: st.error(f"Insufficient stock for {b['name'] if b else bid}."); return
            items.append({"book_id":bid,"name":b['name'],"author":b['author'],"genre":b['genre'],"quantity":qty,"unit_price":b['price'],"cost_price":b['cost'],"line_total":round(b['price']*qty,2),"line_profit":round((b['price']-b['cost'])*qty,2)})
        order={"order_id":new_order_id(),"date":datetime.now().strftime("%d-%m-%Y %H:%M:%S"),"customer_name":clean_name(name),"phone":phone,"flat":clean_address(flat),"street":clean_address(street),"landmark":clean_address(landmark),"city":clean_name(city),"state":clean_name(state),"pin":pin,"payment":"Cash on Delivery","grand_total":round(sum(i['line_total'] for i in items),2),"grand_profit":round(sum(i['line_profit'] for i in items),2)}
        if reduce_stock(items):
            append_order(order,items); log_activity(order['customer_name'],"Order placed",order['order_id']); st.session_state.order=order; st.session_state.invoice=invoice_html(order,items); st.session_state.invoice_pdf=invoice_pdf(order,items); st.session_state.cart={}; go("confirmation")

def confirmation():
    page_bg("customer"); sidebar_customer(); order=st.session_state.get("order")
    if not order: go("customer")
    st.markdown(f'<div class="hero"><div class="pill">ORDER CONFIRMED</div><h1>Thank you, <span class="gradient-text">{escape(order["customer_name"])}.</span></h1><p>Your order <b>{order["order_id"]}</b> has been recorded successfully.</p></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="metric"><div class="l">Order Total · Cash on Delivery</div><div class="v">₹{order["grand_total"]:,.2f}</div></div>',unsafe_allow_html=True)
    if st.session_state.get("invoice"):
        st.download_button("⬇ Download Bill (PDF)",st.session_state.get("invoice_pdf",b""),file_name=f"{order['order_id']}.pdf",mime="application/pdf",use_container_width=True)
        st.components.v1.html(st.session_state.invoice,height=760,scrolling=True)
    if st.button("Continue Shopping →",type="primary",use_container_width=True): go("customer")

def clerk_dashboard():
    page_bg("clerk"); sidebar_staff("Store Clerk"); books=load_books(); out=[b for b in books if b['stock']==0]; low=[b for b in books if 0<b['stock']<=2]; total=len(books); units=sum(b['stock'] for b in books)
    st.markdown('<div class="hero"><div class="pill">STORE CLERK</div><h1>Inventory <span class="gradient-text">Overview</span></h1><p>Receive stock, maintain catalog data and monitor availability.</p></div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for c,label,val in zip(cols,["Catalog","Units on Hand","Low Stock","Out of Stock"],[total,units,len(low),len(out)]): c.markdown(f'<div class="metric"><div class="l">{label}</div><div class="v">{val}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Out-of-stock queue</div>',unsafe_allow_html=True)
    if not out: st.success("No books are currently out of stock.")
    for b in out:
        c1,c2,c3=st.columns([4,2,1]); c1.markdown(f"**{b['name']}**  · {b['id']}  \\n{b['author']}"); c2.markdown('<span class="status-out">0 copies · Out of Stock</span>',unsafe_allow_html=True)
        if c3.button("📥 Restock",key=f"restock_{b['id']}"): st.session_state.restock_book_code=b['id']; go("receiving")
    st.markdown('<div class="section-title">Low-stock queue</div>',unsafe_allow_html=True)
    for b in low: st.markdown(f'<div class="card" style="margin-bottom:10px"><b>{escape(b["name"])}</b> · {escape(b["id"])} · <span class="status-low">{b["stock"]} copies</span></div>',unsafe_allow_html=True)

def receiving():
    page_bg("clerk"); sidebar_staff("Store Clerk"); books=load_books(); mapping={b['id']:b['name'] for b in books}; ids=list(mapping); pre=st.session_state.get("restock_book_code"); default=ids.index(pre) if pre in ids else 0
    st.markdown('<div class="hero"><div class="pill">INVENTORY RECEIVING</div><h1>Receive <span class="gradient-text">New Stock</span></h1><p>Update available copies and record the stock receipt.</p></div>',unsafe_allow_html=True)
    with st.form("receiving_form"):
        bid=st.selectbox("Book",ids,index=default,format_func=lambda x:f"{x} · {mapping[x]}"); copies=st.number_input("Copies received",min_value=1,step=1,value=1)
        if st.form_submit_button("Confirm Stock Receipt →",type="primary",use_container_width=True):
            b=add_stock(bid,copies); log_activity(st.session_state.employee.get("Full Name","Store Clerk"),"Stock received",f"{bid} +{copies}"); st.session_state.restock_book_code=None; st.toast(f"{copies} copies added to {b['name']}"); go("clerk")

def addbook():
    page_bg("clerk"); sidebar_staff("Store Clerk"); genres=load_genres(); st.markdown('<div class="hero"><div class="pill">CATALOG</div><h1>Add a <span class="gradient-text">New Book</span></h1></div>',unsafe_allow_html=True)
    with st.form("add_book_form"):
        a,b=st.columns(2); name=a.text_input("Book Name *"); author=b.text_input("Author Name *"); a,b=st.columns(2); genre=a.selectbox("Genre",genres); language=b.text_input("Language",value="English"); published=st.text_input("Published Date"); a,b,c=st.columns(3); cost=a.number_input("Wholesale / Cost Price",min_value=0.0,step=1.0); price=b.number_input("Market Price",min_value=0.0,step=1.0); stock=c.number_input("Opening Stock",min_value=0,step=1); 
        if st.form_submit_button("Create Book →",type="primary",use_container_width=True):
            if not name or not author: st.error("Book name and author are required.")
            else:
                used={b['id'] for b in load_books()}; n=1
                while f"BK{n:04d}" in used:n+=1
                book={"id":f"BK{n:04d}","name":clean_text(name),"author":clean_name(author),"genre":genre,"language":clean_text(language),"published":clean_text(published),"cost":money(cost),"price":money(price),"profit":money(price-cost),"stock":integer(stock)}
                add_book(book); log_activity(st.session_state.employee.get("Full Name","Store Clerk"),"Book added",book['id']); go("clerk")

def genres():
    page_bg("clerk"); sidebar_staff("Store Clerk"); st.markdown('<div class="hero"><div class="pill">GENRES</div><h1>Manage <span class="gradient-text">Genres</span></h1></div>',unsafe_allow_html=True)
    with st.form("genre_form"):
        g=st.text_input("New genre");
        if st.form_submit_button("Add Genre →",type="primary"):
            if add_genre(g): log_activity(st.session_state.employee.get("Full Name","Store Clerk"),"Genre added",clean_name(g)); st.rerun()
            else: st.error("Genre already exists or is invalid.")
    st.write(" · ".join(load_genres()))

def pricing():
    role=st.session_state.role; page_bg("clerk" if role=="Store Clerk" else "director"); sidebar_staff(role); books=load_books(); st.markdown('<div class="hero"><div class="pill">PRICING</div><h1>Catalog <span class="gradient-text">Rates</span></h1></div>',unsafe_allow_html=True)
    for b in books:
        c1,c2,c3,c4=st.columns([3,1,1,1]); c1.write(f"**{b['name']}** · {b['id']}"); c2.write(f"₹{b['price']:.2f}"); c3.write(f"Cost ₹{b['cost']:.2f}");
        new=c4.number_input("Price",min_value=0.0,value=float(b['price']),step=1.0,key=f"price_{b['id']}",label_visibility="collapsed")
        if new!=b['price'] and c4.button("Save",key=f"saveprice_{b['id']}"): update_book(b['id'],price=money(new),profit=money(new-b['cost'])); log_activity(st.session_state.employee.get("Full Name",role),"Price updated",b['id']); st.rerun()

def activity():
    role=st.session_state.role; page_bg("clerk" if role=="Store Clerk" else "records"); sidebar_staff(role); st.markdown('<div class="hero"><div class="pill">ACTIVITY LOG</div><h1>Activity <span class="gradient-text">Log</span></h1></div>',unsafe_allow_html=True)
    for i,line in enumerate(load_logs(),1): st.markdown(f'<div class="card" style="margin-bottom:10px;padding:15px">🧾 {escape(line)}</div>',unsafe_allow_html=True)

def director():
    page_bg("director"); sidebar_staff("Director"); sales=load_sales(); expenses=load_expenses(); revenue=sum(money(x.get('Line Total')) for x in sales); profit=sum(money(x.get('Line Profit')) for x in sales); exp=sum(money(x.get('Amount')) for x in expenses); books=load_books(); inventory=sum(b['stock'] for b in books); employees=load_employees()
    st.markdown('<div class="hero"><div class="pill">DIRECTOR</div><h1>Business <span class="gradient-text">Overview</span></h1><p>Sales, margin, inventory and workforce overview.</p></div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for c,l,v in zip(cols,["Revenue","Gross Profit","Expenses","Inventory Units","Employees"],[revenue,profit,exp,inventory,len(employees)]): c.markdown(f'<div class="metric"><div class="l">{l}</div><div class="v">{("₹"+format(v,",.2f")) if isinstance(v,float) else v}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Operational snapshot</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3); a.markdown(f'<div class="card"><h3>Catalog</h3><p>{len(books)} active books</p><p>{sum(b["stock"]==0 for b in books)} out of stock</p></div>',unsafe_allow_html=True); b.markdown(f'<div class="card"><h3>Orders</h3><p>{len(set(str(x.get("Order ID")) for x in sales))} orders</p><p>COD enabled</p></div>',unsafe_allow_html=True); c.markdown(f'<div class="card"><h3>Margin</h3><p>Gross profit ₹{profit:,.2f}</p><p>Operating expenses ₹{exp:,.2f}</p></div>',unsafe_allow_html=True)

def employees_page():
    page_bg("director"); sidebar_staff("Director"); emps=load_employees(); st.markdown('<div class="hero"><div class="pill">WORKFORCE MANAGEMENT</div><h1>Employee <span class="gradient-text">Administration</span></h1><p>Employee IDs are generated automatically from the highest existing EMP number.</p></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="metric"><div class="l">Next Employee ID</div><div class="v">{generate_employee_id()}</div></div>',unsafe_allow_html=True)
    with st.form("employee_form"):
        a,b=st.columns(2); name=a.text_input("Full Name *"); phone=b.text_input("Phone"); a,b=st.columns(2); email=a.text_input("Email"); username=b.text_input("Username *"); a,b=st.columns(2); password=a.text_input("Password *",type="password"); designation=b.selectbox("Designation",["Store Clerk","Inventory Manager","Sales Executive","Assistant Manager","Director"])
        if st.form_submit_button("Create Employee →",type="primary",use_container_width=True):
            if not name or not username or not password: st.error("Name, username and password are required.")
            else:
                try:
                    rec=create_employee(name,phone,email,username,password,designation); log_activity(st.session_state.employee.get("Full Name","Director"),"Employee created",rec['Employee ID']); st.success(f"Employee {rec['Employee ID']} created successfully."); st.rerun()
                except ValueError as e: st.error(str(e))
    st.markdown('<div class="section-title">Current employees</div>',unsafe_allow_html=True)
    for e in emps: st.markdown(f'<div class="card" style="margin-bottom:10px"><b>{escape(e.get("Employee ID",""))}</b> · {escape(e.get("Full Name",""))} · {escape(e.get("Designation",""))} · @{escape(e.get("Username",""))} · <span class="status-ok">{escape(e.get("Status","Active"))}</span></div>',unsafe_allow_html=True)

def catalog():
    page_bg("director"); sidebar_staff("Director"); books=load_books(); st.markdown('<div class="hero"><div class="pill">CATALOG</div><h1>Book <span class="gradient-text">Catalog</span></h1></div>',unsafe_allow_html=True)
    q=st.text_input("Search catalog"); rows=[b for b in books if not q or q.lower() in f"{b['name']} {b['author']} {b['id']} {b['genre']}".lower()]
    for b in rows: st.markdown(f'<div class="card" style="margin-bottom:10px"><b>{escape(b["name"])}</b> · {escape(b["id"])} · {escape(b["genre"])}<br>{escape(b["author"])} · ₹{b["price"]:.2f} · Stock {b["stock"]}</div>',unsafe_allow_html=True)

def records():
    page_bg("records"); sidebar_staff("Director"); sales=load_sales(); st.markdown('<div class="hero"><div class="pill">SALES RECORDS</div><h1>Sales <span class="gradient-text">Records</span></h1><p>Customer name and address values shown here are stored after normalization.</p></div>',unsafe_allow_html=True)
    if not sales: st.info("No sales recorded yet."); return
    for r in sales[::-1]: st.markdown(f'''<div class="card" style="margin-bottom:12px"><h3>{escape(str(r.get('Order ID','')))} · {escape(str(r.get('Customer Name','')))}</h3><p>{escape(str(r.get('Flat / House / Building','')))}, {escape(str(r.get('Street / Area','')))}, {escape(str(r.get('Landmark','')))}<br>{escape(str(r.get('City','')))}, {escape(str(r.get('State','')))} - {escape(str(r.get('PIN','')))}</p><p><b>{escape(str(r.get('Book Name','')))}</b> · Qty {r.get('Quantity',0)} · ₹{money(r.get('Line Total')):,.2f} · {escape(str(r.get('Payment Method','')))}</p></div>''',unsafe_allow_html=True)

def expenses():
    page_bg("director"); sidebar_staff("Director"); st.markdown('<div class="hero"><div class="pill">EXPENSES</div><h1>Expense <span class="gradient-text">Management</span></h1></div>',unsafe_allow_html=True)
    with st.form("expense_form"):
        a,b=st.columns(2); cat=a.text_input("Category"); desc=b.text_input("Description"); amount=st.number_input("Amount",min_value=0.0,step=100.0)
        if st.form_submit_button("Record Expense →",type="primary"):
            add_expense(cat,desc,amount); log_activity(st.session_state.employee.get("Full Name","Director"),"Expense recorded",f"₹{amount:.2f}"); st.rerun()
    for e in load_expenses()[::-1]: st.markdown(f'<div class="card" style="margin-bottom:10px"><b>{escape(e.get("Expense ID",""))}</b> · {escape(e.get("Category",""))} · ₹{money(e.get("Amount")):,.2f}<br>{escape(e.get("Description",""))}</div>',unsafe_allow_html=True)

def app():
    p=st.session_state.page
    if p=="landing": landing()
    elif p=="login": login()
    elif p=="customer": customer()
    elif p=="cart": cart_page()
    elif p=="checkout": checkout()
    elif p=="confirmation": confirmation()
    elif p=="clerk": clerk_dashboard()
    elif p=="receiving": receiving()
    elif p=="addbook": addbook()
    elif p=="genres": genres()
    elif p=="pricing": pricing()
    elif p=="activity": activity()
    elif p=="director": director()
    elif p=="employees": employees_page()
    elif p=="catalog": catalog()
    elif p=="records": records()
    elif p=="expenses": expenses()
    else: go("landing")

app()
