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
        
        # Fixed structural enclosing loop within inner methods
        def filter_by_month(df):
            if len(df) == 0: 
                return df
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
    
    # RELATIONAL OBJECT INITIALIZATION REFACTORED SECURELY
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
    else:
        st.info("Equity database amounts stand at 0. Enter partner capital to run distribution matrix scripts.")

# ----------------------------------------------------------------------------------
# MODULE 2: ADVANCED REPORT MANAGER
# ----------------------------------------------------------------------------------
elif choice == "📈 Advanced Report Manager":
    st.title("📈 Strategic Cross-Module Multi-Report Manager Engine")
    
    rep_tab1, rep_tab2, rep_tab3 = st.tabs(["Sales Journal Ledger", "Variable Material Sourcing", "Staff Payroll Distributions"])
    
    with rep_tab1:
        st.markdown("### 🔍 Sales Ledger Filtering Filter")
        sc1, sc2 = st.columns(2)
        with sc1:
            s_start = st.date_input("Sales Tracking From Date", date(2026, 1, 1), key="rep_s_start")
        with sc2:
            s_end = st.date_input("Sales Tracking To Date", datetime.now().date(), key="rep_s_end")
            
        if len(st.session_state.sales_records) > 0:
            df_s_master = st.session_state.sales_records.copy()
            df_s_master["Date"] = pd.to_datetime(df_s_master["Date"]).dt.date
            f_sales = df_s_master[(df_s_master["Date"] >= s_start) & (df_s_master["Date"] <= s_end)]
            
            st.metric("Aggregated Net Filtered Sales Volume", f"{f_sales['Net Total'].sum():,.2f} BDT")
            st.dataframe(f_sales, use_container_width=True)
            st.download_button(label="📥 Export Sales Data as Excel (CSV)", data=f_sales.to_csv(index=False), file_name=f"Sales_Report_{s_start}_to_{s_end}.csv", mime="text/csv")
        else:
            st.info("Sales transaction database table stands empty.")
            
    with rep_tab2:
        st.markdown("### 🔍 Variable Material Bazar Procurement Audit")
        bc1, bc2 = st.columns(2)
        with bc1:
            b_start = st.date_input("Sourcing Tracking From Date", date(2026, 1, 1), key="rep_b_start")
        with bc2:
            b_end = st.date_input("Sourcing Tracking To Date", datetime.now().date(), key="rep_b_end")
            
        if len(st.session_state.variable_bazar) > 0:
            df_b_master = st.session_state.variable_bazar.copy()
            df_b_master["Date"] = pd.to_datetime(df_b_master["Date"]).dt.date
            f_bazar = df_b_master[(df_b_master["Date"] >= b_start) & (df_b_master["Date"] <= b_end)]
            
            st.metric("Aggregated Net Filtered Bazar Outflow", f"{f_bazar['Total Cost (BDT)'].sum():,.2f} BDT")
            st.dataframe(f_bazar, use_container_width=True)
            st.download_button(label="📥 Export Sourcing Data as Excel (CSV)", data=f_bazar.to_csv(index=False), file_name=f"Bazar_Report_{b_start}_to_{b_end}.csv", mime="text/csv")
        else:
            st.info("Bazar tracking tables contain 0 logged items.")

    with rep_tab3:
        st.markdown("### 🔍 Employee Wage Allocation Audit Logs")
        salc1, salc2 = st.columns(2)
        with salc1:
            sal_start = st.date_input("Disbursement From Date", date(2026, 1, 1), key="rep_sal_start")
        with salc2:
            sal_end = st.date_input("Disbursement To Date", datetime.now().date(), key="rep_sal_end")
            
        if len(st.session_state.salary_db) > 0:
            df_sal_master = st.session_state.salary_db.copy()
            df_sal_master["Date"] = pd.to_datetime(df_sal_master["Date"]).dt.date
            f_sal = df_sal_master[(df_sal_master["Date"] >= sal_start) & (df_sal_master["Date"] <= sal_end)]
            
            st.metric("Aggregated Net Payroll Expenditures", f"{f_sal['Amount Paid (BDT)'].sum():,.2f} BDT")
            st.dataframe(f_sal, use_container_width=True)
            st.download_button(label="📥 Export Payroll Ledger as Excel (CSV)", data=f_sal.to_csv(index=False), file_name=f"Payroll_Report_{sal_start}_to_{sal_end}.csv", mime="text/csv")
        else:
            st.info("Salary ledger currently registers 0 entries.")

# ----------------------------------------------------------------------------------
# MODULE 3: DIGITAL INVOICE GENERATOR
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
        st.markdown("""
        <style>
        .invoice-box { max-width: 400px; padding: 20px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0, 0, 0, .15); font-size: 14px; line-height: 22px; font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; color: #555; background-color: #fff; }
        </style>
        """, unsafe_allow_html=True)
        
        invoice_html = f"""
        <div class="invoice-box">
            <h3 style="text-align: center; color: #2ecc71; margin: 0;">SWAPNAJATRA BIRYANI BARI</h3>
            <p style="text-align: center; font-size: 11px; color: gray; margin: 0 0 15px 0;">Mirpur, Dhaka, Bangladesh</p>
            <hr>
            <b>Invoice Date:</b> {datetime.now().strftime('%Y-%m-%d %I:%M %p')}<br>
            <b>Customer Name:</b> {inv_cust}<br>
            <hr>
            <table style="width: 100%; font-size: 13px;">
                <tr style="background: #eee; font-weight: bold;">
                    <td>Particulars Item</td>
                    <td style="text-align: center;">Qty</td>
                    <td style="text-align: right;">Total</td>
                </tr>
                <tr>
                    <td>{inv_item} (@{inv_rate:.0f})</td>
                    <td style="text-align: center;">{inv_qty}</td>
                    <td style="text-align: right;">{inv_gross:.2f} BDT</td>
                </tr>
                <tr style="color: #e74c3c;">
                    <td colspan="2">Discount / Adjustment Out:</td>
                    <td style="text-align: right;">-{inv_disc:.2f} BDT</td>
                </tr>
                <tr style="font-weight: bold; font-size: 15px; color: #2e6f40;">
                    <td colspan="2">Net Cash Billing Inflow:</td>
                    <td style="text-align: right;">{inv_net:.2f} BDT</td>
                </tr>
            </table>
            <br>
            <p style="text-align: center; font-size: 12px; font-style: italic; color: #2ecc71;">Thank you for dining with us! Come back again. 🎉</p>
        </div>
        """
        st.markdown(invoice_html, unsafe_allow_html=True)
        st.caption("💡 Tip: Use your browser print shortcut (Ctrl+P or Cmd+P) to save this block as a PDF file.")

# ----------------------------------------------------------------------------------
# MODULE 4: PARTNER CAPITAL ENGINE
# ----------------------------------------------------------------------------------
elif choice == "🤝 Partner Capital Engine":
    st.title("🤝 Capital Allocations & Fixed Infrastructure Capital Investments")
    
    p_tab1, p_tab2 = st.tabs(["Partner Equity Accounts Ledger", "Fixed Structural Infrastructure Cost Entry"])
    
    with p_tab1:
        st.markdown("### 📋 Live Capital Account Matrix Summary")
        st.dataframe(st.session_state.partners_db, use_container_width=True)
        
        if not is_partner:
            st.markdown("#### ➕ Record / Update Capital Contributions")
            with st.form("capital_form", clear_on_submit=True):
                p_select = st.selectbox("Identify Target Partner Name Vector", st.session_state.partner_list)
                p_inject = st.number_input("Injected Capital Delta Amount (BDT)", min_value=0.0, step=1000.0, value=0.0)
                if st.form_submit_button("Commit Capital Entry Change"):
                    df_m = st.session_state.partners_db
                    if p_select in df_m["Partner Name"].values:
                        df_m.loc[df_m["Partner Name"] == p_select, "Investment Amount"] += p_inject
                        save_permanent_database() # Save to disk
                        st.success(f"Equity balance successfully transformed for partner: {p_select}")
                        st.rerun()

    with p_tab2:
        st.markdown("### 📋 Long-Term Infrastructure Asset Setup Expenditures Log")
        st.dataframe(st.session_state.fixed_expenses, use_container_width=True)
        
        if not is_partner:
            st.markdown("#### ➕ Record New Setup Fixed Expense Item")
            with st.form("fixed_form", clear_on_submit=True):
                f_cat = st.selectbox("Structural Asset Category Class Selection", st.session_state.asset_categories)
                f_desc = st.text_input("Asset Specification Memo Particulars (e.g., Degh, Gas Stove, Signboard Construction)").strip()
                f_cost = st.number_input("Invoiced Capital Cost Asset Value (BDT)", min_value=0.0, step=500.0, value=0.0)
                f_date = st.date_input("Asset Expenditure Ledger Logging Date", datetime.now())
                if st.form_submit_button("Publish Capital Asset Entry"):
                    if f_desc:
                        new_asset = pd.DataFrame([{"Date": f_date.strftime("%Y-%m-%d"), "Category": f_cat, "Asset/Cost Item": f_desc, "Amount": f_cost}])
                        st.session_state.fixed_expenses = pd.concat([st.session_state.fixed_expenses, new_asset], ignore_index=True)
                        save_permanent_database() # Save to disk
                        st.success("Fixed Asset transaction successfully wired to central relational model.")
                        st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 5: DAILY SALES ENTRY
# ----------------------------------------------------------------------------------
elif choice == "💰 Daily Sales Entry":
    st.title("💰 High-Frequency Point of Sale Intake Interface")
    if is_partner:
        st.error("🚫 Access Restructured: View-only privileges cannot execute sales database write commands.")
    else:
        with st.form("sales_submission_form", clear_on_submit=True):
            st.markdown("#### Document Cash Inflow Sales Record Item")
            prod_sel = st.selectbox("Target Menu Product Node", st.session_state.menu_items)
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                p_rate = st.number_input("Unit Plate Billing Rate (BDT)", min_value=0.0, value=220.0, step=5.0)
            with sc2:
                p_qty = st.number_input("Volume Unit Count Sold", min_value=1, value=1, step=1)
            with sc3:
                p_adj = st.number_input("Discount / Rebate Offset (+/- BDT)", step=5.0, value=0.0)
            p_date = st.date_input("Journal Posting Date String Context", datetime.now())
            
            computed_invoice_net = (p_rate * p_qty) + p_adj
            st.markdown(f"**Relational Calculated Invoice Net Result:** `{computed_invoice_net:,.2f} BDT`")
            
            if st.form_submit_button("Post Transaction Journal Entry"):
                new_s_log = pd.DataFrame([{
                    "Date": p_date.strftime("%Y-%m-%d"), 
                    "Month-Year": get_month_year_str(p_date),
                    "Item Name": prod_sel, 
                    "Rate per Plate": p_rate, 
                    "Total Plates": p_qty, 
                    "Adjustment": p_adj, 
                    "Net Total": computed_invoice_net
                }])
                st.session_state.sales_records = pd.concat([st.session_state.sales_records, new_s_log], ignore_index=True)
                save_permanent_database() # Save to disk
                st.success(f"Journal ledger balance increased by {computed_invoice_net:.2f} BDT for item '{prod_sel}'")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 6: DAILY VARIABLE BAZAR COST
# ----------------------------------------------------------------------------------
elif choice == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Variable Material Sourcing Cost Ledger")
    st.dataframe(st.session_state.variable_bazar, use_container_width=True)
    
    if not is_partner:
        st.markdown("### ➕ Input Raw Variable Procurement Sourcing Event")
        with st.form("bazar_log_form", clear_on_submit=True):
            mat_select = st.selectbox("Choose Targeted Inventory Raw Material Asset Descriptor Node", st.session_state.inventory_items + ["Other Unlisted Sourcing Items"])
            bc1, bc2 = st.columns(2)
            with bc1:
                mat_qty = st.text_input("Procured Quantity Metrics (e.g., 15 Kg, 4 Ltr)").strip()
            with bc2:
                mat_cost = st.number_input("Total Outflow Invoiced Sourcing Cost (BDT)", min_value=0.0, step=100.0, value=0.0)
            mat_date = st.date_input("Market Transaction Clearing Settlement Date", datetime.now())
            
            if st.form_submit_button("Post Bazar Cost Entry"):
                new_b_entry = pd.DataFrame([{"Date": mat_date.strftime("%Y-%m-%d"), "Bazar Item Name": mat_select, "Quantity/Weight": mat_qty, "Total Cost (BDT)": mat_cost, "Purchased By": st.session_state.logged_in_user.capitalize()}])
                st.session_state.variable_bazar = pd.concat([st.session_state.variable_bazar, new_b_entry], ignore_index=True)
                save_permanent_database() # Save to disk
                st.success("Bazar variable transaction wired into cash statement arrays.")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 7: MONTHLY OPERATING EXPENSES
# ----------------------------------------------------------------------------------
elif choice == "💼 Monthly Expenses":
    st.title("💼 Periodic Operational Month Expenditures Journal")
    st.dataframe(st.session_state.monthly_expenses_db, use_container_width=True)
    
    if not is_partner:
        st.markdown("### ➕ Register Monthly Administrative Operational Cost Item")
        with st.form("monthly_exp_submission", clear_on_submit=True):
            m_cat = st.selectbox("Identify Expense Account Node Classification", st.session_state.expense_categories)
            m_memo = st.text_input("Operational Particulars Memo Details (e.g., Gas Cylinder Swapping, Facebook Ad Marketing)").strip()
            m_val = st.number_input("Invoiced Value Outflow Amount (BDT)", min_value=0.0, step=100.0, value=0.0)
            m_date = st.date_input("Payment Document Verification Settlement Date", datetime.now())
            if st.form_submit_button("Publish Operating Cost Entry"):
                if m_memo:
                    new_mo_entry = pd.DataFrame([{"Date": m_date.strftime("%Y-%m-%d"), "Category": m_cat, "Particulars": m_memo, "Amount (BDT)": m_val}])
                    st.session_state.monthly_expenses_db = pd.concat([st.session_state.monthly_expenses_db, new_mo_entry], ignore_index=True)
                    save_permanent_database() # Save to disk
                    st.success("Monthly operational ledger updated.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 8: HUMAN RESOURCE STAFF PAYROLL LEDGER
# ----------------------------------------------------------------------------------
elif choice == "🧑‍🍳 Staff Salary Ledger":
    st.title("🧑‍🍳 Workforce Management Payroll & Salary Compensation")
    st.dataframe(st.session_state.salary_db, use_container_width=True)
    
    if not is_partner:
        st.markdown("### ➕ Log Workforce Remuneration / Wage Settlement Outflow")
        with st.form("payroll_form", clear_on_submit=True):
            emp_name = st.text_input("Employee Roster Full Name Context").strip()
            emp_desg = st.text_input("Staff Assignment Role Designation Title (e.g. Cook, Assistant Chef, Waiter Team)").strip()
            
            emc1, emc2 = st.columns(2)
            with emc1:
                sal_class = st.selectbox("Salary Frequency Matrix Type Class", ["Daily Wages Salary", "Monthly Regular Salary"])
            with emc2:
                sal_value = st.number_input("Disbursed Cash Compensation Paid Value (BDT)", min_value=0.0, step=100.0, value=0.0)
            sal_date = st.date_input("Disbursement Payroll Document Release Date", datetime.now())
            
            if st.form_submit_button("Post Workforce Salary Payroll Log"):
                if emp_name and emp_desg:
                    new_payroll = pd.DataFrame([{"Date": sal_date.strftime("%Y-%m-%d"), "Staff Name": emp_name, "Designation": emp_desg, "Salary Type": sal_class, "Amount Paid (BDT)": sal_value}])
                    st.session_state.salary_db = pd.concat([st.session_state.salary_db, new_payroll], ignore_index=True)
                    save_permanent_database() # Save to disk
                    st.success("Human resource payroll disbursement record executed safely.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 9: INVENTORY MANAGEMENT & RAW MATERIAL BULK ALLOCATIONS
# ----------------------------------------------------------------------------------
elif choice == "📦 Inventory & Restock":
    st.title("📦 Raw Material Supply Pipeline Depth Ledger")
    
    df_inv_ledger = st.session_state.inventory_db.copy()
    df_inv_ledger["Pipeline Assessment Status"] = df_inv_ledger.apply(lambda r: "🚨 LOW STOCK WARNING CRITICAL LEVEL" if r["Current Stock"] <= r["Alert Level"] else "✅ Adequate Sourcing Level Optimal", axis=1)
    st.dataframe(df_inv_ledger, use_container_width=True)
    
    low_stocks = df_inv_ledger[df_inv_ledger["Current Stock"] <= df_inv_ledger["Alert Level"]]
    if len(low_stocks) > 0:
        for _, row in low_stocks.iterrows():
            st.error(f"🚨 **Critical Level Depletion Warning:** Sourcing item '{row['Material Name']}' capacity dropped to **{row['Current Stock']} {row['Unit']}** (Configured Safety Buffer Threshold is {row['Alert Level']} {row['Unit']}). Action required.")

    if not is_partner:
        st.markdown("---")
        st.markdown("### 🔄 Restock / Update Raw Material Asset Volume Allocation Pipeline")
        with st.form("restock_pipeline_form", clear_on_submit=True):
            raw_sel = st.selectbox("Identify Target Raw Asset Identifier Stock Row Node", df_inv_ledger["Material Name"].values)
            stock_delta = st.number_input("Inward Supply Volume Stock Intake Metric Addition (+ Quantity)", min_value=0.0, step=5.0, value=0.0)
            if st.form_submit_button("Recompute Target Pipeline Volumetric Balances"):
                st.session_state.inventory_db.loc[st.session_state.inventory_db["Material Name"] == raw_sel, "Current Stock"] += stock_delta
                save_permanent_database() # Save to disk
                st.success(f"Supply capacity parameter expanded for material item node: '{raw_sel}'")
                st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 10: ADMINISTRATIVE STRATEGIC SYSTEM INFRASTRUCTURE DROPDOWN PANEL
# ----------------------------------------------------------------------------------
elif choice == "⚙️ Dropdown Control Panel":
    st.title("⚙️ Infrastructure Configuration Dropdown Options Control")
    st.write("Perform real-time additions or mutations on structural global list configurations across menus instantly.")
    
    tab_m1, tab_m2, tab_m3, tab_m4, tab_m5 = st.tabs(["Food Menu Items Array", "Partners Validation Matrix", "Asset Accounting Categories", "Monthly Expense Codes", "Raw Inventory Item Elements"])
    
    with tab_m1:
        st.write("Current Roster configuration mapping:", st.session_state.menu_items)
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            new_f_item = st.text_input("Enter New Entry Variant String to Append", key="add_food").strip()
            if st.button("Save/Append Food Menu Product"):
                if new_f_item and new_f_item not in st.session_state.menu_items:
                    st.session_state.menu_items.append(new_f_item)
                    save_permanent_database()
                    st.success("Product element wired to dynamic lookup matrices.")
                    st.rerun()
        with col_m2:
            target_f = st.selectbox("Identify Menu Item Target to Rename", st.session_state.menu_items, key="ren_food_sel")
            mutated_f = st.text_input("Enter Mutated String Context Target Name", value=target_f, key="ren_food_val").strip()
            if st.button("Apply Rename on Food Item Node"):
                if mutated_f and mutated_f != target_f:
                    idx = st.session_state.menu_items.index(target_f)
                    st.session_state.menu_items[idx] = mutated_f
                    if len(st.session_state.sales_records) > 0:
                        st.session_state.sales_records.loc[st.session_state.sales_records["Item Name"] == target_f, "Item Name"] = mutated_f
                    save_permanent_database()
                    st.success("Cascade item renaming script complete.")
                    st.rerun()

    with tab_m2:
        st.write("Current Active Account Identifiers List Base:", st.session_state.partner_list)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            new_p_node = st.text_input("Add New Partner Name Element", key="add_p").strip()
            if st.button("Publish Partner Roster Allocation"):
                if new_p_node and new_p_node not in st.session_state.partner_list:
                    st.session_state.partner_list.append(new_p_node)
                    new_r = pd.DataFrame([{"Partner Name": new_p_node, "Investment Amount": 0.0}])
                    st.session_state.partners_db = pd.concat([st.session_state.partners_db, new_r], ignore_index=True)
                    save_permanent_database()
                    st.success("New structural entity partner tracking registered.")
                    st.rerun()
        with col_p2:
            target_p = st.selectbox("Identify Partner Target to Rename", st.session_state.partner_list, key="ren_p_sel")
            mutated_p = st.text_input("Enter Mutated Partner Name", value=target_p, key="ren_p_val").strip()
            if st.button("Apply Rename on Partner Node"):
                if mutated_p and mutated_p != target_p:
                    idx = st.session_state.partner_list.index(target_p)
                    st.session_state.partner_list[idx] = mutated_p
                    st.session_state.partners_db.loc[st.session_state.partners_db["Partner Name"] == target_p, "Partner Name"] = mutated_p
                    save_permanent_database()
                    st.success("Identity profile configuration renaming done.")
                    st.rerun()

    with tab_m3:
        st.write("Current Operational Headings:", st.session_state.asset_categories)
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            new_a_node = st.text_input("Add New Asset Category Classification", key="add_a").strip()
            if st.button("Append Asset Category"):
                if new_a_node and new_a_node not in st.session_state.asset_categories:
                    st.session_state.asset_categories.append(new_a_node)
                    save_permanent_database()
                    st.success("Structural hierarchy configuration transformed.")
                    st.rerun()
        with col_a2:
            target_a = st.selectbox("Identify Asset Target to Rename", st.session_state.asset_categories, key="ren_a_sel")
            mutated_a = st.text_input("Enter Mutated Category Description", value=target_a, key="ren_a_val").strip()
            if st.button("Apply Rename on Asset Category Node"):
                if mutated_a and mutated_a != target_a:
                    idx = st.session_state.asset_categories.index(target_a)
                    st.session_state.asset_categories[idx] = mutated_a
                    if len(st.session_state.fixed_expenses) > 0:
                        st.session_state.fixed_expenses.loc[st.session_state.fixed_expenses["Category"] == target_a, "Category"] = mutated_a
                    save_permanent_database()
                    st.success("Asset ledger categories refactored successfully.")
                    st.rerun()

    with tab_m4:
        st.write("Current Operating Expense Head Codes:", st.session_state.expense_categories)
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            new_e_node = st.text_input("Add Operating Monthly Ledger Expense Type", key="add_e").strip()
            if st.button("Append Operating Cost Type Head"):
                if new_e_node and new_e_node not in st.session_state.expense_categories:
                    st.session_state.expense_categories.append(new_e_node)
                    save_permanent_database()
                    st.success("Expense lookup nodes modified.")
                    st.rerun()
        with col_e2:
            target_e = st.selectbox("Identify Expense Head Target to Rename", st.session_state.expense_categories, key="ren_e_sel")
            mutated_e = st.text_input("Enter Mutated Expense Head Designation", value=target_e, key="ren_e_val").strip()
            if st.button("Apply Rename on Expense Node"):
                if mutated_e and mutated_e != target_e:
                    idx = st.session_state.expense_categories.index(target_e)
                    st.session_state.expense_categories[idx] = mutated_e
                    if len(st.session_state.monthly_expenses_db) > 0:
                        st.session_state.monthly_expenses_db.loc[st.session_state.monthly_expenses_db["Category"] == target_e, "Category"] = mutated_e
                    save_permanent_database()
                    st.success("Operational bill lookup arrays adjusted.")
                    st.rerun()

    with tab_m5:
        st.write("Current Inventory Row Elements Matrix List Mapping:", st.session_state.inventory_items)
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            new_i_node = st.text_input("Add New Raw Inventory Material Item Context", key="add_i").strip()
            if st.button("Append Sourcing Material Descriptor Item"):
                if new_i_node and new_i_node not in st.session_state.inventory_items:
                    st.session_state.inventory_items.append(new_i_node)
                    new_inv_r = pd.DataFrame([{"Material Name": new_i_node, "Current Stock": 0.0, "Unit": "Kg/Ltr", "Alert Level": 10.0}])
                    st.session_state.inventory_db = pd.concat([st.session_state.inventory_db, new_inv_r], ignore_index=True)
                    save_permanent_database()
                    st.success("Asset ledger element linked to pipeline parameters.")
                    st.rerun()
        with col_i2:
            target_i = st.selectbox("Identify Raw Material Asset Target to Rename", st.session_state.inventory_items, key="ren_i_sel")
            mutated_i = st.text_input("Enter Mutated Inventory Row Item Element Node Name", value=target_i, key="ren_i_val").strip()
            if st.button("Apply Rename on Inventory Sourcing Node"):
                if mutated_i and mutated_i != target_i:
                    idx = st.session_state.inventory_items.index(target_i)
                    st.session_state.inventory_items[idx] = mutated_i
                    st.session_state.inventory_db.loc[st.session_state.inventory_db["Material Name"] == target_i, "Material Name"] = mutated_i
                    save_permanent_database()
                    st.success("Inventory node reference altered securely.")
                    st.rerun()

# ----------------------------------------------------------------------------------
# MODULE 11: SYSTEM USER PROVISIONING MANAGEMENT (Super Admin Only)
# ----------------------------------------------------------------------------------
elif choice == "👥 System User Provisioning":
    st.title("👥 Application Identity Access Profiles Matrix Provisioning")
    u_df = pd.DataFrame([{"System Login Identifier Context": k, "Privilege Access Group Matrix": v["role"], "Password Auth Token Block": v["password"]} for k, v in st.session_state.users_db.items()])
    st.dataframe(u_df, use_container_width=True)
    
    with st.form("iam_form"):
        st.markdown("### Provision New Dynamic Profile Identifier Access Connection Entry")
        reg_id = st.text_input("Desired Unique Account Identifier User ID").strip().lower()
        reg_pass = st.text_input("Auth Token Key Password Pass String Value", type="password")
        reg_role = st.selectbox("Access Group Privileges Assignment", ["Super Admin", "Admin", "Partner (View Only)"])
        if st.form_submit_button("Commit Profile Provisioning"):
            if reg_id and reg_pass:
                st.session_state.users_db[reg_id] = {"password": reg_pass, "role": reg_role}
                save_permanent_database()
                st.success("Application account authorization structure expanded successfully.")
                st.rerun()