import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Swapnajatra Biryani Bari ERP", page_icon="🍲", layout="wide")

# ----------------------------------------------------------------------------------
# 1. DATABASE / STATE MANAGEMENT (Simulated using Streamlit Session State)
# ----------------------------------------------------------------------------------
if 'users_db' not in st.session_state:
    # Default Users List (Role: Password)
    st.session_state.users_db = {
        "superadmin": {"password": "123", "role": "Super Admin"},
        "admin": {"password": "456", "role": "Admin"},
        "partner": {"password": "789", "role": "Partner (View Only)"}
    }

if 'menu_items' not in st.session_state:
    # Default Dropdown Menu Items
    st.session_state.menu_items = ["Kacchi Biryani", "Beef Tehari", "Chicken Biryani", "Borhani", "Water"]

if 'sales_records' not in st.session_state:
    # Sample Initial Sales Data
    st.session_state.sales_records = pd.DataFrame(columns=[
        "Date", "Item Name", "Rate per Plate", "Total Plates", "Adjustment", "Net Total", "Entered By"
    ])

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ----------------------------------------------------------------------------------
# 2. LOGIN & AUTHENTICATION SYSTEM
# ----------------------------------------------------------------------------------
def login_page():
    st.markdown("<h2 style='text-align: center;'>🍲 Swapnajatra Biryani Bari ERP 🍲</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>System Secure Login</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username / ID").strip().lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")
            
            if submitted:
                if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.user_role = st.session_state.users_db[username]["role"]
                    st.success(f"Welcome {username.capitalize()} ({st.session_state.user_role})")
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password")

# ----------------------------------------------------------------------------------
# MAIN LOGIC (Check if logged in)
# ----------------------------------------------------------------------------------
if st.session_state.logged_in_user is None:
    login_page()
else:
    # Sidebar - User Info & Logout
    st.sidebar.title("🔒 Security Control")
    st.sidebar.write(f"**User:** {st.session_state.logged_in_user.capitalize()}")
    st.sidebar.write(f"**Role:** {st.session_state.user_role}")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logged_in_user = None
        st.session_state.user_role = None
        st.rerun()

    # Define Role-based Access Privileges
    is_superadmin = st.session_state.user_role == "Super Admin"
    is_admin = st.session_state.user_role in ["Super Admin", "Admin"]
    is_partner = st.session_state.user_role == "Partner (View Only)"

    # Navigation Menu
    st.sidebar.markdown("---")
    st.sidebar.title("📁 ERP Menu")
    
    # Restrict pages based on Roles
    menu_options = ["📊 Live Dashboard", "💰 Daily Sales Entry"]
    if is_admin:
        menu_options.append("⚙️ Menu & Item Settings")
    if is_superadmin:
        menu_options.append("👥 User Creation & Privileges")
        
    choice = st.sidebar.radio("Go to:", menu_options)

    # ----------------------------------------------------------------------------------
    # PAGE 1: LIVE DASHBOARD (All users can view)
    # ----------------------------------------------------------------------------------
    if choice == "📊 Live Dashboard":
        st.title("📊 Swapnajatra Biryani Bari - Financial Dashboard")
        
        if len(st.session_state.sales_records) == 0:
            st.info("No sales records available for today. Please enter data in 'Daily Sales Entry'.")
        else:
            df = st.session_state.sales_records
            total_revenue = df["Net Total"].sum()
            total_plates_sold = df["Total Plates"].sum()
            
            # KPI Cards
            c1, c2 = st.columns(2)
            c1.metric("Total Sales Revenue", f"{total_revenue:,.2f} BDT")
            c2.metric("Total Plates Sold", f"{total_plates_sold} Plates")
            
            st.markdown("### 📋 Recent Sales Ledger")
            st.dataframe(df, use_container_width=True)
            
            # Simple Chart
            st.markdown("### 📈 Item-wise Sales Distribution")
            fig = px.bar(df, x="Item Name", y="Net Total", color="Item Name", title="Revenue per Item")
            st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------------------------------------
    # PAGE 2: DAILY SALES ENTRY (Super Admin, Admin, and managers can input)
    # ----------------------------------------------------------------------------------
    elif choice == "💰 Daily Sales Entry":
        st.title("💰 Item-wise Daily Sales Entry")
        
        if is_partner:
            st.error("🚫 Access Denied! Partners have 'View Only' permission.")
        else:
            with st.form("sales_entry_form", clear_on_submit=True):
                st.markdown("### Input Sales Data")
                
                # Dynamic Dropdown populated from current item settings
                selected_item = st.selectbox("Select Menu Item Name", st.session_state.menu_items)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    rate_per_plate = st.number_input("Per Plate Rate (BDT)", min_value=0.0, step=10.0, value=220.0)
                with col2:
                    total_plates = st.number_input("Number of Total Plates Sold", min_value=0, step=1, value=10)
                with col3:
                    adjustment = st.number_input("Any Adjustment / Discount (- or +)", step=5.0, value=0.0)
                
                sale_date = st.date_input("Sales Date", datetime.now())
                
                # Calculation formula
                calculated_net = (rate_per_plate * total_plates) + adjustment
                st.markdown(f"**Estimated Net Total:** `{calculated_net:,.2f} BDT`")
                
                submit_sale = st.form_submit_button("Save Entry ✅")
                
                if submit_sale:
                    new_row = {
                        "Date": sale_date.strftime("%Y-%m-%d"),
                        "Item Name": selected_item,
                        "Rate per Plate": rate_per_plate,
                        "Total Plates": total_plates,
                        "Adjustment": adjustment,
                        "Net Total": calculated_net,
                        "Entered By": st.session_state.logged_in_user.capitalize()
                    }
                    st.session_state.sales_records = pd.concat([st.session_state.sales_records, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"Successfully recorded sale for {selected_item}!")

    # ----------------------------------------------------------------------------------
    # PAGE 3: DROPDOWN MENU & ITEM SETTINGS (Admin & Super Admin)
    # ----------------------------------------------------------------------------------
    elif choice == "⚙️ Menu & Item Settings":
        st.title("⚙️ Dropdown Menu List Management")
        
        st.markdown("### 📋 Current Active Dropdown Items")
        st.write(st.session_state.menu_items)
        
        # Section A: Create New Item
        st.markdown("---")
        st.markdown("### ➕ Add New Menu Item")
        new_item = st.text_input("Enter New Item Name (e.g., Mutton Kacchi, Salad)").strip()
        if st.button("Save New Item"):
            if new_item and new_item not in st.session_state.menu_items:
                st.session_state.menu_items.append(new_item)
                st.success(f"'{new_item}' successfully added to the system dropdown menu!")
                st.rerun()
            else:
                st.warning("Item already exists or empty!")

        # Section B: Rename Existing Item
        st.markdown("---")
        st.markdown("### ✏️ Rename Existing Item")
        item_to_rename = st.selectbox("Select Item to Rename", st.session_state.menu_items)
        renamed_name = st.text_input("Enter New Name", value=item_to_rename).strip()
        if st.button("Apply Rename"):
            if renamed_name and renamed_name != item_to_rename:
                index = st.session_state.menu_items.index(item_to_rename)
                st.session_state.menu_items[index] = renamed_name
                st.success(f"Renamed '{item_to_rename}' to '{renamed_name}' successfully!")
                st.rerun()

    # ----------------------------------------------------------------------------------
    # PAGE 4: USER CREATION & PRIVILEGES (Super Admin Only)
    # ----------------------------------------------------------------------------------
    elif choice == "👥 User Creation & Privileges":
        st.title("👥 System User Management & Security Privileges")
        
        # Display Current Users
        st.markdown("### 🔑 Existing Users & Roles")
        users_df = pd.DataFrame([
            {"Username": k, "Role": v["role"], "Password": v["password"]} 
            for k, v in st.session_state.users_db.items()
        ])
        st.dataframe(users_df, use_container_width=True)
        
        # Create New User Form
        st.markdown("---")
        st.markdown("### ➕ Register New User Login Option")
        
        with st.form("create_user_form"):
            new_username = st.text_input("New Username / ID (Unique)").strip().lower()
            new_password = st.text_input("Setup Password", type="password")
            new_role = st.selectbox("Assign Privilege Role", ["Super Admin", "Admin", "Partner (View Only)"])
            
            create_btn = st.form_submit_button("Register System User")
            
            if create_btn:
                if not new_username or not new_password:
                    st.error("Username and Password cannot be left blank.")
                elif new_username in st.session_state.users_db:
                    st.error("This Username is already taken! Use a different one.")
                else:
                    st.session_state.users_db[new_username] = {
                        "password": new_password,
                        "role": new_role
                    }
                    st.success(f"Success! User '{new_username}' registered as a '{new_role}'.")
                    st.rerun()