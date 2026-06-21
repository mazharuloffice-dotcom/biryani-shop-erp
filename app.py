import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", page_icon="🍲", layout="wide")

# ----------------------------------------------------------------------------------
# 1. INITIALIZING DATABASE STATES (Session States)
# ----------------------------------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "superadmin": {"password": "123", "role": "Super Admin"},
        "admin": {"password": "456", "role": "Admin"},
        "partner": {"password": "789", "role": "Partner (View Only)"}
    }

if 'menu_items' not in st.session_state:
    st.session_state.menu_items = ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"]

if 'partners_db' not in st.session_state:
    st.session_state.partners_db = pd.DataFrame([
        {"Partner Name": "Foishal", "Investment Amount": 100000.0},
        {"Partner Name": "Anam", "Investment Amount": 100000.0},
        {"Partner Name": "Habib", "Investment Amount": 100000.0},
        {"Partner Name": "Anayat", "Investment Amount": 100000.0}
    ])

if 'fixed_expenses' not in st.session_state:
    st.session_state.fixed_expenses = pd.DataFrame([
        {"Expense Date": "2026-06-01", "Category": "Shop Rent", "Asset/Cost Item": "Advance & Rent", "Amount": 30000.0},
        {"Expense Date": "2026-06-01", "Category": "Startup Assets", "Asset/Cost Item": "Degh, Spoon & Kitchen Tools", "Amount": 25000.0},
        {"Expense Date": "2026-06-01", "Category": "Startup Assets", "Asset/Cost Item": "Decoration & Signboard", "Amount": 15000.0}
    ])

if 'variable_bazar' not in st.session_state:
    st.session_state.variable_bazar = pd.DataFrame(columns=["Date", "Bazar Item Name", "Quantity/Weight", "Total Cost (BDT)", "Purchased By"])

if 'sales_records' not in st.session_state:
    st.session_state.sales_records = pd.DataFrame(columns=["Date", "Item Name", "Rate per Plate", "Total Plates", "Adjustment", "Net Total"])

if 'inventory_db' not in st.session_state:
    st.session_state.inventory_db = pd.DataFrame([
        {"Material Name": "Miniket Rice", "Current Stock": 150.0, "Unit": "Kg", "Alert Level": 30.0},
        {"Material Name": "Beef Meat", "Current Stock": 45.0, "Unit": "Kg", "Alert Level": 15.0},
        {"Material Name": "Polao Rice", "Current Stock": 80.0, "Unit": "Kg", "Alert Level": 20.0},
        {"Material Name": "Soyabean Oil", "Current Stock": 60.0, "Unit": "Ltr", "Alert Level": 12.0}
    ])

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ----------------------------------------------------------------------------------
# 2. SECURE AUTHENTICATION SYSTEM
# ----------------------------------------------------------------------------------
if st.session_state.logged_in_user is None:
    st.markdown("<h2 style='text-align: center;'>🍲 Swapnajatra Biryani Bari ERP 🍲</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Unified Business & Financial Management System</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username / ID").strip().lower()
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In Securely"):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.rerun()
                else:
                    st.error("❌ Access Denied: Invalid Authentication Credentials.")
    st.stop()

# Sidebar Controls
st.sidebar.title("🔒 Security Control")
st.sidebar.write(f"**Active User:** {st.session_state.logged_in_user.capitalize()}")
st.sidebar.write(f"**Access Role:** {st.session_state.user_role}")
if st.sidebar.button("Logout 🚪"):
    st.session_state.logged_in_user = None
    st.session_state.user_role = None
    st.rerun()

is_admin = st.session_state.user_role in ["Super Admin", "Admin"]
is_superadmin = st.session_state.user_role == "Super Admin"
is_partner = st.session_state.user_role == "Partner (View Only)"

st.sidebar.markdown("---")
st.sidebar.title("📁 ERP System Navigation")
menu_options = ["📊 Financial Dashboard", "🤝 Partner Capital Engine", "💰 Daily Sales Entry", "🛒 Variable Bazar Cost", "📦 Inventory Control & Alert"]
if is_admin:
    menu_options.append("⚙️ Dropdown Menu Admin")
if is_superadmin:
    menu_options.append("👥 System User Provisioning")
choice = st.sidebar.radio("Navigate to module:", menu_options)

# ----------------------------------------------------------------------------------
# GLOBAL FINANCIAL ENGINE CALCULATIONS
# ----------------------------------------------------------------------------------
total_investments = st.session_state.partners_db["Investment Amount"].sum()
total_sales = st.session_state.sales_records["Net Total"].sum() if len(st.session_state.sales_records) > 0 else 0.0
total_fixed_expenses = st.session_state.fixed_expenses["Amount"].sum() if len(st.session_state.fixed_expenses) > 0 else 0.0
total_bazar_expenses = st.session_state.variable_bazar["Total Cost (BDT)"].sum() if len(st.session_state.variable_bazar) > 0 else 0.0
total_expenditure = total_fixed_expenses + total_bazar_expenses
net_profit_loss = total_sales - total_expenditure

# ----------------------------------------------------------------------------------
# MODULE 1: FINANCIAL DASHBOARD & REPORTS (Monthly P&L, Partner Payouts)
# ----------------------------------------------------------------------------------
if choice == "📊 Financial Dashboard":
    st.title("📊 Enterprise Financial Analytics & Dashboards")
    
    # Financial KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Sales Revenue", f"{total_sales:,.2f} BDT")
    kpi2.metric("Total Operational Outflow", f"{total_expenditure:,.2f} BDT")
    kpi3.metric("Net P&L (Current Month)", f"{net_profit_loss:,.2f} BDT", delta=f"{net_profit_loss:,.2f} BDT")
    kpi4.metric("Total Startup Capital Base", f"{total_investments:,.2f} BDT")
    
    st.markdown("---")
    
    # Chart.js style Interactive Charts via Plotly
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("### 📈 Revenue vs Expenses Breakdown")
        fig_summary = go.Figure(data=[
            go.Bar(name='Inflow (Sales)', x=['Financial Overview'], y=[total_sales], marker_color='#2ecc71'),
            go.Bar(name='Outflow (Total Costs)', x=['Financial Overview'], y=[total_expenditure], marker_color='#e74c3c')
        ])
        fig_summary.update_layout(barmode='group', height=300)
        st.plotly_chart(fig_summary, use_container_width=True)
        
    with chart_col2:
        st.markdown("### 📉 Expense Category Breakdown")
        if total_expenditure > 0:
            fig_pie = px.pie(values=[total_fixed_expenses, total_bazar_expenses], names=['Fixed/Startup Expenses', 'Daily Variable Bazar'], color_discrete_sequence=['#3498db', '#f1c40f'])
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenditures recorded to display charts.")

    # Monthly P&L Ledger Statement
    st.markdown("---")
    st.markdown("### 📅 Monthly Profit & Loss (P&L) Ledger Statement")
    pl_data = {
        "Financial Line Item Statement": ["Total Sales Revenue Inflow (+)", "Fixed Investment Expenses & Assets (-)", "Daily Variable Bazar Expenses (-)", "Net Operating Balance (P&L)"],
        "Amount (BDT)": [f"{total_sales:,.2f}", f"{total_fixed_expenses:,.2f}", f"{total_bazar_expenses:,.2f}", f"{net_profit_loss:,.2f}"]
    }
    st.table(pd.DataFrame(pl_data))

    # Profit Sharing Engine & Partner Payout Reports
    st.markdown("---")
    st.markdown("### 💰 Profit Sharing Engine & Partner Payout Reports")
    df_payout = st.session_state.partners_db.copy()
    if total_investments > 0:
        df_payout["Investment Share (%)"] = (df_payout["Investment Amount"] / total_investments) * 100
        # If profit is negative, payout is 0 or distributed loss risk
        df_payout["Calculated P&L Share (BDT)"] = (df_payout["Investment Share (%)"] / 100) * net_profit_loss
        
        # Display Formatting
        df_disp = df_payout.copy()
        df_disp["Investment Amount"] = df_disp["Investment Amount"].map("{:,.2f} BDT".format)
        df_disp["Investment Share (%)"] = df_disp["Investment Share (%)"].map("{:.2f}%".format)
        df_disp["Calculated P&L Share (BDT)"] = df_disp["Calculated P&L Share (BDT)"].map("{:,.2f} BDT".format)
        st.dataframe(df_disp, use_container_width=True)
    else:
        st.warning("No capital configuration detected to execute profit sharing algorithms.")

# ----------------------------------------------------------------------------------
# MODULE 2: PARTNER CAPITAL ENGINE & FIXED INVESTMENT
# ----------------------------------------------------------------------------------
elif choice == "🤝 Partner Capital Engine":
    st.title("🤝 Capital Structure & Fixed Startup Investment Assets")
    
    tab1, tab2 = st.tabs(["Partner Equity Registration", "Fixed Capital Investment & Assets"])
    
    with tab1:
        st.markdown("### 📋 Current Active Equity Partners")
        st.dataframe(st.session_state.partners_db, use_container_width=True)
        
        if not is_partner:
            st.markdown("#### ➕ Add / Update Partner Capital Contribution")
            with st.form("partner_equity_form", clear_on_submit=True):
                p_name = st.text_input("Partner Full Name").strip()
                p_amount = st.number_input("Investment Amount Capital (BDT)", min_value=0.0, step=5000.0, value=25000.0)
                if st.form_submit_button("Commit Investment Capital"):
                    if p_name:
                        df_p = st.session_state.partners_db
                        if p_name in df_p["Partner Name"].values:
                            df_p.loc[df_p["Partner Name"] == p_name, "Investment Amount"] += p_amount
                            st.success(f"Successfully appended capital structure for {p_name}.")
                        else:
                            new_p = pd.DataFrame([{"Partner Name": p_name, "Investment Amount": p_amount}])
                            st.session_state.partners_db = pd.concat([df_p, new_p], ignore_index=True)
                            st.success(f"Registered brand new partner: '{p_name}'.")
                        st.rerun()
                    else:
                        st.error("Partner Identity context is invalid.")
                        
    with tab2:
        st.markdown("### 📋 Fixed Setup Investment Assets & Startup Expenditures Ledger")
        st.dataframe(st.session_state.fixed_expenses, use_container_width=True)
        
        if not is_partner:
            st.markdown("#### ➕ Record New Fixed Asset / Setup Cost Entry")
            with st.form("fixed_cost_form", clear_on_submit=True):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    exp_cat = st.selectbox("Expense Category Classification", ["Shop Rent", "Startup Assets", "Utility Installation", "Legal/Licenses"])
                    exp_item = st.text_input("Asset / Cost Particulars Description (e.g. Signboard, Tables, Oven)").strip()
                with col_e2:
                    exp_amt = st.number_input("Cost Allocation Amount (BDT)", min_value=0.0, step=1000.0, value=5000.0)
                    exp_date = st.date_input("Deployment Expenditure Date", datetime.now())
                if st.form_submit_button("Record Fixed/Asset Entry"):
                    if exp_item:
                        new_fix = pd.DataFrame([{"Expense Date": exp_date.strftime("%Y-%m-%d"), "Category": exp_cat, "Asset/Cost Item": exp_item, "Amount": exp_amt}])
                        st.session_state.fixed_expenses = pd.concat([st.session_state.fixed_expenses, new_fix], ignore_index=True)
                        st.success(f"Fixed asset / structural expense successfully recorded.")
                        st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 3: DAILY SALES ENTRY
# ----------------------------------------------------------------------------------
elif choice == "💰 Daily Sales Entry":
    st.title("💰 High-Frequency Daily Item-Wise Sales Entry Module")
    
    if is_partner:
        st.error("🚫 Security Authorization failure: View-Only roles restricted from data logging.")
    else:
        with st.form("sales_log_form", clear_on_submit=True):
            st.markdown("### Record Point of Sale Log Record")
            sel_item = st.selectbox("Product Dropdown Selection Base", st.session_state.menu_items)
            
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                rate = st.number_input("Rate Per Plate Unit (BDT)", min_value=0.0, step=5.0, value=220.0)
            with sc2:
                qty = st.number_input("Total Unit Plate Sales Volume count", min_value=1, step=1, value=20)
            with sc3:
                adj = st.number_input("Discount / Adjustment Offset (+/- BDT)", step=5.0, value=0.0)
                
            s_date = st.date_input("Transaction Ledger Date Context", datetime.now())
            net_comp = (rate * qty) + adj
            st.markdown(f"**Calculated Invoice Net Value Flow Summary:** `{net_comp:,.2f} BDT`")
            
            if st.form_submit_button("Publish Sales Log Entry"):
                new_sale = pd.DataFrame([{"Date": s_date.strftime("%Y-%m-%d"), "Item Name": sel_item, "Rate per Plate": rate, "Total Plates": qty, "Adjustment": adj, "Net Total": net_comp}])
                st.session_state.sales_records = pd.concat([st.session_state.sales_records, new_sale], ignore_index=True)
                st.success(f"Transaction journal entry created for product: {sel_item}.")

# ----------------------------------------------------------------------------------
# MODULE 4: DAILY VARIABLE BAZAR EXPENSES
# ----------------------------------------------------------------------------------
elif choice == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Variable Material Bazar Expenses Journal")
    
    st.markdown("### 📋 Raw Material Sourcing & Bazar Outflow Records")
    st.dataframe(st.session_state.variable_bazar, use_container_width=True)
    
    if is_partner:
        st.info("ℹ️ Account restriction: Partner accounts hold view-only access matrix privileges.")
    else:
        st.markdown("---")
        st.markdown("### ➕ Input Raw Variable Material Purchasing Log")
        with st.form("bazar_variable_form", clear_on_submit=True):
            bc1, bc2 = st.columns(2)
            with bc1:
                b_name = st.text_input("Material Item Description (e.g. Onion, Beef Sourcing, Spices, Ghee)").strip()
                b_qty = st.text_input("Quantity Metric (e.g. 5 Kg, 2 Litres, 1 Bundle)")
            with bc2:
                b_cost = st.number_input("Total Bazar Outflow Invoiced Cost (BDT)", min_value=0.0, step=50.0, value=500.0)
                b_date = st.date_input("Market Transaction Sourcing Date", datetime.now())
                
            if st.form_submit_button("Commit Bazar Cost Entry"):
                if b_name:
                    new_bazar = pd.DataFrame([{"Date": b_date.strftime("%Y-%m-%d"), "Bazar Item Name": b_name, "Quantity/Weight": b_qty, "Total Cost (BDT)": b_cost, "Purchased By": st.session_state.logged_in_user.capitalize()}])
                    st.session_state.variable_bazar = pd.concat([st.session_state.variable_bazar, new_bazar], ignore_index=True)
                    st.success("Variable bazar cost ledger item safely recorded.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 5: INVENTORY REPORTS & STOCK ALERTS
# ----------------------------------------------------------------------------------
elif choice == "📦 Inventory Control & Alert":
    st.title("📦 Live Raw Material Inventory Ledger & Auto Alerts")
    
    st.markdown("### 📊 Material Inventory Stock Matrix Summary")
    
    df_inv = st.session_state.inventory_db.copy()
    
    # Custom Function to flag system stock warnings
    def check_alert(row):
        if row["Current Stock"] <= row["Alert Level"]:
            return "🚨 LOW STOCK CRITICAL ALERT"
        return "✅ Operational Stock Level Optimal"
        
    df_inv["System Status Code"] = df_inv.apply(check_alert, axis=1)
    st.dataframe(df_inv, use_container_width=True)
    
    # Highlight Critical Status Alerts
    critical_items = df_inv[df_inv["Current Stock"] <= df_inv["Alert Level"]]
    if len(critical_items) > 0:
        for idx, row in critical_items.iterrows():
            st.error(f"**🚨 Stock Critical Shortage Notification:** '{row['Material Name']}' inventory depth is down to **{row['Current Stock']} {row['Unit']}** (Configured Buffer Matrix Warning Level threshold is {row['Alert Level']} {row['Unit']}). Please reorder immediately!")

    if not is_partner:
        st.markdown("---")
        st.markdown("### 🔄 Restock / Update Raw Material Asset Volume Allocation")
        with st.form("inventory_update_form", clear_on_submit=True):
            inv_sel = st.selectbox("Select Target Raw Inventory Item", df_inv["Material Name"].values)
            inv_add = st.number_input("Inward Supply Stock Volume Delta Additions (+ Quantity)", min_value=0.0, step=5.0, value=10.0)
            if st.form_submit_button("Recompute Inventory Balances"):
                st.session_state.inventory_db.loc[st.session_state.inventory_db["Material Name"] == inv_sel, "Current Stock"] += inv_add
                st.success(f"System inventory pipeline restocked for raw materials asset item '{inv_sel}'.")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 6: ADMIN DROPDOWN SETTINGS
# ----------------------------------------------------------------------------------
elif choice == "⚙️ Dropdown Menu Admin":
    st.title("⚙️ Dropdown Menu Item Infrastructure Maintenance")
    st.write("Current Dropdown Menu Items:", st.session_state.menu_items)
    
    st.markdown("### ➕ Create New Menu Product Variant")
    new_prod = st.text_input("Enter Product Variant Name String").strip()
    if st.button("Save New Product Variant"):
        if new_prod and new_prod not in st.session_state.menu_items:
            st.session_state.menu_items.append(new_prod)
            st.success(f"Product '{new_prod}' appended into global dropdown arrays.")
            st.rerun()
            
    st.markdown("### ✏️ Rename Active Drodown Asset Item")
    old_prod = st.selectbox("Select Existing Registered Product Target", st.session_state.menu_items)
    ren_prod = st.text_input("Enter New Name String Context Value", value=old_prod).strip()
    if st.button("Apply Structural Refactor"):
        if ren_prod and ren_prod != old_prod:
            idx = st.session_state.menu_items.index(old_prod)
            st.session_state.menu_items[idx] = ren_prod
            st.success("Menu array structure successfully refactored.")
            st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 7: USER PROVISIONING MANAGEMENT (Super Admin Only)
# ----------------------------------------------------------------------------------
elif choice == "👥 System User Provisioning":
    st.title("👥 Corporate System IAM & User Security Access Control Matrix")
    
    users_list_df = pd.DataFrame([
        {"System ID Login": k, "Privilege Classification Matrix": v["role"], "Password Security Token": v["password"]} 
        for k, v in st.session_state.users_db.items()
    ])
    st.dataframe(users_list_df, use_container_width=True)
    
    st.markdown("### ➕ Create/Provision New Dynamic System Identity Profile Access")
    with st.form("iam_provisioning_form"):
        u_id = st.text_input("Desired Unique ID String User context").strip().lower()
        u_pass = st.text_input("Secure String Authentication Token Pass", type="password")
        u_rol = st.selectbox("Access Privilege Structural Role Allocation Matrix", ["Super Admin", "Admin", "Partner (View Only)"])
        if st.form_submit_button("Commit Identity Provisioning Request"):
            if u_id and u_pass:
                st.session_state.users_db[u_id] = {"password": u_pass, "role": u_rol}
                st.success(f"System profile identifier access context provisioning for user '{u_id}' complete.")
                st.rerun()