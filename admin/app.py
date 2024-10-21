import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker
import altair as alt
import plotly.express as px
import base64

# Database connection and model setup
engine = create_engine("sqlite://///home/zorin/webtech/py/db's/app_data5.db")
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    seller_id = Column(String, unique=True)
    password = Column(String)
    seller_name = Column(String)

    bank_name_1 = Column(String)
    bank_account_number_1 = Column(String)
    ifsc_code_1 = Column(String)
    bank_name_2 = Column(String, default='-')
    bank_account_number_2 = Column(String, default='-')
    ifsc_code_2 = Column(String, default='-')

class SellerBill(Base):
    __tablename__ = 'sellerBill'
    id = Column(Integer, primary_key=True)
    seller_id = Column(String)
    
    driver_name = Column(String)
    driver_phone_number = Column(Float)
    vehicle_number = Column(String)
    transport_name = Column(String)
    reverse_charges = Column(String)

    invoice_number = Column(String)
    date_of_invoice = Column(Date)
    delivery_date = Column(Date)
    waybill_number = Column(Float)
    mep_number = Column(String)

    billing_name = Column(String)
    billing_address = Column(String)
    billing_city = Column(String)
    billing_state = Column(String)
    billing_phone_number = Column(Float)
    billing_gst_number = Column(String)
 
    shipping_name = Column(String)
    shipping_address = Column(String)
    shipping_city = Column(String)
    shipping_state = Column(String)
    shipping_phone_number = Column(Float)
    shipping_gst_number = Column(String)
    
    broker_name = Column(String)
    # buyer_name = Column(String)
    seller_name = Column(String)

    total_amount = Column(Float)

    bank_name_1 = Column(String)
    bank_account_number_1 = Column(String)
    ifsc_code_1 = Column(String)
    bank_name_2 = Column(String, default='-')
    bank_account_number_2 = Column(String, default='-')
    ifsc_code_2 = Column(String, default='-')

    brokerage = Column(Float, default=0)
    status = Column(String, default='pending')


class Buyer(Base):
    __tablename__ = 'buyers'
    
    id = Column(Integer, primary_key=True)
    billing_name = Column(String)
    billing_address = Column(String)
    billing_city = Column(String)
    billing_state = Column(String)
    billing_phone_number = Column(Float)
    billing_gst_number = Column(String)
    
    shipping_name = Column(String)
    shipping_address = Column(String)
    shipping_city = Column(String)
    shipping_state = Column(String)
    shipping_phone_number = Column(Float)
    shipping_gst_number = Column(String)

# Create tables if they do not exist
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
def admin_interface():
    st.title("Admin Dashboard")
    
    # Create Seller
    st.subheader("Create Seller Account")
    seller_id = st.text_input("Seller ID")
    seller_name = st.text_input("Seller Name")
    password = st.text_input("Password", type="password")
    
    if st.button("Create Seller"):
        if seller_id and password:
            session = Session()
            try:
                new_user = User(seller_id=seller_id, password=password, seller_name=seller_name)
                session.add(new_user)
                session.commit()
                st.success(f"Seller {seller_id} created.")
            except Exception as e:
                session.rollback()
                st.error(f"Error: {e}")
            finally:
                session.close()
        else:
            st.error("Please provide both Seller ID and Password.")

    # View Sellers
    st.subheader("Registered Sellers")
    try:
        sellers = pd.read_sql('SELECT * FROM users', con=engine)
        if sellers.empty:
            st.write("No sellers registered.")
        else:
            st.dataframe(sellers)
    except Exception as e:
        st.error(f"Error retrieving sellers: {e}")


def add_buyer():
    st.subheader("Add Buyer Details")

    # Input fields for billing details
    billing_name = st.text_input("Billing Name")
    billing_address = st.text_input("Billing Address")
    billing_city = st.text_input("Billing City")
    billing_state = st.text_input("Billing State")
    billing_phone_number = st.text_input("Billing Phone Number")
    billing_gst_number = st.text_input("Billing GST Number")
    
    # Checkbox to check if shipping and billing addresses are the same
    same_address = st.checkbox("Shipping address is the same as billing address")

    # Input fields for shipping details
    shipping_name = st.text_input("Shipping Name", value=billing_name if same_address else "")
    shipping_address = st.text_input("Shipping Address", value=billing_address if same_address else "")
    shipping_city = st.text_input("Shipping City", value=billing_city if same_address else "")
    shipping_state = st.text_input("Shipping State", value=billing_state if same_address else "")
    shipping_phone_number = st.text_input("Shipping Phone Number", value=billing_phone_number if same_address else 0)
    shipping_gst_number = st.text_input("Shipping GST Number", value=billing_gst_number if same_address else "")

    if st.button("Submit Buyer"):
        session = Session()
        try:
            session.execute(
                text('INSERT INTO buyers (billing_name, billing_address, billing_city, billing_state, '
                     'billing_phone_number, billing_gst_number, shipping_name, shipping_address, '
                     'shipping_city, shipping_state, shipping_phone_number, shipping_gst_number) VALUES '
                     '(:billing_name, :billing_address, :billing_city, :billing_state, '
                     ':billing_phone_number, :billing_gst_number, :shipping_name, :shipping_address, '
                     ':shipping_city, :shipping_state, :shipping_phone_number, :shipping_gst_number)'),
                {
                    'billing_name': billing_name,
                    'billing_address': billing_address,
                    'billing_city': billing_city,
                    'billing_state': billing_state,
                    'billing_phone_number': billing_phone_number,
                    'billing_gst_number': billing_gst_number,
                    'shipping_name': shipping_name,
                    'shipping_address': shipping_address,
                    'shipping_city': shipping_city,
                    'shipping_state': shipping_state,
                    'shipping_phone_number': shipping_phone_number,
                    'shipping_gst_number': shipping_gst_number,
                }
            )
            session.commit()
            st.success("Buyer added successfully.")
        except Exception as e:
            session.rollback()
            st.error(f"Error adding buyer: {e}")
        finally:
            session.close()

def list_and_manage_buyers():
    st.subheader("List and Edit Buyers")

    session = Session()
    try:
        # Fetch all buyers from the database
        buyers = pd.read_sql(text('SELECT * FROM buyers'), con=session.bind)

        if buyers.empty:
            st.write("No buyers found.")
            return
        
        # Display buyers in a table
        selected_buyer_id = st.selectbox("Select Buyer", buyers['id'].tolist(), format_func=lambda x: buyers.loc[buyers['id'] == x, 'billing_name'].values[0])
        
        # Get selected buyer's details
        selected_buyer = buyers[buyers['id'] == selected_buyer_id].iloc[0]

        # Input fields for editing buyer details
        billing_name = st.text_input("Billing Name", value=selected_buyer['billing_name'])
        billing_address = st.text_input("Billing Address", value=selected_buyer['billing_address'])
        billing_city = st.text_input("Billing City", value=selected_buyer['billing_city'])
        billing_state = st.text_input("Billing State", value=selected_buyer['billing_state'])
        billing_phone_number = st.text_input("Billing Phone Number", value=str(selected_buyer['billing_phone_number']))
        billing_gst_number = st.text_input("Billing GST Number", value=selected_buyer['billing_gst_number'])

        # Checkbox for same address
        same_address = st.checkbox("Shipping address is the same as billing address", value=True)
        
        shipping_name = st.text_input("Shipping Name", value=selected_buyer['shipping_name'] if not same_address else billing_name)
        shipping_address = st.text_input("Shipping Address", value=selected_buyer['shipping_address'] if not same_address else billing_address)
        shipping_city = st.text_input("Shipping City", value=selected_buyer['shipping_city'] if not same_address else billing_city)
        shipping_state = st.text_input("Shipping State", value=selected_buyer['shipping_state'] if not same_address else billing_state)
        shipping_phone_number = st.text_input("Shipping Phone Number", value=str(selected_buyer['shipping_phone_number']) if not same_address else billing_phone_number)
        shipping_gst_number = st.text_input("Shipping GST Number", value=selected_buyer['shipping_gst_number'] if not same_address else billing_gst_number)

        if st.button("Update Buyer"):
            try:
                # Update buyer details in the database
                session.execute(
                    text('UPDATE buyers SET billing_name = :billing_name, billing_address = :billing_address, '
                         'billing_city = :billing_city, billing_state = :billing_state, '
                         'billing_phone_number = :billing_phone_number, billing_gst_number = :billing_gst_number, '
                         'shipping_name = :shipping_name, shipping_address = :shipping_address, '
                         'shipping_city = :shipping_city, shipping_state = :shipping_state, '
                         'shipping_phone_number = :shipping_phone_number, shipping_gst_number = :shipping_gst_number '
                         'WHERE id = :id'),
                    {
                        'billing_name': billing_name,
                        'billing_address': billing_address,
                        'billing_city': billing_city,
                        'billing_state': billing_state,
                        'billing_phone_number': billing_phone_number,
                        'billing_gst_number': billing_gst_number,
                        'shipping_name': shipping_name,
                        'shipping_address': shipping_address,
                        'shipping_city': shipping_city,
                        'shipping_state': shipping_state,
                        'shipping_phone_number': shipping_phone_number,
                        'shipping_gst_number': shipping_gst_number,
                        'id': selected_buyer_id
                    }
                )
                session.commit()
                st.success("Buyer updated successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error updating buyer: {e}")

        # Delete Buyer Option
        if st.button("Delete Buyer"):
            confirm_delete = st.warning("Are you sure you want to delete this buyer?")

            if confirm_delete:
                try:
                    # Log the ID for debugging
                    st.write(f"Attempting to delete buyer with ID: {selected_buyer_id}")
                    session.execute(
                        text('DELETE FROM buyers WHERE id = :id'),
                        {'id': selected_buyer_id}
                    )
                    session.commit()
                    st.success("Buyer deleted successfully.")
                    # Refresh the buyer list if needed
                    st.rerun()  # This will refresh the page
                except Exception as e:
                    session.rollback()
                    st.error(f"Error deleting buyer: {e}")
    finally:
        session.close()


def view_and_edit_bills():
    
    st.subheader("View and Edit Bills")
    session = Session()

    try:
        bills = pd.read_sql('SELECT * FROM sellerBill', con=engine)
        st.write(bills)
        if not bills.empty:
            # Select a bill to edit
            selected_bill_id = st.selectbox(
                "Select Bill to Edit", 
                bills['id'].tolist(),
                format_func=lambda x: f"Bill ID: {x} - Invoice: {bills.loc[bills['id'] == x, 'invoice_number'].values[0]}"
            )

            # Get selected bill details
            selected_bill = bills[bills['id'] == selected_bill_id].iloc[0]

            # Display all fields in a form for editing
            with st.form(key="bill_edit_form"):
                driver_name = st.text_input("Driver Name", value=selected_bill['driver_name'])
                driver_phone_number = st.text_input("Driver Phone Number", value=selected_bill['driver_phone_number'])
                vehicle_number = st.text_input("Vehicle Number", value=selected_bill['vehicle_number'])
                transport_name = st.text_input("Transport Name", value=selected_bill['transport_name'])
                reverse_charges = st.text_input("Reverse Charges", value=selected_bill['reverse_charges'])
                invoice_number = st.text_input("Invoice Number", value=selected_bill['invoice_number'])
                date_of_invoice = st.date_input("Date of Invoice", value=pd.to_datetime(selected_bill['date_of_invoice']))
                delivery_date = st.date_input("Delivery Date", value=pd.to_datetime(selected_bill['delivery_date']))
                waybill_number = st.text_input("Waybill Number", value=selected_bill['waybill_number'])
                mep_number = st.text_input("MEP Number", value=selected_bill['mep_number'])
                billing_name = st.text_input("Billing Name", value=selected_bill['billing_name'])
                billing_address = st.text_input("Billing Address", value=selected_bill['billing_address'])
                billing_city = st.text_input("Billing City", value=selected_bill['billing_city'])
                billing_state = st.text_input("Billing State", value=selected_bill['billing_state'])
                billing_phone_number = st.text_input("Billing Phone Number", value=selected_bill['billing_phone_number'])
                billing_gst_number = st.text_input("Billing GST Number", value=selected_bill['billing_gst_number'])
                shipping_name = st.text_input("Shipping Name", value=selected_bill['shipping_name'])
                shipping_address = st.text_input("Shipping Address", value=selected_bill['shipping_address'])
                shipping_city = st.text_input("Shipping City", value=selected_bill['shipping_city'])
                shipping_state = st.text_input("Shipping State", value=selected_bill['shipping_state'])
                shipping_phone_number = st.text_input("Shipping Phone Number", value=selected_bill['shipping_phone_number'])
                shipping_gst_number = st.text_input("Shipping GST Number", value=selected_bill['shipping_gst_number'])
                broker_name = st.text_input("Broker Name", value=selected_bill['broker_name'])
                seller_name = st.text_input("Seller Name", value=selected_bill['seller_name'])
                total_amount = st.number_input("Total Amount", value=selected_bill['total_amount'])
                bank_name_1 = st.text_input("Bank Name 1", value=selected_bill['bank_name_1'])
                bank_account_number_1 = st.text_input("Bank Account Number 1", value=selected_bill['bank_account_number_1'])
                ifsc_code_1 = st.text_input("IFSC Code 1", value=selected_bill['ifsc_code_1'])
                bank_name_2 = st.text_input("Bank Name 2", value=selected_bill['bank_name_2'])
                bank_account_number_2 = st.text_input("Bank Account Number 2", value=selected_bill['bank_account_number_2'])
                ifsc_code_2 = st.text_input("IFSC Code 2", value=selected_bill['ifsc_code_2'])
                brokerage = st.number_input("Brokerage", value=selected_bill['brokerage'], min_value=0.0)

                # Form submit button
                submitted = st.form_submit_button("Update Bill")

                if submitted:
                    try:
                        # Set status based on brokerage
                        status = 'pending' if brokerage == 0 or pd.isnull(brokerage) else 'completed'

                        # Update the selected bill
                        session.execute(
                            text('UPDATE sellerBill SET driver_name = :driver_name, driver_phone_number = :driver_phone_number, '
                                 'vehicle_number = :vehicle_number, transport_name = :transport_name, reverse_charges = :reverse_charges, '
                                 'invoice_number = :invoice_number, date_of_invoice = :date_of_invoice, delivery_date = :delivery_date, '
                                 'waybill_number = :waybill_number, mep_number = :mep_number, billing_name = :billing_name, '
                                 'billing_address = :billing_address, billing_city = :billing_city, billing_state = :billing_state, '
                                 'billing_phone_number = :billing_phone_number, billing_gst_number = :billing_gst_number, '
                                 'shipping_name = :shipping_name, shipping_address = :shipping_address, shipping_city = :shipping_city, '
                                 'shipping_state = :shipping_state, shipping_phone_number = :shipping_phone_number, '
                                 'shipping_gst_number = :shipping_gst_number, broker_name = :broker_name, seller_name = :seller_name, '
                                 'total_amount = :total_amount, bank_name_1 = :bank_name_1, bank_account_number_1 = :bank_account_number_1, '
                                 'ifsc_code_1 = :ifsc_code_1, bank_name_2 = :bank_name_2, bank_account_number_2 = :bank_account_number_2, '
                                 'ifsc_code_2 = :ifsc_code_2, brokerage = :brokerage, status = :status WHERE id = :id'),
                            {
                                'driver_name': driver_name,
                                'driver_phone_number': driver_phone_number,
                                'vehicle_number': vehicle_number,
                                'transport_name': transport_name,
                                'reverse_charges': reverse_charges,
                                'invoice_number': invoice_number,
                                'date_of_invoice': date_of_invoice,
                                'delivery_date': delivery_date,
                                'waybill_number': waybill_number,
                                'mep_number': mep_number,
                                'billing_name': billing_name,
                                'billing_address': billing_address,
                                'billing_city': billing_city,
                                'billing_state': billing_state,
                                'billing_phone_number': billing_phone_number,
                                'billing_gst_number': billing_gst_number,
                                'shipping_name': shipping_name,
                                'shipping_address': shipping_address,
                                'shipping_city': shipping_city,
                                'shipping_state': shipping_state,
                                'shipping_phone_number': shipping_phone_number,
                                'shipping_gst_number': shipping_gst_number,
                                'broker_name': broker_name,
                                'seller_name': seller_name,
                                'total_amount': total_amount,
                                'bank_name_1': bank_name_1,
                                'bank_account_number_1': bank_account_number_1,
                                'ifsc_code_1': ifsc_code_1,
                                'bank_name_2': bank_name_2,
                                'bank_account_number_2': bank_account_number_2,
                                'ifsc_code_2': ifsc_code_2,
                                'brokerage': brokerage,
                                'status': status,
                                'id': selected_bill_id
                            }
                        )
                        session.commit()
                        st.success("Bill updated successfully.")
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error updating bill: {e}")

        else:
            st.write("No bills available.")
    except Exception as e:
        st.error(f"Error retrieving bills: {e}")
    finally:
        session.close()

import matplotlib.pyplot as plt
import seaborn as sns
    
def view_statistics():
    st.subheader("Statistics")
    session = Session()
    try:
        # Sample city coordinates (you can expand this list)
        city_coordinates = {
            'Bangalore': (12.9716, 77.5946),
            'Bengaluru': (12.9716, 77.5946),  # Same as Bangalore
            'Hyderabad': (17.3850, 78.4867),
            'Mysuru': (12.2958, 76.6393),
            'Mangaluru': (12.9141, 74.8560),
            'Hubballi': (15.3640, 75.1240),
            'Belgaum': (15.8489, 74.5019),
            'Kolar': (13.1282, 78.8344),
            'Chennai': (13.0827, 80.2707),
            'Davanagere': (14.4687, 75.9152),
        }

        bills = pd.read_sql('SELECT * FROM sellerBill', con=engine)
        if not bills.empty:
            # Total Amount and Transactions
            total_amount = bills['total_amount'].sum()
            total_transactions = len(bills)
            st.write(f"Total Amount: {total_amount:.2f}")
            st.write(f"Total Transactions: {total_transactions}")
            # Interactive visualization using Streamlit's selectbox and Altair
            columns = bills.columns.tolist()

            # Select columns for visualization
            data=bills
            
            # Streamlit app
            st.title("Interactive Dashboard with Drag-and-Drop")

            # Drag-and-drop interface for selecting columns
            selected_x = st.selectbox("Select X-axis:", data.columns)
            selected_y = st.selectbox("Select Y-axis:", data.columns)

            # Create visualization using Plotly
            if selected_x and selected_y:
                fig = px.bar(data, x=selected_x, y=selected_y, title=f"{selected_y} vs {selected_x}")
                st.plotly_chart(fig)
            
            # Create a DataFrame for city shipment counts
            if 'shipping_city' in bills.columns:
                city_counts = bills['shipping_city'].value_counts().reset_index()
                city_counts.columns = ['city', 'count']

                # Convert city names to coordinates
                city_counts['coordinates'] = city_counts['city'].map(city_coordinates)

                # Filter out cities that don't have coordinates
                filtered_city_counts = city_counts[city_counts['coordinates'].notna()]

                if not filtered_city_counts.empty:
                    # Create a scatter plot map
                    filtered_city_counts[['lat', 'lon']] = pd.DataFrame(filtered_city_counts['coordinates'].tolist(), index=filtered_city_counts.index)

                    fig = px.scatter_geo(
                        filtered_city_counts,
                        lat='lat',
                        lon='lon',
                        text='city',  # City name
                        size='count',
                        title="Shipments by City",
                        color='count',
                        color_continuous_scale=px.colors.sequential.algae,
                        projection='natural earth'  # You can adjust the projection type
                    )
                    fig.update_traces(textfont=dict(color='black'))  # Set text color to black
                    fig.update_layout(
                        plot_bgcolor='lightblue'  # Background color for the plot area
                    )
                    st.plotly_chart(fig)
                else:
                    st.write("No valid cities found for visualization.")

            # Date-related statistics
            bills['date_of_invoice'] = pd.to_datetime(bills['date_of_invoice'])
            bills['delivery_date'] = pd.to_datetime(bills['delivery_date'])

            # Area Chart for total amount over time
            area_data = bills.groupby('date_of_invoice')['total_amount'].sum().reset_index()
            st.area_chart(area_data.set_index('date_of_invoice'))

            # Bar Chart for transport name distribution
            transport_data = bills['transport_name'].value_counts()
            st.bar_chart(transport_data)

            bills['date_of_invoice'] = pd.to_datetime(bills['date_of_invoice'], format='%Y/%m/%d')  # Convert to datetime

            # Check for any missing values
            if bills['date_of_invoice'].isnull().any():
                st.error("There are missing dates in the 'date_of_invoice' column.")
            else:
                # Line Chart for total amount per month
                monthly_data = bills.resample('M', on='date_of_invoice')['total_amount'].sum().reset_index()
                st.line_chart(monthly_data.set_index('date_of_invoice'))
            # Scatter Plot for total amount vs delivery date
            fig, ax = plt.subplots()
            ax.scatter(bills['delivery_date'], bills['total_amount'])
            ax.set_title("Total Amount vs Delivery Date")
            ax.set_xlabel("Delivery Date")
            ax.set_ylabel("Total Amount")
            st.pyplot(fig)

            # Additional statistics based on other attributes
            billing_state_data = bills['billing_state'].value_counts()
            st.bar_chart(billing_state_data)

            shipping_city_data = bills['shipping_city'].value_counts()
            st.bar_chart(shipping_city_data)

        else:
            st.write("No transactions to calculate statistics.")
    except Exception as e:
        st.error(f"Error retrieving bills: {e}")
    finally:
        session.close()

def manage_agents():
    st.subheader("Manage Agents")

    session = Session()

    # Search agents
    search_term = st.text_input("Search Agents")
    if search_term:
        agents = pd.read_sql(
            text('SELECT * FROM agents WHERE name LIKE :search_term'),
            con=session.bind,
            params={'search_term': f'%{search_term}%'})
    else:
        agents = pd.read_sql(text('SELECT * FROM agents'), con=session.bind)

    if not agents.empty:
        st.dataframe(agents)

        selected_agent_id = st.selectbox("Select Agent to Update/Delete", agents['id'].tolist())

        # Delete Agent
        if st.button("Delete Agent"):
            try:
                session.execute(text('DELETE FROM agents WHERE id = :id'), {'id': selected_agent_id})
                session.commit()
                st.success("Agent deleted successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error deleting agent: {e}")

        # Update Agent
        agent_details = agents[agents['id'] == selected_agent_id].iloc[0]
        agent_name = st.text_input("Agent Name", value=agent_details['name'])
        pan_number = st.text_input("PAN Number", value=agent_details['pan_number'])
        address = st.text_area("Address", value=agent_details['address'])
        mobile_number = st.text_input("Mobile Number", value=agent_details['mobile_number'])
        email = st.text_input("Email", value=agent_details['email'])
        terms_and_conditions = st.text_area("Terms and Conditions", value=agent_details['terms_and_conditions'])

        if st.button("Update Agent"):
            try:
                session.execute(
                    text('UPDATE agents SET name = :name, pan_number = :pan_number, address = :address, '
                         'mobile_number = :mobile_number, email = :email, terms_and_conditions = :terms '
                         'WHERE id = :id'),
                    {
                        'name': agent_name,
                        'pan_number': pan_number,
                        'address': address,
                        'mobile_number': mobile_number,
                        'email': email,
                        'terms': terms_and_conditions,
                        'id': selected_agent_id
                    }
                )
                session.commit()
                st.success("Agent updated successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error updating agent: {e}")

    # Add New Agent
    new_agent_name = st.text_input("Add New Agent Name")
    new_pan_number = st.text_input("PAN Number")
    new_address = st.text_area("Address")
    new_mobile_number = st.text_input("Mobile Number")
    new_email = st.text_input("Email")
    new_terms_and_conditions = st.text_area("Terms and Conditions")

    if st.button("Add Agent"):
        try:
            session.execute(
                text('INSERT INTO agents (name, pan_number, address, mobile_number, email, terms_and_conditions) '
                     'VALUES (:name, :pan_number, :address, :mobile_number, :email, :terms)'),
                {
                    'name': new_agent_name,
                    'pan_number': new_pan_number,
                    'address': new_address,
                    'mobile_number': new_mobile_number,
                    'email': new_email,
                    'terms': new_terms_and_conditions
                }
            )
            session.commit()
            st.success("Agent added successfully.")
        except Exception as e:
            session.rollback()
            st.error(f"Error adding agent: {e}")

    session.close()

def manage_broker_bills():
    st.subheader("Manage Broker Bills")

    session = Session()
    
    # Search broker bills
    search_term = st.text_input("Search Broker Bills")
    if search_term:
        bills = pd.read_sql(
            text('SELECT * FROM broker_bills WHERE order_number LIKE :search_term'),
            con=session.bind,
            params={'search_term': f'%{search_term}%'})
    else:
        bills = pd.read_sql(text('SELECT * FROM broker_bills'), con=session.bind)

    if not bills.empty:
        st.dataframe(bills)

        selected_bill_id = st.selectbox("Select Bill to Update/Delete", bills['id'].tolist())

        if st.button("Delete Bill"):
            try:
                session.execute(text('DELETE FROM broker_bills WHERE id = :id'), {'id': selected_bill_id})
                session.commit()
                st.success("Bill deleted successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error deleting bill: {e}")

        # Update bill
        bill_details = bills[bills['id'] == selected_bill_id].iloc[0]

        order_date = st.date_input("Order Date", value=bill_details['order_date'])
        order_number = st.text_input("Order Number", value=bill_details['order_number'])
        total_tons = st.number_input("Total Tons", min_value=0.0, value=bill_details['total_tons'])

        if st.button("Update Bill"):
            try:
                session.execute(
                    text('UPDATE broker_bills SET order_date = :order_date, order_number = :order_number, total_tons = :total_tons '
                         'WHERE id = :id'),
                    {
                        'order_date': order_date,
                        'order_number': order_number,
                        'total_tons': total_tons,
                        'id': selected_bill_id
                    }
                )
                session.commit()
                st.success("Bill updated successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error updating bill: {e}")

    else:
        st.write("No bills found.")
    
    session.close()

def initiate_broker_bill():
    st.subheader("Initiate Broker Bill")

    session = Session()

    # Fetch agents, sellers, and buyers from the database
    agents = pd.read_sql(text('SELECT id, name FROM agents'), con=session.bind)
    sellers = pd.read_sql(text('SELECT seller_id, seller_name FROM users'), con=session.bind)
    buyers = pd.read_sql(text('SELECT id, billing_name FROM buyers'), con=session.bind)
    
    # Dropdowns for agent, seller, and buyer selection
    selected_agent = st.selectbox("Select Agent", agents['id'].tolist(), 
                                   format_func=lambda x: agents.loc[agents['id'] == x, 'name'].values[0])
    selected_seller = st.selectbox("Select Seller", sellers['seller_id'].tolist(), 
                                     format_func=lambda x: sellers.loc[sellers['seller_id'] == x, 'seller_name'].values[0])
    selected_buyer = st.selectbox("Select Buyer", buyers['id'].tolist(), 
                                    format_func=lambda x: buyers.loc[buyers['id'] == x, 'billing_name'].values[0])

    order_date = st.date_input("Order Date")
    order_number = st.text_input("Order Number")
    total_tons = st.number_input("Total Tons", min_value=0.0)

    if st.button("Initiate Broker Bill"):
        try:
            # Insert into broker_bills
            session.execute(
                text('INSERT INTO broker_bills (agent_id, order_date, order_number, total_tons, seller_id, buyer_id) '
                     'VALUES (:agent_id, :order_date, :order_number, :total_tons, :seller_id, :buyer_id)'),
                {
                    'agent_id': selected_agent,
                    'order_date': order_date,
                    'order_number': order_number,
                    'total_tons': total_tons,
                    'seller_id': selected_seller,
                    'buyer_id': selected_buyer
                }
            )
            session.commit()
            st.success("Broker Bill initiated successfully.")
        except Exception as e:
            session.rollback()
            st.error(f"Error initiating broker bill: {e}")

    # Fetch initiated broker bills to allow selection
    initiated_bills = pd.read_sql(text('SELECT * FROM broker_bills'), con=session.bind)
    
    if not initiated_bills.empty:
        selected_bill_id = st.selectbox("Select Initiated Bill by ID", initiated_bills['id'].tolist())

        # Display the details of the selected bill
        selected_bill = initiated_bills[initiated_bills['id'] == selected_bill_id]
        
        st.write("### Selected Bill Details")
        st.dataframe(selected_bill)

        # Add Bill Details
        st.subheader("Add Bill Details")
        
        quality_name = st.text_input("Quality Name")
        brand_name = st.text_input("Brand Name")
        quantity = st.number_input("Quantity (in tons)", min_value=0.0)
        rate = st.number_input("Rate", min_value=0.0)
        condition = st.text_input("Condition")

        if st.button("Add Bill Detail"):
            try:
                # Insert into broker_bill_details
                session.execute(
                    text('INSERT INTO broker_bill_details (broker_bill_id, quality_name, brand_name, quantity, rate, condition) '
                         'VALUES (:broker_bill_id, :quality_name, :brand_name, :quantity, :rate, :condition)'),
                    {
                        'broker_bill_id': selected_bill_id,
                        'quality_name': quality_name,
                        'brand_name': brand_name,
                        'quantity': quantity,
                        'rate': rate,
                        'condition': condition
                    }
                )
                session.commit()
                st.success("Bill detail added successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error adding bill detail: {e}")

    session.close()

# def view_broker_bills():
#     st.subheader("View Broker Bills")

#     session = Session()
#     # Fetch all broker bills
#     broker_bills = pd.read_sql(text('SELECT * FROM broker_bills'), con=session.bind)
    
#     if not broker_bills.empty:
#         st.dataframe(broker_bills)
    
#     if broker_bills.empty:
#         st.write("No broker bills found.")
#     else:
#         selected_bill_id = st.selectbox("Select Broker Bill by ID", broker_bills['id'].tolist())

#         # Fetch selected bill details
#         bill_details = broker_bills[broker_bills['id'] == selected_bill_id].iloc[0]

#         # Display basic bill details
#         st.write("### Broker Bill Details")
#         st.write(pd.DataFrame([bill_details]))

#         # Fetch agent info
#         agent_info = pd.read_sql(
#             text('SELECT * FROM agents WHERE id = :agent_id'),
#             con=session.bind,
#             params={'agent_id': bill_details['agent_id']}
#         )

#         # Fetch seller info
#         seller_info = pd.read_sql(
#             text('SELECT * FROM users WHERE seller_id = :seller_id'),
#             con=session.bind,
#             params={'seller_id': bill_details['seller_id']}
#         )

#         # Fetch buyer info
#         buyer_info = pd.read_sql(
#             text('SELECT * FROM buyers WHERE id = :buyer_id'),
#             con=session.bind,
#             params={'buyer_id': bill_details['buyer_id']}
#         )

#         # Display agent info in table format
#         if not agent_info.empty:
#             st.write("### Agent Info")
#             st.dataframe(agent_info)

#         # Display seller info in table format
#         if not seller_info.empty:
#             st.write("### Seller Info")
#             st.dataframe(seller_info)

#         # Display buyer info in table format
#         if not buyer_info.empty:
#             st.write("### Buyer Info")
#             st.dataframe(buyer_info)

#         # Fetch broker bill details
#         bill_details_df = pd.read_sql(
#             text('SELECT * FROM broker_bill_details WHERE broker_bill_id = :broker_bill_id'),
#             con=session.bind,
#             params={'broker_bill_id': selected_bill_id}
#         )

#         # Display broker bill details in table format
#         st.write("### Bill Details")
#         if not bill_details_df.empty:
#             st.dataframe(bill_details_df)
#         else:
#             st.write("No bill details found for this broker bill.")

#     session.close()
def view_broker_bills():
    st.subheader("View Broker Bills")

    session = Session()

    # Fetch all broker bills
    broker_bills = pd.read_sql(text('SELECT * FROM broker_bills'), con=session.bind)

    if broker_bills.empty:
        st.write("No broker bills found.")
    else:
        # Initialize session state for pagination
        if 'page' not in st.session_state:
            st.session_state.page = 0
            st.session_state.page_size = 10

        # Calculate total pages
        total_rows = len(broker_bills)
        total_pages = total_rows // st.session_state.page_size + (total_rows % st.session_state.page_size > 0)

        # Get the current page data
        start_row = st.session_state.page * st.session_state.page_size
        end_row = start_row + st.session_state.page_size
        page_data = broker_bills.iloc[start_row:end_row]

        # Display the current page of broker bills
        st.dataframe(page_data)

        # Pagination controls, displayed only if there are more than 10 rows
        if total_rows > st.session_state.page_size:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button("Previous Page") and st.session_state.page > 0:
                    st.session_state.page -= 1
            with col2:
                st.write(f"Page {st.session_state.page + 1} of {total_pages}")
            with col3:
                if st.button("Next Page") and st.session_state.page < total_pages - 1:
                    st.session_state.page += 1

        selected_bill_id = st.selectbox("Select Broker Bill by ID", broker_bills['id'].tolist())

        # Fetch and display additional details when a bill is selected
        if selected_bill_id:
            # Fetch selected bill details
            bill_details = broker_bills[broker_bills['id'] == selected_bill_id].iloc[0]

            # Display basic bill details
            st.write("### Broker Bill Details")
            st.write(pd.DataFrame([bill_details]))
            st.write(bill_details['agent_id'])

            # Fetch and display agent, seller, buyer info
            agent_info = pd.read_sql(
                text('SELECT * FROM agents WHERE id = :agent_id'),
                con=session.bind,
                params={'agent_id': int(bill_details['agent_id'])}
            )

            seller_info = pd.read_sql(
                text('SELECT * FROM users WHERE seller_id = :seller_id'),
                con=session.bind,
                params={'seller_id': bill_details['seller_id']}
            )

            buyer_info = pd.read_sql(
                text('SELECT * FROM buyers WHERE id = :buyer_id'),
                con=session.bind,
                params={'buyer_id': bill_details['buyer_id']}
            )
            if not agent_info.empty:
                st.write("### Agent Info")
                st.dataframe(agent_info)

            if not seller_info.empty:
                st.write("### Seller Info")
                st.dataframe(seller_info)

            if not buyer_info.empty:
                st.write("### Buyer Info")
                st.dataframe(buyer_info)

            # Fetch and display broker bill details
            bill_details_df = pd.read_sql(
                text('SELECT * FROM broker_bill_details WHERE broker_bill_id = :broker_bill_id'),
                con=session.bind,
                params={'broker_bill_id': selected_bill_id}
            )

            st.write("### Bill Details")
            if not bill_details_df.empty:
                st.dataframe(bill_details_df)
            else:
                st.write("No bill details found for this broker bill.")
            # Display the PDF generation button
            if st.button("Generate PDF"):
                pdf_buffer = create_broker_bill_pdf(bill_details, agent_info, seller_info, buyer_info, bill_details_df)

                # View the PDF
                display_pdf(pdf_buffer.getvalue())

                # Download the PDF
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=f"broker_bill_{selected_bill_id}.pdf",
                    mime="application/pdf"
                )
    
    session.close()
# Function to display PDF inline in the Streamlit app
def display_pdf(pdf_data):
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

import io
from reportlab.lib.pagesizes import letter, A1
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def create_broker_bill_pdf(bill_details, agent_info, seller_info, buyer_info, bill_details_df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.5 * inch)
    elements = []
    styles = getSampleStyleSheet()

    # Section 1: Bill Details
    elements.append(Paragraph(f"Broker Bill ID: {bill_details['id']}", styles['Title']))
    elements.append(Spacer(1, 0.2 * inch))

    bill_data = [
        ["Order Date", bill_details['order_date'], "Order Number", bill_details['order_number']],
        ["Total Tons", bill_details['total_tons'], "Status", bill_details['status']],
        ["Seller ID", bill_details['seller_id'], "Buyer ID", bill_details['buyer_id']],
    ]

    bill_table = Table(bill_data, colWidths=[1.75 * inch] * 4)
    bill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(bill_table)
    elements.append(Spacer(0.3, 0.1 * inch))

    # Section 2: Agent Info
    if not agent_info.empty:
        elements.append(Paragraph("Agent Information", styles['Heading2']))

        # Create a new list to hold rows for the agent table
        agent_data = []

        # Loop through each column in the DataFrame
        for column in agent_info.columns:
            # Create a new row for each field
            agent_data.append([column, agent_info[column].iloc[0]])  # Assuming you want the first agent's details

        # Create a table from the list of rows
        agent_table = Table(agent_data, colWidths=[2.0 * inch, 3.0 * inch])  # Adjust widths as necessary
        agent_table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(agent_table)
        elements.append(Spacer(0.3, 0.1 * inch))


    # Section 3: Seller Info
    if not seller_info.empty:
        elements.append(Paragraph("Seller Information", styles['Heading2']))

        # Transform seller_info into a list of lists for rows
        seller_data = [['Field', 'Value']] + [[column, seller_info.iloc[0][column]] for column in seller_info.columns]

        # Create the seller table with fields in rows
        seller_table = Table(seller_data, colWidths=[2.0 * inch, 4.0 * inch])
        seller_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),               # Header text alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),             # Padding for the header
        ]))

        elements.append(seller_table)
        elements.append(Spacer(1, 0.2 * inch))

    # Section 4: Buyer Info
    if not buyer_info.empty:
        elements.append(Paragraph("Buyer Information", styles['Heading2']))

        # Transform buyer_info into a list of lists for rows
        buyer_data = [['Field', 'Value']] + [[column, buyer_info.iloc[0][column]] for column in buyer_info.columns]

        # Create the buyer table with fields in rows
        buyer_table = Table(buyer_data, colWidths=[2.0 * inch, 4.0 * inch])
        buyer_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),               # Header text alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),             # Padding for the header
        ]))

        elements.append(buyer_table)
        elements.append(Spacer(1, 0.2 * inch))


    # Section 5: Detailed Bill Information
    if not bill_details_df.empty:
        elements.append(Paragraph("Bill Details", styles['Heading2']))

        # Add the column headers (table names) to the table data
        bill_details_data = [bill_details_df.columns.tolist()] + bill_details_df.values.tolist()

        # Create the table with the headers
        bill_details_table = Table(bill_details_data, colWidths=[0.9 * inch] * len(bill_details_df.columns))

        # Apply a style to the table
        bill_details_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),               # Header text alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),             # Padding for the header
        ]))

        elements.append(bill_details_table)
        elements.append(Spacer(1, 0.2 * inch))


    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def view_deleted_seller_bills():
    st.subheader("View Deleted Seller Bills")
    session = Session()
    try:
        deleted_bills = pd.read_sql('SELECT * FROM deleted_sellerBills', con=engine)
        if deleted_bills.empty:
            st.write("No deleted seller bills.")
        else:
            st.dataframe(deleted_bills)
    except Exception as e:
        st.error(f"Error retrieving deleted seller bills: {e}")
    finally:
        session.close()

def main():
    st.sidebar.title("Admin Menu")
    page = st.sidebar.selectbox("Choose a page", ["Initiate Broker Bill","View Broker Bills", "Manage Broker Bills", "Manage Agents", "Add Buyer" , "List and Manage Buyers", "View and Edit Bills", "Statistics", "View Deleted Seller Bills", "Create and View Users"])

    if page == "View and Edit Bills":
        view_and_edit_bills()
    elif page == "Statistics":
        view_statistics()
    elif page == "Create and View Users":
        admin_interface()
    elif page == "View Deleted Seller Bills":
        view_deleted_seller_bills()
    elif page == "Add Buyer":
        add_buyer()
    elif page == "List and Manage Buyers":
        list_and_manage_buyers()
    elif page == "Initiate Broker Bill":
        initiate_broker_bill()
    elif page == "Manage Broker Bills":
        manage_broker_bills()
    elif page == "Manage Agents":
        manage_agents()
    elif page == "View Broker Bills":
        view_broker_bills()

if __name__ == "__main__":
    main()
