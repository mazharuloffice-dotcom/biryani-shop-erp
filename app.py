import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os
import base64

# Page Configuration
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", page_icon="🍲", layout="wide")

# ----------------------------------------------------------------------------------
# DATABASE HARD-DRIVE STORAGE SYSTEM (JSON Persistent Layer)
# ----------------------------------------------------------------------------------
DB_FILE = "erp_database.json"

def load_permanent_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_permanent_database():
    sync_data = {
        "menu_items": st.session_state.menu_items,
        "partner_list": st.session_state.partner_list,
        "asset_categories": st.session_state.asset_categories,
        "expense_categories": st.session_state.expense_categories,
        "inventory_items": st.session_state.inventory_items,
        "employees_profiles": st.session_state.employees_profiles,
        "shop_name": st.session_state.shop_name,
        "shop_address": st.session_state.shop_address,
        
        "partners_db": st.session_state.partners_db.to_dict(orient="records") if isinstance(st.session_state.partners_db, pd.DataFrame) else [],
        "fixed_expenses": st.session_state.fixed_expenses.to_dict(orient="records") if isinstance(st.session_state.fixed_expenses, pd.DataFrame) else [],
        "monthly_expenses_db": st.session_state.monthly_expenses_db.to_dict(orient="records") if isinstance(st.session_state.monthly_expenses_db, pd.DataFrame) else [],
        "variable_bazar": st.session_state.variable_bazar.to_dict(orient="records") if isinstance(st.session_state.variable_bazar, pd.DataFrame) else [],
        "sales_records": st.session_state.sales_records.to_dict(orient="records") if isinstance(st.session_state.sales_records, pd.DataFrame) else [],
        "salary_db": st.session_state.salary_db.to_dict(orient="records") if isinstance(st.session_state.salary_db, pd.DataFrame) else [],
        "inventory_db": st.session_state.inventory_db.to_dict(orient="records") if isinstance(st.session_state.inventory_db, pd.DataFrame) else [],
        
        "users_db": st.session_state.users_db,
        "logged_in_user": st.session_state.logged_in_user,
        "user_role": st.session_state.user_role
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, indent=4, ensure_ascii=False)

disk_data = load_permanent_database()

ALL_AVAILABLE_MENUS = [
    "📊 Financial Dashboard", 
    "📈 Advanced Report Manager",
    "🧾 Digital Invoice Generator",
    "🤝 Partner Capital Engine", 
    "💰 Daily Sales Entry", 
    "🛒 Variable Bazar Cost", 
    "💼 Monthly Expenses",
    "🧑‍🍳 Staff Salary Ledger",
    "📦 Inventory & Restock",
    "⚙️ Dropdown Control Panel",
    "👥 System User Provisioning"
]

if 'shop_name' not in st.session_state:
    st.session_state.shop_name = disk_data.get("shop_name", "SWAPNAJATRA BIRYANI BARI")
if 'shop_address' not in st.session_state:
    st.session_state.shop_address = disk_data.get("shop_address", "Mirpur, Dhaka, Bangladesh")

if 'users_db' not in st.session_state:
    st.session_state.users_db = disk_data.get("users_db", {
        "superadmin": {"password": "123", "role": "Super Admin", "permissions": ALL_AVAILABLE_MENUS},
        "admin": {"password": "456", "role": "Admin", "permissions": ALL_AVAILABLE_MENUS[:-1]},
        "partner": {"password": "789", "role": "Partner (View Only)", "permissions": ["📊 Financial Dashboard"]}
    })

if 'menu_items' not in st.session_state:
    st.session_state.menu_items = disk_data.get("menu_items", ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"])
if 'partner_list' not in st.session_state:
    st.session_state.partner_list = disk_data.get("partner_list", ["Foishal", "Anam", "Habib", "Anayat"])
if 'asset_categories' not in st.session_state:
    st.session_state.asset_categories = disk_data.get("asset_categories", ["Shop Rent", "Startup Assets", "Utility Installation", "Legal/Licenses"])
if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = disk_data.get("expense_categories", ["Electricity Bill", "Gas/Wood Bill", "Waste Management", "Marketing", "Others"])
if 'inventory_items' not in st.session_state:
    st.session_state.inventory_items = disk_data.get("inventory_items", ["Miniket Rice", "Beef Meat", "Polao Rice", "Soyabean Oil", "Onion", "Spices"])
if 'employees_profiles' not in st.session_state:
    st.session_state.employees_profiles = disk_data.get("employees_profiles", {})

# Database DataFrames Bootstrapping
if 'partners_db' not in st.session_state:
    p_records = disk_data.get("partners_db", [])
    st.session_state.partners_db = pd.DataFrame(p_records) if p_records else pd.DataFrame([{"Partner Name": p, "Investment Amount": 0.0} for p in st.session_state.partner_list])

if 'fixed_expenses' not in st.session_state:
    st.session_state.fixed_expenses = pd.DataFrame(disk_data.get("fixed_expenses", [])) if disk_data.get("fixed_expenses", []) else pd.DataFrame(columns=["Date", "Category", "Asset/Cost Item", "Amount"])

if 'monthly_expenses_db' not in st.session_state:
    st.session_state.monthly_expenses_db = pd.DataFrame(disk_data.get("monthly_expenses_db", [])) if disk_data.get("monthly_expenses_db", []) else pd.DataFrame(columns=["Date", "Category", "Particulars", "Amount (BDT)"])

if 'variable_bazar' not in st.session_state:
    st.session_state.variable_bazar = pd.DataFrame(disk_data.get("variable_bazar", [])) if disk_data.get("variable_bazar", []) else pd.DataFrame(columns=["Date", "Bazar Item Name", "Quantity/Weight", "Total Cost (BDT)", "Purchased By"])

if 'sales_records' not in st.session_state:
    st.session_state.sales_records = pd.DataFrame(disk_data.get("sales_records", [])) if disk_data.get("sales_records", []) else pd.DataFrame(columns=["Date", "Month-Year", "Item Name", "Rate per Plate", "Total Plates", "Adjustment", "Net Total"])

if 'salary_db' not in st.session_state:
    st.session_state.salary_db = pd.DataFrame(disk_data.get("salary_db", [])) if disk_data.get("salary_db", []) else pd.DataFrame(columns=["Date", "Staff Name", "Designation", "Salary Type", "Amount Paid (BDT)"])

if 'inventory_db' not in st.session_state:
    i_records = disk_data.get("inventory_db", [])
    st.session_state.inventory_db = pd.DataFrame(i_records) if i_records else pd.DataFrame([{"Material Name": m, "Current Stock": 0.0, "Unit": "Kg/Ltr", "Alert Level": 10.0} for m in st.session_state.inventory_items])

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = disk_data.get("logged_in_user", None)
if 'user_role' not in st.session_state:
    st.session_state.user_role = disk_data.get("user_role", None)

def get_month_year_str(dt_val):
    return dt_val.strftime("%B %Y")

# Authentication Check
if st.session_state.logged_in_user is None:
    st.markdown(f"<h2 style='text-align: center;'>🍲 {st.session_state.shop_name} </h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Enterprise Resource Planning Matrix</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username").strip().lower()
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In Securely"):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    save_permanent_database()
                    st.rerun()
                else:
                    st.error("❌ Access Denied: Invalid Credentials.")
    st.stop()

st.sidebar.title("🔒 Security Control")
st.sidebar.write(f"**User:** {st.session_state.logged_in_user.upper()}")
st.sidebar.write(f"**Role:** {st.session_state.user_role}")
if st.sidebar.button("Logout 🚪"):
    st.session_state.logged_in_user = None
    st.session_state.user_role = None
    save_permanent_database()
    st.rerun()

user_allowed_menus = st.session_state.users_db.get(st.session_state.logged_in_user, {}).get("permissions", ALL_AVAILABLE_MENUS)

st.sidebar.markdown("---")
st.sidebar.title("📁 ERP Navigation")
filtered_menu_options = [m for m in ALL_AVAILABLE_MENUS if m in user_allowed_menus]
if not filtered_menu_options:
    st.sidebar.error("No Menu Permissions Allowed.")
    st.stop()

choice = st.sidebar.radio("Navigate to module:", filtered_menu_options)
is_partner = st.session_state.user_role == "Partner (View Only)"

# ----------------------------------------------------------------------------------
# 1. FINANCIAL DASHBOARD WITH PARTNER EQUITY PROFIT/LOSS PRO-RATA SHARE
# ----------------------------------------------------------------------------------
if choice == "📊 Financial Dashboard":
    st.title("📊 Month-Wise Enterprise Financial Analytics & Partner P&L Dist.")
    
    available_months = ["All Time"]
    if len(st.session_state.sales_records) > 0:
        available_months.extend(st.session_state.sales_records["Month-Year"].unique().tolist())
    selected_month = st.selectbox("📅 Select Target Filter Month", available_months)
    
    df_sales = st.session_state.sales_records.copy()
    df_fixed = st.session_state.fixed_expenses.copy()
    df_variable = st.session_state.variable_bazar.copy()
    df_monthly = st.session_state.monthly_expenses_db.copy()
    df_salary = st.session_state.salary_db.copy()
    
    if selected_month != "All Time":
        df_sales = df_sales[df_sales["Month-Year"] == selected_month]
        def filter_by_month(df):
            if len(df) == 0: return df
            df["Temp-Month"] = pd.to_datetime(df["Date"]).dt.strftime("%B %Y")
            filtered = df[df["Temp-Month"] == selected_month]
            return filtered.drop(columns=["Temp-Month"]) if len(filtered) > 0 else pd.DataFrame(columns=df.columns)
        df_fixed = filter_by_month(df_fixed)
        df_variable = filter_by_month(df_variable)
        df_monthly = filter_by_month(df_monthly)
        df_salary = filter_by_month(df_salary)

    m_sales = df_sales["Net Total"].sum() if len(df_sales) > 0 else 0.0
    m_fixed = df_fixed["Amount"].sum() if len(df_fixed) > 0 else 0.0
    m_variable = df_variable["Total Cost (BDT)"].sum() if len(df_variable) > 0 else 0.0
    m_monthly = df_monthly["Amount (BDT)"].sum() if len(df_monthly) > 0 else 0.0
    m_salary = df_salary["Amount Paid (BDT)"].sum() if len(df_salary) > 0 else 0.0
    
    m_outflow = m_fixed + m_variable + m_monthly + m_salary
    m_net_profit_loss = m_sales - m_outflow

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Sales Revenue Generated", f"{m_sales:,.2f} BDT")
    kpi2.metric("Total Business Expenses", f"{m_outflow:,.2f} BDT")
    kpi3.metric("Net Operational Profit / Loss", f"{m_net_profit_loss:,.2f} BDT", delta=f"{m_net_profit_loss:,.2f} BDT")
    
    # NEW FEATURE: AUTOMATED PARTNER INVESTMENT-WISE STATEMENT SHARE ENGINE
    st.markdown("---")
    st.markdown(f"### 🤝 Investment-Wise Monthly Profit / Loss Allocation ({selected_month})")
    
    if len(st.session_state.partners_db) > 0:
        df_partner_calc = st.session_state.partners_db.copy()
        total_equity_capital = df_partner_calc["Investment Amount"].sum()
        
        if total_equity_capital > 0:
            df_partner_calc["Ownership Ratio (%)"] = (df_partner_calc["Investment Amount"] / total_equity_capital) * 100
            df_partner_calc["Allocated Net Share (BDT)"] = (df_partner_calc["Ownership Ratio (%)"] / 100) * m_net_profit_loss
            
            # Format display for easy dashboard layout visibility
            df_display = df_partner_calc.copy()
            df_display["Investment Amount"] = df_display["Investment Amount"].map("{:,.2f} BDT".format)
            df_display["Ownership Ratio (%)"] = df_display["Ownership Ratio (%)"].map("{:.2f}%".format)
            df_display["Allocated Net Share (BDT)"] = df_display["Allocated Net Share (BDT)"].map("{:,.2f} BDT".format)
            
            st.dataframe(df_display, use_container_width=True)
        else:
            st.warning("⚠️ Ownership ratios cannot be determined because Total Equity Capital is 0. Please add investment amounts in Partner Capital Engine.")
    else:
        st.info("No partner equity nodes currently found.")

# ----------------------------------------------------------------------------------
# 2. ADVANCED REPORT MANAGER
# ----------------------------------------------------------------------------------
elif choice == "📈 Advanced Report Manager":
    st.title("📈 Cross-Module Financial Journals Ledger Logs")
    t1, t2, t3, t4 = st.tabs(["Sales Logs", "Bazar Purchase Logs", "Fixed Investments Logs", "Operating Expenses"])
    with t1: st.dataframe(st.session_state.sales_records, use_container_width=True)
    with t2: st.dataframe(st.session_state.variable_bazar, use_container_width=True)
    with t3: st.dataframe(st.session_state.fixed_expenses, use_container_width=True)
    with t4: st.dataframe(st.session_state.monthly_expenses_db, use_container_width=True)

# ----------------------------------------------------------------------------------
# 3. DIGITAL INVOICE GENERATOR
# ----------------------------------------------------------------------------------
elif choice == "🧾 Digital Invoice Generator":
    st.title("🧾 Digital Cash POS Invoice Generator")
    inv_item = st.selectbox("Line Item", st.session_state.menu_items)
    inv_rate = st.number_input("Rate (BDT)", min_value=0.0, value=220.0)
    inv_qty = st.number_input("Qty Count", min_value=1, value=1)
    st.markdown(f"### Gross Invoice Total: **{inv_rate * inv_qty:,.2f} BDT**")

# ----------------------------------------------------------------------------------
# 4. PARTNER CAPITAL ENGINE
# ----------------------------------------------------------------------------------
elif choice == "🤝 Partner Capital Engine":
    st.title("🤝 Partner Equity Ledger Base Engine")
    st.dataframe(st.session_state.partners_db, use_container_width=True)
    if not is_partner:
        with st.form("cap_entry_form", clear_on_submit=True):
            p_sel = st.selectbox("Select Partner Node", st.session_state.partner_list)
            p_amt = st.number_input("Injected Capital Add (BDT)", min_value=0.0, step=500.0)
            if st.form_submit_button("Commit Investment Capital Line Entry"):
                st.session_state.partners_db.loc[st.session_state.partners_db["Partner Name"] == p_sel, "Investment Amount"] += p_amt
                save_permanent_database()
                st.success("Capital allocation records updated successfully on hardware database disk!")
                st.rerun()

# ----------------------------------------------------------------------------------
# 5. DAILY SALES TRANSACTIONAL REGISTER ENTRY
# ----------------------------------------------------------------------------------
elif choice == "💰 Daily Sales Entry":
    st.title("💰 Register High-Frequency Daily Sales Intake")
    if is_partner: st.error("Access Prohibited.")
    else:
        with st.form("sales_direct_form", clear_on_submit=True):
            s_prod = st.selectbox("Product Dish Line", st.session_state.menu_items)
            s_rate = st.number_input("Rate per Plate Base (BDT)", min_value=0.0, value=220.0)
            s_qty = st.number_input("Plates Count Volume", min_value=1, value=1)
            s_date = st.date_input("Journal Posting Date Entry", datetime.now())
            if st.form_submit_button("Post Sales Entry Into System Ledger"):
                # CRITICAL DATA TYPE DATE TO STRING PARSING TO FIX SAVING FAILURE
                date_str = s_date.strftime("%Y-%m-%d") if isinstance(s_date, (date, datetime)) else str(s_date)
                new_sales_row = pd.DataFrame([{
                    "Date": date_str, "Month-Year": s_date.strftime("%B %Y"),
                    "Item Name": s_prod, "Rate per Plate": s_rate, "Total Plates": s_qty, "Adjustment": 0.0, "Net Total": s_rate * s_qty
                }])
                st.session_state.sales_records = pd.concat([st.session_state.sales_records, new_sales_row], ignore_index=True)
                save_permanent_database()
                st.success("Success! Sales transactional node posted permanently to disk storage!")
                st.rerun()

# ----------------------------------------------------------------------------------
# 6. DAILY VARIABLE BAZAR PROCUREMENT COST LEDGER
# ----------------------------------------------------------------------------------
elif choice == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Variable Material Sourcing Cost Ledger")
    if is_partner: st.error("Access Prohibited.")
    else:
        with st.form("bazar_direct_form", clear_on_submit=True):
            b_item = st.selectbox("Raw Materials Node Selection", st.session_state.inventory_items)
            b_qty = st.text_input("Quantity Weight String Format", value="10 Kg")
            b_cost = st.number_input("Invoiced Procurement Total Cost (BDT)", min_value=0.0)
            b_date = st.date_input("Purchase Ledger Entry Date", datetime.now())
            if st.form_submit_button("Post Sourcing Cost"):
                date_str = b_date.strftime("%Y-%m-%d") if isinstance(b_date, (date, datetime)) else str(b_date)
                new_bazar_row = pd.DataFrame([{
                    "Date": date_str, "Bazar Item Name": b_item, "Quantity/Weight": b_qty, "Total Cost (BDT)": b_cost, "Purchased By": st.session_state.logged_in_user.upper()
                }])
                st.session_state.variable_bazar = pd.concat([st.session_state.variable_bazar, new_bazar_row], ignore_index=True)
                save_permanent_database()
                st.success("Success! Variable bazar purchase entry securely integrated onto database hardware.")
                st.rerun()

# ----------------------------------------------------------------------------------
# 7. PERIODIC OPERATIONAL EXPENDITURES 
# ----------------------------------------------------------------------------------
elif choice == "💼 Monthly Expenses":
    st.title("💼 Monthly Periodic Business Expenses Register Portal")
    if is_partner: st.error("Access Prohibited.")
    else:
        with st.form("exp_direct_form", clear_on_submit=True):
            e_cat = st.selectbox("Operational Classification Dropdowns", st.session_state.expense_categories)
            e_memo = st.text_input("Particulars Memo Specification Summary")
            e_val = st.number_input("Outflow Cash Value (BDT)", min_value=0.0)
            e_date = st.date_input("Accounting Settlement Settlement Date", datetime.now())
            if st.form_submit_button("Publish Cost Logs"):
                date_str = e_date.strftime("%Y-%m-%d") if isinstance(e_date, (date, datetime)) else str(e_date)
                new_exp_row = pd.DataFrame([{"Date": date_str, "Category": e_cat, "Particulars": e_memo, "Amount (BDT)": e_val}])
                st.session_state.monthly_expenses_db = pd.concat([st.session_state.monthly_expenses_db, new_exp_row], ignore_index=True)
                save_permanent_database()
                st.success("Operational expense transaction logged to database disk.")
                st.rerun()

# ----------------------------------------------------------------------------------
# 8. WORKFORCE PAYROLL MATRIX LOGS & COMPEHENSIVE PROFILES
# ----------------------------------------------------------------------------------
elif choice == "🧑‍🍳 Staff Salary Ledger":
    st.title("🧑‍🍳 Advanced Workforce Directory & Payroll Distribution Engine")
    tab1, tab2 = st.tabs(["💰 Salary Matrix Payroll Distributions Logs", "👥 Comprehensive Employee Profiles Directory"])
    
    with tab2:
        st.markdown("### Register Profile Data Cards Bundle")
        with st.form("profile_direct_form", clear_on_submit=True):
            en = st.text_input("Employee Name Profile Key").strip()
            ed = st.text_input("Designation Role Title").strip()
            em = st.text_input("Mobile Contact Line").strip()
            if st.form_submit_button("Save Employee Identity Profile Cluster Array ✅"):
                if en and em:
                    st.session_state.employees_profiles[en] = {"designation": ed, "mobile": em, "father": "", "nid": "", "address": "", "photo": ""}
                    save_permanent_database()
                    st.success(f"Identity Profile structure for '{en}' registered onto database layer.")
                    st.rerun()

    with tab1:
        if len(st.session_state.salary_db) > 0:
            st.dataframe(st.session_state.salary_db, use_container_width=True)
        else:
            st.info("No transaction histories logs currently found for human resources payroll distributions on database disk.")
            
        if not is_partner and st.session_state.employees_profiles:
            st.markdown("---")
            st.markdown("### 💸 Post New Wage/Salary Payment Entry")
            with st.form("payroll_direct_submission", clear_on_submit=True):
                emp_sel = st.selectbox("Employee Reference Node Mapping", list(st.session_state.employees_profiles.keys()))
                sal_type = st.selectbox("Salary Matrix Type Class", ["Daily Wages Salary", "Monthly Regular Salary"])
                sal_val = st.number_input("Disbursed Cash Compensation Amount Value (BDT)", min_value=0.0, step=100.0)
                sal_date = st.date_input("Disbursement Operational Matrix Date", datetime.now())
                if st.form_submit_button("Confirm Payment & Log Entry ✅"):
                    mapped_desg = st.session_state.employees_profiles[emp_sel]["designation"]
                    date_str = sal_date.strftime("%Y-%m-%d") if isinstance(sal_date, (date, datetime)) else str(sal_date)
                    new_payroll = pd.DataFrame([{
                        "Date": date_str, "Staff Name": emp_sel, "Designation": mapped_desg, "Salary Type": sal_type, "Amount Paid (BDT)": float(sal_val)
                    }])
                    st.session_state.salary_db = pd.concat([st.session_state.salary_db, new_payroll], ignore_index=True)
                    save_permanent_database()
                    st.success(f"{sal_type} to {emp_sel} recorded securely!")
                    st.rerun()

# ----------------------------------------------------------------------------------
# 9. RAW MATERIAL SUPPLY PIPELINE DEPTH LEDGER
# ----------------------------------------------------------------------------------
elif choice == "📦 Inventory & Restock":
    st.title("📦 Raw Material Supply Pipeline Depth Ledger")
    st.dataframe(st.session_state.inventory_db, use_container_width=True)

# ----------------------------------------------------------------------------------
# 10. DROPDOWN MATRIX HUB CONTROL PANEL
# ----------------------------------------------------------------------------------
elif choice == "⚙️ Dropdown Control Panel":
    st.title("⚙️ Dropdown Configurations Control Matrix Hub")
    st.write("Active Food Items Array Configured Options Vector:", st.session_state.menu_items)

# ----------------------------------------------------------------------------------
# 11. APPLICATION IDENTITY ACCESS PROFILES PROVISIONING MATRIX
# ----------------------------------------------------------------------------------
elif choice == "👥 System User Provisioning":
    st.title("👥 Application Identity Access Matrix Provisioning")
    with st.form("sys_user_form", clear_on_submit=True):
        u_id = st.text_input("New Identity Account User Unique ID").strip().lower()
        u_pass = st.text_input("Security Access Token Password", type="password")
        if st.form_submit_button("Save User Node Instance Parameters"):
            if u_id and u_pass:
                st.session_state.users_db[u_id] = {"password": u_pass, "role": "Admin", "permissions": ALL_AVAILABLE_MENUS}
                save_permanent_database()
                st.success("User identity configurations matrix provisioned successfully.")
                st.rerun()