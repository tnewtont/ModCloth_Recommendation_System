import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import pickle
import random


st.title('ModCloth Recommendations')
st.header("Curious to see what users are recommended?")
st.header("Discover the many awesome, vintage-inspired choices we have for women's apparel!")

# Initialize SQL queries
conn = sqlite3.connect('user_recommendations.sqlite')
recs = pd.read_sql('SELECT * FROM recommendations', conn)

users = pd.read_sql('SELECT username FROM recommendations', conn)

# Dropdown menu of selecting a user
option = st.selectbox("Select a user to see their recommendations.",
                      (users),)

# Check whether or not the username has a single quote in the beginning of their name
# By default, the SQL query won't run unless there are single quotes surrouneded in the username
# Here, results gets returned as a list of a tuple of length 3 (b/c 3 items), so we need to index twice 
def get_recs(username):
    cursor = conn.cursor()
    if "'" in username:
        username2 = '"' + username + '"'
        items = f'''SELECT product_1, product_2, product_3
                            FROM recommendations 
                            WHERE username = {username2}'''
        cursor.execute(items)
        results = cursor.fetchall()
        return results[0][0], results[0][1], results[0][2]
    else:
        username2 = "'" + username + "'"
        items = f'''SELECT product_1, product_2, product_3
                            FROM recommendations 
                            WHERE username = {username2}'''
        cursor.execute(items)
        results = cursor.fetchall()
        return results[0][0], results[0][1], results[0][2]
        
prods_recommended = get_recs(option)
prods_recommended


# # Load the list of users
# with open("user_list.pickle", "rb") as f:
#     user_list = pickle.load(f)

# # Press a button to select a random user~
# st.header("Click on this button to select a random user.")
# if st.button("Click!"):
#     random_user = random.choice(user_list)
#     st.caption(f"You have selected username {random_user}. Here are their recommended items!")
#     recommended_items = get_recs(random_user)
#     recommended_items

# if selected_user:
#     recs = get_recommendations(selected_user)
#     if recs is not None:
#         st.write(f"### Recommendations for {selected_user}")
#         cols = st.columns(3) # Create three columns for the three displayed recommendations
#         for i, col in enumerate(cols, start = 1):
#             product_id = int(recs[f'product_{i}']) # Remove decimal displayed
#             category = recs[f'cat_{i}'] # Extract the category
#             image_path = random.choice(image_mapping.get(category, [image_mapping['default']]))
#             # Display each individual recommendation as its own column
#             with col:
#                 st.image(image_path, caption=f"Product {product_id} ({category})", use_container_width = True)
#     else:
#         st.warning("No recommendations found for this user.")