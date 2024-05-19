

![Streamlit notion](https://github.com/TH-Activities/saturday-hack-night-template/assets/117498997/e8052bb6-ad89-48c3-b6e9-124f94c1cd01)




# Green Table
Green Table is a web app that allows restaurants to share if they have leftover food available and people who are in need can come and collect it. The restaurants can give it at a discounted price or for free, it's totally upto them. Lots of food are wasted everyday by restaurants and will be of great use if they are given to the needy and homeless people. The app provides a platform where restaurants can log in and list their available leftover food, and users can view these listings.

You can find the deployed app [here](https://greentable-jmgh1328.streamlit.app/)

## Team members
1. [Jamie](https://github.com/jamieemathew)
2. [Gayathri](https://github.com/Gxyathri)
## Link to product walkthrough
[link to video](https://drive.google.com/file/d/1H5CUWn1EXrOjwS2M8_GammFcdkyKNmm7/view?usp=drive_link)
## How it Works ?
1. There are 4 pages in the web app: home, available food, restaurant login and food submission, restaurant registration
2. New restaurants can register at the restaurant registration page and set their passwords
3. Then they can login to their account from the login page
4. After logging in, they can fill in the food submission form where they will provide details like restaurant name, food description, quantity available, pickup time, city, address and contact information
5. The submission can be seen on the table in 'available food' page. Users can refer this table and pickup the food that they want
6. After the customer has picked up the food, restaurants can delete that food entry/quantity of food that has been bought from the available food table
7. The restaurants can then logout from the application

## Libraries used
Library Name - Version
1. Streamlit    - 1.32.2
2. Pandas       - 2.2.1
3. SQLAlchemy   - 2.0.30
4. Pillow(PIL)  - 10.1.0
5. Passlib      - 1.7.4
6. SQLite
## How to configure
1. Clone this repository
   ```bash
   git clone https://github.com/jamieemathew/greentable
   ```
2. Install the requirements
   ```bash
   pip install -r requirements.txt
   ```
## How to Run
```bash
   streamlit run app.py
   ```
