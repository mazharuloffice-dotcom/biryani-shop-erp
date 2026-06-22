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

# CRITICAL SALARY DATAFRAME RECOVERY FORMAT FIXED
if 'salary_db' not in st.session_state:
    s_records = disk_data.get("salary_db", [])
    st.session_state.salary_db = pd.DataFrame(s_records) if s_records else pd.DataFrame(columns=["Date", "Staff Name", "Designation", "Salary Type", "Amount Paid (BDT)"])

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

user_allowed_menus = st.session_state.users_db.get(st.session_state.logged_in_user, {}).get("permissions", ALL_AVAILABLE_MENUS)

st.sidebar.markdown("---")
st.sidebar.title("📁 ERP Navigation")
filtered_menu_options = [m for m in ALL_AVAILABLE_MENUS if m in user_allowed_menus]
if not filtered_menu_options:
    st.sidebar.error("No Menu Permissions Configured.")
    st.stop()

choice = st.sidebar.radio("Navigate to module:", filtered_menu_options)

# ----------------------------------------------------------------------------------
# MODULES IMPLEMENTATION
# ----------------------------------------------------------------------------------
if choice == "📊 Financial Dashboard":
    st.title("📊 Month-Wise Enterprise Financial Analytics")
    available_months = ["All Time"]
    if len(st.session_state.sales_records) > 0:
        available_months.extend(st.session_state.sales_records["Month-Year"].unique().tolist())
    selected_month = st.selectbox("📅 Select Target Month", available_months)
    
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
    kpi1.metric("Sales Revenue", f"{m_sales:,.2f} BDT")
    kpi2.metric("Total Expenses Outflow", f"{m_outflow:,.2f} BDT")
    kpi3.metric("Net Profit / Loss", f"{m_net_profit_loss:,.2f} BDT")

elif choice == "📈 Advanced Report Manager":
    st.title("📈 Strategic Cross-Module Multi-Report Manager Engine")
    rep_tab1, rep_tab2, rep_tab3 = st.tabs(["Sales Journal Ledger", "Variable Material Sourcing", "Staff Payroll Distributions"])
    with rep_tab1:
        st.dataframe(st.session_state.sales_records, use_container_width=True)
    with rep_tab2:
        st.dataframe(st.session_state.variable_bazar, use_container_width=True)
    with rep_tab3:
        st.dataframe(st.session_state.salary_db, use_container_width=True)

elif choice == "🧾 Digital Invoice Generator":
    st.title("🧾 Interactive Point of Sale (POS) Invoice Generator")
    inv_item = st.selectbox("Product Line Item Context", st.session_state.menu_items)
    inv_rate = st.number_input("Unit Price Base (BDT)", min_value=0.0, value=220.0)
    inv_qty = st.number_input("Billed Quantity Count", min_value=1, value=1)
    st.write(f"Gross Bill: {inv_rate * inv_qty} BDT")

elif choice == "🤝 Partner Capital Engine":
    st.title("🤝 Capital Allocations & Fixed Infrastructure Investments")
    st.dataframe(st.session_state.partners_db, use_container_width=True)

elif choice == "💰 Daily Sales Entry":
    st.title("💰 High-Frequency Point of Sale Intake Interface")
    with st.form("sales_form", clear_on_submit=True):
        prod_sel = st.selectbox("Product", st.session_state.menu_items)
        p_rate = st.number_input("Rate per Plate", min_value=0.0, value=220.0)
        p_qty = st.number_input("Plates Sold", min_value=1, value=1)
        p_date = st.date_input("Posting Date", datetime.now())
        if st.form_submit_button("Post Sales Entry"):
            new_s = pd.DataFrame([{"Date": p_date.strftime("%Y-%m-%d"), "Month-Year": get_month_year_str(p_date), "Item Name": prod_sel, "Rate per Plate": p_rate, "Total Plates": p_qty, "Adjustment": 0.0, "Net Total": p_rate * p_qty}])
            st.session_state.sales_records = pd.concat([st.session_state.sales_records, new_s], ignore_index=True)
            save_permanent_database()
            st.success("Sales entry recorded permanently!")
            st.rerun()

elif choice == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Variable Material Sourcing Cost Ledger")
    with st.form("bazar_form", clear_on_submit=True):
        mat_select = st.selectbox("Bazar Item", st.session_state.inventory_items)
        mat_qty = st.text_input("Quantity/Weight", value="10 Kg")
        mat_cost = st.number_input("Total Cost (BDT)", min_value=0.0)
        mat_date = st.date_input("Date", datetime.now())
        if st.form_submit_button("Post Bazar Cost"):
            new_b = pd.DataFrame([{"Date": mat_date.strftime("%Y-%m-%d"), "Bazar Item Name": mat_select, "Quantity/Weight": mat_qty, "Total Cost (BDT)": mat_cost, "Purchased By": st.session_state.logged_in_user}])
            st.session_state.variable_bazar = pd.concat([st.session_state.variable_bazar, new_b], ignore_index=True)
            save_permanent_database()
            st.success("Bazar entry saved permanently!")
            st.rerun()

elif choice == "💼 Monthly Expenses":
    st.title("💼 Identify Expense Classification Portal")
    with st.form("exp_form", clear_on_submit=True):
        m_cat = st.selectbox("Category", st.session_state.expense_categories)
        m_memo = st.text_input("Particulars Memo")
        m_val = st.number_input("Amount (BDT)", min_value=0.0)
        m_date = st.date_input("Date", datetime.now())
        if st.form_submit_button("Publish Entry"):
            new_e = pd.DataFrame([{"Date": m_date.strftime("%Y-%m-%d"), "Category": m_cat, "Particulars": m_memo, "Amount (BDT)": m_val}])
            st.session_state.monthly_expenses_db = pd.concat([st.session_state.monthly_expenses_db, new_e], ignore_index=True)
            save_permanent_database()
            st.success("Expense log updated permanently!")
            st.rerun()

# ----------------------------------------------------------------------------------
# CRITICAL FIX: WORKFORCE MANAGEMENT AND PAYROLL LOGGING SYSTEM
# ----------------------------------------------------------------------------------
elif choice == "🧑‍🍳 Staff Salary Ledger":
    st.title("🧑‍🍳 Advanced Workforce Directory & Payroll Systems")
    
    tab_pay1, tab_pay2 = st.tabs(["💰 Salary Matrix Payroll Distributions Logs", "👥 Comprehensive Employee Profiles Directory"])
    
    with tab_pay2:
        st.markdown("### 📝 Register Complete Employee Profile Bundle")
        col_e1, col_e2 = st.columns([2, 1])
        with col_e1:
            with st.form("emp_profile_form", clear_on_submit=True):
                e_name = st.text_input("Employee Full Name").strip()
                e_father = st.text_input("Father's Name").strip()
                e_mob = st.text_input("Mobile Contact Number").strip()
                e_nid = st.text_input("National ID (NID) Number").strip()
                e_addr = st.text_area("Address Details").strip()
                e_desg = st.text_input("Designation / System Role").strip()
                e_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
                
                if st.form_submit_button("Save Employee Profile Array ✅"):
                    if e_name and e_mob:
                        pic_base64 = ""
                        if e_pic is not None:
                            pic_base64 = base64.b64encode(e_pic.read()).decode()
                        
                        st.session_state.employees_profiles[e_name] = {
                            "father": e_father, "mobile": e_mob, "nid": e_nid, "address": e_addr, "designation": e_desg, "photo": pic_base64
                        }
                        save_permanent_database()
                        st.success(f"Success! Profile for '{e_name}' successfully added.")
                        st.rerun()
                        
        with col_e2:
            st.markdown("### 👥 View Profile Documents")
            if st.session_state.employees_profiles:
                view_emp = st.selectbox("Select Profile", list(st.session_state.employees_profiles.keys()))
                prof = st.session_state.employees_profiles[view_emp]
                if prof.get("photo"):
                    st.image(base64.b64decode(prof["photo"]), width=150)
                st.write(f"**Role:** {prof['designation']}")
                st.write(f"**Mobile:** {prof['mobile']}")
                if st.button("Delete Profile 🗑️"):
                    del st.session_state.employees_profiles[view_emp]
                    save_permanent_database()
                    st.success("Profile deleted.")
                    st.rerun()

    with tab_pay1:
        st.markdown("### 📊 Active Payroll Distribution Records")
        
        # Display logs table clearly
        if len(st.session_state.salary_db) > 0:
            st.dataframe(st.session_state.salary_db, use_container_width=True)
            
            # Inline Row Delete System
            sal_del_idx = st.selectbox("Select Row Index to Delete", st.session_state.salary_db.index, key="sal_del_select")
            if st.button("Delete Selected Salary Entry 🗑️"):
                st.session_state.salary_db = st.session_state.salary_db.drop(sal_del_idx).reset_index(drop=True)
                save_permanent_database()
                st.success("Salary log dropped successfully.")
                st.rerun()
        else:
            st.info("No payroll distribution transactions found on disk.")
            
        # FIXED: Daily and Monthly Salary Paid submission block
        if not is_partner and st.session_state.employees_profiles:
            st.markdown("---")
            st.markdown("### 💸 Post New Wage/Salary Payment Entry")
            with st.form("payroll_form_direct", clear_on_submit=True):
                emp_name_sel = st.selectbox("Select Paid Employee", list(st.session_state.employees_profiles.keys()))
                sal_class = st.selectbox("Salary Matrix Type Class", ["Daily Wages Salary", "Monthly Regular Salary"])
                sal_value = st.number_input("Disbursed Cash Compensation Amount (BDT)", min_value=0.0, step=100.0)
                sal_date = st.date_input("Disbursement Date", datetime.now())
                
                if st.form_submit_button("Confirm Payment & Log Entry ✅"):
                    mapped_desg = st.session_state.employees_profiles[emp_name_sel]["designation"]
                    
                    # Construct matching dictionary object structure
                    new_payroll = pd.DataFrame([{
                        "Date": sal_date.strftime("%Y-%m-%d"),
                        "Staff Name": emp_name_sel,
                        "Designation": mapped_desg,
                        "Salary Type": sal_class,
                        "Amount Paid (BDT)": float(sal_value)
                    }])
                    
                    # Concat & Hard-save instantly
                    st.session_state.salary_db = pd.concat([st.session_state.salary_db, new_payroll], ignore_index=True)
                    save_permanent_database()
                    st.success(f"Success! {sal_class} of {sal_value} BDT to {emp_name_sel} has been safely saved!")
                    st.rerun()
        elif not st.session_state.employees_profiles:
            st.warning("⚠️ Form Locked: Please add at least 1 employee profile in the second tab first.")

elif choice == "📦 Inventory & Restock":
    st.title("📦 Raw Material Supply Pipeline Depth Ledger")
    st.dataframe(st.session_state.inventory_db, use_container_width=True)

elif choice == "⚙️ Dropdown Control Panel":
    st.title("⚙️ Dropdown Matrix Configurations Control Hub")
    st.write("Food Roster:", st.session_state.menu_items)

elif choice == "👥 System User Provisioning":
    st.title("👥 Application Identity Access Profiles Matrix Provisioning")
    with st.form("user_form"):
        reg_id = st.text_input("User ID").strip().lower()
        reg_pass = st.text_input("Password", type="password")
        if st.form_submit_button("Save User"):
            if reg_id and reg_pass:
                st.session_state.users_db[reg_id] = {"password": reg_pass, "role": "Admin", "permissions": ALL_AVAILABLE_MENUS}
                save_permanent_database()
                st.success("User added permanently.")
                st.rerun()