import streamlit as st
from graphviz import Digraph

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
