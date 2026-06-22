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
        "employee_roster": st.session_state.employee_roster,
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

# Core Shop Settings Recovery
if 'shop_name' not in st.session_state:
    st.session_state.shop_name = disk_data.get("shop_name", "SWAPNAJATRA BIRYANI BARI")
if 'shop_address' not in st.session_state:
    st.session_state.shop_address = disk_data.get("shop_address", "Mirpur, Dhaka, Bangladesh")

# Secure Accounts Recovery Block
if 'users_db' not in st.session_state:
    st.session_state.users_db = disk_data.get("users_db", {
        "superadmin": {"password": "123", "role": "Super Admin"},
        "admin": {"password": "456", "role": "Admin"},
        "partner": {"password": "789", "role": "Partner (View Only)"}
    })

# Master Lists Mapping
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = disk_data.get("menu_items", ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"])
if 'partner_list' not in st.session_state:
    st.session_state.partner_list = disk_data.get("partner_list", ["Foishal", "Anam", "Habib", "Anayat"])
if 'employee_roster' not in st.session_state:
    st.session_state.employee_roster = disk_data.get("employee_roster", ["Head Cook", "Assistant Chef", "Server Lead"])
if 'asset_categories' not in st.session_state:
    st.session_state.asset_categories = disk_data.get("asset_categories", ["Shop Rent", "Startup Assets", "Utility Installation", "Legal/Licenses"])
if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = disk_data.get("expense_categories", ["Electricity Bill", "Gas/Wood Bill", "Waste Management", "Marketing", "Others"])
if 'inventory_items' not in st.session_state:
    st.session_state.inventory_items = disk_data.get("inventory_items", ["Miniket Rice", "Beef Meat", "Polao Rice", "Soyabean Oil", "Onion", "Spices"])

# Safe DataFrame recovery blocks from JSON Disk Storage
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

# ----------------------------------------------------------------------------------
# AUTHENTICATION
# ----------------------------------------------------------------------------------
if st.session_state.logged_in_user is None:
    st.markdown(f"<h2 style='text-align: center;'>🍲 {st.session_state.shop_name} 🍲</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Enterprise Resource Planning Architecture</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username / ID").strip().lower()
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

# Sidebar Control Center
st.sidebar.title("🔒 Security Control")
st.sidebar.write(f"**User:** {st.session_state.logged_in_user.capitalize()}")
st.sidebar.write(f"**Role:** {st.session_state.user_role}")
if st.sidebar.button("Logout 🚪"):
    st.session_state.logged_in_user = None
    st.session_state.user_role = None
    save_permanent_database()
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
# FINANCIAL DASHBOARD
# ----------------------------------------------------------------------------------
if choice == "📊 Financial Dashboard":
    st.title("📊 Month-Wise Enterprise Financial Analytics")
    
    available_months = ["All Time"]
    if len(st.session_state.sales_records) > 0:
        available_months.extend(st.session_state.sales_records["Month-Year"].unique().tolist())
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
    total_capital_base = st.session_state.partners_db["Investment Amount"].sum() if len(st.session_state.partners_db) > 0 else 0.0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(f"Sales Revenue ({selected_month})", f"{m_sales:,.2f} BDT")
    kpi2.metric("Total Expenses Outflow", f"{m_outflow:,.2f} BDT")
    kpi3.metric("Net Profit / Loss", f"{m_net_profit_loss:,.2f} BDT", delta=f"{m_net_profit_loss:,.2f} BDT")
    kpi4.metric("Total Equity Capital", f"{total_capital_base:,.2f} BDT")
    
    st.markdown("---")
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
    }
    st.table(pd.DataFrame(pl_data))

    st.markdown("---")
    st.markdown(f"### 🤝 Automated Month-Wise Profit Sharing Engine ({selected_month})")
    df_payout = st.session_state.partners_db.copy()
    if total_capital_base > 0:
        df_payout["Capital Ownership Share (%)"] = (df_payout["Investment Amount"] / total_capital_base) * 100
        df_payout["Calculated Month P&L Share (BDT)"] = (df_payout["Capital Ownership Share (%)"] / 100) * m_net_profit_loss
        
        df_p_disp = df_payout.copy()
        df_p_disp["Investment Amount"] = df_p_disp["Investment Amount"].map("{:,.2f} BDT".format)
        df_p_disp["Capital Ownership Share (%)"] = df_p_disp["Capital Ownership Share (%)"].map("{:.2f}%".format)
        df_p_disp["Calculated Month P&L Share (BDT)"] = df_p_disp["Calculated Month P&L Share (BDT)"].map("{:,.2f} BDT".format)
        st.dataframe(df_p_disp, use_container_width=True)

# ----------------------------------------------------------------------------------
# ADVANCED REPORT MANAGER
# ----------------------------------------------------------------------------------
elif choice == "📈 Advanced Report Manager":
    st.title("📈 Strategic Cross-Module Multi-Report Manager Engine")
    rep_tab1, rep_tab2, rep_tab3 = st.tabs(["Sales Journal Ledger", "Variable Material Sourcing", "Staff Payroll Distributions"])
    
    with rep_tab1:
        st.markdown("### 🔍 Sales Ledger Filtering Filter")
        if len(st.session_state.sales_records) > 0:
            st.dataframe(st.session_state.sales_records, use_container_width=True)
            if not is_partner:
                idx_to_del = st.selectbox("Select Row Index to Delete from Sales", st.session_state.sales_records.index, key="del_sales_idx")
                if st.button("Delete Selected Sales Row 🗑️"):
                    st.session_state.sales_records = st.session_state.sales_records.drop(idx_to_del).reset_index(drop=True)
                    save_permanent_database()
                    st.success("Record dropped successfully.")
                    st.rerun()

    with rep_tab2:
        st.markdown("### 🔍 Variable Material Bazar Procurement Audit")
        if len(st.session_state.variable_bazar) > 0:
            st.dataframe(st.session_state.variable_bazar, use_container_width=True)
            if not is_partner:
                idx_to_del = st.selectbox("Select Row Index to Delete from Bazar", st.session_state.variable_bazar.index, key="del_bazar_idx")
                if st.button("Delete Selected Bazar Row 🗑️"):
                    st.session_state.variable_bazar = st.session_state.variable_bazar.drop(idx_to_del).reset_index(drop=True)
                    save_permanent_database()
                    st.success("Record dropped successfully.")
                    st.rerun()

    with rep_tab3:
        st.markdown("### 🔍 Employee Wage Allocation Audit Logs")
        if len(st.session_state.salary_db) > 0:
            st.dataframe(st.session_state.salary_db, use_container_width=True)
            if not is_partner:
                idx_to_del = st.selectbox("Select Row Index to Delete from Payroll", st.session_state.salary_db.index, key="del_salary_idx")
                if st.button("Delete Selected Payroll Row 🗑️"):
                    st.session_state.salary_db = st.session_state.salary_db.drop(idx_to_del).reset_index(drop=True)
                    save_permanent_database()
                    st.success("Record dropped successfully.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# DIGITAL INVOICE GENERATOR WITH CUSTOM ADDRESS DYNAMIC LINKS
# ----------------------------------------------------------------------------------
elif choice == "🧾 Digital Invoice Generator":
    st.title("🧾 Interactive Point of Sale (POS) Invoice Generator")
    col_inv1, col_inv2 = st.columns([1, 1])
    with col_inv1:
        st.markdown("#### 📝 Compile Bill Elements")
        inv_cust = st.text_input("Client/Customer Name String", value="Walk-in Customer")
        inv_item = st.selectbox("Product Line Item Context", st.session_state.menu_items)
        inv_rate = st.number_input("Unit Price Base (BDT)", min_value=0.0, value=220.0, step=10.0)
        inv_qty = st.number_input("Billed Quantity Count (Plates)", min_value=1, value=2, step=1)
        inv_disc = st.number_input("Invoice Structural Discount (Minus BDT)", min_value=0.0, value=0.0, step=5.0)
        
        inv_gross = inv_rate * inv_qty
        inv_net = inv_gross - inv_disc
        
    with col_inv2:
        st.markdown("<style>.invoice-box { max-width: 400px; padding: 20px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0, 0, 0, .15); font-size: 14px; background-color: #fff; }</style>", unsafe_allow_html=True)
        invoice_html = f"""
        <div class="invoice-box">
            <h3 style="text-align: center; color: #2ecc71; margin: 0;">{st.session_state.shop_name.upper()}</h3>
            <p style="text-align: center; font-size: 11px; color: gray; margin: 0 0 15px 0;">{st.session_state.shop_address}</p>
            <hr>
            <b>Invoice Date:</b> {datetime.now().strftime('%Y-%m-%d %I:%M %p')}<br>
            <b>Customer:</b> {inv_cust}<br>
            <hr>
            <table style="width: 100%; font-size: 13px;">
                <tr style="background: #eee; font-weight: bold;"><td>Particulars</td><td style="text-align: center;">Qty</td><td style="text-align: right;">Total</td></tr>
                <tr><td>{inv_item} (@{inv_rate:.0f})</td><td style="text-align: center;">{inv_qty}</td><td style="text-align: right;">{inv_gross:.2f} BDT</td></tr>
                <tr style="color: #e74c3c;"><td colspan="2">Discount:</td><td style="text-align: right;">-{inv_disc:.2f} BDT</td></tr>
                <tr style="font-weight: bold; font-size: 15px; color: #2e6f40;"><td colspan="2">Net Total:</td><td style="text-align: right;">{inv_net:.2f} BDT</td></tr>
            </table><br>
            <p style="text-align: center; font-size: 12px; font-style: italic; color: #2ecc71;">Thank you! 🎉</p>
        </div>
        """
        st.markdown(invoice_html, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# PARTNER CAPITAL ENGINE
# ----------------------------------------------------------------------------------
elif choice == "🤝 Partner Capital Engine":
    st.title("🤝 Capital Allocations & Fixed Infrastructure Investments")
    p_tab1, p_tab2 = st.tabs(["Partner Equity Accounts Ledger", "Fixed Structural Cost Entry"])
    
    with p_tab1:
        st.dataframe(st.session_state.partners_db, use_container_width=True)
        if not is_partner:
            with st.form("capital_form", clear_on_submit=True):
                p_select = st.selectbox("Identify Target Partner Name Vector", st.session_state.partner_list)
                p_inject = st.number_input("Injected Capital Delta Amount (BDT)", min_value=0.0, step=1000.0)
                if st.form_submit_button("Commit Capital Entry Change"):
                    st.session_state.partners_db.loc[st.session_state.partners_db["Partner Name"] == p_select, "Investment Amount"] += p_inject
                    save_permanent_database()
                    st.success("Equity balance transformed.")
                    st.rerun()

    with p_tab2:
        st.dataframe(st.session_state.fixed_expenses, use_container_width=True)
        if not is_partner:
            if len(st.session_state.fixed_expenses) > 0:
                f_del = st.selectbox("Select Fixed Asset Row Index to Delete", st.session_state.fixed_expenses.index)
                if st.button("Delete Selected Asset Row 🗑️"):
                    st.session_state.fixed_expenses = st.session_state.fixed_expenses.drop(f_del).reset_index(drop=True)
                    save_permanent_database()
                    st.success("Asset row deleted.")
                    st.rerun()
                    
            with st.form("fixed_form", clear_on_submit=True):
                f_cat = st.selectbox("Category Class Selection", st.session_state.asset_categories)
                f_desc = st.text_input("Asset Specification Memo Particulars").strip()
                f_cost = st.number_input("Invoiced Cost Asset Value (BDT)", min_value=0.0, step=500.0)
                f_date = st.date_input("Asset Expenditure Logging Date", datetime.now())
                if st.form_submit_button("Publish Capital Asset Entry"):
                    if f_desc:
                        new_asset = pd.DataFrame([{"Date": f_date.strftime("%Y-%m-%d"), "Category": f_cat, "Asset/Cost Item": f_desc, "Amount": f_cost}])
                        st.session_state.fixed_expenses = pd.concat([st.session_state.fixed_expenses, new_asset], ignore_index=True)
                        save_permanent_database()
                        st.success("Fixed Asset saved.")
                        st.rerun()

# ----------------------------------------------------------------------------------
# DAILY SALES ENTRY
# ----------------------------------------------------------------------------------
elif choice == "💰 Daily Sales Entry":
    st.title("💰 High-Frequency Point of Sale Intake Interface")
    if is_partner:
        st.error("🚫 Access Restructured: View-only account privilege limitations.")
    else:
        with st.form("sales_submission_form", clear_on_submit=True):
            prod_sel = st.selectbox("Target Menu Product Node", st.session_state.menu_items)
            p_rate = st.number_input("Unit Plate Billing Rate (BDT)", min_value=0.0, value=220.0, step=5.0)
            p_qty = st.number_input("Volume Unit Count Sold", min_value=1, value=1, step=1)
            p_adj = st.number_input("Discount / Rebate Offset (+/- BDT)", step=5.0, value=0.0)
            p_date = st.date_input("Journal Posting Date String Context", datetime.now())
            
            if st.form_submit_button("Post Transaction Journal Entry"):
                new_s_log = pd.DataFrame([{
                    "Date": p_date.strftime("%Y-%m-%d"), "Month-Year": get_month_year_str(p_date),
                    "Item Name": prod_sel, "Rate per Plate": p_rate, "Total Plates": p_qty, "Adjustment": p_adj, "Net Total": (p_rate * p_qty) + p_adj
                }])
                st.session_state.sales_records = pd.concat([st.session_state.sales_records, new_s_log], ignore_index=True)
                save_permanent_database()
                st.success("Sales record posted successfully.")
                st.rerun()

# ----------------------------------------------------------------------------------
# DAILY VARIABLE BAZAR COST
# ----------------------------------------------------------------------------------
elif choice == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Variable Material Sourcing Cost Ledger")
    if is_partner:
        st.error("🚫 Access Restricted.")
    else:
        with st.form("bazar_log_form", clear_on_submit=True):
            mat_select = st.selectbox("Choose Inventory Item Node", st.session_state.inventory_items + ["Other Unlisted Sourcing Items"])
            mat_qty = st.text_input("Procured Quantity Metrics (e.g., 15 Kg)").strip()
            mat_cost = st.number_input("Total Outflow Invoiced Sourcing Cost (BDT)", min_value=0.0, step=100.0)
            mat_date = st.date_input("Settlement Date", datetime.now())
            if st.form_submit_button("Post Bazar Cost Entry"):
                new_b_entry = pd.DataFrame([{"Date": mat_date.strftime("%Y-%m-%d"), "Bazar Item Name": mat_select, "Quantity/Weight": mat_qty, "Total Cost (BDT)": mat_cost, "Purchased By": st.session_state.logged_in_user.capitalize()}])
                st.session_state.variable_bazar = pd.concat([st.session_state.variable_bazar, new_b_entry], ignore_index=True)
                save_permanent_database()
                st.success("Bazar entry posted safely.")
                st.rerun()

# ----------------------------------------------------------------------------------
# MONTHLY OPERATING EXPENSES
# ----------------------------------------------------------------------------------
elif choice == "💼 Monthly Expenses":
    st.title("💼 Periodic Operational Month Expenditures Journal")
    if is_partner:
        st.error("🚫 Access Restricted.")
    else:
        if len(st.session_state.monthly_expenses_db) > 0:
            st.dataframe(st.session_state.monthly_expenses_db, use_container_width=True)
            me_del = st.selectbox("Select Row Index to Delete from Monthly Expenses", st.session_state.monthly_expenses_db.index)
            if st.button("Delete Selected Expense Row 🗑️"):
                st.session_state.monthly_expenses_db = st.session_state.monthly_expenses_db.drop(me_del).reset_index(drop=True)
                save_permanent_database()
                st.success("Expense row deleted.")
                st.rerun()
                
        with st.form("monthly_exp_submission", clear_on_submit=True):
            m_cat = st.selectbox("Identify Expense Classification", st.session_state.expense_categories)
            m_memo = st.text_input("Operational Particulars Memo Details").strip()
            m_val = st.number_input("Invoiced Value Outflow Amount (BDT)", min_value=0.0, step=100.0)
            m_date = st.date_input("Settlement Date", datetime.now())
            if st.form_submit_button("Publish Operating Cost Entry"):
                if m_memo:
                    new_mo_entry = pd.DataFrame([{"Date": m_date.strftime("%Y-%m-%d"), "Category": m_cat, "Particulars": m_memo, "Amount (BDT)": m_val}])
                    st.session_state.monthly_expenses_db = pd.concat([st.session_state.monthly_expenses_db, new_mo_entry], ignore_index=True)
                    save_permanent_database()
                    st.success("Monthly cost item logged.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# WORKFORCE MANAGEMENT (STAFF PAYROLL + EMPLOYEE ENTRY ROSTER)
# ----------------------------------------------------------------------------------
elif choice == "🧑‍🍳 Staff Salary Ledger":
    st.title("🧑‍🍳 Workforce Management Payroll & Employee Control")
    
    tab_pay1, tab_pay2 = st.tabs(["Log Salary Disbursements", "Employee Roster Entry Control"])
    
    with tab_pay2:
        st.write("Current Registered Employees:", st.session_state.employee_roster)
        new_emp = st.text_input("Enter New Employee Full Name Context").strip()
        if st.button("Add/Save Employee to Roster ✅"):
            if new_emp and new_emp not in st.session_state.employee_roster:
                st.session_state.employee_roster.append(new_emp)
                save_permanent_database()
                st.success(f"Success! '{new_emp}' has been integrated into the central system roster matrix.")
                st.rerun()
        
        target_emp_del = st.selectbox("Select Employee to Remove from Active Roster", st.session_state.employee_roster, key="del_emp_ros")
        if st.button("Delete Employee from Roster 🗑️"):
            st.session_state.employee_roster.remove(target_emp_del)
            save_permanent_database()
            st.success("Employee removed from options roster.")
            st.rerun()

    with tab_pay1:
        if len(st.session_state.salary_db) > 0:
            st.dataframe(st.session_state.salary_db, use_container_width=True)
            
        if not is_partner:
            with st.form("payroll_form", clear_on_submit=True):
                emp_name = st.selectbox("Employee Roster Mapping Selection", st.session_state.employee_roster)
                emp_desg = st.text_input("Role Designation Title (e.g. Cook, Waiter)").strip()
                sal_class = st.selectbox("Salary Matrix Type Class", ["Daily Wages Salary", "Monthly Regular Salary"])
                sal_value = st.number_input("Disbursed Cash Compensation (BDT)", min_value=0.0, step=100.0)
                sal_date = st.date_input("Disbursement Date", datetime.now())
                
                if st.form_submit_button("Post Workforce Salary Payroll Log"):
                    if emp_name and emp_desg:
                        new_payroll = pd.DataFrame([{"Date": sal_date.strftime("%Y-%m-%d"), "Staff Name": emp_name, "Designation": emp_desg, "Salary Type": sal_class, "Amount Paid (BDT)": sal_value}])
                        st.session_state.salary_db = pd.concat([st.session_state.salary_db, new_payroll], ignore_index=True)
                        save_permanent_database()
                        st.success("Salary log successfully pushed.")
                        st.rerun()

# ----------------------------------------------------------------------------------
# INVENTORY MANAGEMENT
# ----------------------------------------------------------------------------------
elif choice == "📦 Inventory & Restock":
    st.title("📦 Raw Material Supply Pipeline Depth Ledger")
    df_inv_ledger = st.session_state.inventory_db.copy()
    st.dataframe(df_inv_ledger, use_container_width=True)
    
    if not is_partner:
        with st.form("restock_pipeline_form", clear_on_submit=True):
            raw_sel = st.selectbox("Identify Target Raw Stock Node", df_inv_ledger["Material Name"].values)
            stock_delta = st.number_input("Inward Supply Volume Intake (+ Quantity)", min_value=0.0, step=5.0)
            if st.form_submit_button("Recompute Target Pipeline Volumetric Balances"):
                st.session_state.inventory_db.loc[st.session_state.inventory_db["Material Name"] == raw_sel, "Current Stock"] += stock_delta
                save_permanent_database()
                st.success("Supply pipeline capacity expanded.")
                st.rerun()

# ----------------------------------------------------------------------------------
# DROPDOWN CONTROL PANEL + SHOP ADDRESS SETUP
# ----------------------------------------------------------------------------------
elif choice == "⚙️ Dropdown Control Panel":
    st.title("⚙️ Infrastructure Configuration Dropdown Options Control")
    
    tab_set, tab_m1, tab_m2, tab_m5 = st.tabs(["🏢 Shop Identity Settings", "Food Menu Items Array", "Partners Validation Matrix", "Raw Inventory Elements"])
    
    with tab_set:
        st.markdown("### Update Shop Identity Metadata Layout (Invoice Header)")
        s_name_input = st.text_input("Registered Enterprise Name Header Context", value=st.session_state.shop_name)
        s_addr_input = st.text_area("Physical Branch/Store Address String Context", value=st.session_state.shop_address)
        if st.button("Save Shop Settings Parameters ✅"):
            st.session_state.shop_name = s_name_input.strip()
            st.session_state.shop_address = s_addr_input.strip()
            save_permanent_database()
            st.success("Shop branding configurations updated permanently across modules!")
            st.rerun()

    with tab_m1:
        st.write("Food Roster Mapping:", st.session_state.menu_items)
        new_f_item = st.text_input("Enter New Variant String to Append", key="add_food").strip()
        if st.button("Save/Append Food Menu Product"):
            if new_f_item and new_f_item not in st.session_state.menu_items:
                st.session_state.menu_items.append(new_f_item)
                save_permanent_database()
                st.success("Product element wired.")
                st.rerun()

    with tab_m2:
        st.write("Current Partners List Base:", st.session_state.partner_list)
        new_p_node = st.text_input("Add New Partner Name Element", key="add_p").strip()
        if st.button("Publish Partner Roster Allocation"):
            if new_p_node and new_p_node not in st.session_state.partner_list:
                st.session_state.partner_list.append(new_p_node)
                new_r = pd.DataFrame([{"Partner Name": new_p_node, "Investment Amount": 0.0}])
                st.session_state.partners_db = pd.concat([st.session_state.partners_db, new_r], ignore_index=True)
                save_permanent_database()
                st.success("New structural entity partner tracked.")
                st.rerun()

    with tab_m5:
        st.write("Current Inventory Items:", st.session_state.inventory_items)
        new_i_node = st.text_input("Add New Raw Inventory Material Item Context", key="add_i").strip()
        if st.button("Append Sourcing Material Descriptor Item"):
            if new_i_node and new_i_node not in st.session_state.inventory_items:
                st.session_state.inventory_items.append(new_i_node)
                new_inv_r = pd.DataFrame([{"Material Name": new_i_node, "Current Stock": 0.0, "Unit": "Kg/Ltr", "Alert Level": 10.0}])
                st.session_state.inventory_db = pd.concat([st.session_state.inventory_db, new_inv_r], ignore_index=True)
                save_permanent_database()
                st.success("Inventory node linked.")
                st.rerun()

# ----------------------------------------------------------------------------------
# SYSTEM USER PROVISIONING MANAGEMENT (FIXED MULTI-SAVE PIPELINE)
# ----------------------------------------------------------------------------------
elif choice == "👥 System User Provisioning":
    st.title("👥 Application Identity Access Profiles Matrix Provisioning")
    
    u_df = pd.DataFrame([{"System Login Identifier Context": k, "Privilege Access Group Matrix": v["role"], "Password Auth Token Block": v["password"]} for k, v in st.session_state.users_db.items()])
    st.dataframe(u_df, use_container_width=True)
    
    if len(st.session_state.users_db) > 1:
        user_to_del = st.selectbox("Select Account ID to Delete/Revoke Access Matrix 🗑️", [u for u in st.session_state.users_db.keys() if u != "superadmin"])
        if st.button("Confirm Deletion/Removal of User"):
            del st.session_state.users_db[user_to_del]
            save_permanent_database()
            st.success(f"Identity profile context for user root '{user_to_del}' deleted.")
            st.rerun()
            
    with st.form("iam_form", clear_on_submit=True):
        st.markdown("### Provision New Profile / Update Existing Password Matrix")
        reg_id = st.text_input("Account Username / User ID (Case-Insensitive String)").strip().lower()
        reg_pass = st.text_input("Auth Token Key Password (New Registration / Overwrite Update)", type="password")
        reg_role = st.selectbox("Access Group Privileges Assignment", ["Super Admin", "Admin", "Partner (View Only)"])
        
        if st.form_submit_button("Commit Profile / Update Password Token ✅"):
            if reg_id and reg_pass:
                st.session_state.users_db[reg_id] = {"password": reg_pass, "role": reg_role}
                save_permanent_database()
                st.success(f"Success! User account mapping configurations saved permanently to database cloud storage layer! 💾")
                st.rerun()
            else:
                st.error("Validation Error: Profile Identity rows and tokens cannot stay null.")