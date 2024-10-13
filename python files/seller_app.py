import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('sqlite:///app_data.db')
Session = sessionmaker(bind=engine)

def seller_interface():
    st.title("Seller Dashboard")
    
    # Login Fields
    seller_id = st.text_input("Seller ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        session = Session()
        try:
            result = session.execute(
                text('SELECT * FROM users WHERE seller_id = :seller_id AND password = :password'), 
                {'seller_id': seller_id, 'password': password}
            ).fetchone()

            if result:
                st.session_state.logged_in = True
                st.session_state.current_user = seller_id
                st.success(f"Welcome {seller_id}")
            else:
                st.error("Invalid ID or Password")
        except Exception as e:
            st.error(f"Error during login: {e}")
        finally:
            session.close()

    # If logged in, allow bill submission and view bills
    if getattr(st.session_state, 'logged_in', False):
        bill_amount = st.number_input("Enter Bill Amount", min_value=0.0)
        
        if st.button("Submit Bill"):
            session = Session()
            try:
                session.execute(
                    text('INSERT INTO bills (seller_id, bill_amount) VALUES (:seller_id, :bill_amount)'), 
                    {'seller_id': seller_id, 'bill_amount': bill_amount}
                )
                session.commit()
                st.success("Bill submitted.")
            except Exception as e:
                session.rollback()
                st.error(f"Error submitting bill: {e}")
            finally:
                session.close()

        # Display Seller's Bills
        st.subheader("Your Bills")
        session = Session()
        try:
            bills = pd.read_sql(
                text('SELECT * FROM bills WHERE seller_id = :seller_id'), 
                con=engine, 
                params={'seller_id': seller_id}
            )
            if not bills.empty:
                st.dataframe(bills)
            else:
                st.write("No bills found for this seller.")
        except Exception as e:
            st.error(f"Error retrieving bills: {e}")
        finally:
            session.close()

def main():
    seller_interface()

if __name__ == "__main__":
    main()
