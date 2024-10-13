import sqlite3

# Create a new SQLite database
conn = sqlite3.connect('app_data6.db')
# Create a cursor object
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL, 
    seller_id VARCHAR, 
    password VARCHAR, 
    seller_name VARCHAR, 
    bank_name_1 VARCHAR, 
    bank_account_number_1 VARCHAR, 
    ifsc_code_1 VARCHAR, 
    bank_name_2 VARCHAR, 
    bank_account_number_2 VARCHAR, 
    ifsc_code_2 VARCHAR, 
    PRIMARY KEY (id), 
    UNIQUE (seller_id)
);
''')

# Create the sellerBill table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sellerBill (
    id INTEGER NOT NULL, 
    seller_id VARCHAR, 
    driver_name VARCHAR, 
    driver_phone_number FLOAT, 
    vehicle_number VARCHAR, 
    transport_name VARCHAR, 
    reverse_charges VARCHAR, 
    invoice_number VARCHAR, 
    date_of_invoice DATE, 
    delivery_date DATE, 
    waybill_number FLOAT, 
    mep_number VARCHAR, 
    billing_name VARCHAR, 
    billing_address VARCHAR, 
    billing_city VARCHAR, 
    billing_state VARCHAR, 
    billing_phone_number FLOAT, 
    billing_gst_number VARCHAR, 
    shipping_name VARCHAR, 
    shipping_address VARCHAR, 
    shipping_city VARCHAR, 
    shipping_state VARCHAR, 
    shipping_phone_number FLOAT, 
    shipping_gst_number VARCHAR, 
    broker_name VARCHAR, 
    total_amount FLOAT, 
    bank_name_1 VARCHAR, 
    bank_account_number_1 VARCHAR, 
    ifsc_code_1 VARCHAR, 
    bank_name_2 VARCHAR, 
    bank_account_number_2 VARCHAR, 
    ifsc_code_2 VARCHAR, 
    brokerage FLOAT, 
    status VARCHAR, 
    seller_name TEXT, 
    PRIMARY KEY (id)
);
''')

# Create the buyers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS buyers (
    id INTEGER NOT NULL, 
    billing_name VARCHAR, 
    billing_address VARCHAR, 
    billing_city VARCHAR, 
    billing_state VARCHAR, 
    billing_phone_number FLOAT, 
    billing_gst_number VARCHAR, 
    shipping_name VARCHAR, 
    shipping_address VARCHAR, 
    shipping_city VARCHAR, 
    shipping_state VARCHAR, 
    shipping_phone_number FLOAT, 
    shipping_gst_number VARCHAR, 
    PRIMARY KEY (id)
);
''')

# Create the deleted_sellerBills table
cursor.execute('''
CREATE TABLE IF NOT EXISTS deleted_sellerBills (
    id INTEGER NOT NULL, 
    seller_id VARCHAR, 
    driver_name VARCHAR, 
    driver_phone_number FLOAT, 
    vehicle_number VARCHAR, 
    transport_name VARCHAR, 
    reverse_charges VARCHAR, 
    invoice_number VARCHAR, 
    date_of_invoice DATE, 
    delivery_date DATE, 
    waybill_number FLOAT, 
    mep_number VARCHAR, 
    billing_name VARCHAR, 
    billing_address VARCHAR, 
    billing_city VARCHAR, 
    billing_state VARCHAR, 
    billing_phone_number FLOAT, 
    billing_gst_number VARCHAR, 
    shipping_name VARCHAR, 
    shipping_address VARCHAR, 
    shipping_city VARCHAR, 
    shipping_state VARCHAR, 
    shipping_phone_number FLOAT, 
    shipping_gst_number VARCHAR, 
    broker_name VARCHAR, 
    total_amount FLOAT, 
    bank_name_1 VARCHAR, 
    bank_account_number_1 VARCHAR, 
    ifsc_code_1 VARCHAR, 
    bank_name_2 VARCHAR, 
    bank_account_number_2 VARCHAR, 
    ifsc_code_2 VARCHAR, 
    brokerage FLOAT, 
    status VARCHAR, 
    seller_name TEXT, 
    PRIMARY KEY (id)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
