import streamlit as st
from graphviz import Digraph

# Class Diagram
class_diagram = Digraph()

# Classes
class_diagram.node('A', 'Broker\n- broker_id\n- name\n- email\n+ register_seller()\n+ generate_bill()')
class_diagram.node('B', 'Seller\n- seller_id\n- name\n- email\n+ bill_buyer()')
class_diagram.node('C', 'Buyer\n- buyer_id\n- name\n- email\n+ make_payment()')
class_diagram.node('D', 'Transaction\n- transaction_id\n- amount\n- date\n+ record_transaction()')
class_diagram.node('E', 'Bill\n- bill_id\n- amount_due\n- due_date\n+ generate_bill()')

# Relationships
class_diagram.edge('A', 'B', 'registers')
class_diagram.edge('B', 'C', 'sells to')
class_diagram.edge('B', 'D', 'creates')
class_diagram.edge('D', 'E', 'generates')
class_diagram.edge('C', 'D', 'makes payment for')

# Render the class diagram
st.title("Brokerage Platform Class Diagram")
st.graphviz_chart(class_diagram.source)

# State Diagram
state_diagram = Digraph()

# States
state_diagram.node('A', 'Start')
state_diagram.node('B', 'Invoice Generated')
state_diagram.node('C', 'Payment Pending')
state_diagram.node('D', 'Payment Received')
state_diagram.node('E', 'Late Payment Charged')

# Transitions
state_diagram.edge('A', 'B', 'generate invoice')
state_diagram.edge('B', 'C', 'wait for payment')
state_diagram.edge('C', 'D', 'payment received')
state_diagram.edge('C', 'E', '15 days pass without payment')
state_diagram.edge('E', 'D', 'payment received after charge')

# Render the state diagram
st.title("Brokerage Platform State Diagram")
st.graphviz_chart(state_diagram.source)


# Sequence Diagram
sequence_diagram = Digraph()

# Lifelines
sequence_diagram.node('A', 'Broker')
sequence_diagram.node('B', 'Seller')
sequence_diagram.node('C', 'Buyer')

# Messages
sequence_diagram.edge('A', 'B', 'register_seller()')
sequence_diagram.edge('B', 'C', 'bill_buyer()')
sequence_diagram.edge('C', 'B', 'make_payment()')
sequence_diagram.edge('B', 'A', 'record_transaction()')
sequence_diagram.edge('A', 'C', 'send_invoice()')

# Render the sequence diagram
st.title("Brokerage Platform Sequence Diagram")
st.graphviz_chart(sequence_diagram.source)



# Create a Graphviz graph
dot = Digraph()

# Define the nodes
dot.node('A', 'Broker')
dot.node('B', 'Seller')
dot.node('C', 'Buyer')
dot.node('D', 'Bill Management')
dot.node('E', 'Transaction Tracking')
dot.node('F', 'Search Functionality')
dot.node('G', 'Dynamic Billing')

# Define the edges
dot.edges(['AB', 'AC'])  # Broker connects to Seller and Buyer
dot.edge('B', 'C', 'Sells to')  # Seller sells to Buyer
dot.edge('A', 'D', 'Generates Bills')
dot.edge('A', 'E', 'Tracks Transactions')
dot.edge('A', 'F', 'Searches Users')
dot.edge('A', 'G', 'Imposes Charges if Needed')

# Render the graph
st.title("Brokerage Platform Block Diagram")
st.graphviz_chart(dot.source)
