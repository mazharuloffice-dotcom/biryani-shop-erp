import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os
import base64

# Page Configuration for Premium UI look
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", page_icon="🍲", layout="wide")

# Custom CSS Injector for modern card designs, clean forms and premium aesthetic
st.markdown("""
    <style>
    /* Global Styles */
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700; color: #1E1E24; }
    
    /* Premium KPI Card Styling */
    .kpi-card-container {
        display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap;
    }
    .kpi-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); border-left: 5px solid #ff4b4b;
        flex: 1; min-width: 220px; transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .kpi-title { font-size: 14px; color: #6D6D75; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
    .kpi-value { font-size: 24px; font-weight: 700; color: #1E1E24; margin-top: 5px; }
    
    /* Form & Section Wrappers */
    .stForm { background-color: #ffffff; padding: 25px !important; border-radius: 12px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important; border: 1px solid #EAEAEA !important; }
    div[data-testid="stExpander"] { background-color: #ffffff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
    
    /* Login Page Design Styling */
    .login-header { text-align: center; padding: 20px; background: linear-gradient(135deg, #FF4B4B, #FF7676); border-radius: 12px 12px 0 0; color: white; }
    .login-box { border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); background-color: white; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# DATABASE HARD-DRIVE STORAGE SYSTEM (JSON Persistent Layer)
# ----------------------------------------------------------------------------------
DB_FILE = "erp_database.json"

def load_permanent_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
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

if 'shop_name' not in st.session_state: st.session_state.shop_name = disk_data.get("shop_name", "SWAPNAJATRA BIRYANI BARI")
if 'shop_address' not in st.session_state: st.session_state.shop_address = disk_data.get("shop_address", "Mirpur, Dhaka, Bangladesh")

if 'users_db' not in st.session_state:
    st.session_state.users_db = disk_data.get("users_db", {
        "superadmin": {"password": "123", "role": "Super Admin", "permissions": ALL_AVAILABLE_MENUS},
        "admin": {"password": "456", "role": "Admin", "permissions": ALL_AVAILABLE_MENUS[:-1]},
        "partner": {"password": "789", "role": "Partner (View Only)", "permissions": ["📊 Financial Dashboard"]}
    })

if 'menu_items' not in st.session_state: st.session_state.menu_items = disk_data.get("menu_items", ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"])
if 'partner_list' not in st.session_state: st.session_state.partner_list = disk_data.get("partner_list", ["Foishal", "Anam", "Habib", "Anayat"])
if 'asset_categories' not in st.session_state: st.session_state.asset_categories = disk_data.get("asset_categories", ["Shop Rent", "Startup Assets", "Utility Installation", "Legal/Licenses"])
if 'expense_categories' not in st.session_state: st.session_state.expense_categories = disk_data.get("expense_categories", ["Electricity Bill", "Gas/Wood Bill", "Waste Management", "Marketing", "Others"])
if 'inventory_items' not in st.session_state: st.session_state.inventory_items = disk_data.get("inventory_items", ["Miniket Rice", "Beef Meat", "Polao Rice", "Soyabean Oil", "Onion", "Spices"])
if 'employees_profiles' not in st.session_state: st.session_state.employees_profiles = disk_data.get("employees_profiles", {})

if 'partners_db' not in st.session_state:
    p_records = disk_data.get("partners_db", [])
    st.session_state.partners_db = pd.DataFrame(p_records) if p_records else pd.DataFrame([{"Partner Name": p, "Investment Amount": 0.0} for p in st.session_state.partner_list])
if 'fixed_expenses' not in st.session_state: st.session_state.fixed_expenses = pd.DataFrame(disk_data.get("fixed_expenses", [])) if disk_data.get("fixed_expenses", []) else pd.DataFrame(columns=["Date", "Category", "Asset/Cost Item", "Amount"])
if 'monthly_expenses_db' not in st.session_state: st.session_state.monthly_expenses_db = pd.DataFrame(disk_data.get("monthly_expenses_db", [])) if disk_data.get("monthly_expenses_db", []) else pd.DataFrame(columns=["Date", "Category", "Particulars", "Amount (BDT)"])
if 'variable_bazar' not in st.session_state: st.session_state.variable_bazar = pd.DataFrame(disk_data.get("variable_bazar", [])) if disk_data.get("variable_bazar", []) else pd.DataFrame(columns=["Date", "Bazar Item Name", "Quantity/Weight", "Total Cost (BDT)", "Purchased By"])
if 'sales_records' not in st.session_state: st.session_state.sales_records = pd.DataFrame(disk_data.get("sales_records", [])) if disk_data.get("sales_records", []) else pd.DataFrame(columns=["Date", "Month-Year", "Item Name", "Rate per Plate", "Total Plates", "Adjustment", "Net Total"])
if 'salary_db' not in st.session_state: st.session_state.salary_db = pd.DataFrame(disk_data.get("salary_db", [])) if disk_data.get("salary_db", []) else pd.DataFrame(columns=["Date", "Staff Name", "Designation", "Salary Type", "Amount Paid (BDT)"])
if 'inventory_db' not in st.session_state:
    i_records = disk_data.get("inventory_db", [])
    st.session_state.inventory_db = pd.DataFrame(i_records) if i_records else pd.DataFrame([{"Material Name": m, "Current Stock": 0.0, "Unit": "Kg/Ltr", "Alert Level": 10.0} for m in st.session_state.inventory_items])

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = disk_data.get("logged_in_user", None)
if 'user_role' not in st.session_state: st.session_state.user_role = disk_data.get("user_role", None)

def get_month_year_str(dt_val): return dt_val.strftime("%B %Y")

# ----------------------------------------------------------------------------------
# SECURITY AUTHENTICATION SHIELD (Beautiful Box Login UI)
# ----------------------------------------------------------------------------------
if st.session_state.logged_in_user is None:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="login-header"><h2>🍲 {st.session_state.shop_name}</h2><p style="margin:0;opacity:0.9;">Enterprise Resource Planning Base Platform</p></div>', unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("👤 Username / Unique ID").strip().lower()
            password = st.text_input("🔑 Security Access Password", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Sign In Securely To System", use_container_width=True):
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    save_permanent_database()
                    st.rerun()
                else: st.error("❌ Access Denied: Invalid Credentials Configuration.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Sidebar Luxury Brand Header Panel
st.sidebar.markdown(f"<div style='text-align: center; padding: 10px; background-color: #ff4b4b; color: white; border-radius: 8px; margin-bottom: 15px;'><h3>🍲 Swapnajatra ERP</h3><small>{st.session_state.shop_address}</small></div>", unsafe_allow_html=True)

# User Info Card
with st.sidebar.container(border=True):
    st.markdown(f"👤 **User:** `{st.session_state.logged_in_user.upper()}`")
    st.markdown(f"🛡️ **Role:** `{st.session_state.user_role}`")
    if st.sidebar.button("Logout Securely 🚪", use_container_width=True, type="secondary"):
        st.session_state.logged_in_user = None
        st.session_state.user_role = None
        save_permanent_database()
        st.rerun()

user_allowed_menus = st.session_state.users_db.get(st.session_state.logged_in_user, {}).get("permissions", ALL_AVAILABLE_MENUS)
st.sidebar.markdown("---")
filtered_menu_options = [m for m in ALL_AVAILABLE_MENUS if m in user_allowed_menus]
choice = st.sidebar.radio("🎯 Select Module to Navigate:", filtered_menu_options)
is_partner_view = st.session_state.user_role == "Partner (View Only)"

# ----------------------------------------------------------------------------------
# 1. FINANCIAL DASHBOARD MODULE (LOOKTIVE & USER-FRIEND