import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os

# Page Configuration
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", page_icon="🍲", layout="wide")

# ----------------------------------------------------------------------------------
# DATABASE HARD-DRIVE STORAGE SYSTEM (JSON Persistent Layer)
# ----------------------------------------------------------------------------------
DB_FILE = "erp_database.json"

def load_permanent_database():
    """Reads data from JSON file into session state so reload won't wipe it."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_permanent_database():
    """Writes all current state tables into JSON file instantly on any entry."""
    sync_data = {
        "menu_items": st.session_state.menu_items,
        "partner_list": st.session_state.partner_list,
        "asset_categories": st.session_state.asset_categories,
        "expense_categories": st.session_state.expense_categories,
        "inventory_items": st.session_state.inventory_items,
        
        # Convert DataFrames to dict/json format safely
        "partners_db": st.session_state.partners_db.to_dict(orient="records") if isinstance(st.session_state.partners_db, pd.DataFrame) else [],
        "fixed_expenses": st.session_state.fixed_expenses.to_dict(orient="records") if isinstance(st.session_state.fixed_expenses, pd.DataFrame) else [],
        "monthly_expenses_db": st.session_state.monthly_expenses_db.to_dict(orient="records") if isinstance(st.session_state.monthly_expenses_db, pd.DataFrame) else [],
        "variable_bazar": st.session_state.variable_bazar.to_dict(orient="records") if isinstance(st.session_state.variable_bazar, pd.DataFrame) else [],
        "sales_records": st.session_state.sales_records.to_dict(orient="records") if isinstance(st.session_state.sales_records, pd.DataFrame) else [],
        "salary_db": st.session_state.salary_db.to_dict(orient="records") if isinstance(st.session_state.salary_db, pd.DataFrame) else [],
        "inventory_db": st.session_state.inventory_db.to_dict(orient="records") if isinstance(st.session_state.inventory_db, pd.DataFrame) else [],
        
        # Save login active session status
        "logged_in_user": st.session_state.logged_in_user,
        "user_role": st.session_state.user_role
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, indent=4, ensure_ascii=False)

# Initialize Hard-Drive Read Scheme
disk_data = load_permanent_database()

# User Accounts Configurations
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "superadmin": {"password": "123", "role": "Super Admin"},
        "admin": {"password": "456", "role": "Admin"},
        "partner": {"password": "789", "role": "Partner (View Only)"}
    }

# Core Dynamic Master Lists Mapping
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

# Safe DataFrame recovery blocks from JSON Disk Storage
if 'partners_db' not in st.session_state:
    p_records = disk_data.get("partners_db", [])
    if p_records:
        st.session_state.partners_db = pd.DataFrame(p_records)
    else:
        st.session_state.partners_db = pd.DataFrame([{"Partner Name": p, "Investment Amount": 0.0} for p in st.session_state.partner_list])

if 'fixed_expenses' not in st.session_state:
    f_records = disk_data.get("fixed_expenses", [])
    if f_records:
        st.session_state.fixed_expenses = pd.DataFrame(f_records)
    else:
        st.session_state.fixed_expenses = pd.DataFrame(columns=["Date", "Category", "Asset/Cost Item", "Amount"])

if 'monthly_expenses_db' not in st.session_state:
    m_records = disk_data.get("monthly_expenses_db", [])
    if m_records:
        st.session_state.monthly_expenses_db = pd.DataFrame(m_records)
    else:
        st.session_state.monthly_expenses_db = pd.DataFrame(columns=["Date", "Category", "Particulars", "Amount (BDT)"])

if 'variable_bazar' not in st.session_state:
    v_records = disk_data.get("variable_bazar", [])
    if v_records:
        st.session_state.variable_bazar = pd.DataFrame(v_records)
    else:
        st.session_state.variable_bazar = pd.DataFrame(columns=["Date", "Bazar Item Name", "Quantity/Weight", "Total Cost (BDT)", "Purchased By"])

if 'sales_records' not in st.session_state:
    s_records = disk_data.get("sales_records", [])
    if s_records:
        st.session_state.sales_records = pd.DataFrame(s_records)
    else:
        st.session_state.sales_records = pd.DataFrame(columns=["Date", "Month-Year", "Item Name", "Rate per Plate", "Total Plates", "Adjustment", "Net Total"])

if 'salary_db' not in st.session_state:
    sal_records = disk_data.get("salary_db", [])
    if sal_records:
        st.session_state.salary_db = pd.DataFrame(sal_records)
    else:
        st.session_state.salary_db = pd.DataFrame(columns=["Date", "Staff Name", "Designation", "Salary Type", "Amount Paid (BDT)"])

if 'inventory_db' not in st.session_state:
    i_records = disk_data.get("inventory_db", [])
    if i_records:
        st.session_state.inventory_db = pd.DataFrame(i_records)
    else:
        st.session_state.inventory_db = pd.DataFrame([{"Material Name": m, "Current Stock": 0.0, "Unit": "Kg/Ltr", "Alert Level": 10.0} for m in st.session_state.inventory_items])

# Retain Authentication Login Session on Reload
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = disk_data.get("logged_in_user", None)
if 'user_role' not in st.session_state:
    st.session_state.user_role = disk_data.get("user_role", None)

def get_month_year_str(dt_val):
    return dt_val.strftime("%B %Y")

# ----------------------------------------------------------------------------------
# 2. SECURE AUTHENTICATION SYSTEM
# ----------------------------------------------------------------------------------
if st.session_state.logged_in_user is None:
    st.markdown("<h2 style='text-align: center;'>🍲 Swapnajatra Biryani Bari ERP 🍲</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Automated Financial Architecture & Month-Wise Profit Sharing Engine</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username / ID").strip().lower()
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In Securely"):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    save_permanent_database() # Save login token session instantly
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
    save_permanent_database() # Overwrite files to null login tokens
    st.rerun()

is_admin = st.session_state.user_role in ["Super Admin", "Admin"]
is_superadmin = st.session_state.user_role == "Super Admin"
is_partner = st.session_state.user_role == "Partner (View Only)"

st.sidebar.markdown("---")
st.sidebar.title("📁 ERP Navigation")
menu_options = [
    "📊 Financial Dashboard", 
    "📈 Advanced Report Manager",
    "🧾 Digital Invoice Generator",
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
# MODULE 1: MONTH-WISE AUTOMATED FINANCIAL DASHBOARD
# ----------------------------------------------------------------------------------
if choice == "📊 Financial Dashboard":
    st.title("📊 Month-Wise Enterprise Financial Analytics")
    
    available_months = ["All Time"]
    if len(st.session_state.sales_records) > 0:
        unique_months = st.session_state.sales_records["Month-Year"].unique().tolist()
        available_months.extend(unique_months)
    else:
        available_months.append(get_month_year_str(datetime.now()))
        
    selected_month = st.selectbox("📅 Select Target Month for Statement Filtering", available_months)
    
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
            if len(filtered) > 0:
                return filtered.drop(columns=["Temp-Month"])
            return pd.DataFrame(columns=df.columns)
            
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
    total_capital_base = st.session_state.partners_db["Investment Amount"].sum() if len(st.session_state.partners_db) > 0 else 0.0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(f"Sales Revenue ({selected_month})", f"{m_sales:,.2f} BDT")
    kpi2.metric(f"Total Expenses Outflow", f"{m_outflow:,.2f} BDT")
    kpi3.metric(f"Net Profit / Loss", f"{m_net_profit_loss:,.2f} BDT", delta=f"{m_net_profit_loss:,.2f} BDT")
    kpi4.metric("Total Equity Capital", f"{total_capital_base:,.2f} BDT")
    
    st.markdown("---")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown("### 📈 Monthly Cash Inflow vs Outflow Overview")
        fig_summary = go.Figure(data=[
            go.Bar(name='Sales Revenue Inflow', x=[selected_month], y=[m_sales], marker_color='#2ecc71'),
            go.Bar(name='Total Operational Costs', x=[selected_month], y=[m_outflow], marker_color='#e74c3c')
        ])
        fig_summary.update_layout(barmode='group', height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig_summary, use_container_width=True)
        
    with c_col2:
        st.markdown("### 📉 Cost Operational Factor Distribution")
        if m_outflow > 0:
            fig_pie = px.pie(
                values=[m_fixed, m_variable, m_monthly, m_salary], 
                names=['Fixed Assets Setup', 'Daily Variable Bazar', 'Monthly Bills/Costs', 'Staff Payroll'],
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenditures logged for the selected calendar boundary.")

    st.markdown("---")
    st.markdown(f"### 📅 Relational Profit & Loss (P&L) Statement Ledger — {selected_month}")
    pl_data = {
        "Accounting Line Item Particulars Header": [
            "Total Invoiced Revenue generated from Sales (+)", 
            "Fixed Setup Infrastructure Investment & Assets Allocation (-)", 
            "Daily Variable Material Bazar Sourcing Cost Logs (-)", 
            "Regular Periodic Monthly Operating Bills/Expenses (-)",
            "Total Human Resource Payroll Distributions (-)",
            "Net Resultant Operational Balance (P&L profit base)"
        ],
        "Calculated Statement Values (BDT)": [f"{m_sales:,.2f}", f"{m_fixed:,.2f}", f"{m_variable:,.2f}", f"{m_monthly:,.2f}", f"{m_salary:,.2f}", f"{m_net_profit_loss:,.2f}"]