import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection and model setup
engine = create_engine('sqlite:///app_data.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    seller_id = Column(String, unique=True)
    password = Column(String)

class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    seller_id = Column(String)
    bill_amount = Column(Integer)
    brokerage = Column(Integer, default=0)
    status = Column(String, default='Pending')

class DeletedRecord(Base):
    __tablename__ = 'deleted_records'
    id = Column(Integer, primary_key=True)
    seller_id = Column(String)
    bill_amount = Column(Integer)
    brokerage = Column(Integer)
    status = Column(String)

# Create tables if they do not exist
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)

def admin_interface():
    st.title("Admin Dashboard")
    
    # Create Seller
    st.subheader("Create Seller Account")
    seller_id = st.text_input("Seller ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Create Seller"):
        if seller_id and password:
            session = Session()
            try:
                new_user = User(seller_id=seller_id, password=password)
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

    # View and Edit Bills
    st.subheader("Bills")
    session = Session()
    try:
        bills = pd.read_sql('SELECT * FROM bills', con=engine)

        # Editable dataframe for bills
        if not bills.empty:
            edited_bills = st.data_editor(bills, key="bills_editor")

            # Update option for bills
            if st.button("Update Bills"):
                try:
                    for index, row in edited_bills.iterrows():
                        session.execute(
                            text('UPDATE bills SET bill_amount = :bill_amount, brokerage = :brokerage, status = :status WHERE id = :id'), 
                            {
                                'bill_amount': row['bill_amount'],
                                'brokerage': row['brokerage'],
                                'status': row['status'],
                                'id': row['id']
                            }
                        )
                    session.commit()
                    st.success("Bills updated successfully.")
                except Exception as e:
                    session.rollback()
                    st.error(f"Error updating bills: {e}")

            # Delete option for each bill
            bill_to_delete = st.selectbox("Select Bill to Delete", options=bills['id'].tolist(), format_func=lambda x: f"Bill ID: {x}")
            if st.button("Delete Bill"):
                try:
                    # Move to deleted_records table
                    bill_to_move = session.execute(
                        text('SELECT * FROM bills WHERE id = :id'), 
                        {'id': bill_to_delete}
                    ).fetchone()
                    
                    if bill_to_move:
                        session.execute(
                            text('INSERT INTO deleted_records (seller_id, bill_amount, brokerage, status) VALUES (:seller_id, :bill_amount, :brokerage, :status)'), 
                            {
                                'seller_id': bill_to_move.seller_id,
                                'bill_amount': bill_to_move.bill_amount,
                                'brokerage': bill_to_move.brokerage,
                                'status': bill_to_move.status
                            }
                        )
                        session.execute(
                            text('DELETE FROM bills WHERE id = :id'), 
                            {'id': bill_to_delete}
                        )
                        session.commit()
                        st.success("Bill deleted successfully and moved to deleted records.")
                    else:
                        st.error("Bill not found.")
                except Exception as e:
                    session.rollback()
                    st.error(f"Error deleting bill: {e}")
        else:
            st.write("No bills available.")
    except Exception as e:
        st.error(f"Error retrieving bills: {e}")
    finally:
        session.close()

    # Statistics
    st.subheader("Statistics")
    if not bills.empty:
        total_profit = bills['bill_amount'].sum() - bills['brokerage'].sum()
        total_transactions = len(bills)
        
        st.write(f"Total Profit: {total_profit:.2f}")
        st.write(f"Total Transactions: {total_transactions}")
    else:
        st.write("No transactions to calculate statistics.")

    # View Deleted Records
    st.subheader("Deleted Bills")
    try:
        deleted_bills = pd.read_sql('SELECT * FROM deleted_records', con=engine)
        if deleted_bills.empty:
            st.write("No deleted bills.")
        else:
            st.dataframe(deleted_bills)
    except Exception as e:
        st.error(f"Error retrieving deleted bills: {e}")

def main():
    admin_interface()

if __name__ == "__main__":
    main()
