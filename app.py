import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Page Configuration
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", page_icon="🍲", layout="wide")

# ----------------------------------------------------------------------------------
# 1. DYNAMIC DATABASE INITIALIZATION (Session States)
# ----------------------------------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "superadmin": {"password": "123", "role": "Super Admin"},
        "admin": {"password": "456", "role": "Admin"},
        "partner": {"password": "789", "role": "Partner (View Only)"}
    }

# Dynamic Dropdown Arrays
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"]
if 'partner_list' not in st.session_state:
    st.session_state.partner_list = ["Foishal", "Anam", "Habib", "Anayat"]
if 'asset_categories' not in st.session_state:
    st.session_state.asset_categories = ["Shop Rent", "Startup Assets", "Utility Installation", "Legal/Licenses"]
if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = ["Electricity Bill", "Gas/Wood Bill", "Waste Management", "Marketing", "Others"]

# Master Data Tables
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
        {"Expense Date": "2026-06-01", "Category": "Startup Assets", "Asset/Cost Item": "Degh, Spoon & Kitchen Tools", "Amount": 25000.0}
    ])

if 'monthly_expenses_db' not in st.session_state:
    st.session_state.monthly_expenses_db = pd.DataFrame(columns=["Date", "Category", "Particulars", "Amount (BDT)"])

if 'variable_bazar' not in st.session_state:
    st.session_state.variable_bazar = pd.DataFrame(columns=["Date", "Bazar Item Name", "Quantity/Weight", "Total Cost (BDT)", "Purchased By"])

if 'sales_records' not in st.session_state:
    st.session_state.sales_records = pd.DataFrame(columns=["Date", "Item Name", "Rate per Plate", "Total Plates", "Adjustment", "Net Total"])

if 'salary_db' not in st.session_state:
    st.session_state.salary_db = pd.DataFrame(columns=["Date", "Staff Name", "Designation", "Salary Type", "Amount Paid (BDT)"])

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
    st.markdown("<h4 style='text-align: center; color: gray;'>Unified Business Management & Automated Profit Sharing Engine</h4>", unsafe_allow_html=True)
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

# Sidebar Control Center
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
st.sidebar.title("📁 ERP Navigation")
menu_options = [
    "📊 Financial Dashboard", 
    "📈 Date-Wise Report Manager",
    "🤝 Partner Capital Engine", 
    "💰 Daily Sales Entry", 
    "🛒 Variable Bazar Cost", 
    "💼 Monthly Expenses",
    "🧑‍🍳 Staff Salary Ledger",
    "📦 Inventory & Restock"
]
if is_admin:
    menu_options.append("⚙️ Dropdown Control Panel")
if is_superadmin:
    menu_options.append("👥 System User Provisioning")
choice = st.sidebar.radio("Navigate to module:", menu_options)

# ----------------------------------------------------------------------------------
# GLOBAL FINANCIAL AUTO CALCULATION ENGINE
# ----------------------------------------------------------------------------------
total_investments = st.session_state.partners_db["Investment Amount"].sum()
total_sales = st.session_state.sales_records["Net Total"].sum() if len(st.session_state.sales_records) > 0 else 0.0
total_fixed_expenses = st.session_state.fixed_expenses["Amount"].sum() if len(st.session_state.fixed_expenses) > 0 else 0.0
total_bazar_expenses = st.session_state.variable_bazar["Total Cost (BDT)"].sum() if len(st.session_state.variable_bazar) > 0 else 0.0
total_monthly_expenses = st.session_state.monthly_expenses_db["Amount (BDT)"].sum() if len(st.session_state.monthly_expenses_db) > 0 else 0.0
total_salary_expenses = st.session_state.salary_db["Amount Paid (BDT)"].sum() if len(st.session_state.salary_db) > 0 else 0.0

total_outflow = total_fixed_expenses + total_bazar_expenses + total_monthly_expenses + total_salary_expenses
net_profit_loss = total_sales - total_outflow

# ----------------------------------------------------------------------------------
# MODULE 1: FINANCIAL DASHBOARD
# ----------------------------------------------------------------------------------
if choice == "📊 Financial Dashboard":
    st.title("📊 Enterprise Financial Analytics & Dashboards")
    
    # Financial KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Sales Revenue", f"{total_sales:,.2f} BDT")
    kpi2.metric("Total Expenses Outflow", f"{total_outflow:,.2f} BDT")
    kpi3.metric("Net Profit / Loss", f"{net_profit_loss:,.2f} BDT", delta=f"{net_profit_loss:,.2f} BDT")
    kpi4.metric("Total Capital Base", f"{total_investments:,.2f} BDT")
    
    st.markdown("---")
    
    # Graphs Block
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown("### 📈 Cash Inflow vs Outflow")
        fig_summary = go.Figure(data=[
            go.Bar(name='Total Inflow (Sales)', x=['Financial Summary'], y=[total_sales], marker_color='#2ecc71'),
            go.Bar(name='Total Outflow (Costs)', x=['Financial Summary'], y=[total_outflow], marker_color='#e74c3c')
        ])
        fig_summary.update_layout(barmode='group', height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig_summary, use_container_width=True)
        
    with c_col2:
        st.markdown("### 📉 Expense Expense Type Distribution")
        if total_outflow > 0:
            fig_pie = px.pie(
                values=[total_fixed_expenses, total_bazar_expenses, total_monthly_expenses, total_salary_expenses], 
                names=['Fixed Assets', 'Daily Variable Bazar', 'Monthly Expenses', 'Staff Salaries'],
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig_pie.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data recorded to generate visualization.")

    # Master P&L Statement Table
    st.markdown("---")
    st.markdown("### 📅 Monthly Statement of Profit & Loss (P&L)")
    pl_data = {
        "Financial Line Item Particulars": [
            "Total Revenue Inflow from Sales (+)", 
            "Fixed Setup Investment & Startup Assets (-)", 
            "Daily Variable Bazar Sourcing Costs (-)", 
            "Regular Monthly Operating Expenses (-)",
            "Total Staff Salary Payouts (Daily + Monthly) (-)",
            "Net Operating Profit / Loss Balance"
        ],
        "Amount (BDT)": [
            f"{total_sales:,.2f}", 
            f"{total_fixed_expenses:,.2f}", 
            f"{total_bazar_expenses:,.2f}", 
            f"{total_monthly_expenses:,.2f}",
            f"{total_salary_expenses:,.2f}",
            f"{net_profit_loss:,.2f}"
        ]
    }
    st.table(pd.DataFrame(pl_data))

# ----------------------------------------------------------------------------------
# MODULE 2: DATE-WISE REPORT MANAGER (Admin & Partner View Only)
# ----------------------------------------------------------------------------------
elif choice == "📈 Date-Wise Report Manager":
    st.title("📈 Multi-Module Advanced Date-Range Report Manager")
    st.write("Filter transactions and export reports within custom time boundaries.")
    
    rep_tab1, rep_tab2, rep_tab3 = st.tabs(["Sales Revenue Reports", "Variable Bazar Expenses", "Staff Salary Reports"])
    
    with rep_tab1:
        st.markdown("### 🔍 Sales Filtering Engine")
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            sales_start = st.date_input("Sales From Date", date(2026, 1, 1), key="s_start")
        with r_col2:
            sales_end = st.date_input("Sales To Date", datetime.now().date(), key="s_end")
            
        if len(st.session_state.sales_records) > 0:
            df_s = st.session_state.sales_records.copy()
            df_s["Date"] = pd.to_datetime(df_s["Date"]).dt.date
            filtered_sales = df_s[(df_s["Date"] >= sales_start) & (df_s["Date"] <= sales_end)]
            
            st.metric("Filtered Net Sales Total", f"{filtered_sales['Net Total'].sum():,.2f} BDT")
            st.dataframe(filtered_sales, use_container_width=True)
        else:
            st.info("Sales ledger is empty.")
            
    with rep_tab2:
        st.markdown("### 🔍 Daily Variable Bazar Filtering Engine")
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            bazar_start = st.date_input("Bazar From Date", date(2026, 1, 1), key="b_start")
        with b_col2:
            bazar_end = st.date_input("Bazar To Date", datetime.now().date(), key="b_end")
            
        if len(st.session_state.variable_bazar) > 0:
            df_b = st.session_state.variable_bazar.copy()
            df_b["Date"] = pd.to_datetime(df_b["Date"]).dt.date
            filtered_bazar = df_b[(df_b["Date"] >= bazar_start) & (df_b["Date"] <= bazar_end)]
            
            st.metric("Filtered Total Bazar Cost", f"{filtered_bazar['Total Cost (BDT)'].sum():,.2f} BDT")
            st.dataframe(filtered_bazar, use_container_width=True)
        else:
            st.info("Bazar expense ledger is empty.")

    with rep_tab3:
        st.markdown("### 🔍 Salary Disbursement Logs")
        sal_col1, sal_col2 = st.columns(2)
        with sal_col1:
            sal_start = st.date_input("Salary From Date", date(2026, 1, 1), key="sal_start")
        with sal_col2:
            sal_end = st.date_input("Salary To Date", datetime.now().date(), key="sal_end")
            
        if len(st.session_state.salary_db) > 0:
            df_sal = st.session_state.salary_db.copy()
            df_sal["Date"] = pd.to_datetime(df_sal["Date"]).dt.date
            filtered_sal = df_sal[(df_sal["Date"] >= sal_start) & (df_sal["Date"] <= sal_end)]
            
            st.metric("Filtered Total Salary Disbursed", f"{filtered_sal['Amount Paid (BDT)'].sum():,.2f} BDT")
            st.dataframe(filtered_sal, use_container_width=True)
        else:
            st.info("Salary database is empty.")

# ----------------------------------------------------------------------------------
# MODULE 3: PARTNER CAPITAL ENGINE
# ----------------------------------------------------------------------------------
elif choice == "🤝 Partner Capital Engine":
    st.title("🤝 Partner Equity & Fixed Setup Capital Registry")
    
    t1, t2 = st.tabs(["Partner Capital Allocation Matrix", "Fixed Assets / Setup Cost Entry"])
    
    with t1:
        st.markdown("### 📋 Dynamic Ownership & Profit Sharing Engine")
        df_p = st.session_state.partners_db.copy()
        if total_investments > 0:
            df_p["Ownership Share (%)"] = (df_p["Investment Amount"] / total_investments) * 100
            df_p["Current Profit Share (BDT)"] = (df_p["Ownership Share (%)"] / 100) * net_profit_loss
            
            df_p_disp = df_p.copy()
            df_p_disp["Investment Amount"] = df_p_disp["Investment Amount"].map("{:,.2f} BDT".format)
            df_p_disp["Ownership Share (%)"] = df_p_disp["Ownership Share (%)"].map("{:.2f}%".format)
            df_p_disp["Current Profit Share (BDT)"] = df_p_disp["Current Profit Share (BDT)"].map("{:,.2f} BDT".format)
            st.dataframe(df_p_disp, use_container_width=True)
        else:
            st.dataframe(df_p, use_container_width=True)
            
        if not is_partner:
            st.markdown("#### ➕ Add / Update Partner Capital Contribution")
            with st.form("add_capital_form", clear_on_submit=True):
                # Partner Name selection from dynamic dropdown
                p_select = st.selectbox("Select Partner Name", st.session_state.partner_list)
                p_amt = st.number_input("Capital Injection Amount (BDT)", min_value=0.0, step=5000.0, value=10000.0)
                
                if st.form_submit_button("Commit Partner Capital Entry"):
                    df_master = st.session_state.partners_db
                    if p_select in df_master["Partner Name"].values:
                        df_master.loc[df_master["Partner Name"] == p_select, "Investment Amount"] += p_amt
                    else:
                        new_row = pd.DataFrame([{"Partner Name": p_select, "Investment Amount": p_amt}])
                        st.session_state.partners_db = pd.concat([df_master, new_row], ignore_index=True)
                    st.success(f"Capital updated for {p_select}!")
                    st.rerun()

    with t2:
        st.markdown("### 📋 Fixed Setup Assets Expenditures Journal")
        st.dataframe(st.session_state.fixed_expenses, use_container_width=True)
        
        if not is_partner:
            st.markdown("#### ➕ Record New Fixed Asset / Setup Cost Entry")
            with st.form("fixed_asset_form", clear_on_submit=True):
                # Category dropdown from dynamic settings
                f_cat = st.selectbox("Select Asset Category Class", st.session_state.asset_categories)
                f_item = st.text_input("Asset Item Description Particulars (e.g. Rice Cooker, Table, Fan)").strip()
                f_amt = st.number_input("Cost Value (BDT)", min_value=0.0, step=500.0, value=2000.0)
                f_date = st.date_input("Expenditure Ledger Date", datetime.now())
                
                if st.form_submit_button("Record Fixed Asset Entry"):
                    if f_item:
                        new_fa = pd.DataFrame([{"Expense Date": f_date.strftime("%Y-%m-%d"), "Category": f_cat, "Asset/Cost Item": f_item, "Amount": f_amt}])
                        st.session_state.fixed_expenses = pd.concat([st.session_state.fixed_expenses, new_fa], ignore_index=True)
                        st.success("Fixed cost safely committed to data ledger.")
                        st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 4: DAILY SALES ENTRY
# ----------------------------------------------------------------------------------
elif choice == "💰 Daily Sales Entry":
    st.title("💰 High-Frequency Daily Sales Intake Module")
    if is_partner:
        st.error("🚫 Security restriction: View-Only accounts cannot input sales data records.")
    else:
        with st.form("sales_form", clear_on_submit=True):
            s_item = st.selectbox("Product Selection Dropdown", st.session_state.menu_items)
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                s_rate = st.number_input("Rate Per Plate (BDT)", min_value=0.0, value=220.0, step=10.0)
            with sc2:
                s_qty = st.number_input("Total Plates Sold", min_value=1, value=10, step=1)
            with sc3:
                s_adj = st.number_input("Invoice Adjustment/Discount Allocation (+/- BDT)", value=0.0, step=5.0)
            s_date = st.date_input("Sales Record Date", datetime.now())
            
            net_calc = (s_rate * s_qty) + s_adj
            st.markdown(f"**Net Invoice Billing Total:** `{net_calc:,.2f} BDT`")
            
            if st.form_submit_button("Publish Sales Log"):
                new_s_log = pd.DataFrame([{"Date": s_date.strftime("%Y-%m-%d"), "Item Name": s_item, "Rate per Plate": s_rate, "Total Plates": s_qty, "Adjustment": s_adj, "Net Total": net_calc}])
                st.session_state.sales_records = pd.concat([st.session_state.sales_records, new_s_log], ignore_index=True)
                st.success("Sales record added securely.")

# ----------------------------------------------------------------------------------
# MODULE 5: DAILY VARIABLE BAZAR COST
# ----------------------------------------------------------------------------------
elif choice == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Variable Material Bazar Sourcing Records")
    st.dataframe(st.session_state.variable_bazar, use_container_width=True)
    
    if not is_partner:
        st.markdown("### ➕ Input Raw Variable Material Purchasing Log")
        with st.form("bazar_form", clear_on_submit=True):
            # Dynamic list from current active inventory matrix names
            inv_list = list(st.session_state.inventory_db["Material Name"].values) + ["Other Miscellaneous Items"]
            b_item = st.selectbox("Material Item Description Selection", inv_list)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                b_qty = st.text_input("Quantity Metric (e.g. 10 Kg, 5 Litres)")
            with col_b2:
                b_cost = st.number_input("Total Bazar Cost Paid (BDT)", min_value=0.0, step=100.0, value=1000.0)
            b_date = st.date_input("Market Transaction Date", datetime.now())
            
            if st.form_submit_button("Commit Bazar Cost Entry"):
                new_b = pd.DataFrame([{"Date": b_date.strftime("%Y-%m-%d"), "Bazar Item Name": b_item, "Quantity/Weight": b_qty, "Total Cost (BDT)": b_cost, "Purchased By": st.session_state.logged_in_user.capitalize()}])
                st.session_state.variable_bazar = pd.concat([st.session_state.variable_bazar, new_b], ignore_index=True)
                st.success("Bazar purchase cost added to ledger ledger state.")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 6: MONTHLY OPERATING EXPENSES
# ----------------------------------------------------------------------------------
elif choice == "💼 Monthly Expenses":
    st.title("💼 Operating Expenses Monthly Journal")
    st.dataframe(st.session_state.monthly_expenses_db, use_container_width=True)
    
    if not is_partner:
        st.markdown("### ➕ Record Monthly Expense Entry")
        with st.form("monthly_exp_form", clear_on_submit=True):
            # Expense Category from dynamic dropdown array state
            me_cat = st.selectbox("Select Expense Category", st.session_state.expense_categories)
            me_part = st.text_input("Particulars Details Memo (e.g. June Gas Bill payment, Facebook ad spend)").strip()
            me_amt = st.number_input("Total Paid Bill Amount (BDT)", min_value=0.0, step=100.0, value=1500.0)
            me_date = st.date_input("Payment Ledger Clearing Date", datetime.now())
            
            if st.form_submit_button("Log Operating Expense"):
                if me_part:
                    new_me = pd.DataFrame([{"Date": me_date.strftime("%Y-%m-%d"), "Category": me_cat, "Particulars": me_part, "Amount (BDT)": me_amt}])
                    st.session_state.monthly_expenses_db = pd.concat([st.session_state.monthly_expenses_db, new_me], ignore_index=True)
                    st.success("Operational expense logged successfully.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 7: STAFF SALARY MANAGEMENT (Daily / Monthly Tracking)
# ----------------------------------------------------------------------------------
elif choice == "🧑‍🍳 Staff Salary Ledger":
    st.title("🧑‍🍳 Human Resource Management & Staff Salary Tracking")
    st.dataframe(st.session_state.salary_db, use_container_width=True)
    
    if not is_partner:
        st.markdown("---")
        st.markdown("### ➕ Record Staff Salary Remuneration Payout")
        with st.form("salary_form", clear_on_submit=True):
            sal_name = st.text_input("Employee / Staff Name").strip()
            sal_desg = st.text_input("Staff Designation (e.g. Head Cook, Manager, Waiter, Cleaner)").strip()
            
            sc1, sc2 = st.columns(2)
            with sc1:
                sal_type = st.selectbox("Salary Distribution Type Matrix", ["Daily Wages Salary", "Monthly Regular Salary"])
            with sc2:
                sal_paid = st.number_input("Disbursed Amount Paid (BDT)", min_value=0.0, step=200.0, value=500.0)
            sal_date = st.date_input("Disbursement Operational Date", datetime.now())
            
            if st.form_submit_button("Log Salary Payroll Disbursed ✅"):
                if sal_name and sal_desg:
                    new_sal_row = pd.DataFrame([{"Date": sal_date.strftime("%Y-%m-%d"), "Staff Name": sal_name, "Designation": sal_desg, "Salary Type": sal_type, "Amount Paid (BDT)": sal_paid}])
                    st.session_state.salary_db = pd.concat([st.session_state.salary_db, new_sal_row], ignore_index=True)
                    st.success(f"Payroll record generated for employee '{sal_name}' safely.")
                    st.rerun()
                else:
                    st.error("Employee verification requires structural Name and Designation inputs.")

# ----------------------------------------------------------------------------------
# MODULE 8: INVENTORY MANAGEMENT & AUTO ALERTS
# ----------------------------------------------------------------------------------
elif choice == "📦 Inventory & Restock":
    st.title("📦 Raw Materials Real-Time Inventory Control Pipeline")
    
    df_i = st.session_state.inventory_db.copy()
    df_i["Status Assessment"] = df_i.apply(lambda r: "🚨 CRITICAL LOW SUPPLY ALERT" if r["Current Stock"] <= r["Alert Level"] else "✅ Optimal Balanced Stock Level", axis=1)
    st.dataframe(df_i, use_container_width=True)
    
    # Render system warning triggers
    crit_list = df_i[df_i["Current Stock"] <= df_i["Alert Level"]]
    if len(crit_list) > 0:
        for _, row in crit_list.iterrows():
            st.error(f"🚨 **Critical Level Depletion Warning:** Sourcing item '{row['Material Name']}' capacity dropped to **{row['Current Stock']} {row['Unit']}** (Configured Safety Buffer Threshold is {row['Alert Level']} {row['Unit']}). Action required.")

    if not is_partner:
        st.markdown("---")
        st.markdown("### 🔄 Restock Inventory Asset Stock Pipeline Matrix")
        with st.form("restock_form", clear_on_submit=True):
            i_select = st.selectbox("Choose Targeted Inventory Raw Material Asset", df_i["Material Name"].values)
            i_delta = st.number_input("Inbound Supply Restock Volume (+ Addition Quantity)", min_value=0.0, step=5.0, value=10.0)
            if st.form_submit_button("Commit Pipeline Inventory Restock"):
                st.session_state.inventory_db.loc[st.session_state.inventory_db["Material Name"] == i_select, "Current Stock"] += i_delta
                st.success(f"Stock depth expanded for material item: {i_select}.")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 9: ADMINISTRATIVE DROPDOWN PANEL (Admin & Super Admin)
# ----------------------------------------------------------------------------------
elif choice == "⚙️ Dropdown Control Panel":
    st.title("⚙️ Strategic Administrative System Infrastructure Configuration Dropdown Options")
    st.write("Add new entries instantly into global dropdown list components across application menus.")
    
    adm_t1, adm_t2, adm_t3, adm_t4 = st.tabs(["Menu Sales Items", "Equity Partners List", "Fixed Asset Categories", "Monthly Expense Heads"])
    
    with adm_t1:
        st.write("Current Sales Food Menu Configuration:", st.session_state.menu_items)
        new_food = st.text_input("Enter New Food Variant Name (e.g. Mutton Kacchi XL, Salad)").strip()
        if st.button("Publish New Food Menu Option"):
            if new_food and new_food not in st.session_state.menu_items:
                st.session_state.menu_items.append(new_food)
                st.success("Food menu configuration matrix updated.")
                st.rerun()
                
    with adm_t2:
        st.write("Current Registered Partner Identifiers:", st.session_state.partner_list)
        new_part_name = st.text_input("Enter Brand New Partner Name Options (e.g. Asif)").strip()
        if st.button("Append New Partner Into System Array"):
            if new_part_name and new_part_name not in st.session_state.partner_list:
                st.session_state.partner_list.append(new_part_name)
                st.success("Global partner validation roster altered.")
                st.rerun()
                
    with adm_t3:
        st.write("Current Fixed Capital Asset Structural Headings:", st.session_state.asset_categories)
        new_asset_cat = st.text_input("Enter Structural Asset Category Designation").strip()
        if st.button("Append Asset Structural Classification Category"):
            if new_asset_cat and new_asset_cat not in st.session_state.asset_categories:
                st.session_state.asset_categories.append(new_asset_cat)
                st.success("Asset classification hierarchy updated.")
                st.rerun()

    with adm_t4:
        st.write("Current Operating Monthly Expense Classification Codes:", st.session_state.expense_categories)
        new_exp_cat = st.text_input("Enter Operating Month Ledger Expense Classification Head").strip()
        if st.button("Commit Expense Ledger Framework Type Option"):
            if new_exp_cat and new_exp_cat not in st.session_state.expense_categories:
                st.session_state.expense_categories.append(new_exp_cat)
                st.success("Operational cost accounting framework headings appended.")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 10: USER SECURITY PROVISIONING (Super Admin Only)
# ----------------------------------------------------------------------------------
elif choice == "👥 System User Provisioning":
    st.title("👥 Corporate Security IAM System Account Matrix Profile Provisioning")
    u_df = pd.DataFrame([{"System Login Identifier Context": k, "Privilege Access Group Matrix": v["role"], "Password Auth Token Block": v["password"]} for k, v in st.session_state.users_db.items()])
    st.dataframe(u_df, use_container_width=True)
    
    with st.form("iam_form"):
        st.markdown("### Provision New Profile Identifier Access Entry")
        reg_id = st.text_input("Account Identification ID String Context User Context").strip().lower()
        reg_pass = st.text_input("Auth Token Key Password Pass String", type="password")
        reg_role = st.selectbox("Access Privilege Matrix Authorization Framework Assignment", ["Super Admin", "Admin", "Partner (View Only)"])
        if st.form_submit_button("Commit Security Profile Provisioning Request"):
            if reg_id and reg_pass:
                st.session_state.users_db[reg_id] = {"password": reg_pass, "role": reg_role}
                st.success("System application security framework provision profile context complete.")
                st.rerun()