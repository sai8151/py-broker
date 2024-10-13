from graphviz import Digraph

# Initialize diagram
schema_diagram = Digraph('Database Schema', node_attr={'shape': 'record'})

# Define tables and their fields
schema_diagram.node('users', '''{
    users | 
    id: INTEGER | seller_id: VARCHAR | password: VARCHAR | seller_name: VARCHAR | bank_name_1: VARCHAR |
    bank_account_number_1: VARCHAR | ifsc_code_1: VARCHAR | bank_name_2: VARCHAR | 
    bank_account_number_2: VARCHAR | ifsc_code_2: VARCHAR | PRIMARY KEY (id), UNIQUE (seller_id)
}''')

schema_diagram.node('buyers', '''{
    buyers | 
    id: INTEGER | billing_name: VARCHAR | billing_address: VARCHAR | billing_city: VARCHAR | billing_state: VARCHAR |
    billing_phone_number: FLOAT | billing_gst_number: VARCHAR | shipping_name: VARCHAR | shipping_address: VARCHAR |
    shipping_city: VARCHAR | shipping_state: VARCHAR | shipping_phone_number: FLOAT | shipping_gst_number: VARCHAR |
    PRIMARY KEY (id)
}''')

schema_diagram.node('products', '''{
    products | 
    id: INTEGER | seller_id: TEXT | bill_id: INTEGER | product_description: TEXT | product_brand: TEXT |
    hsn_code: TEXT | product_bags: INTEGER | product_weight_in_kg: REAL | product_weight_in_qtls: REAL | 
    rate: REAL | amount: REAL | PRIMARY KEY (id)
}''')

schema_diagram.node('agents', '''{
    agents | 
    id: INTEGER | name: TEXT | pan_number: TEXT | address: TEXT | mobile_number: TEXT | email: TEXT |
    terms_and_conditions: TEXT | PRIMARY KEY (id)
}''')

schema_diagram.node('broker_bills', '''{
    broker_bills | 
    id: INTEGER | agent_id: INTEGER | order_date: DATE | order_number: TEXT | total_tons: REAL | seller_id: TEXT |
    buyer_id: TEXT | status: TEXT | FOREIGN KEY (agent_id) REFERENCES agents(id) |
    FOREIGN KEY (seller_id) REFERENCES users(seller_id) | FOREIGN KEY (buyer_id) REFERENCES buyers(id) |
    PRIMARY KEY (id)
}''')

schema_diagram.node('broker_bill_details', '''{
    broker_bill_details | 
    id: INTEGER | broker_bill_id: INTEGER | quality_name: TEXT | brand_name: TEXT | quantity: REAL | 
    rate: REAL | condition: TEXT | FOREIGN KEY (broker_bill_id) REFERENCES broker_bills(id) | PRIMARY KEY (id)
}''')

schema_diagram.node('deleted_sellerBills', '''{
    deleted_sellerBills | 
    id: INTEGER | seller_id: VARCHAR | driver_name: VARCHAR | driver_phone_number: FLOAT | vehicle_number: VARCHAR |
    transport_name: VARCHAR | reverse_charges: VARCHAR | invoice_number: VARCHAR | date_of_invoice: DATE |
    delivery_date: DATE | waybill_number: FLOAT | mep_number: VARCHAR | billing_name: VARCHAR | billing_address: VARCHAR |
    billing_city: VARCHAR | billing_state: VARCHAR | billing_phone_number: FLOAT | billing_gst_number: VARCHAR |
    shipping_name: VARCHAR | shipping_address: VARCHAR | shipping_city: VARCHAR | shipping_state: VARCHAR |
    shipping_phone_number: FLOAT | shipping_gst_number: VARCHAR | broker_name: VARCHAR | total_amount: FLOAT |
    bank_name_1: VARCHAR | bank_account_number_1: VARCHAR | ifsc_code_1: VARCHAR | bank_name_2: VARCHAR |
    bank_account_number_2: VARCHAR | ifsc_code_2: VARCHAR | brokerage: FLOAT | status: VARCHAR | seller_name: TEXT |
    PRIMARY KEY (id)
}''')

schema_diagram.node('sellerBill', '''{
    sellerBill | 
    id: INTEGER | seller_id: VARCHAR | broker_bill_id: INTEGER | agent_id: INTEGER | driver_name: VARCHAR |
    driver_phone_number: FLOAT | vehicle_number: VARCHAR | transport_name: VARCHAR | reverse_charges: VARCHAR |
    invoice_number: VARCHAR | date_of_invoice: DATE | delivery_date: DATE | waybill_number: FLOAT |
    mep_number: VARCHAR | billing_name: VARCHAR | billing_address: VARCHAR | billing_city: VARCHAR |
    billing_state: VARCHAR | billing_phone_number: FLOAT | billing_gst_number: VARCHAR | shipping_name: VARCHAR |
    shipping_address: VARCHAR | shipping_city: VARCHAR | shipping_state: VARCHAR | shipping_phone_number: FLOAT |
    shipping_gst_number: VARCHAR | broker_name: VARCHAR | total_amount: FLOAT | bank_name_1: VARCHAR |
    bank_account_number_1: VARCHAR | ifsc_code_1: VARCHAR | bank_name_2: VARCHAR | bank_account_number_2: VARCHAR |
    ifsc_code_2: VARCHAR | brokerage: FLOAT | status: VARCHAR | seller_name: TEXT | PRIMARY KEY (id)
}''')

# Define relationships
schema_diagram.edge('agents', 'broker_bills', label='agent_id')
schema_diagram.edge('users', 'broker_bills', label='seller_id')
schema_diagram.edge('buyers', 'broker_bills', label='buyer_id')
schema_diagram.edge('broker_bills', 'broker_bill_details', label='broker_bill_id')

# Render diagram to file
schema_diagram.render('sql_schema_diagram', format='png')