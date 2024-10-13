import streamlit as st
import pandas as pd

# Sample DataFrame to hold users and bills
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'bills' not in st.session_state:
    st.session_state.bills = pd.DataFrame(columns=['Seller', 'Bill Amount', 'Brokerage', 'Status'])
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Admin Interface
def admin_interface():
    st.title("Admin Dashboard")
    
    # Create Seller
    st.subheader("Create Seller Account")
    seller_id = st.text_input("Seller ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Create Seller"):
        if seller_id and password:
            st.session_state.users[seller_id] = password
            st.success(f"Seller {seller_id} created.")
        else:
            st.error("Please provide both Seller ID and Password.")
    
    # View Sellers Online
    st.subheader("Online Sellers")
    st.write(len(st.session_state.users))  # For demo, counting users as online for now

    # View Bills
    st.subheader("Bills")
    st.dataframe(st.session_state.bills)

    # Update Brokerage
    if not st.session_state.bills.empty:
        selected_bill = st.selectbox("Select Bill to Update", st.session_state.bills.index)
        brokerage_amount = st.number_input("Brokerage Amount", min_value=0.0)
        
        if st.button("Add Brokerage"):
            st.session_state.bills.at[selected_bill, 'Brokerage'] = brokerage_amount
            st.session_state.bills.at[selected_bill, 'Status'] = 'Processed'
            st.success("Brokerage added to the bill.")

    # Statistics
    st.subheader("Statistics")
    total_profit = st.session_state.bills['Bill Amount'].sum() - st.session_state.bills['Brokerage'].sum()
    st.write(f"Total Profit: {total_profit}")
    st.write(f"Total Transactions: {len(st.session_state.bills)}")

# Seller Interface
def seller_interface():
    st.title("Seller Dashboard")
    seller_id = st.text_input("Seller ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if seller_id in st.session_state.users and st.session_state.users[seller_id] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = seller_id
            st.success(f"Welcome {seller_id}")
        else:
            st.error("Invalid ID or Password")

    if st.session_state.logged_in:
        bill_amount = st.number_input("Enter Bill Amount", min_value=0.0)
        
        if st.button("Submit Bill"):
            new_bill = pd.DataFrame([[seller_id, bill_amount, 0, 'Pending']], columns=['Seller', 'Bill Amount', 'Brokerage', 'Status'])
            st.session_state.bills = pd.concat([st.session_state.bills, new_bill], ignore_index=True)
            st.success("Bill submitted.")

# Navigation between admin and seller
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose Role", ["Admin", "Seller"])

    if choice == "Admin":
        admin_interface()
    else:
        seller_interface()

if __name__ == "__main__":
    main()
