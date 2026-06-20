import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Biryani Shop ERP & Inventory Management System",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SYSTEM STATE INITIALIZATION (IN-MEMORY DATABASE) ---
if 'initialized' not in st.session_state:
    # 1. Partner Capital Structure
    st.session_state.partners = [
        {"name": "Foishal", "investment": 200000, "share": 18.18},
        {"name": "Anam", "investment": 200000, "share": 18.18},
        {"name": "Habib", "investment": 200000, "share": 18.18},
        {"name": "Anayat", "investment": 200000, "share": 18.18},
        {"name": "Rasel Karim", "investment": 200000, "share": 18.18},
        {"name": "Mazharul", "investment": 100000, "share": 9.09},
    ]
    
    # 2. Fixed Assets
    st.session_state.assets = [
        {"item": "Shop Advance", "cost": 300000},
        {"item": "Kitchen Advance", "cost": 50000},
        {"item": "Degh/Pots", "cost": 40000},
        {"item": "Burners", "cost": 24000},
        {"item": "Deep Freezer", "cost": 35000},
        {"item": "Interior & Signboard", "cost": 60000},
        {"item": "Tables & Chairs", "cost": 36000},
        {"item": "Crockery", "cost": 15000},
        {"item": "POS Setup", "cost": 18000},
    ]
    
    # 3. Inventory Stock Master
    st.session_state.inventory = {
        "Rice": {"opening": 500, "purchase": 100, "used": 120, "reorder": 100, "unit": "kg"},
        "Beef": {"opening": 200, "purchase": 50, "used": 60, "reorder": 50, "unit": "kg"},
        "Chicken": {"opening": 150, "purchase": 80, "used": 95, "reorder": 40, "unit": "kg"},
        "Onion": {"opening": 100, "purchase": 20, "used": 35, "reorder": 20, "unit": "kg"},
        "Potato": {"opening": 300, "purchase": 50, "used": 80, "reorder": 50, "unit": "kg"},
        "Oil": {"opening": 200, "purchase": 40, "used": 55, "reorder": 30, "unit": "Ltr"},
        "Spices": {"opening": 50, "purchase": 10, "used": 12, "reorder": 10, "unit": "kg"},
        "Egg": {"opening": 1000, "purchase": 200, "used": 350, "reorder": 200, "unit": "Pcs"},
        "Soft Drinks": {"opening": 500, "purchase": 120, "used": 150, "reorder": 100, "unit": "Pcs"}
    }
    
    # 4. Daily Variable Material Bazar Expenses
    st.session_state.bazar_expenses = [
        {"date": "2026-06-05", "item": "Beef Stock Order", "amount": 12000, "category": "Meat"},
        {"date": "2026-06-12", "item": "Rice & Oils Delivery", "amount": 4500, "category": "Groceries"},
        {"date": "2026-06-18", "item": "Spices & Vegetables", "amount": 2500, "category": "Spices/Veg"},
    ]
    
    # 5. Menu Items
    st.session_state.menu = [
        {"item": "Chicken Biryani", "price": 180},
        {"item": "Beef Khichuri", "price": 220},
        {"item": "Vegetable Khichuri", "0": 90}, # Handled standard uniform naming key below
        {"item": "Vegetable Khichuri", "price": 90},
        {"item": "Tehari", "price": 150},
        {"item": "Mubarak Pulao", "price": 200},
    ]
    
    # 6. Sales Logs (Pre-filled to match June targeted Sales data of 36,500)
    st.session_state.sales_log = [
        {"invoice": "INV-001", "date": "2026-06-02", "product": "Chicken Biryani", "qty": 50, "amount": 9000, "payment": "Cash"},
        {"invoice": "INV-002", "date": "2026-06-10", "product": "Beef Khichuri", "qty": 18, "amount": 3960, "payment": "Bkash"},
        {"invoice": "INV-003", "date": "2026-06-15", "product": "Mubarak Pulao", "qty": 45, "amount": 9000, "payment": "Card"},
        {"invoice": "INV-004", "date": "2026-06-20", "product": "Tehari", "qty": 66, "amount": 9900, "payment": "Cash"},
        {"invoice": "INV-005", "date": "2026-06-21", "product": "Chicken Biryani", "qty": 26, "amount": 4640, "payment": "Bkash"},
    ]
    st.session_state.initialized = True

# --- GLOBAL CALCULATION ENGINES ---
def calculate_financials():
    total_capital = sum(p['investment'] for p in st.session_state.partners)
    total_setup_cost = sum(a['cost'] for a in st.session_state.assets)
    remaining_liquidity = total_capital - total_setup_cost
    
    # June specific filtered calculation metrics
    june_sales = sum(s['amount'] for s in st.session_state.sales_log if "-06-" in s['date'])
    june_variable = sum(e['amount'] for e in st.session_state.bazar_expenses if "-06-" in e['date'])
    fixed_overhead = 106500
    net_profit = june_sales - june_variable - fixed_overhead
    
    return total_capital, total_setup_cost, remaining_liquidity, june_sales, june_variable, fixed_overhead, net_profit

total_capital, total_setup_cost, remaining_liquidity, june_sales, june_variable, fixed_overhead, net_profit = calculate_financials()


# --- SIDEBAR NAV & USER ROLES ---
st.sidebar.markdown("# 🍲 Biryani Shop ERP")
st.sidebar.markdown("---")
user_role = st.sidebar.selectbox("🔑 Access Control Role", ["Super Admin", "Admin", "Manager", "Cashier", "Partner (View Only)"])
menu_selection = st.sidebar.radio("📁 ERP Navigation Menu", [
    "Self Dashboard",
    "Admin Dashboard",
    "Partner Management",
    "Fixed Assets Register",
    "Inventory Management",
    "POS Billing & Sales Log",
    "Financial & Analytical Reports"
])

# Role restrictions validation helper
def check_clearance(allowed_roles):
    if user_role not in allowed_roles:
        st.error(f"🚫 Access Denied! Your current role [{user_role}] does not have authorization to view this section.")
        st.stop()


# ==========================================
# 1. SELF DASHBOARD
# ==========================================
if menu_selection == "Self Dashboard":
    st.title("👤 Self User Dashboard")
    st.subheader("Shop Capital Runway & Monthly Summary (June)")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Capital Raised", f"{total_capital:,.2f} BDT")
    col2.metric("Total Spent Setup Assets", f"{total_setup_cost:,.2f} BDT", delta="-Fixed Capex")
    col3.metric("Remaining Liquidity Capital", f"{remaining_liquidity:,.2f} BDT")
    col4.metric("Net Profit (June Selected)", f"{net_profit:,.2f} BDT", delta=f"{net_profit:,.2f} BDT", delta_color="inverse")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🧮 Calculations Audit Flow")
        st.info(f"**Sales Revenue Calculation:** \n\n June Total: **{june_sales:,.2f} BDT**")
        st.warning(f"**Variable Cost Calculation:** \n\n June Total Bazar Outflow: **{june_variable:,.2f} BDT**")
        st.error(f"**Net Profit Calculation:** \n\n Revenue ({june_sales:,.0f}) - Variable Cost ({june_variable:,.0f}) - Fixed Operational Rent/Overhead ({fixed_overhead:,.0f}) = **{net_profit:,.2f} BDT**")

    with c2:
        st.markdown("### 👥 Partner Loss/Profit Distribution Share")
        partner_payouts = []
        for p in st.session_state.partners:
            # Weighted dynamically on current equity structure
            allocated_share = round((p['investment'] / total_capital) * net_profit, 2)
            partner_payouts.append({
                "Partner Name": p['name'],
                "Investment Share %": f"{(p['investment'] / total_capital)*100:.2f}%",
                "Payout (BDT)": f"{allocated_share:,.2f}"
            })
        st.table(pd.DataFrame(partner_payouts))

    st.markdown("---")
    st.markdown("### 📊 Whole Year Month-by-Month Glance")
    
    months_data = [
        {"Month": "January", "Sales": 0, "Net Profit": -106500},
        {"Month": "February", "Sales": 0, "Net Profit": -106500},
        {"Month": "March", "Sales": 0, "Net Profit": -106500},
        {"Month": "April", "Sales": 0, "Net Profit": -106500},
        {"Month": "May", "Sales": 0, "Net Profit": -106500},
        {"Month": "June", "Sales": june_sales, "Net Profit": net_profit},
        {"Month": "July", "Sales": 0, "Net Profit": -106500},
        {"Month": "August", "Sales": 0, "Net Profit": -106500},
        {"Month": "September", "Sales": 0, "Net Profit": -106500},
        {"Month": "October", "Sales": 0, "Net Profit": -106500},
        {"Month": "November", "Sales": 0, "Net Profit": -106500},
        {"Month": "December", "Sales": 0, "Net Profit": -106500},
    ]
    st.dataframe(pd.DataFrame(months_data), use_container_width=True)


# ==========================================
# 2. ADMIN DASHBOARD
# ==========================================
elif menu_selection == "Admin Dashboard":
    check_clearance(["Super Admin", "Admin"])
    st.title("🔐 Admin Executive Dashboard")
    st.caption("Comprehensive operational control interface including raw analytics.")
    
    st.markdown("### 🎛️ Strategic ERP Operations Panel")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Capital Raised", f"{total_capital:,.0f} BDT")
    m2.metric("Setup Asset Cost", f"{total_setup_cost:,.0f} BDT")
    m3.metric("Remaining Liquidity", f"{remaining_liquidity:,.0f} BDT")
    m4.metric("Net Profit / Loss", f"{net_profit:,.0f} BDT")

    m5, m6, m7, m8 = st.columns(4)
    tot_rice = st.session_state.inventory["Rice"]["opening"] + st.session_state.inventory["Rice"]["purchase"] - st.session_state.inventory["Rice"]["used"]
    tot_meat = st.session_state.inventory["Beef"]["opening"] + st.session_state.inventory["Beef"]["purchase"] - st.session_state.inventory["Beef"]["used"]
    m5.metric("Total Rice Stock", f"{tot_rice} kg")
    m6.metric("Total Meat Stock (Beef)", f"{tot_meat} kg")
    m7.metric("Monthly Fixed Cost", f"{fixed_overhead:,.0f} BDT")
    m8.metric("Monthly Variable Cost", f"{june_variable:,.0f} BDT")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Sales Revenue Stream Tracking")
        df_sales = pd.DataFrame(st.session_state.sales_log)
        fig_sales = px.bar(df_sales, x="date", y="amount", color="product", title="Daily Sales Composition Data")
        st.plotly_chart(fig_sales, use_container_width=True)
    with c2:
        st.markdown("#### ⚠️ Low Inventory Material Warnings")
        low_stock_items = []
        for k, v in st.session_state.inventory.items():
            bal = v['opening'] + v['purchase'] - v['used']
            if bal <= v['reorder']:
                low_stock_items.append({"Material Item": k, "Current Bal": bal, "Reorder Trigger Level": v['reorder'], "Unit": v['unit']})
        if low_stock_items:
            st.warning("Immediate Purchase Order/Reorder required for items listed below:")
            st.table(pd.DataFrame(low_stock_items))
        else:
            st.success("All raw materials storage profiles are healthy above reorder thresholds.")


# ==========================================
# 3. PARTNER MANAGEMENT
# ==========================================
elif menu_selection == "Partner Management":
    check_clearance(["Super Admin", "Admin"])
    st.title("👥 Partner Capital Investment & Equity Structure")
    
    df_partners = pd.DataFrame(st.session_state.partners)
    st.dataframe(df_partners, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ Equity Adjustments Management Controls")
    
    with st.expander("➕ Register New Entering Capital Partner"):
        with st.form("Add Partner Form"):
            name = st.text_input("New Partner Name")
            investment = st.number_input("Capital Investment Fund Amount (BDT)", min_value=0.0, step=10000.0)
            submit = st.form_submit_button("Submit & Recalculate Share")
            if submit and name:
                st.session_state.partners.append({"name": name, "investment": investment, "share": 0.0})
                # Recalculate equity automatically
                t_cap = sum(p['investment'] for p in st.session_state.partners)
                for p in st.session_state.partners:
                    p['share'] = round((p['investment'] / t_cap) * 100, 2)
                st.success(f"Partner {name} enrolled successfully. Capital base altered.")
                st.rerun()

    with st.expander("💸 Capital Infusion or Emergency Withdrawal"):
        p_names = [p['name'] for p in st.session_state.partners]
        selected_p = st.selectbox("Select Partner Profile", p_names)
        action_type = st.radio("Transaction Type Direction", ["Investment Increase (+)", "Capital Withdrawal (-)"])
        delta_amount = st.number_input("Transaction Volume Amount (BDT)", min_value=0.0, step=5000.0)
        if st.button("Authorize Ledger Transaction"):
            for p in st.session_state.partners:
                if p['name'] == selected_p:
                    if action_type == "Investment Increase (+)":
                        p['investment'] += delta_amount
                    else:
                        p['investment'] -= delta_amount
            # Automatic recalculation run
            t_cap = sum(p['investment'] for p in st.session_state.partners)
            for p in st.session_state.partners:
                p['share'] = round((p['investment'] / t_cap) * 100, 2)
            st.success("Capital allocation ledger updated instantly.")
            st.rerun()


# ==========================================
# 4. FIXED ASSETS REGISTER
# ==========================================
elif menu_selection == "Fixed Assets Register":
    check_clearance(["Super Admin", "Admin", "Manager"])
    st.title("📁 Fixed Investment Expenses & Startup Assets Register")
    
    df_assets = pd.DataFrame(st.session_state.assets)
    st.dataframe(df_assets, use_container_width=True)
    st.info(f"**Total Capital Value Bound in Fixed CapEx Assets:** {total_setup_cost:,.2f} BDT")
    
    st.markdown("---")
    st.markdown("### 🛠️ Asset Accounting Action Panel")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Register Capital Outlay Asset Item")
        with st.form("Asset Form"):
            asset_name = st.text_input("Asset Item Description")
            asset_cost = st.number_input("Procurement System Cost (BDT)", min_value=0.0, step=1000.0)
            if st.form_submit_button("Log Asset to Ledger"):
                if asset_name:
                    st.session_state.assets.append({"item": asset_name, "cost": asset_cost})
                    st.success(f"Logged asset asset register updated.")
                    st.rerun()
    with col2:
        st.markdown("#### Deprecate / Dispose Asset Account")
        del_asset = st.selectbox("Select Asset Entry", options=[a['item'] for a in st.session_state.assets])
        if st.button("De-register / Liquidate Selected Asset"):
            st.session_state.assets = [a for a in st.session_state.assets if a['item'] != del_asset]
            st.success("Asset profile eliminated from balance tracking sheets.")
            st.rerun()


# ==========================================
# 5. INVENTORY MANAGEMENT
# ==========================================
elif menu_selection == "Inventory Management":
    check_clearance(["Super Admin", "Admin", "Manager"])
    st.title("🗄️ Raw Material Master & Stock Ledger Logs")
    
    inv_records = []
    for k, v in st.session_state.inventory.items():
        bal = v['opening'] + v['purchase'] - v['used']
        inv_records.append({
            "Item Name": k,
            "Opening Stock": v['opening'],
            "Purchased Addition": v['purchase'],
            "Used / Consumed": v['used'],
            "Current Balance": bal,
            "Reorder Minimum Level": v['reorder'],
            "Unit Scale": v['unit'],
            "Alert Trigger": "⚠️ REORDER NOW" if bal <= v['reorder'] else "🟢 Healthy"
        })
    df_inv = pd.DataFrame(inv_records)
    st.dataframe(df_inv, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🛒 Daily Variable Bazar Purchases Logging")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("#### Registered Bazar Vouchers Ledger")
        st.dataframe(pd.DataFrame(st.session_state.bazar_expenses), use_container_width=True)
    with c2:
        st.markdown("#### Log Fresh Material Bazar Outflow")
        with st.form("Bazar Voucher Form"):
            b_item = st.text_input("Expense Description / Item details")
            b_amt = st.number_input("Bazar Bill Cost (BDT)", min_value=0.0, step=500.0)
            b_cat = st.selectbox("Bazar Category", ["Meat", "Groceries", "Spices/Veg", "Beverage", "Overheads"])
            if st.form_submit_button("Post Bazar Expense"):
                if b_item:
                    st.session_state.bazar_expenses.append({
                        "date": datetime.today().strftime('%Y-%m-%d'),
                        "item": b_item,
                        "amount": b_amt,
                        "category": b_cat
                    })
                    st.success("Outflow transaction posted successfully.")
                    st.rerun()


# ==========================================
# 6. POS BILLING & SALES LOG
# ==========================================
elif menu_selection == "POS Billing & Sales Log":
    check_clearance(["Super Admin", "Admin", "Manager", "Cashier"])
    st.title("⚡ POS Billing Counter Terminal & Sales Logs")
    
    tab1, tab2 = st.tabs(["🛒 Quick POS Cashier Interface", "📋 Historic Invoice Transaction Logs"])
    
    with tab1:
        st.markdown("### Generate Fresh Invoice Customer Order")
        c1, c2 = st.columns(2)
        with c1:
            menu_options = {m['item']: m['price'] for m in st.session_state.menu}
            selected_item = st.selectbox("Select Menu Dish Item Ordered", list(menu_options.keys()))
            unit_price = menu_options[selected_item]
            st.info(f"Standard Menu Retail Rate: **{unit_price} BDT**")
            
            qty = st.number_input("Order Quantity Units", min_value=1, value=1, step=1)
            payment_mod = st.selectbox("Payment Gateway Channel", ["Cash", "Bkash", "Nagad", "Card"])
            
        with c2:
            st.markdown("#### Live Invoice Summary Billing Calculation")
            subtotal = unit_price * qty
            vat_opt = st.checkbox("Apply Official Food VAT (5%)")
            discount = st.number_input("Discount Deductions Applied (BDT)", min_value=0.0, value=0.0)
            
            vat_amt = round(subtotal * 0.05, 2) if vat_opt else 0.0
            grand_total = subtotal + vat_amt - discount
            
            st.code(f"""
            ==================================
              BIRYANI SHOP ERP POS INVOICE
            ==================================
            Item Ordered: {selected_item}
            Quantity:     {qty} Pcs
            Subtotal:     {subtotal:,.2f} BDT
            VAT (5%):     {vat_amt:,.2f} BDT
            Discounts:   -{discount:,.2f} BDT
            ----------------------------------
            GRAND TOTAL:  {grand_total:,.2f} BDT
            ==================================
            """)
            
            if st.button("🖨️ Commit Sale Order & Print Receipt"):
                inv_id = f"INV-{len(st.session_state.sales_log) + 1:03d}"
                st.session_state.sales_log.append({
                    "invoice": inv_id,
                    "date": datetime.today().strftime('%Y-%m-%d'),
                    "product": selected_item,
                    "qty": qty,
                    "amount": grand_total,
                    "payment": payment_mod
                })
                st.success(f"Sale Committed Successfully! Generated Order Record {inv_id}")
                st.rerun()

    with tab2:
        st.markdown("### Historic Audit Master Log Table")
        st.dataframe(pd.DataFrame(st.session_state.sales_log), use_container_width=True)


# ==========================================
# 7. FINANCIAL & ANALYTICAL REPORTS
# ==========================================
elif menu_selection == "Financial & Analytical Reports":
    check_clearance(["Super Admin", "Admin", "Partner (View Only)"])
    st.title("📊 BI Analytics Center & Financial Statements Report Module")
    
    st.markdown("### 📈 Comprehensive Operating Trend Insights")
    
    r1, r2 = st.columns(2)
    with r1:
        # Visual breakdown chart of bazar costs
        df_baz = pd.DataFrame(st.session_state.bazar_expenses)
        if not df_baz.empty:
            fig_pie = px.pie(df_baz, values='amount', names='category', hole=0.4, title="Variable Procurement Expense Categorization")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No variable data for plotting charts.")
            
    with r2:
        # Dynamic calculation metrics visual tracking gage
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = net_profit,
            title = {'text': "Current Operating Net Income (June BDT)"},
            gauge = {
                'axis': {'range': [-150000, 150000]},
                'bar': {'color': "red" if net_profit < 0 else "green"},
                'steps': [
                    {'range': [-150000, 0], 'color': "lavender"},
                    {'range': [0, 150000], 'color': "honeydew"}
                ],
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Downloadable Statements Engine & Exports")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Official P&L Statement Snapshot")
        pl_report = pd.DataFrame([
            {"Line Item Structure Description": "Gross Retail Sales Revenue", "June Financial Metric Total (BDT)": june_sales},
            {"Line Item Structure Description": "Less: Variable Bazar Raw Materials Outlays", "June Financial Metric Total (BDT)": -june_variable},
            {"Line Item Structure Description": "Less: Fixed Operational Overheads & Rent", "June Financial Metric Total (BDT)": -fixed_overhead},
            {"Line Item Structure Description": "Net Net-Profit Retained Income Allocation", "June Financial Metric Total (BDT)": net_profit}
        ])
        st.table(pl_report)
    with col_b:
        st.subheader("Partner Current Equity Matrix Status")
        cap_report = []
        for p in st.session_state.partners:
            allocated_share_loss = round((p['investment'] / total_capital) * net_profit, 2)
            cap_report.append({
                "Partner": p['name'],
                "Initial Capital": p['investment'],
                "Equity Share %": f"{(p['investment']/total_capital)*100:.2f}%",
                "June Payout Status": allocated_share_loss
            })
        st.table(pd.DataFrame(cap_report))