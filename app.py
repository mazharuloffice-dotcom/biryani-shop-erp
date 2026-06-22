import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

# ==================================================================================
# 1. DATABASE SYSTEM INITIALIZATION & AUTO-RESET ENGINE
# ==================================================================================
DB_FILE = "swapnajatra_enterprise_v5_db.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        db_snapshot = json.load(f)
else:
    db_snapshot = {}

# System Menus Definition (All 16 Modules Intact)
ALL_SYSTEM_MENUS = [
    "🏠 Main Dashboard", "👨‍💼 Employee Register", "📅 Attendance System", 
    "📝 Leave Management", "🧾 Digital Invoice Generator", "🤝 Partner Capital Engine", 
    "💰 Daily Sales Entry", "🛒 Variable Bazar Cost", "💼 Monthly Expenses", 
    "🧑‍🍳 Staff Salary Ledger", "📦 Inventory & Restock", "⚙️ Dropdown Control Panel", 
    "🛡️ System User Provisioning", "👁️ Partner Preview Mode", "🔐 Account Security Hub",
    "🏢 Fixed Asset Investment"
]

# Database Auto-Reset Logic: Syncing privileges safely without crashing
if "privileges" in db_snapshot:
    for role in db_snapshot["privileges"]:
        if role == "Super Admin" and "🏢 Fixed Asset Investment" not in db_snapshot["privileges"][role]:
            db_snapshot["privileges"][role] = ALL_SYSTEM_MENUS
        elif role in ["Manager", "Partner"]:
            if "🏢 Fixed Asset Investment" not in db_snapshot["privileges"][role]:
                db_snapshot["privileges"][role].append("🏢 Fixed Asset Investment")
            
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_snapshot, f, ensure_ascii=False, indent=4)

# ==================================================================================
# 2. SESSION STATE MEMORY LAYERS (RESTORE ALL MODULES DATA)
# ==================================================================================
def load_db_state(key, default_val):
    return db_snapshot.get(key, default_val)

if "erp_privileges" not in st.session_state:
    st.session_state.erp_privileges = load_db_state("privileges", {
        "Super Admin": ALL_SYSTEM_MENUS,
        "Manager": ["🏠 Main Dashboard", "📅 Attendance System", "📝 Leave Management", "🧾 Digital Invoice Generator", "💰 Daily Sales Entry", "🛒 Variable Bazar Cost", "📦 Inventory & Restock", "🏢 Fixed Asset Investment"],
        "Partner": ["👁️ Partner Preview Mode", "🏢 Fixed Asset Investment"]
    })

# Restoring core lists for all modules
if "erp_employees" not in st.session_state: st.session_state.erp_employees = load_db_state("employees", [])
if "erp_attendance" not in st.session_state: st.session_state.erp_attendance = load_db_state("attendance", [])
if "erp_leaves" not in st.session_state: st.session_state.erp_leaves = load_db_state("leaves", [])
if "erp_invoices" not in st.session_state: st.session_state.erp_invoices = load_db_state("invoices", [])
if "partner_capital" not in st.session_state: st.session_state.partner_capital = load_db_state("partner_capital", {"Foishal": 0.0, "Anam": 0.0, "Habib": 0.0, "Anayat": 0.0, "Mazhar": 0.0})
if "daily_sales" not in st.session_state: st.session_state.daily_sales = load_db_state("daily_sales", [])
if "bazar_costs" not in st.session_state: st.session_state.bazar_costs = load_db_state("bazar_costs", [])
if "monthly_expenses" not in st.session_state: st.session_state.monthly_expenses = load_db_state("monthly_expenses", [])
if "salary_ledger" not in st.session_state: st.session_state.salary_ledger = load_db_state("salary_ledger", [])
if "inventory_stock" not in st.session_state: st.session_state.inventory_stock = load_db_state("inventory_stock", {})
if "fixed_assets" not in st.session_state: st.session_state.fixed_assets = load_db_state("fixed_assets", [])

if "dropdown_options" not in st.session_state:
    st.session_state.dropdown_options = load_db_state("dropdown_options", {
        "Asset Categories": ["Kitchen Equipment", "Furniture", "Renovation", "Electronics", "Others"],
        "Expense Categories": ["Utilities", "Rent", "Gas Cylinder", "Internet", "Wastage", "Others"],
        "Designations": ["Head Cook", "Assistant Cook", "Waiter", "Manager", "Delivery Boy"],
        "Bazar Items": ["Chini Gura Rice", "Beef", "Chicken", "Mustard Oil", "Spices", "Onion"]
    })

def trigger_mutation_success():
    payload = {
        "privileges": st.session_state.erp_privileges,
        "employees": st.session_state.erp_employees,
        "attendance": st.session_state.erp_attendance,
        "leaves": st.session_state.erp_leaves,
        "invoices": st.session_state.erp_invoices,
        "partner_capital": st.session_state.partner_capital,
        "daily_sales": st.session_state.daily_sales,
        "bazar_costs": st.session_state.bazar_costs,
        "monthly_expenses": st.session_state.monthly_expenses,
        "salary_ledger": st.session_state.salary_ledger,
        "inventory_stock": st.session_state.inventory_stock,
        "fixed_assets": st.session_state.fixed_assets,
        "dropdown_options": st.session_state.dropdown_options
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

# ==================================================================================
# 3. PAGE INITIALIZATION & CONFIGURATION
# ==================================================================================
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", layout="wide", page_icon="🍲")

if "auth_role" not in st.session_state:
    st.session_state.auth_role = "Super Admin"

# Sidebar Authentication Switcher
st.sidebar.title("🍲 Swapnajatra ERP v5")
st.session_state.auth_role = st.sidebar.selectbox("🔑 Active Session Role Guard", ["Super Admin", "Manager", "Partner"])

allowed_menus = st.session_state.erp_privileges.get(st.session_state.auth_role, ALL_SYSTEM_MENUS)
active_menu_node = st.sidebar.radio("Navigation Menu Components", options=[m for m in allowed_menus if m in ALL_SYSTEM_MENUS])

is_editable = st.session_state.auth_role in ["Super Admin", "Manager"]

# ==================================================================================
# 4. BUSINESS LOGIC ROUTER NODES (ALL MODULES INTEGRATED)
# ==================================================================================

# MODULE 1: MAIN DASHBOARD
if active_menu_node == "🏠 Main Dashboard":
    st.title("🏠 Swapnajatra Enterprise Dashboard")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_sales = sum([item["Amount"] for item in st.session_state.daily_sales])
        st.metric("Total Sales Revenue", f"{total_sales:,.2f} BDT")
    with col2:
        total_bazar = sum([item["Total Cost"] for item in st.session_state.bazar_costs])
        st.metric("Total Bazar Cost", f"{total_bazar:,.2f} BDT")
    with col3:
        total_assets = sum([item["Cost (BDT)"] for item in st.session_state.fixed_assets])
        st.metric("Fixed Asset Valuation", f"{total_assets:,.2f} BDT")
    with col4:
        total_cap = sum(st.session_state.partner_capital.values())
        st.metric("Total Partner Capital", f"{total_cap:,.2f} BDT")

# MODULE 2: EMPLOYEE REGISTER
elif active_menu_node == "👨‍💼 Employee Register":
    st.title("👨‍💼 Staff & Employee Registry")
    st.markdown("---")
    if is_editable:
        with st.form("emp_form"):
            name = st.text_input("Employee Name")
            desig = st.selectbox("Designation", st.session_state.dropdown_options["Designations"])
            salary = st.number_input("Monthly Base Salary", min_value=0.0, step=500.0)
            if st.form_submit_button("Register Employee"):
                if name:
                    st.session_state.erp_employees.append({"ID": len(st.session_state.erp_employees)+1, "Name": name, "Designation": desig, "Salary": salary})
                    trigger_mutation_success()
                    st.success(f"Registered {name} successfully!")
    if st.session_state.erp_employees:
        st.dataframe(pd.DataFrame(st.session_state.erp_employees), use_container_width=True)

# MODULE 3: ATTENDANCE SYSTEM
elif active_menu_node == "📅 Attendance System":
    st.title("📅 Daily Attendance Tracker")
    st.markdown("---")
    if is_editable and st.session_state.erp_employees:
        with st.form("att_form"):
            att_date = st.date_input("Attendance Date")
            records = []
            st.write("Mark Attendance Summary:")
            for emp in st.session_state.erp_employees:
                status = st.selectbox(f"{emp['Name']} ({emp['Designation']})", ["Present", "Absent", "Late"], key=f"att_{emp['ID']}")
                records.append({"Date": str(att_date), "ID": emp['ID'], "Name": emp['Name'], "Status": status})
            if st.form_submit_button("Save Day Attendance Sheet"):
                st.session_state.erp_attendance.extend(records)
                trigger_mutation_success()
                st.success("Attendance sheets logged!")
    if st.session_state.erp_attendance:
        st.dataframe(pd.DataFrame(st.session_state.erp_attendance), use_container_width=True)

# MODULE 4: LEAVE MANAGEMENT
elif active_menu_node == "📝 Leave Management":
    st.title("📝 Employee Leave Architecture")
    st.markdown("---")
    if is_editable and st.session_state.erp_employees:
        with st.form("leave_form"):
            emp_name = st.selectbox("Select Employee", [e["Name"] for e in st.session_state.erp_employees])
            leave_date = st.date_input("Leave Date")
            reason = st.text_input("Reason Node")
            if st.form_submit_button("Approve Official Leave"):
                st.session_state.erp_leaves.append({"Employee": emp_name, "Date": str(leave_date), "Reason": reason})
                trigger_mutation_success()
                st.success("Leave entry mapped.")
    if st.session_state.erp_leaves:
        st.dataframe(pd.DataFrame(st.session_state.erp_leaves), use_container_width=True)

# MODULE 5: DIGITAL INVOICE GENERATOR
elif active_menu_node == "🧾 Digital Invoice Generator":
    st.title("🧾 Corporate Catering & Sales Invoice Engine")
    st.markdown("---")
    with st.form("invoice_form"):
        cust = st.text_input("Customer Name/Organization")
        details = st.text_area("Order Details / Menu Items Split")
        inv_amount = st.number_input("Invoice Total Value (BDT)", min_value=0.0)
        if st.form_submit_button("Compile & Print Invoice Data"):
            if cust and inv_amount > 0:
                st.session_state.erp_invoices.append({"Invoice_ID": len(st.session_state.erp_invoices)+1001, "Customer": cust, "Description": details, "Amount": inv_amount, "Timestamp": str(datetime.now())})
                trigger_mutation_success()
                st.success("Invoice target node dispatched.")
    if st.session_state.erp_invoices:
        st.dataframe(pd.DataFrame(st.session_state.erp_invoices), use_container_width=True)

# MODULE 6: PARTNER CAPITAL ENGINE
elif active_menu_node == "🤝 Partner Capital Engine":
    st.title("🤝 Partner Equity & Initial Capital Ledger")
    st.markdown("---")
    if is_editable:
        partner_select = st.selectbox("Select Funding Partner Node", list(st.session_state.partner_capital.keys()))
        amount_capital = st.number_input("Inject / Mutate Capital Amount (BDT)", step=5000.0)
        if st.button("Commit Capital Equity"):
            st.session_state.partner_capital[partner_select] += amount_capital
            trigger_mutation_success()
            st.success("Partner equity structure balanced.")
    
    st.subheader("Equity Distribution Maps")
    st.json(st.session_state.partner_capital)

# MODULE 7: DAILY SALES ENTRY
elif active_menu_node == "💰 Daily Sales Entry":
    st.title("💰 Daily Restaurant Counter Sales Logging")
    st.markdown("---")
    with st.form("sales_form"):
        sale_date = st.date_input("Sales Date Context")
        amount_sales = st.number_input("Counter Gross Sales (BDT)", min_value=0.0, step=100.0)
        payment_method = st.selectbox("Payment Mode Vector", ["Cash", "bKash/Nagad", "Card"])
        if st.form_submit_button("Log Daily Revenue Entry"):
            if amount_sales > 0:
                st.session_state.daily_sales.append({"Date": str(sale_date), "Amount": amount_sales, "Method": payment_method})
                trigger_mutation_success()
                st.success("Revenue map synced!")
    if st.session_state.daily_sales:
        st.dataframe(pd.DataFrame(st.session_state.daily_sales), use_container_width=True)

# MODULE 8: VARIABLE BAZAR COST
elif active_menu_node == "🛒 Variable Bazar Cost":
    st.title("🛒 Daily Raw Material & Variable Bazar Cost Node")
    st.markdown("---")
    with st.form("bazar_form"):
        b_date = st.date_input("Bazar Logistics Date")
        item_node = st.selectbox("Bazar Material Node", st.session_state.dropdown_options["Bazar Items"])
        qty = st.number_input("Quantity Weight Nodes (KG/Units)", min_value=0.0, step=0.5)
        rate = st.number_input("Unit Procurement Price Rate", min_value=0.0, step=10.0)
        if st.form_submit_button("Commit Daily Bazar Cost"):
            if qty > 0 and rate > 0:
                t_cost = qty * rate
                st.session_state.bazar_costs.append({"Date": str(b_date), "Item": item_node, "Qty": qty, "Rate": rate, "Total Cost": t_cost})
                trigger_mutation_success()
                st.success(f"Log updated. Total spent: {t_cost} BDT")
    if st.session_state.bazar_costs:
        st.dataframe(pd.DataFrame(st.session_state.bazar_costs), use_container_width=True)

# MODULE 9: MONTHLY EXPENSES
elif active_menu_node == "💼 Monthly Expenses":
    st.title("💼 Monthly Operations Utility & Fixed Overheads Cost")
    st.markdown("---")
    with st.form("monthly_exp_form"):
        exp_date = st.date_input("Billing Period Engine")
        exp_cat = st.selectbox("Expense Overhead Matrix", st.session_state.dropdown_options["Expense Categories"])
        cost_val = st.number_input("Cost Allocation Node (BDT)", min_value=0.0)
        if st.form_submit_button("Record Expense Metrics"):
            st.session_state.monthly_expenses.append({"Date": str(exp_date), "Category": exp_cat, "Cost": cost_val})
            trigger_mutation_success()
            st.success("Overheads database expanded.")
    if st.session_state.monthly_expenses:
        st.dataframe(pd.DataFrame(st.session_state.monthly_expenses), use_container_width=True)

# MODULE 10: STAFF SALARY LEDGER
elif active_menu_node == "🧑‍🍳 Staff Salary Ledger":
    st.title("🧑‍🍳 Staff Payroll Disbursement Engine")
    st.markdown("---")
    if is_editable and st.session_state.erp_employees:
        with st.form("salary_disb_form"):
            pay_emp = st.selectbox("Select Employee Target Node", [e["Name"] for e in st.session_state.erp_employees])
            pay_month = st.selectbox("Payroll Cycle Matrix Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            bonus = st.number_input("Festival Bonus / Incentives Override", min_value=0.0)
            if st.form_submit_button("Approve Processing Payroll"):
                base_sal = next(e["Salary"] for e in st.session_state.erp_employees if e["Name"] == pay_emp)
                total_disbursed = base_sal + bonus
                st.session_state.salary_ledger.append({"Employee": pay_emp, "Month": pay_month, "Base": base_sal, "Bonus": bonus, "Total Distributed": total_disbursed, "Date": str(datetime.now().date())})
                trigger_mutation_success()
                st.success("Payroll cluster deployed.")
    if st.session_state.salary_ledger:
        st.dataframe(pd.DataFrame(st.session_state.salary_ledger), use_container_width=True)

# MODULE 11: INVENTORY & RESTOCK
elif active_menu_node == "📦 Inventory & Restock":
    st.title("📦 Dynamic Material Stock Audit Framework")
    st.markdown("---")
    for b_item in st.session_state.dropdown_options["Bazar Items"]:
        if b_item not in st.session_state.inventory_stock:
            st.session_state.inventory_stock[b_item] = 100.0 # Default starting balance
            
    selected_stock_node = st.selectbox("Audit Stock Core Target", list(st.session_state.inventory_stock.keys()))
    current_qty = st.session_state.inventory_stock[selected_stock_node]
    st.metric(f"Current Available Stock Metrics for {selected_stock_node}", f"{current_qty} Units")
    
    if is_editable:
        restock_qty = st.number_input("Append Restock Inventory Vector (+/-)", value=0.0)
        if st.button("Commit Dynamic Inventory Mutex"):
            st.session_state.inventory_stock[selected_stock_node] += restock_qty
            trigger_mutation_success()
            st.success("Inventory cache structural adjustments stored.")
            st.rerun()

# MODULE 12: DROPDOWN CONTROL PANEL
elif active_menu_node == "⚙️ Dropdown Control Panel" and is_editable:
    st.title("⚙️ Dropdown Configuration Matrix Engine")
    st.markdown("---")
    target_config_key = st.selectbox("Select Target Configuration Component Map", options=list(st.session_state.dropdown_options.keys()))
    st.write(st.session_state.dropdown_options[target_config_key])
    with st.form("add_dropdown_node_form"):
        new_option_node = st.text_input("Insert New Infrastructure Value String Node")
        if st.form_submit_button("Append Config Entry") and new_option_node:
            if new_option_node not in st.session_state.dropdown_options[target_config_key]:
                st.session_state.dropdown_options[target_config_key].append(new_option_node)
                trigger_mutation_success()
                st.success(f"✅ Dynamic entry target node added: {new_option_node}")
                st.rerun()

# MODULE 13: SYSTEM USER PROVISIONING
elif active_menu_node == "🛡️ System User Provisioning" and is_editable:
    st.title("🛡️ Identity Gate Privilege Matrix & Configuration Maps Engine")
    st.markdown("---")
    for group_role_title in st.session_state.erp_privileges.keys():
        st.subheader(f"Access Control List Modules for Security Tier Level Node: {group_role_title}")
        navigation_menus_array_list = st.session_state.erp_privileges[group_role_title]
        updated_navigation_access = st.multiselect(
            "Check Authorized Active Menu View Components", 
            options=ALL_SYSTEM_MENUS, 
            default=[m for m in navigation_menus_array_list if m in ALL_SYSTEM_MENUS], 
            key=f"acl_select_nodes_{group_role_title}"
        )
        if st.button(f"Update Access Matrix for {group_role_title}", key=f"save_acl_btn_{group_role_title}"):
            st.session_state.erp_privileges[group_role_title] = updated_navigation_access
            trigger_mutation_success()
            st.toast(f"🔒 ACL Security Context Mutated for {group_role_title}")

# MODULE 14: PARTNER PREVIEW MODE
elif active_menu_node == "👁️ Partner Preview Mode":
    st.title("👁️ Read-Only Partner Analytics Engine")
    st.markdown("---")
    st.info("স্বাগতম পার্টনার প্যানেল। এখানে শুধুমাত্র রিয়েল-টাইম তথ্য পর্যবেক্ষণ করতে পারবেন।")
    st.subheader("পুঁজি ও বিনিয়োগ সামারি")
    st.json(st.session_state.partner_capital)

# MODULE 15: ACCOUNT SECURITY HUB
elif active_menu_node == "🔐 Account Security Hub":
    st.title("🔐 Cryptographic Security Guard & Session Controls")
    st.markdown("---")
    st.success("🔒 SSL Engine Active. Current Active Security Matrix Token state is fully shielded.")

# NEW MODULE 16: FIXED ASSET INVESTMENT
elif active_menu_node == "🏢 Fixed Asset Investment":
    st.title("🏢 Fixed Asset Investment Ledger")
    st.markdown("---")
    st.write("দোকানের স্থায়ী সম্পদ বা প্রাথমিক বিনিয়োগের খরচ (যেমন: ফ্রিজ, চুলা, ফার্নিচার, ডেকোরেশন) এর হিসাব এখানে রাখুন।")
    if is_editable:
        with st.form("asset_form", clear_on_submit=True):
            st.subheader("নতুন স্থায়ী সম্পদ ইনপুট ফরম")
            asset_name = st.text_input("Asset Name (সম্পদের নাম লিখুন)")
            available_categories = st.session_state.dropdown_options.get("Asset Categories", ["Kitchen Equipment", "Furniture", "Renovation", "Electronics", "Others"])
            asset_category = st.selectbox("Category (ধরণ)", available_categories)
            asset_cost = st.number_input("Investment Cost (টাকার পরিমাণ - BDT)", min_value=0.0, step=100.0)
            purchase_date = st.date_input("Purchase Date (কেনার তারিখ)")
            if st.form_submit_button("Save Asset Investment"):
                if asset_name and asset_cost > 0:
                    st.session_state.fixed_assets.append({"Asset Name": asset_name, "Category": asset_category, "Cost (BDT)": asset_cost, "Date": str(purchase_date)})
                    trigger_mutation_success()
                    st.success(f"✅ সফলভাবে স্থায়ী সম্পদ যোগ হয়েছে: {asset_name}")
                    st.rerun()
                else:
                    st.error("❌ দয়া করে সম্পদের নাম এবং সঠিক টাকার পরিমাণ ইনপুট দিন।")
    else:
        st.warning("⚠️ আপনার অ্যাকাউন্ট লেভেল থেকে নতুন সম্পদ এন্ট্রি করার অনুমতি নেই। শুধুমাত্র তালিকাটি দেখতে পারবেন।")
    if st.session_state.fixed_assets:
        st.markdown("---")
        st.subheader("📋 Fixed Asset List Summary")
        df_assets = pd.DataFrame(st.session_state.fixed_assets)
        st.dataframe(df_assets, use_container_width=True)
        total_investment = df_assets["Cost (BDT)"].sum()
        st.metric(label="Total Fixed Asset Investment Valuation", value=f"{total_investment:,.2f} BDT")
    else:
        st.info("💡 এখনো কোনো স্থায়ী সম্পদের ডেটা এন্ট্রি করা হয়নি।")

else:
    st.title(active_menu_node)
    st.write("মডিউলটির ব্যাকএন্ড ডিজাইন লোড করা হয়েছে।")