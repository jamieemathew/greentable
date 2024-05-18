import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from database import FoodData, get_db, create_user
from auth import authenticate_user
from PIL import Image

st.set_page_config(layout='wide')


placeholder = st.empty()
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()

left_co, cent_co, right_co = st.columns(3)

def add_food_data(db: Session, food_data: dict):
    db_food = FoodData(**food_data)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

def get_all_food_data(db: Session):
    return db.query(FoodData).all()

def update_food_data_quantity(db: Session, food_id: int, new_quantity: int):
    food_data = db.query(FoodData).filter(FoodData.id == food_id).first()
    if food_data:
        if new_quantity <= 0:
            db.delete(food_data)
        else:
            food_data.quantity = new_quantity
        db.commit()
        return True
    return False

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'delete_success' not in st.session_state:
    st.session_state['delete_success'] = False

def main():
    placeholder1.markdown("<h1 style='text-align: center; color: green;'>GreenTable</h1>", unsafe_allow_html=True)
    placeholder4.markdown("<h2 style='text-align: center; color: green;'>A Step Towards Sustainability</h2>", unsafe_allow_html=True)
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Options", ["Home", "Available Food", "Restaurant Login / Food Item Submission", "Restaurant Registration"])
    
    if page == "Home":
        home_page()
    elif page == "Available Food":
        available_food_page()
    elif page == "Restaurant Login / Food Item Submission":
        restaurant_login_page()
    elif page == "Restaurant Registration":
        restaurant_registration_page()

def home_page():
    st.markdown("<p style='text-align: center; font-size: 25px'>GreenTable is a platform dedicated to reducing food waste and promoting sustainability. Join us in making a difference by connecting restaurants with leftover food to those in need!</p>", unsafe_allow_html=True)

def available_food_page():
    st.header("Available Food")
    st.write("Here you can view the available leftover food from various restaurants.")
    
    try:
        image = Image.open('foodpic.jpeg')  
        new_image = image.resize((200, 200))
        st.image(new_image)
    except FileNotFoundError:
        st.error("Food image not found. Please check the path.")
    
    with next(get_db()) as db:
        food_data_list = get_all_food_data(db)
        if food_data_list:
            df = pd.DataFrame([food.__dict__ for food in food_data_list])
            df = df.drop(columns='_sa_instance_state')
            df.index = df.index + 1
            df.index.name = "No."
            st.dataframe(df)
        else:
            st.write("No leftover food available at the moment.")

def restaurant_login_page():
    placeholder1.empty()
    placeholder4.empty()
    with cent_co:
        placeholder2.header("Restaurant Login")
        placeholder3.write("Restaurants can login here to enter their leftover food items and delete the ones that have been picked up.")
    
    if not st.session_state['logged_in']:
        with placeholder.form(key='login_form'):
            username = st.text_input("Restaurant Name")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button(label="Login")
        
            if login_button:
                with next(get_db()) as db:
                    user = authenticate_user(db, username, password)
                    if user:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.success("🎉 Logged in successfully!")
                    else:
                        st.error("❗ Invalid username or password")
    
    if st.session_state['logged_in']:
        with st.container():
            placeholder.empty()
            placeholder2.empty()
            placeholder3.empty()
            st.markdown("<div style='display: flex; justify-content: space-between;'>", unsafe_allow_html=True)
            
            if st.button("Logout", key="logout_button"):
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.success("Successfully logged out.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.header("🍽️ Restaurant Food Submission Form")
        with st.form(key='food_submission_form'):
            restaurant_name = st.text_input("Restaurant Name")
            food_description = st.text_area("Food Description")
            quantity = st.number_input("Quantity Available", min_value=1)
            pickup_time = st.time_input("Pickup Time")
            location = st.selectbox("City", ["Trivandrum", "Kottayam", "Kochi", "Trissur", "Calicut"])
            address = st.text_input("Address")
            contact_info = st.text_input("Contact Information (Phone or Email)")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if restaurant_name and food_description and quantity and pickup_time and location and address and contact_info:
                    food_data = {
                        'restaurant_name': restaurant_name,
                        'food_description': food_description,
                        'quantity': quantity,
                        'pickup_time': pickup_time,
                        'location': location,
                        'address': address,
                        'contact_info': contact_info,
                        'date_submitted': datetime.now()
                    }
                    with next(get_db()) as db:
                        add_food_data(db, food_data)
                        st.success("🎉 Food submission successful!")
                else:
                    st.error("❗ Please fill in all fields")
        
        st.header("🗑️ Delete Submitted Food")
        with next(get_db()) as db:
            food_data_list = db.query(FoodData).filter(FoodData.restaurant_name == st.session_state['username']).all()
            if food_data_list:
                df = pd.DataFrame([food.__dict__ for food in food_data_list])
                df = df.drop(columns=['_sa_instance_state', 'date_submitted'])
                for index, row in df.iterrows():
                    st.write(f"{row['food_description']} - {row['quantity']} servings")
                    delete_quantity = st.number_input(f"Quantity to delete from {row['food_description']}", min_value=1, max_value=row['quantity'], key=f"delete_{row['id']}")
                    if st.button(f"Delete {delete_quantity} of {row['food_description']}", key=f"delete_button_{row['id']}"):
                        new_quantity = row['quantity'] - delete_quantity
                        if update_food_data_quantity(db, row['id'], new_quantity):
                            st.session_state['delete_success'] = True
                            st.rerun()
        
        if st.session_state['delete_success']:
            st.success("🎉 Food item quantity updated successfully!")
            st.session_state['delete_success'] = False

def restaurant_registration_page():
    placeholder1.empty()
    placeholder4.empty()
    with cent_co:
        placeholder2.header("Restaurant Registration")
        placeholder3.write("New restaurants can register here.")
    
    with placeholder.form(key='registration_form'):
        username = st.text_input("Restaurant Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_button = st.form_submit_button(label="Register")
        
        if register_button:
            if password == confirm_password:
                success, message = create_user(username, password)
                if success:
                    st.success("🎉 Registration successful! You can now login.")
                else:
                    st.error(f"❗ {message}")
            else:
                st.error("❗ Passwords do not match")

if __name__ == "__main__":
    main()
