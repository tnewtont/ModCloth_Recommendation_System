import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import random
import os


# Initialize SQL queries
conn = sqlite3.connect('user_recommendations.sqlite')

# Image mappings from product category to a respective image
def get_image_paths(base_path="images"):
    image_mapping = {} # Initialize dictionary for mappings
    for category in os.listdir(base_path): # category is case-sensitive so that it matches cat_1, cat_2, cat_3
        category_path = os.path.join(base_path, category)
        if os.path.isdir(category_path):
            # Get all image filenames in each category folder using list comprehension
            image_mapping[category] = [
                os.path.join(category_path, file)
                for file in os.listdir(category_path)
                if file.endswith((".jpeg", ".jpg", ".png")) # All of the images are saved as .jpeg, but we'll be inclusive here for other common image formats
            ]
    image_mapping["default"] = ["images/placeholder.jpeg"]
    return image_mapping

# Generate image mapping dynamically
image_mapping = get_image_paths()
recs = pd.read_sql('SELECT * FROM recommendations', conn)

users_df = pd.read_sql('SELECT username FROM recommendations', conn)
users = users_df['username'].tolist()

# UI elements
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EDDDBF;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title('👗 ModCloth Recommendations 👗')
st.header("Curious to see what users are recommended? Discover the many awesome, vintage-inspired pieces!")

# Dropdown menu of selecting a user
selected_user = st.selectbox("Select a user to see their recommendations.",
                      (users),)


def get_recommendations(username):
    query = f"""
    SELECT product_1, product_2, product_3, cat_1, cat_2, cat_3
    FROM recommendations
    WHERE username = ?
    """
    recs = pd.read_sql(query, conn, params=(username,)) # Parameterize the query and pass forth username onto WHERE clause
    if recs.empty:
        return None
    return recs.iloc[0]
        

if selected_user:
    recs = get_recommendations(selected_user)
    if recs is not None:
        st.write(f"### Recommendations for {selected_user}")
        cols = st.columns(3) # Create three columns for the three displayed recommendations
        for i, col in enumerate(cols, start = 1):
            product_id = int(recs[f'product_{i}']) # Remove decimal displayed
            category = recs[f'cat_{i}'] # Extract the category
            images = image_mapping.get(category, image_mapping['default'])

            # We want the images displayed to be unique
            if len(images) >= 3:
                selected_images = random.sample(images, 3)
                image_path = selected_images[i - 1]
            # In case less than three images are available
            else:
                image_path = images[0] if images else image_mapping['default'][0]
            
            # Display each unique image as its own column
            with col:
                st.image(image_path, caption = f"Product {product_id} ({category})", use_container_width = True)
    else:
        st.warning("No recommendations found for this user.")