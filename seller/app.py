import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.platypus import Spacer

from reportlab.pdfgen import canvas
import io
import numpy as np
# Database connection
engine = create_engine("sqlite://///home/zorin/webtech/py/db's/app_data5.db")
Session = sessionmaker(bind=engine)

# Initialize session state variables if not already initialized
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    st.session_state.seller_name = None

# Function to handle login
def login_page():
    st.subheader("Login")
    seller_id = st.text_input("Seller ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        session = Session()
        try:
            result = session.execute(
                text('SELECT * FROM users WHERE seller_id = :seller_id AND password = :password'), 
                {'seller_id': seller_id, 'password': password}
            ).fetchone()
            st.write(type(result))
            st.write(result)

            if result:
                user_data = list(result)
                st.session_state.logged_in = True
                st.session_state.current_user = seller_id
                st.session_state.seller_name = user_data[3]
                st.success(f"Welcome {st.session_state.seller_name}")
                st.rerun()
            else:
                st.error("Invalid Seller ID or Password")
        except Exception as e:
            st.error(f"Error during login: {e}")
        finally:
            session.close()

# Function to update seller profile
def update_seller_profile():
    st.subheader("Update Seller Profile")
    
    # Fetch current seller details
    session = Session()
    seller_id = st.session_state.current_user
    try:
        # Fetch user details
        result = session.execute(
            text('SELECT * FROM users WHERE seller_id = :seller_id'),
            {'seller_id': seller_id}
        ).fetchone()

        if result:
            # Convert the result to a dictionary using the column names
            seller_data = dict(result._mapping)  # Using _mapping to get a dictionary

            # Input fields for profile and bank details
            new_seller_name = st.text_input("Seller Name", value=seller_data['seller_name'])
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            # Bank details
            new_bank_name_1 = st.text_input("Bank Name 1", value=seller_data['bank_name_1'])
            new_bank_account_number_1 = st.text_input("Bank Account Number 1", value=seller_data['bank_account_number_1'])
            new_ifsc_code_1 = st.text_input("IFSC Code 1", value=seller_data['ifsc_code_1'])
            new_bank_name_2 = st.text_input("Bank Name 2", value=seller_data['bank_name_2'])
            new_bank_account_number_2 = st.text_input("Bank Account Number 2", value=seller_data['bank_account_number_2'])
            new_ifsc_code_2 = st.text_input("IFSC Code 2", value=seller_data['ifsc_code_2'])
            
            if st.button("Update Profile"):
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    # Update seller profile in the database
                    session.execute(
                        text('UPDATE users SET seller_name = :seller_name, password = :password, '
                             'bank_name_1 = :bank_name_1, bank_account_number_1 = :bank_account_number_1, '
                             'ifsc_code_1 = :ifsc_code_1, bank_name_2 = :bank_name_2, '
                             'bank_account_number_2 = :bank_account_number_2, ifsc_code_2 = :ifsc_code_2 '
                             'WHERE seller_id = :seller_id'),
                        {
                            'seller_name': new_seller_name,
                            'password': new_password,
                            'bank_name_1': new_bank_name_1,
                            'bank_account_number_1': new_bank_account_number_1,
                            'ifsc_code_1': new_ifsc_code_1,
                            'bank_name_2': new_bank_name_2,
                            'bank_account_number_2': new_bank_account_number_2,
                            'ifsc_code_2': new_ifsc_code_2,
                            'seller_id': seller_id
                        }
                    )
                    session.commit()
                    st.success("Profile updated successfully.")
        else:
            st.error("Seller not found.")
    except Exception as e:
        st.error(f"Error updating profile: {e}")
    finally:
        session.close()


def submit_seller_bill():
    st.subheader("Submit Seller Bill")
    session = Session()
    
    try:
        # Fetch broker bills for the logged-in seller
        broker_bills = pd.read_sql(
            text('SELECT * FROM broker_bills WHERE seller_id = :seller_id AND status = "not accepted"'), 
            con=session.bind, 
            params={'seller_id': st.session_state.current_user}
        )
        st.dataframe(broker_bills)

        # Dropdown to select a broker bill
        broker_bill_id = st.selectbox("Select Broker Bill", broker_bills['id'].tolist(), 
                                       format_func=lambda x: f"Broker Bill ID: {x}")

        # Fetch selected broker bill details
        selected_broker_bill = broker_bills[broker_bills['id'] == broker_bill_id]
        
        if not selected_broker_bill.empty:
            # Extract the buyer ID and agent ID from the selected broker bill
            buyer_id = selected_broker_bill.iloc[0]['buyer_id']
            agent_id = selected_broker_bill.iloc[0]['agent_id']  # Get the agent_id directly
            status=selected_broker_bill.iloc[0]['status']
            st.write(status)
            # Ensure agent_id is in the correct format (string for text storage)
            agent_id_str = str(agent_id)

            seller_name = st.session_state.seller_name
            
            # Fetch buyer details
            buyer_details = pd.read_sql(
                text('SELECT * FROM buyers WHERE id = :buyer_id'), 
                con=session.bind, 
                params={'buyer_id': buyer_id}
            )

            if not buyer_details.empty:
                selected_buyer = dict(buyer_details.iloc[0])  # Convert to dictionary
                st.caption(f"Agent ID: {agent_id_str}, Type: {type(agent_id_str)}")

                # Autofill Billing and Shipping Details
                billing_name = selected_buyer['billing_name']
                billing_address = selected_buyer['billing_address']
                billing_city = selected_buyer['billing_city']
                billing_state = selected_buyer['billing_state']
                billing_phone_number = selected_buyer['billing_phone_number']
                billing_gst_number = selected_buyer['billing_gst_number']
                
                shipping_name = selected_buyer['shipping_name']
                shipping_address = selected_buyer['shipping_address']
                shipping_city = selected_buyer['shipping_city']
                shipping_state = selected_buyer['shipping_state']
                shipping_phone_number = selected_buyer['shipping_phone_number']
                shipping_gst_number = selected_buyer['shipping_gst_number']

                # Input fields for driver and invoice details
                col1, col2 = st.columns(2)

                # Driver Details
                with col1:
                    st.subheader("Driver Details")
                    driver_name = st.text_input("Driver Name")
                    driver_phone_number = st.text_input("Driver Phone Number")
                    vehicle_number = st.text_input("Vehicle Number")
                    transport_name = st.text_input("Transport Name")
                    reverse_charges = st.text_input("Reverse Charges")

                # Invoice Details
                with col2:
                    st.subheader("Invoice Details")
                    invoice_number = st.text_input("Invoice Number")
                    date_of_invoice = st.date_input("Date of Invoice")
                    delivery_date = st.date_input("Delivery Date")
                    waybill_number = st.text_input("Waybill Number")
                    mep_number = st.text_input("MEP Number")

                col3, col4 = st.columns(2)

                with col3:
                    # Autofilled Billing Details
                    st.subheader("Billing Details")
                    st.text_input("Billing Name", value=billing_name, disabled=True)
                    st.text_input("Billing Address", value=billing_address, disabled=True)
                    st.text_input("Billing City", value=billing_city, disabled=True)
                    st.text_input("Billing State", value=billing_state, disabled=True)
                    st.text_input("Billing Phone Number", value=str(billing_phone_number), disabled=True)
                    st.text_input("Billing GST Number", value=billing_gst_number, disabled=True)

                with col4:
                    # Autofilled Shipping Details
                    st.subheader("Shipping Details")
                    st.text_input("Shipping Name", value=shipping_name, disabled=True)
                    st.text_input("Shipping Address", value=shipping_address, disabled=True)
                    st.text_input("Shipping City", value=shipping_city, disabled=True)
                    st.text_input("Shipping State", value=shipping_state, disabled=True)
                    st.text_input("Shipping Phone Number", value=str(shipping_phone_number), disabled=True)
                    st.text_input("Shipping GST Number", value=shipping_gst_number, disabled=True)

                # Broker and Buyer Details
                st.subheader("Broker and Seller Details")
                broker_name = st.text_input("Broker Name")
                st.text_input("Seller Name", value=seller_name, disabled=True)
                total_amount = st.number_input("Total Amount", min_value=0.0)

                # Fetch seller bank details
                seller_id = st.session_state.current_user
                seller_details = session.execute(
                    text('SELECT bank_name_1, bank_account_number_1, ifsc_code_1, bank_name_2, '
                         'bank_account_number_2, ifsc_code_2 FROM users WHERE seller_id = :seller_id'),
                    {'seller_id': seller_id}
                ).fetchone()

                bank_details = dict(seller_details._mapping) if seller_details else {
                    'bank_name_1': '',
                    'bank_account_number_1': '',
                    'ifsc_code_1': '',
                    'bank_name_2': '',
                    'bank_account_number_2': '',
                    'ifsc_code_2': ''
                }

                # Bank Details
                st.subheader("Bank Details")
                st.text_input("Bank Name 1", value=bank_details['bank_name_1'], disabled=True)
                st.text_input("Bank Account Number 1", value=bank_details['bank_account_number_1'], disabled=True)
                st.text_input("IFSC Code 1", value=bank_details['ifsc_code_1'], disabled=True)
                st.text_input("Bank Name 2", value=bank_details['bank_name_2'], disabled=True)
                st.text_input("Bank Account Number 2", value=bank_details['bank_account_number_2'], disabled=True)
                st.text_input("IFSC Code 2", value=bank_details['ifsc_code_2'], disabled=True)
                # status = st.selectbox("Select Status", ["completed", "pending"])
                # Submit button
                if st.button("Submit Bill"):
                    try:
                        session.execute(
                            text('INSERT INTO sellerBill (seller_id, driver_name, driver_phone_number, vehicle_number, '
                                 'transport_name, reverse_charges, invoice_number, date_of_invoice, delivery_date, '
                                 'waybill_number, mep_number, billing_name, billing_address, billing_city, billing_state, '
                                 'billing_phone_number, billing_gst_number, shipping_name, shipping_address, shipping_city, '
                                 'shipping_state, shipping_phone_number, shipping_gst_number, broker_name, seller_name, '
                                 'total_amount, bank_name_1, bank_account_number_1, ifsc_code_1, bank_name_2, '
                                 'bank_account_number_2, ifsc_code_2, broker_bill_id, agent_id, status) VALUES '
                                 '(:seller_id, :driver_name, :driver_phone_number, :vehicle_number, :transport_name, '
                                 ':reverse_charges, :invoice_number, :date_of_invoice, :delivery_date, :waybill_number, '
                                 ':mep_number, :billing_name, :billing_address, :billing_city, :billing_state, '
                                 ':billing_phone_number, :billing_gst_number, :shipping_name, :shipping_address, '
                                 ':shipping_city, :shipping_state, :shipping_phone_number, :shipping_gst_number, '
                                 ':broker_name, :seller_name, :total_amount, :bank_name_1, :bank_account_number_1, '
                                 ':ifsc_code_1, :bank_name_2, :bank_account_number_2, :ifsc_code_2, :broker_bill_id, :agent_id, :status)'),
                            {
                                'seller_id': st.session_state.current_user,
                                'driver_name': driver_name,
                                'driver_phone_number': driver_phone_number,
                                'vehicle_number': vehicle_number,
                                'broker_bill_id': broker_bill_id,
                                'agent_id': agent_id_str,  # Use the string representation
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
                                'bank_name_1': bank_details['bank_name_1'],
                                'bank_account_number_1': bank_details['bank_account_number_1'],
                                'ifsc_code_1': bank_details['ifsc_code_1'],
                                'bank_name_2': bank_details['bank_name_2'],
                                'bank_account_number_2': bank_details['bank_account_number_2'],
                                'ifsc_code_2': bank_details['ifsc_code_2'],
                                'status':"pending",
                            }
                        )
                        session.commit()
                        st.success("Bill submitted successfully.")
                        # Update the status of the broker bill to 'accepted'
                        session.execute(
                            text('UPDATE broker_bills SET status = :status WHERE id = :broker_bill_id'),
                            {'status': 'completed', 'broker_bill_id': broker_bill_id})
                        session.commit()
                        st.success("Bill updated successfully.")
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error submitting bill: {e}")
            else:
                st.error("No buyer details found for the selected broker bill.")
        else:
            st.error("No broker bill selected.")
    finally:
        session.close()

# Function to view bills
def view_bills_page():
    st.subheader("Your Bills")
    
    if st.session_state.logged_in:
        seller_id = st.session_state.current_user
        session = Session()
        try:
            bills = pd.read_sql(
                text('SELECT * FROM sellerBill WHERE seller_id = :seller_id'), 
                con=engine, 
                params={'seller_id': seller_id}
            )
            st.write(seller_id)
            if not bills.empty:
                st.dataframe(bills)
            else:
                st.write("No bills found for this seller.")
        except Exception as e:
            st.error(f"Error retrieving bills: {e}")
        finally:
            session.close()
    else:
        st.error("Please log in first.")

import base64

def view_bills_pdf(status):
    st.subheader(f"View {status} Bills")
    
    if st.session_state.logged_in:
        seller_id = st.session_state.current_user
        session = Session()
        try:
            # Normalize the status to lower case
            normalized_status = status.lower()
            st.write(f"Seller ID from session: {seller_id}")
            
            # Prepare the SQL query
            query = text('SELECT * FROM sellerBill WHERE seller_id = :seller_id AND LOWER(status) = LOWER(:status)')
            params = {'seller_id': seller_id, 'status': normalized_status}

            # Display the SQL query and parameters
            st.write(f"SQL Query: {query}")
            st.write(f"Parameters: {params}")

            # Fetch bills for the logged-in seller
            bills = pd.read_sql(
                query,
                con=session.bind,
                params=params
            )

            st.write(bills)  # Check fetched bills

            # Handle empty bills case
            if bills.empty:
                st.write(f"No {normalized_status} bills found for this seller.")
                return
            
            # Dropdown to select a bill
            selected_bill_id = st.selectbox(
                "Select Bill", 
                bills['id'].tolist(),
                format_func=lambda x: bills.loc[bills['id'] == x, 'invoice_number'].values[0]
            )

            if st.button("View PDF"):
                bill_details = bills[bills['id'] == selected_bill_id].iloc[0]
                products = pd.read_sql(
                    text('SELECT * FROM products WHERE seller_id = :seller_id AND bill_id = :bill_id'),
                    con=session.bind,
                    params={'seller_id': seller_id, 'bill_id': selected_bill_id}
                )

                # Check if products were retrieved
                if products.empty:
                    st.write("No products found for this bill.")
                    return
                
                # Create PDF
                pdf_buffer = create_pdf(bill_details, products, normalized_status)

                # Encode the PDF for embedding
                pdf_data = pdf_buffer.getvalue()
                b64_pdf = base64.b64encode(pdf_data).decode('utf-8')

                # Display PDF in the app
                st.write("### Bill PDF:")
                st.markdown(
                    f'<embed src="data:application/pdf;base64,{b64_pdf}" width="700" height="500" type="application/pdf">',
                    unsafe_allow_html=True
                )

                # Add download button
                st.download_button("Download PDF", data=pdf_data, file_name="bill.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error retrieving bills: {e}")
        finally:
            session.close()
    else:
        st.error("Please log in first.")


def create_pdf(bill_details, products, status):
    buffer = io.BytesIO()
    # doc = SimpleDocTemplate(buffer, pagesize=letter)
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.5 * inch)
    elements = []
    styles = getSampleStyleSheet()

    # Section 1: Seller Name
    elements.append(Paragraph(bill_details['seller_name'], styles['Title']))
    elements.append(Spacer(1, 0.2 * inch))

    # Section 2: Driver & Transport Details
    driver_data = [
        ["Driver Name", bill_details['driver_name'], "Invoice Number", bill_details['invoice_number']],
        ["Driver Phone", bill_details['driver_phone_number'], "Date of Invoice", bill_details['date_of_invoice']],
        ["Vehicle Number", bill_details['vehicle_number'], "Delivery Date", bill_details['delivery_date']],
        ["Transport Name", bill_details['transport_name'], "Waybill Number", bill_details['waybill_number']],
        ["Reverse Charges", bill_details['reverse_charges'], "MEP Number", bill_details['mep_number']],
    ]
    elements.append(Spacer(1, 0.2 * inch))

    driver_table = Table(driver_data, colWidths=[1.75 * inch] * 4)
    driver_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(driver_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Section 3: Billing and Shipping Information
    billing_shipping_data = [
        ["Billing Name", bill_details['billing_name'], "Shipping Name", bill_details['shipping_name']],
        ["Billing Address", bill_details['billing_address'], "Shipping Address", bill_details['shipping_address']],
        ["City", bill_details['billing_city'], "City", bill_details['shipping_city']],
        ["State", bill_details['billing_state'], "State", bill_details['shipping_state']],
        ["Phone", bill_details['billing_phone_number'], "Phone", bill_details['shipping_phone_number']],
        ["GST Number", bill_details['billing_gst_number'], "GST Number", bill_details['shipping_gst_number']],
    ]

    billing_shipping_table = Table(billing_shipping_data, colWidths=[1.75 * inch] * 4)
    billing_shipping_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(billing_shipping_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Section 4: Product Details
    product_data = [["Product \nDescription", "Brand", "HSN Code", "Bags", "Weight (kg)", "Rate", "Amount"]]
    
    for index, row in products.iterrows():
        product_data.append([
            row['product_description'], row['product_brand'], row['hsn_code'], row['product_bags'],
            row['product_weight_in_kg'], row['rate'], row['amount']
        ])
    
    product_table = Table(product_data, colWidths=[1.0 * inch] * 7)
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(product_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Section 5: Total Amount
    total_amount_table = Table([["Total Amount", bill_details['total_amount']]], colWidths=[4.5 * inch, 2.5 * inch])
    total_amount_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(total_amount_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Section 6: Bank Details
    # Adjusted bank details layout: one after another
    bank_details_data = [
        ["Bank Name 1:", bill_details['bank_name_1']],
        ["Account Number:", bill_details['bank_account_number_1']],
        ["IFSC Code:", bill_details['ifsc_code_1']],
    ]

    # Create the table with two columns (labels and values)
    bank_details_table = Table(bank_details_data, colWidths=[2 * inch, 3 * inch])

    # Apply styles
    bank_details_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Adding borders
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),  # Set background color for labels
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Align text to the left
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Vertically align text to the top
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Set font
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Set font size
    ]))

    # Align table to the left by setting table alignment
    bank_details_table.hAlign = 'LEFT'

    # Add the table to the elements
    elements.append(bank_details_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Section 7: Brokerage
    if status.lower() == "completed":
        elements.append(Paragraph(f"Brokerage: {bill_details['brokerage']}", styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))

    # Section 8: Authorised Signatory and Status
    elements.append(Paragraph("Authorised Signatory:", styles['Normal']))
    elements.append(Paragraph("_______________________", styles['Normal']))
    if bill_details['brokerage']=='None' or bill_details['brokerage']==0 or bill_details['brokerage']==None:
        elements.append(Paragraph(f"Status: pending", styles['Normal']))
    else:
        elements.append(Paragraph(f"Status: completed", styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Function to submit products
def submit_products():
    st.subheader("Submit Products")

    session = Session()
    try:
        # Check if the products table exists, and create it if it doesn't
        session.execute(text('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_id TEXT NOT NULL,
                bill_id INTEGER NOT NULL,
                product_description TEXT NOT NULL,
                product_brand TEXT,
                hsn_code TEXT,
                product_bags INTEGER,
                product_weight_in_kg REAL,
                product_weight_in_qtls REAL,
                rate REAL,
                amount REAL
            )
        '''))
        session.commit()  # Commit the creation of the table

        # Fetch seller bills for the dropdown
        seller_bills = pd.read_sql(
            text('SELECT id, invoice_number FROM sellerBill WHERE seller_id = :seller_id'),
            con=session.bind,
            params={'seller_id': st.session_state.current_user}
        )
        
        if seller_bills.empty:
            st.error("No seller bills found. Please submit a seller bill first.")
            return

        # Dropdown to select a seller bill
        selected_bill = st.selectbox("Select Seller Bill", seller_bills['id'].tolist(), 
                                      format_func=lambda x: seller_bills.loc[seller_bills['id'] == x, 'invoice_number'].values[0])
        st.text(selected_bill)

        # Input fields for products
        bill_id = selected_bill
        product_description = st.text_input("Product Description")
        product_brand = st.text_input("Product Brand")
        hsn_code = st.text_input("HSN Code")
        product_bags = st.number_input("Product Bags", min_value=0)
        product_weight_in_kg = st.number_input("Product Weight (kg)", min_value=0.0)
        product_weight_in_qtls = st.number_input("Product Weight (qtls)", min_value=0.0)
        rate = st.number_input("Rate", min_value=0.0)
        amount = st.number_input("Amount", min_value=0.0)

        # Submit button
        if st.button("Submit Product"):
            try:
                session.execute(
                    text('INSERT INTO products (seller_id, bill_id, product_description, product_brand, hsn_code, '
                         'product_bags, product_weight_in_kg, product_weight_in_qtls, rate, amount) VALUES '
                         '(:seller_id, :bill_id, :product_description, :product_brand, :hsn_code, :product_bags, '
                         ':product_weight_in_kg, :product_weight_in_qtls, :rate, :amount)'),
                    {
                        'seller_id': st.session_state.current_user,
                        'bill_id': bill_id,
                        'product_description': product_description,
                        'product_brand': product_brand,
                        'hsn_code': hsn_code,
                        'product_bags': product_bags,
                        'product_weight_in_kg': product_weight_in_kg,
                        'product_weight_in_qtls': product_weight_in_qtls,
                        'rate': rate,
                        'amount': amount,
                    }
                )
                session.commit()
                st.success("Product submitted successfully.")
            except Exception as e:
                session.rollback()
                st.error(f"Error submitting product: {e}")
    finally:
        session.close()


# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.seller_name = None
    st.success("Successfully logged out.")
    st.rerun()

# Main function with dynamic sidebar menu
def main():
    st.sidebar.title("Seller Menu")
    
    # Check if user is logged in
    if st.session_state.logged_in:
        st.sidebar.write(f"Logged in as: {st.session_state.current_user}")
        st.sidebar.write(f"Seller name: {st.session_state.seller_name}")
        page = st.sidebar.selectbox("Choose a page", ["Submit Bill", "Submit Products", "View Bills", "View Pending Bills PDF", "View Completed Bills PDF", "Update Profile"])

        # Logout button
        if st.sidebar.button("Logout"):
            logout()

        # Show respective pages
        if page == "Submit Bill":
            submit_seller_bill()
        elif page == "Submit Products":
            submit_products()
        elif page == "View Bills":
            view_bills_page()
        elif page == "View Pending Bills PDF":
            view_bills_pdf("Pending")
        elif page == "View Completed Bills PDF":
            view_bills_pdf("Completed")
        elif page == "Update Profile":
            update_seller_profile()
    else:
        # If not logged in, show login option
        page = st.sidebar.selectbox("Choose a page", ["Login"])

        # Show login page if not logged in
        if page == "Login":
            login_page()

if __name__ == "__main__":
    main()
