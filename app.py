import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import json
import os

# ----------------------------------------------------------------------------------
# 1. CORE ENTERPRISE SYSTEM CONFIGURATION & LOOK
# ----------------------------------------------------------------------------------
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP Premium v5.1", page_icon="🍲", layout="wide")

# Premium Dynamic Corporate CSS Style Injection
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    h1, h2, h3, h4 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700; color: #1E293B; }
    .kpi-container { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 25px; }
    .kpi-card {
        flex: 1; min-width: 220px; background: #FFFFFF; padding: 20px; 
        border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #D35400; transition: all 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
    .kpi-title { font-size: 11px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 24px; color: #0F172A; font-weight: 700; margin-top: 6px; }
    .sidebar-brand { text-align: center; background: linear-gradient(135deg, #D35400, #E67E22); color: white; padding: 18px; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { border-radius: 6px; font-weight: 600; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: 600; color: #475569; }
    .stTabs [data-baseweb="tab"]:hover { color: #D35400; }
    .stTabs [aria-selected="true"] { color: #D35400 !important; border-color: #D35400 !important; }
    .invoice-box { background: #FFF; padding: 30px; border: 1px solid #E2E8F0; border-radius: 8px; font-family: monospace; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "swapnajatra_enterprise_v5_db.json"

# ----------------------------------------------------------------------------------
# 2. HOLISTIC FILE DATABASE SYSTEMS (CRUD CORE)
# ----------------------------------------------------------------------------------
def load_erp_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def commit_erp_database():
    payload = {
        "users": st.session_state.erp_users,
        "privileges": st.session_state.erp_privileges,
        "dropdowns": st.session_state.erp_dropdowns,
        "partners": st.session_state.erp_partners,
        "employees": st.session_state.erp_employees,
        "attendance": st.session_state.erp_attendance,
        "leaves": st.session_state.erp_leaves,
        "sales": st.session_state.sales_ledger.to_dict(orient="records"),
        "bazar": st.session_state.bazar_ledger.to_dict(orient="records"),
        "expenses": st.session_state.monthly_expenses.to_dict(orient="records"),
        "payroll": st.session_state.payroll_ledger.to_dict(orient="records"),
        "inventory": st.session_state.inventory_master.to_dict(orient="records")
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)

db_snapshot = load_erp_database()

# ----------------------------------------------------------------------------------
# 3. GLOBAL MASTER STATE MANAGEMENT SYSTEM
# ----------------------------------------------------------------------------------
if "erp_users" not in st.session_state: 
    st.session_state.erp_users = db_snapshot.get("users", {
        "superadmin": {"password": "MiB@#32!", "role": "Super Admin"},
        "manager": {"password": "MngrBari789", "role": "Manager"},
        "partner": {"password": "PrtnrPool456", "role": "Partner"}
    })

ALL_SYSTEM_MENUS = [
    "🏠 Main Dashboard", "👨‍💼 Employee Register", "📅 Attendance System", 
    "📝 Leave Management", "🧾 Digital Invoice Generator", "🤝 Partner Capital Engine", 
    "💰 Daily Sales Entry", "🛒 Variable Bazar Cost", "💼 Monthly Expenses", 
    "🧑‍🍳 Staff Salary Ledger", "📦 Inventory & Restock", "⚙️ Dropdown Control Panel", 
    "🛡️ System User Provisioning", "👁️ Partner Preview Mode", "🔐 Account Security Hub"
]

if "erp_privileges" not in st.session_state:
    st.session_state.erp_privileges = db_snapshot.get("privileges", {
        "Super Admin": ALL_SYSTEM_MENUS,
        "Manager": ["🏠 Main Dashboard", "📅 Attendance System", "📝 Leave Management", "🧾 Digital Invoice Generator", "💰 Daily Sales Entry", "🛒 Variable Bazar Cost", "📦 Inventory & Restock"],
        "Partner": ["👁️ Partner Preview Mode"]
    })

if "erp_dropdowns" not in st.session_state:
    st.session_state.erp_dropdowns = db_snapshot.get("dropdowns", {
        "shifts": ["Day Shift", "Night Shift"],
        "dishes": ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"],
        "suppliers": ["Mayer Doa Rice Agency", "Dhaka Meat House", "Karwan Bazar Traders"],
        "expense_categories": ["Shop Rent", "Electricity Bill", "Gas Bill", "Water Bill", "Internet", "Cleaning", "Marketing"],
        "departments": ["Kitchen Crew", "Front Desk Management", "Delivery Operations", "Accounts & Audit"],
        "designations": ["Head Chef", "Assistant Chef", "Cashier", "Store Keeper", "Senior Server"],
        "employment_status": ["Permanent", "Probationary", "Part-Time"]
    })

if "erp_partners" not in st.session_state:
    st.session_state.erp_partners = db_snapshot.get("partners", {
        "Foishal": {"capital": 500000.0, "profit_pct": 0.0},
        "Anam": {"capital": 300000.0, "profit_pct": 0.0},
        "Habib": {"capital": 200000.0, "profit_pct": 0.0},
        "Anayat": {"capital": 200000.0, "profit_pct": 0.0}
    })

if "erp_employees" not in st.session_state: st.session_state.erp_employees = db_snapshot.get("employees", {})
if "erp_attendance" not in st.session_state: st.session_state.erp_attendance = db_snapshot.get("attendance", [])
if "erp_leaves" not in st.session_state: st.session_state.erp_leaves = db_snapshot.get("leaves", [])

# DataFrames Persistence Integration
if "sales_ledger" not in st.session_state: st.session_state.sales_ledger = pd.DataFrame(db_snapshot.get("sales", []), columns=["ID", "Date", "Month-Year", "Shift", "Product Name", "Quantity", "Rate", "Payment Method", "Net Total"])
if "bazar_ledger" not in st.session_state: st.session_state.bazar_ledger = pd.DataFrame(db_snapshot.get("bazar", []), columns=["ID", "Date", "Supplier", "Item Category", "Quantity", "Unit Price", "Total Cost"])
if "monthly_expenses" not in st.session_state: st.session_state.monthly_expenses = pd.DataFrame(db_snapshot.get("expenses", []), columns=["ID", "Date", "Category", "Amount", "Description"])
if "payroll_ledger" not in st.session_state: st.session_state.payroll_ledger = pd.DataFrame(db_snapshot.get("payroll", []), columns=["ID", "Date", "Employee ID", "Name", "Designation", "Base Salary", "Bonus", "Deductions", "Net Disbursed"])
if "inventory_master" not in st.session_state:
    st.session_state.inventory_master = pd.DataFrame(db_snapshot.get("inventory", []), columns=["ID", "Material Name", "Category", "Stock", "Unit", "Min Alert"]) if db_snapshot.get("inventory", []) else pd.DataFrame([
        {"ID": 101, "Material Name": "Miniket Rice", "Category": "Rice", "Stock": 250.0, "Unit": "Kg", "Min Alert": 50.0},
        {"ID": 102, "Material Name": "Beef Meat", "Category": "Meat", "Stock": 120.0, "Unit": "Kg", "Min Alert": 30.0},
        {"ID": 103, "Material Name": "Polao Rice", "Category": "Rice", "Stock": 180.0, "Unit": "Kg", "Min Alert": 40.0}
    ])

# ----------------------------------------------------------------------------------
# AUTO CALCULATION ENGINE FOR PARTNER PROFIT SHARE RATIO
# ----------------------------------------------------------------------------------
total_equity_pool_calc = sum(p["capital"] for p in st.session_state.erp_partners.values())
for p_key in st.session_state.erp_partners.keys():
    if total_equity_pool_calc > 0:
        st.session_state.erp_partners[p_key]["profit_pct"] = (st.session_state.erp_partners[p_key]["capital"] / total_equity_pool_calc) * 100
    else:
        st.session_state.erp_partners[p_key]["profit_pct"] = 0.0

# ----------------------------------------------------------------------------------
# 4. SYSTEM INITIAL SECURITY BLOCK (AUTHENTICATION GATEWAY)
# ----------------------------------------------------------------------------------
if "current_user" not in st.session_state:
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.session_state.preview_mode = False

if st.session_state.current_user is None:
    _, auth_col, _ = st.columns([1.2, 1.3, 1.2])
    with auth_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.form("enterprise_gateway_form"):
            st.markdown("<h2 style='text-align: center; color:#D35400;'>🍲 Swapnajatra ERP Login</h2>", unsafe_allow_html=True)
            u_id = st.text_input("Username ID Key").strip().lower() 
            u_pw = st.text_input("Password Token ID", type="password")
            if st.form_submit_button("Initialize Enterprise Core Engine", use_container_width=True):
                if u_id in st.session_state.erp_users and st.session_state.erp_users[u_id]["password"] == u_pw:
                    st.session_state.current_user = u_id
                    st.session_state.current_role = st.session_state.erp_users[u_id]["role"]
                    st.session_state.preview_mode = False
                    st.success("Core Security Matrix Cleared!")
                    st.rerun()
                else:
                    st.error("Invalid Security ID Credentials Matrix Combination.")
        st.stop()

# ----------------------------------------------------------------------------------
# 5. DYNAMIC ACCESS CONFIGURATION ARCHITECTURE
# ----------------------------------------------------------------------------------
t_gross_sales = st.session_state.sales_ledger["Net Total"].sum() if len(st.session_state.sales_ledger) > 0 else 0.0
t_bazar_outflow = st.session_state.bazar_ledger["Total Cost"].sum() if len(st.session_state.bazar_ledger) > 0 else 0.0
t_expense_outflow = st.session_state.monthly_expenses["Amount"].sum() if len(st.session_state.monthly_expenses) > 0 else 0.0
t_payroll_outflow = st.session_state.payroll_ledger["Net Disbursed"].sum() if len(st.session_state.payroll_ledger) > 0 else 0.0

total_expenses_calc = t_bazar_outflow + t_expense_outflow + t_payroll_outflow
net_corporate_profit_calc = t_gross_sales - total_expenses_calc

user_role_node = st.session_state.current_role
permitted_navigation_nodes = st.session_state.erp_privileges.get(user_role_node, [])

st.sidebar.markdown(f'<div class="sidebar-brand"><h4>Swapnajatra v5.1 Pro</h4></div>', unsafe_allow_html=True)
with st.sidebar.container(border=True):
    st.markdown(f"👤 **User:** `{st.session_state.current_user.upper()}`")
    st.markdown(f"🛡️ **Group Security:** `{user_role_node}`")
    if st.sidebar.button("Term Session 🚪", use_container_width=True):
        st.session_state.current_user = None
        st.rerun()

active_menu_node = st.sidebar.radio("🗂️ System Navigation Panels", [m for m in ALL_SYSTEM_MENUS if m in permitted_navigation_nodes])

if st.session_state.preview_mode or active_menu_node == "👁️ Partner Preview Mode":
    is_editable = False
    st.info("ℹ️ Partner Read-Only Preview Simulation Architecture Engine Active. Data Mutation Suspended.")
else:
    is_editable = True

def trigger_mutation_success():
    commit_erp_database()
    st.success("✅ Ledger State Operations Mutation Sync Complete.")
    st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 1: MAIN DASHBOARD CORE
# ----------------------------------------------------------------------------------
if active_menu_node == "🏠 Main Dashboard" or active_menu_node == "👁️ Partner Preview Mode":
    st.markdown("## 🏠 Corporate Metrics Master Control Dashboard")
    st.markdown("---")
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-title">Total Gross Revenue</div><div class="kpi-value">{t_gross_sales:,.2f} ৳</div></div>
        <div class="kpi-card" style="border-top-color:#C0392B;"><div class="kpi-title">Total System Expenses</div><div class="kpi-value">{total_expenses_calc:,.2f} ৳</div></div>
        <div class="kpi-card" style="border-top-color:{'#27AE60' if net_corporate_profit_calc >= 0 else '#C0392B'};">
            <div class="kpi-title">Net Corporate Profit</div>
            <div class="kpi-val" style="font-size:24px; font-weight:700; margin-top:6px; color:{'#27AE60' if net_corporate_profit_calc >= 0 else '#C0392B'};">{net_corporate_profit_calc:,.2f} ৳</div>
        </div>
        <div class="kpi-card" style="border-top-color:#2980B9;"><div class="kpi-title">Total Capital Equity Pool</div><div class="kpi-value">{total_equity_pool_calc:,.2f} ৳</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("### 📊 Expense Allocation Framework Matrix")
        if total_expenses_calc > 0:
            fig_p = px.pie(names=["Bazar Cost", "Overheads Operational", "Wages Ledger"], values=[t_bazar_outflow, t_expense_outflow, t_payroll_outflow], hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_p, use_container_width=True)
        else: st.info("No expense allocation logs found in system context pipeline.")
        
    with col_g2:
        st.markdown("### 📈 Revenue Intake Stream Chronology")
        if len(st.session_state.sales_ledger) > 0:
            df_g = st.session_state.sales_ledger.groupby("Date")["Net Total"].sum().reset_index()
            fig_l = px.line(df_g, x="Date", y="Net Total", markers=True, color_discrete_sequence=["#D35400"])
            st.plotly_chart(fig_l, use_container_width=True)
        else: st.info("Chronology pipeline data fields empty.")
        
    st.markdown("### 🤝 Month-Wise Partner Investment & Profit/Loss Yield Structure")
    p_data_rows = []
    for p_name, p_info in st.session_state.erp_partners.items():
        partner_share_val = (p_info["profit_pct"] / 100) * net_corporate_profit_calc
        p_data_rows.append({
            "Shareholder Partner": p_name,
            "Investment Balance": f"{p_info['capital']:,.2f} ৳",
            "Auto Allocated Profit Percent": f"{p_info['profit_pct']:.2f} %",
            "Current Month Share Yield Amount": f"{partner_share_val:,.2f} ৳"
        })
    st.table(pd.DataFrame(p_data_rows))

# ----------------------------------------------------------------------------------
# MODULE 2: EMPLOYEE REGISTER
# ----------------------------------------------------------------------------------
elif active_menu_node == "👨‍💼 Employee Register" and is_editable:
    st.markdown("## 👨‍💼 Corporate Human Resources Onboarding Terminal")
    st.markdown("---")
    tab_e1, tab_e2 = st.tabs(["➕ Register New Corporate Profile", "📋 Manage Stored Profiles"])
    
    with tab_e1:
        with st.form("hr_onboarding_terminal", clear_on_submit=True):
            ce1, ce2 = st.columns(2)
            with ce1:
                e_id = st.text_input("Employee ID Key (Unique)").strip()
                e_name = st.text_input("Full Employee Legal Name").strip()
                e_fname = st.text_input("Father's Name").strip()
                e_mname = st.text_input("Mother's Name").strip()
                e_dob = st.date_input("Date of Birth", date(2000, 1, 1))
                e_gen = st.selectbox("Gender Group", ["Male", "Female", "Other"])
                e_mob = st.text_input("Primary Mobile Connection").strip()
            with ce2:
                e_addr = st.text_area("Complete Legal Residential Address").strip()
                e_nid = st.text_input("National ID Card (NID) Token").strip()
                e_jdate = st.date_input("Corporate Onboarding Joining Date", date.today())
                e_desg = st.selectbox("Designation Mapping", st.session_state.erp_dropdowns["designations"])
                e_dept = st.selectbox("Department Allocation Unit", st.session_state.erp_dropdowns["departments"])
                e_sal_d = st.number_input("Salary Daily Base (৳)", min_value=0.0)
                e_sal_m = st.number_input("Salary Monthly Fixed Yield (৳)", min_value=0.0)
                e_stat = st.selectbox("Employment Workflow Status Type", st.session_state.erp_dropdowns["employment_status"])
                
            if st.form_submit_button("Commit & Persist HR Profile"):
                if e_id and e_name and e_nid:
                    st.session_state.erp_employees[e_id] = {
                        "name": e_name, "father": e_fname, "mother": e_mname, "dob": str(e_dob), "gender": e_gen,
                        "mobile": e_mob, "address": e_addr, "nid": e_nid, "joining_date": str(e_jdate),
                        "designation": e_desg, "department": e_dept, "salary_daily": e_sal_d, "salary_monthly": e_sal_m,
                        "status": e_stat
                    }
                    trigger_mutation_success()
                else: st.error("Validation Error: ID, Full Name, and NID are required.")
                
    with tab_e2:
        if st.session_state.erp_employees:
            select_e_id = st.selectbox("Identify Target Employee Profile Record Pointer", list(st.session_state.erp_employees.keys()))
            emp_rec = st.session_state.erp_employees[select_e_id]
            with st.form("hr_mutation_form"):
                me1, me2 = st.columns(2)
                with me1:
                    m_name = st.text_input("Full Name Change Value", value=emp_rec["name"])
                    m_mob = st.text_input("Mobile System Key Data String", value=emp_rec["mobile"])
                    m_desg = st.selectbox("Target Designation", st.session_state.erp_dropdowns["designations"], index=st.session_state.erp_dropdowns["designations"].index(emp_rec["designation"]) if emp_rec["designation"] in st.session_state.erp_dropdowns["designations"] else 0)
                with me2:
                    m_sal_d = st.number_input("Daily Wage Struct Target Base", value=float(emp_rec["salary_daily"]))
                    m_sal_m = st.number_input("Monthly Wage Target Struct Base", value=float(emp_rec["salary_monthly"]))
                    m_stat = st.selectbox("Target Pipeline Lifecycle Status", st.session_state.erp_dropdowns["employment_status"], index=st.session_state.erp_dropdowns["employment_status"].index(emp_rec["status"]) if emp_rec["status"] in st.session_state.erp_dropdowns["employment_status"] else 0)
                    
                col_eb1, col_eb2 = st.columns(2)
                with col_eb1:
                    if st.form_submit_button("Update HR Master Profile Registry", type="primary"):
                        st.session_state.erp_employees[select_e_id].update({"name": m_name, "mobile": m_mob, "designation": m_desg, "salary_daily": m_sal_d, "salary_monthly": m_sal_m, "status": m_stat})
                        trigger_mutation_success()
                with col_eb2:
                    if st.form_submit_button("Purge Employee Record Block Entirely"):
                        st.session_state.erp_employees.pop(select_e_id)
                        trigger_mutation_success()
        else: st.info("Human Capital Profile Register is empty.")

# ----------------------------------------------------------------------------------
# MODULE 3: ATTENDANCE MANAGEMENT ENGINE
# ----------------------------------------------------------------------------------
elif active_menu_node == "📅 Attendance System" and is_editable:
    st.markdown("## 📅 High-Velocity Attendance Terminal Engine")
    st.markdown("---")
    if not st.session_state.erp_employees: st.warning("Human capital records register is empty."); st.stop()
    
    col_at1, col_at2 = st.columns([1, 2])
    with col_at1:
        with st.form("attendance_journal_gate", clear_on_submit=True):
            att_emp = st.selectbox("Target Identity Roster Profile", list(st.session_state.erp_employees.keys()), format_func=lambda x: f"{st.session_state.erp_employees[x]['name']} ({x})")
            att_d = st.date_input("Attendance Log Date Entry", date.today())
            att_in = st.time_input("Check-In Timestamp", datetime.now().time())
            att_out = st.time_input("Check-Out Timestamp", datetime.now().time())
            if st.form_submit_button("Save Attendance Record", use_container_width=True):
                st.session_state.erp_attendance.append({
                    "Index_ID": len(st.session_state.erp_attendance) + 1000, "Employee ID": att_emp, "Name": st.session_state.erp_employees[att_emp]["name"],
                    "Date": str(att_d), "Check In": str(att_in), "Check Out": str(att_out)
                })
                trigger_mutation_success()
    with col_at2:
        if st.session_state.erp_attendance:
            df_att = pd.DataFrame(st.session_state.erp_attendance)
            st.dataframe(df_att, use_container_width=True)
            with st.form("attendance_mutation_purge_gate"):
                target_idx = st.selectbox("Identify Log Reference Index Key", df_att["Index_ID"].tolist())
                if st.form_submit_button("Purge Selected Shift Log Row Component Block", type="primary"):
                    st.session_state.erp_attendance = [r for r in st.session_state.erp_attendance if r["Index_ID"] != target_idx]
                    trigger_mutation_success()
        else: st.info("Attendance journals database is empty.")

# ----------------------------------------------------------------------------------
# MODULE 4: LEAVE MANAGEMENT LAYER
# ----------------------------------------------------------------------------------
elif active_menu_node == "📝 Leave Management" and is_editable:
    st.markdown("## 📝 Employee Leave Management Framework")
    st.markdown("---")
    if not st.session_state.erp_employees: st.warning("Human capital records register empty."); st.stop()
    
    col_lv1, col_lv2 = st.columns([1, 2])
    with col_lv1:
        with st.form("leave_entry_terminal_gate", clear_on_submit=True):
            lv_emp = st.selectbox("Target Identity Roster Profile", list(st.session_state.erp_employees.keys()), format_func=lambda x: f"{st.session_state.erp_employees[x]['name']} ({x})")
            lv_start = st.date_input("Exclusion Start Date", date.today())
            lv_end = st.date_input("Exclusion Concluding Target Date", date.today())
            lv_type = st.selectbox("Leave Metric Type Sourcing Matrix", ["Sick Leave", "Casual Leave", "Earned Leave", "Unpaid Leave"])
            if st.form_submit_button("Commit Leave Ledger Records", use_container_width=True):
                st.session_state.erp_leaves.append({
                    "Leave_ID": len(st.session_state.erp_leaves) + 5000, "Employee ID": lv_emp, "Name": st.session_state.erp_employees[lv_emp]["name"],
                    "Start Date": str(lv_start), "End Date": str(lv_end), "Type Asset Class Mapping": lv_type
                })
                trigger_mutation_success()
    with col_lv2:
        if st.session_state.erp_leaves:
            df_lv = pd.DataFrame(st.session_state.erp_leaves)
            st.dataframe(df_lv, use_container_width=True)
            with st.form("leave_mutation_purge_gate"):
                target_lv_idx = st.selectbox("Identify Leave Reference Instance", df_lv["Leave_ID"].tolist())
                if st.form_submit_button("Purge Selected Leave Instance", type="primary"):
                    st.session_state.erp_leaves = [r for r in st.session_state.erp_leaves if r["Leave_ID"] != target_lv_idx]
                    trigger_mutation_success()
        else: st.info("Leave entries database tracking stack empty.")

# ----------------------------------------------------------------------------------
# MODULE 5: DIGITAL INVOICE GENERATOR
# ----------------------------------------------------------------------------------
elif active_menu_node == "🧾 Digital Invoice Generator" and is_editable:
    st.markdown("## 🧾 Smart POS Real-Time Digital Invoice Generator Terminal")
    st.markdown("---")
    col_inv1, col_inv2 = st.columns([1.1, 1])
    with col_inv1:
        with st.form("pos_invoice_live_generator_gate"):
            inv_cx_name = st.text_input("Customer Full Name", value="Walk-In Retail Client")
            inv_cx_phone = st.text_input("Customer Contact Line Number", value="017XXXXXXXX")
            inv_dish = st.selectbox("Product Mapping Dish Selected", st.session_state.erp_dropdowns["dishes"])
            inv_rate = st.number_input("Rate Value per Unit Plate (৳)", min_value=0.0, value=250.0)
            inv_volume = st.number_input("Unit Plate Count Volume Vector Quantity", min_value=1, value=2)
            gross_bill_calc = inv_rate * inv_volume
            if st.form_submit_button("Save POS Bill & Update Sales Ledger", type="primary"):
                fresh_sale_row = pd.DataFrame([{
                    "ID": len(st.session_state.sales_ledger) + 7000, "Date": str(date.today()), "Month-Year": date.today().strftime("%B %Y"),
                    "Shift": "POS Dynamic Entry", "Product Name": inv_dish, "Quantity": inv_volume, "Rate": inv_rate,
                    "Payment Method": "Cash POS Console", "Net Total": gross_bill_calc
                }])
                st.session_state.sales_ledger = pd.concat([st.session_state.sales_ledger, fresh_sale_row], ignore_index=True)
                commit_erp_database()
                st.toast("POS Transaction Committed Successfully!")
    with col_inv2:
        invoice_blueprint_markup = f"""
        <div class="invoice-box">
            <h3 style="text-align:center; color:#D35400; margin:0; font-weight:bold;">SWAPNAJATRA BIRYANI BARI</h3>
            <p style="text-align:center; font-size:12px; color:#64748B; margin:2px 0 15px 0;">Mirpur Sector 10, Dhaka, Bangladesh</p>
            <hr style="border-top:1px dashed #CBD5E1;">
            <b>Invoice Date:</b> {datetime.now().strftime('%Y-%m-%d %I:%M %p')}<br>
            <b>Client Target Ref:</b> {inv_cx_name}<br>
            <b>Contact Line:</b> {inv_cx_phone}<br>
            <hr style="border-top:1px dashed #CBD5E1;">
            <table style="width:100%; font-size:14px; font-family:monospace;">
                <tr style="font-weight:bold;"><td>Description</td><td style="text-align:center;">Qty</td><td style="text-align:right;">Total</td></tr>
                <tr><td>{inv_dish} (@{inv_rate:.2f})</td><td style="text-align:center;">{inv_volume}</td><td style="text-align:right;">{gross_bill_calc:,.2f} ৳</td></tr>
                <tr style="font-weight:bold; font-size:16px; color:#27AE60;"><td colspan="2">Net Cash Collection:</td><td style="text-align:right;">{gross_bill_calc:,.2f} ৳</td></tr>
            </table><br>
            <p style="text-align:center; font-size:12px; font-style:italic; color:#E67E22; margin:0;">Receipt Generated Automated Output. Thank you! 🍲</p>
        </div>
        """
        st.markdown(invoice_blueprint_markup, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# MODULE 6: PARTNER CAPITAL ENGINE (WITH AUTOMATED PERCENTAGE CALCULATION)
# ----------------------------------------------------------------------------------
elif active_menu_node == "🤝 Partner Capital Engine" and is_editable:
    st.markdown("## 🤝 Shareholder Equity Capital & Automated Profit Ratio Engine")
    st.markdown("---")
    st.markdown("### 🏛️ Active Partner Investment Metrics Balance View")
    if st.session_state.erp_partners:
        p_cols = st.columns(len(st.session_state.erp_partners))
        for p_idx, (p_name, p_metrics) in enumerate(st.session_state.erp_partners.items()):
            with p_cols[p_idx]:
                st.metric(label=f"💳 {p_name} Investment Pool", value=f"{p_metrics['capital']:,.2f} ৳", delta=f"{p_metrics['profit_pct']:.2f}% Auto Share")
    else: st.info("No active partner profiles mapped.")
            
    tab_p1, tab_p2 = st.tabs(["⚙️ Handle Existing Partner Matrix", "➕ Add Brand New Partner Entity"])
    with tab_p1:
        if st.session_state.erp_partners:
            with st.form("partner_equity_dropdown_mutation_gate"):
                selected_dropdown_partner = st.selectbox("Identify Target Partner Account Profile (Case-Sensitive Match Node Key)", list(st.session_state.erp_partners.keys()))
                curr_p_data = st.session_state.erp_partners[selected_dropdown_partner]
                p_update_cap = st.number_input("Adjust Investment Value Balance (৳)", min_value=0.0, value=float(curr_p_data["capital"]))
                st.caption(f"ℹ️ প্রফিট স্প্লিট অনুপাত বর্তমানে: **{curr_p_data['profit_pct']:.2f}%** (যা ইনভেস্টমেন্ট পরিবর্তন করলে স্বয়ংক্রিয়ভাবে পুনঃহিসাব হবে।)")
                
                col_pb_dropdown_row = st.columns(2)
                with col_pb_dropdown_row[0]:
                    if st.form_submit_button("Update Selected Partner Node", type="primary"):
                        st.session_state.erp_partners[selected_dropdown_partner]["capital"] = p_update_cap
                        trigger_mutation_success()
                with col_pb_dropdown_row[1]:
                    if st.form_submit_button("Purge Selected Partner From Registry"):
                        st.session_state.erp_partners.pop(selected_dropdown_partner)
                        trigger_mutation_success()
        else: st.info("No active partner pools data found to manage.")

    with tab_p2:
        with st.form("add_brand_new_partner_form", clear_on_submit=True):
            new_p_name = st.text_input("Enter New Partner Full Handle String Name (Unique)").strip()
            new_p_cap = st.number_input("Initial Injected Fund Capital Investment (৳)", min_value=0.0)
            st.info("💡 নতুন পার্টনারের প্রফিট পার্সেন্টেজ (%) ইনভেস্ট করা অ্যামাউন্টের ভিত্তিতে অটোমেটিক সেট হয়ে যাবে।")
            if st.form_submit_button("Save & Append New Profile Line Node"):
                if new_p_name:
                    st.session_state.erp_partners[new_p_name] = {"capital": new_p_cap, "profit_pct": 0.0}
                    trigger_mutation_success()
                else: st.error("Error: Partner Handle String Key Cannot be blank.")

# ----------------------------------------------------------------------------------
# MODULE 7: DAILY SALES ENTRY
# ----------------------------------------------------------------------------------
elif active_menu_node == "💰 Daily Sales Entry" and is_editable:
    st.markdown("## 💰 Daily Sales High-Frequency Operational Intake Ledger Engine")
    st.markdown("---")
    col_ds1, col_ds2 = st.columns([1, 2])
    with col_ds1:
        with st.form("sales_direct_ledger_submission_gate", clear_on_submit=True):
            ds_d = st.date_input("Journal Posting Date Mapping Node", date.today())
            ds_s = st.selectbox("Operational Window Shift Node", st.session_state.erp_dropdowns["shifts"])
            ds_i = st.selectbox("Product Mapping Dish Target Options", st.session_state.erp_dropdowns["dishes"])
            ds_r = st.number_input("Unit Plate Mapping Value Cost Base (৳)", min_value=0.0, value=250.0)
            ds_q = st.number_input("Volume Index Counts Total Plates Sold", min_value=1, value=10)
            ds_p = st.selectbox("Gateway Sourcing Node", ["Cash", "bKash", "Nagad", "Card"])
            if st.form_submit_button("Commit Sales Entry Node Row", use_container_width=True):
                calc_ds_total = ds_r * ds_q
                fresh_ds_frame = pd.DataFrame([{
                    "ID": len(st.session_state.sales_ledger) + 1100, "Date": str(ds_d), "Month-Year": ds_d.strftime("%B %Y"),
                    "Shift": ds_s, "Product Name": ds_i, "Quantity": ds_q, "Rate": ds_r, "Payment Method": ds_p, "Net Total": calc_ds_total
                }])
                st.session_state.sales_ledger = pd.concat([st.session_state.sales_ledger, fresh_ds_frame], ignore_index=True)
                trigger_mutation_success()
    with col_ds2:
        st.dataframe(st.session_state.sales_ledger, use_container_width=True)
        if len(st.session_state.sales_ledger) > 0:
            with st.form("sales_purge_terminal_node"):
                ds_purge_target_id = st.selectbox("Identify Ledger Row ID Pointer for Target Exclusion", st.session_state.sales_ledger["ID"].tolist())
                if st.form_submit_button("Purge Target Row", type="primary"):
                    st.session_state.sales_ledger = st.session_state.sales_ledger[st.session_state.sales_ledger["ID"] != ds_purge_target_id]
                    trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 8: VARIABLE BAZAR COST
# ----------------------------------------------------------------------------------
elif active_menu_node == "🛒 Variable Bazar Cost" and is_editable:
    st.markdown("## 🛒 Raw Material Procurement Variable Bazar Expenses Cost Tracking Engine")
    st.markdown("---")
    col_vbc1, col_vbc2 = st.columns([1, 2])
    with col_vbc1:
        with st.form("bazar_procurement_journal_gate", clear_on_submit=True):
            vb_d = st.date_input("Procurement Log Date", date.today())
            vb_s = st.selectbox("Supplier Allocation Mapping", st.session_state.erp_dropdowns["suppliers"])
            vb_c = st.selectbox("Classification Category Mapping", ["Rice", "Meat", "Chicken", "Oil", "Onion", "Spices", "Packaging Items"])
            vb_q = st.text_input("Quantity Metric (e.g., 50 Kg)", value="10 Units")
            vb_amt = st.number_input("Total Bill Value Cost (৳)", min_value=0.0)
            if st.form_submit_button("Publish Sourcing Ledger Data Row", use_container_width=True):
                fresh_vb_frame = pd.DataFrame([{"ID": len(st.session_state.bazar_ledger) + 2100, "Date": str(vb_d), "Supplier": vb_s, "Item Category": vb_c, "Quantity": vb_q, "Unit Price": vb_amt, "Total Cost": vb_amt}])
                st.session_state.bazar_ledger = pd.concat([st.session_state.bazar_ledger, fresh_vb_frame], ignore_index=True)
                trigger_mutation_success()
    with col_vbc2:
        st.dataframe(st.session_state.bazar_ledger, use_container_width=True)
        if len(st.session_state.bazar_ledger) > 0:
            with st.form("bazar_purge_terminal_node"):
                vb_purge_target_id = st.selectbox("Identify Sourcing Item ID Key Node for Elimination", st.session_state.bazar_ledger["ID"].tolist())
                if st.form_submit_button("Purge Selected Procurement Row Component Instance", type="primary"):
                    st.session_state.bazar_ledger = st.session_state.bazar_ledger[st.session_state.bazar_ledger["ID"] != vb_purge_target_id]
                    trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 9: MONTHLY EXPENSES
# ----------------------------------------------------------------------------------
elif active_menu_node == "💼 Monthly Expenses" and is_editable:
    st.markdown("## 💼 Fixed Periodic & Structural Corporate Overheads Console Terminal")
    st.markdown("---")
    col_me1, col_me2 = st.columns([1, 2])
    with col_me1:
        with st.form("overhead_journal_submission_gate", clear_on_submit=True):
            me_d = st.date_input("Settlement Processing Date", date.today())
            me_c = st.selectbox("Overhead Class Profile Selection", st.session_state.erp_dropdowns["expense_categories"])
            me_a = st.number_input("Settlement Invoiced Outflow Value Amount (৳)", min_value=0.0)
            me_m = st.text_input("Operational Specification Memo Details Descriptor").strip()
            if st.form_submit_button("Authorize & Post Expense Log Row Instance", use_container_width=True):
                fresh_me_frame = pd.DataFrame([{"ID": len(st.session_state.monthly_expenses) + 3100, "Date": str(me_d), "Category": me_c, "Amount": me_a, "Description": me_m}])
                st.session_state.monthly_expenses = pd.concat([st.session_state.monthly_expenses, fresh_me_frame], ignore_index=True)
                trigger_mutation_success()
    with col_me2:
        st.dataframe(st.session_state.monthly_expenses, use_container_width=True)
        if len(st.session_state.monthly_expenses) > 0:
            with st.form("overhead_purge_terminal_node"):
                me_purge_target_id = st.selectbox("Identify Expense Unique Transaction Log Reference ID", st.session_state.monthly_expenses["ID"].tolist())
                if st.form_submit_button("Purge Selected Overhead Row Component Block", type="primary"):
                    st.session_state.monthly_expenses = st.session_state.monthly_expenses[st.session_state.monthly_expenses["ID"] != me_purge_target_id]
                    trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 10: STAFF SALARY LEDGER
# ----------------------------------------------------------------------------------
elif active_menu_node == "🧑‍🍳 Staff Salary Ledger" and is_editable:
    st.markdown("## 🧑‍🍳 Payroll Processing Ledger Disbursement Terminal Panel Node Core")
    st.markdown("---")
    if not st.session_state.erp_employees: st.warning("Human capital records register is empty."); st.stop()
    col_ssl1, col_ssl2 = st.columns([1, 2])
    with col_ssl1:
        with st.form("payroll_direct_processing_disbursement_gate", clear_on_submit=True):
            pr_emp = st.selectbox("Select Target Employee Registry ID Profile", list(st.session_state.erp_employees.keys()), format_func=lambda x: f"{st.session_state.erp_employees[x]['name']} ({x})")
            pr_d = st.date_input("Disbursement Pay Processing Date", date.today())
            target_emp_meta_data = st.session_state.erp_employees[pr_emp]
            base_monthly_contract_val = float(target_emp_meta_data["salary_monthly"])
            st.markdown(f"ℹ️ **Rank:** `{target_emp_meta_data['designation']}` | **Fixed Base Monthly Structure:** `{base_monthly_contract_val:,.2f} ৳`")
            pr_bonus = st.number_input("Incentive Bonus Additions Premium Delta (৳)", min_value=0.0)
            pr_deduct = st.number_input("Deductions Financial Offset Penalties (৳)", min_value=0.0)
            if st.form_submit_button("Confirm Payment & Transmit Log Node", use_container_width=True):
                net_wage_disbursed_calc_val = base_monthly_contract_val + pr_bonus - pr_deduct
                fresh_pr_frame = pd.DataFrame([{
                    "ID": len(st.session_state.payroll_ledger) + 4100, "Date": str(pr_d), "Employee ID": pr_emp, "Name": target_emp_meta_data["name"],
                    "Designation": target_emp_meta_data["designation"], "Base Salary": base_monthly_contract_val, "Bonus": pr_bonus,
                    "Deductions": pr_deduct, "Net Disbursed": net_wage_disbursed_calc_val
                }])
                st.session_state.payroll_ledger = pd.concat([st.session_state.payroll_ledger, fresh_pr_frame], ignore_index=True)
                trigger_mutation_success()
    with col_ssl2:
        st.dataframe(st.session_state.payroll_ledger, use_container_width=True)
        if len(st.session_state.payroll_ledger) > 0:
            with st.form("payroll_purge_terminal_node"):
                pr_purge_target_id = st.selectbox("Identify Pay Slip Instance Unique Record", st.session_state.payroll_ledger["ID"].tolist())
                if st.form_submit_button("Purge Selected Ledger Record Frame Line", type="primary"):
                    st.session_state.payroll_ledger = st.session_state.payroll_ledger[st.session_state.payroll_ledger["ID"] != pr_purge_target_id]
                    trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 11: INVENTORY & RESTOCK
# ----------------------------------------------------------------------------------
elif active_menu_node == "📦 Inventory & Restock" and is_editable:
    st.markdown("## 📦 Enterprise Raw Material Inventory Pipeline Supply Depth Logistics Console")
    st.markdown("---")
    col_invt1, col_invt2 = st.columns([1, 2])
    with col_invt1:
        with st.form("inventory_tuning_manual_override_gate", clear_on_submit=True):
            inv_name = st.text_input("Raw Stock Material Object Title Identity Handle (e.g., Basmati Rice)").strip()
            inv_cat = st.selectbox("Material Stock Classification Bucket Type Allocation Options", ["Rice", "Meat", "Chicken", "Oil", "Onion", "Spices", "Packaging Items"])
            inv_stock = st.number_input("Current Volume In-Stock Metric Quantity Metric Value", min_value=0.0)
            inv_unit = st.text_input("Unit Measurement Metric Notation Identity Token (e.g., Kg, Ltr, Pcs)", value="Kg").strip()
            inv_alert = st.number_input("Minimum Safe Lower Threshold Warning Alert Limits", min_value=0.0)
            if st.form_submit_button("Save Stock Item Master Tracker", type="primary"):
                match_index_array = st.session_state.inventory_master[st.session_state.inventory_master["Material Name"] == inv_name].index
                if len(match_index_array) > 0:
                    st.session_state.inventory_master.loc[match_index_array[0], ["Category", "Stock", "Unit", "Min Alert"]] = [inv_cat, inv_stock, inv_unit, inv_alert]
                else:
                    fresh_inv_item_row = pd.DataFrame([{"ID": len(st.session_state.inventory_master) + 500, "Material Name": inv_name, "Category": inv_cat, "Stock": inv_stock, "Unit": inv_unit, "Min Alert": inv_alert}])
                    st.session_state.inventory_master = pd.concat([st.session_state.inventory_master, fresh_inv_item_row], ignore_index=True)
                trigger_mutation_success()
    with col_invt2:
        st.dataframe(st.session_state.inventory_master, use_container_width=True)
        if len(st.session_state.inventory_master) > 0:
            with st.form("inventory_purge_terminal_node"):
                inv_purge_target_id = st.selectbox("Identify Raw Inventory Unique Reference Code", st.session_state.inventory_master["ID"].tolist())
                if st.form_submit_button("Purge Item Component From Database", type="primary"):
                    st.session_state.inventory_master = st.session_state.inventory_master[st.session_state.inventory_master["ID"] != inv_purge_target_id]
                    trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 12: DROPDOWN CONTROL PANEL
# ----------------------------------------------------------------------------------
elif active_menu_node == "⚙️ Dropdown Control Panel" and is_editable:
    st.markdown("## ⚙️ Dropdown Matrix Configuration Control Panel Hub")
    st.markdown("---")
    dropdown_master_keys = list(st.session_state.erp_dropdowns.keys())
    tab_nodes = st.tabs([k.upper().replace("_", " ") for k in dropdown_master_keys])
    
    for idx, tab_object in enumerate(tab_nodes):
        target_dropdown_data_key = dropdown_master_keys[idx]
        active_working_dropdown_elements = st.session_state.erp_dropdowns[target_dropdown_data_key]
        with tab_object:
            st.markdown(f"**Current Options Mapped under category link: `{target_dropdown_data_key}`**")
            for element_index, element_value_string in enumerate(active_working_dropdown_elements):
                col_row_cells = st.columns([4, 1, 1])
                with col_row_cells[0]:
                    modified_text = st.text_input(f"Element Input Node Code [{element_index}]", value=element_value_string, key=f"dd_input_{target_dropdown_data_key}_{element_index}", label_visibility="collapsed")
                with col_row_cells[1]:
                    if st.button("Update 📝", key=f"dd_btn_up_{target_dropdown_data_key}_{element_index}"):
                        st.session_state.erp_dropdowns[target_dropdown_data_key][element_index] = modified_text
                        trigger_mutation_success()
                with col_row_cells[2]:
                    if st.button("Delete ❌", key=f"dd_btn_del_{target_dropdown_data_key}_{element_index}"):
                        st.session_state.erp_dropdowns[target_dropdown_data_key].pop(element_index)
                        trigger_mutation_success()
            st.markdown("---")
            with st.form(f"add_fresh_dropdown_option_node_form_{target_dropdown_data_key}", clear_on_submit=True):
                fresh_option = st.text_input("Append New Option Element to Configuration Array").strip()
                if st.form_submit_button("Append Option Elements", type="primary"):
                    if fresh_option and fresh_option not in st.session_state.erp_dropdowns[target_dropdown_data_key]:
                        st.session_state.erp_dropdowns[target_dropdown_data_key].append(fresh_option)
                        trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 13: SYSTEM USER PROVISIONING
# ----------------------------------------------------------------------------------
elif active_menu_node == "🛡️ System User Provisioning" and is_editable:
    st.markdown("## 🛡️ Role-Based Identity Gate Privilege Matrix & Configuration Maps Engine")
    st.markdown("---")
    for group_role_title, navigation_menus_array_list in st.session_state.erp_privileges.items():
        with st.expander(f"⚙️ Access Control List Modules for Security Tier Level Node: {group_role_title.upper()}"):
            updated_navigation_access = st.multiselect("Check Authorized Active Menu View Components", options=ALL_SYSTEM_MENUS, default=navigation_menus_array_list, key=f"acl_select_nodes_{group_role_title}")
            if st.button("Update Access Matrix", key=f"acl_save_btn_{group_role_title}"):
                st.session_state.erp_privileges[group_role_title] = updated_navigation_access
                trigger_mutation_success()

# ----------------------------------------------------------------------------------
# MODULE 14: PARTNER PREVIEW MOCK GENERATOR CENTRE
# ----------------------------------------------------------------------------------
elif active_menu_node == "👁️ Partner Preview Mode":
    st.markdown("## 📈 Corporate Accounting Ledgers Audit Report Manager (Read-Only Preview)")
    st.markdown("---")
    st.info("Partner View Node Mode Active. Structural updates are suspended.")
    report_category_options = ["Sales Report", "Expenses Report", "Purchase Report", "Salary Report"]
    selected_report = st.selectbox("Identify Audit Framework Target Matrix for Export", report_category_options)
    with st.container(border=True):
        if "Sales Report" in selected_report: st.dataframe(st.session_state.sales_ledger, use_container_width=True)
        elif "Expenses Report" in selected_report: st.dataframe(st.session_state.monthly_expenses, use_container_width=True)
        elif "Purchase Report" in selected_report: st.dataframe(st.session_state.bazar_ledger, use_container_width=True)
        elif "Salary Report" in selected_report: st.dataframe(st.session_state.payroll_ledger, use_container_width=True)

# ----------------------------------------------------------------------------------
# NEW MODULE 15: ACCOUNT SECURITY HUB (DEDICATED SOFTWARE ACCOUNT PROVISIONING MENU)
# ----------------------------------------------------------------------------------
elif active_menu_node == "🔐 Account Security Hub" and is_editable:
    st.markdown("## 🔐 System Identity Authentication Access Control Panel Hub")
    st.markdown("---")
    tab_security_1, tab_security_2 = st.tabs(["🔒 Alter Security Passwords Matrix", "➕ Provision New Software Account User"])
    
    with tab_security_1:
        with st.form("account_password_modification_form"):
            st.markdown("#### Modify Existing Authentication Passwords")
            target_profile_id = st.selectbox("Identify Target System User Account to Alter", list(st.session_state.erp_users.keys()))
            fresh_secure_password = st.text_input("Enter New Secure Token Password", type="password")
            if st.form_submit_button("Commit Security Password Change", type="primary"):
                if fresh_secure_password:
                    st.session_state.erp_users[target_profile_id]["password"] = fresh_secure_password
                    st.toast(f"🔑 Password for user '{target_profile_id}' has been updated successfully!")
                    trigger_mutation_success()
                else: st.error("Error: Password field cannot process blank entries.")
                    
    with tab_security_2:
        with st.form("create_new_software_login_user_form", clear_on_submit=True):
            st.markdown("#### Provision Brand New Enterprise Access Profiles")
            cs_col1, cs_col2 = st.columns(2)
            with cs_col1:
                provision_u_id = st.text_input("New Account Login Username ID (Lowercase, unique)").strip().lower()
                provision_u_pw = st.text_input("New Account Cryptographic Password", type="password")
            with cs_col2:
                provision_u_role = st.selectbox("Select Access Control Role Allocation Tier Level", ["Super Admin", "Manager", "Partner"])
                
            col_action_btn_nodes = st.columns(2)
            with col_action_btn_nodes[0]: 
                execute_user_creation = st.form_submit_button("Create New User Login", type="primary")
            with col_action_btn_nodes[1]: 
                execute_user_purge = st.form_submit_button("Purge Target User Identity")
            
            if execute_user_creation and provision_u_id and provision_u_pw:
                if provision_u_id not in st.session_state.erp_users:
                    st.session_state.erp_users[provision_u_id] = {"password": provision_u_pw, "role": provision_u_role}
                    st.toast(f"🎉 New account setup for '{provision_u_id}' is active on Gateway!")
                    trigger_mutation_success()
                else: st.error("Operation Aborted: Target account username already exists.")
                    
            if execute_user_purge and provision_u_id:
                if provision_u_id in st.session_state.erp_users and provision_u_id != "superadmin":
                    st.session_state.erp_users.pop(provision_u_id)
                    st.toast(f"🗑️ System user access node '{provision_u_id}' has been completely purged.")
                    trigger_mutation_success()
                else: st.error("Access Refused: Primary core system root superadmin profile node cannot be altered.")