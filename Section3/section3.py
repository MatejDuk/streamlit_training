#Capstone project
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.ensemble import GradientBoostingClassifier

URL = "Section3/mushrooms.csv"
COLS = ['odor', 'gill-size', 'gill-color', 'stalk-surface-above-ring',
       'stalk-surface-below-ring', 'stalk-color-above-ring',
       'stalk-color-below-ring', 'ring-type', 'spore-print-color']

# Function to read the data
@st.cache_data
def read_data(URL):
    data = pd.read_csv(URL)
    return data

# Function to fit the LabelEncoder
@st.cache_resource
def label_encoder_function(data):
    le = LabelEncoder()
    data['class'] = le.fit_transform(data['class'])
    return data, le

# Function to fit the OrdinalEncoder
@st.cache_resource
def ordinal_encoder_function(data, X_cols):
    oe = OrdinalEncoder()
    
    data[X_cols] = oe.fit_transform(data[X_cols])
    return data, oe

# Function to encode data
@st.cache_data
def encode_data(data, X_cols):
    X = data[X_cols]
    y = data['class']

    return X, y

# Function to train the model
@st.cache_resource
def train_model(X, y):
    gbc = GradientBoostingClassifier(max_depth=5, random_state=42)
    gbc.fit(X, y)
    return gbc

# Function to make a prediction
@st.cache_resource
def predict(_gbc, row):
    return _gbc.predict(row)

if __name__ == "__main__":
    st.title("Mushroom classifier 🍄")
    
    # Read the data
    data = read_data(URL)
    
    st.subheader("Step 1: Select the values for prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        odor = st.selectbox('Odor', ('a - almond', 'l - anisel', 'c - creosote', 'y - fishy', 'f - foul', 'm - musty', 'n - none', 'p - pungent', 's - spicy'))
        stalk_surface_above_ring = st.selectbox('Stalk surface above ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        stalk_color_below_ring = st.selectbox('Stalk color below ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
    with col2:
        gill_size = st.selectbox('Gill size', ('b - broad', 'n - narrow'))
        stalk_surface_below_ring = st.selectbox('Stalk surface below ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        ring_type = st.selectbox('Ring type', ('e - evanescente', 'f - flaring', 'l - large', 'n - none', 'p - pendant', 's - sheathing', 'z - zone'))
    with col3:
        gill_color = st.selectbox('Gill color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'g - gray', 'r - green', 'o - orange', 'p - pink', 'u - purple', 'e - red', 'w - white', 'y - yellow'))
        stalk_color_above_ring = st.selectbox('Stalk color above ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
        spore_print_color = st.selectbox('Spore print color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'r - green', 'o - orange', 'u - purple', 'w - white', 'y - yellow'))

    st.subheader("Step 2: Ask the model for a prediction")

    pred_btn = st.button("Predict", type="primary")

    # If the button is clicked:
    # 1. Fit the LabelEncoder
    # 2. Fit the OrdinalEncoder
    # 3. Encode the data
    # 4. Train the model
    if pred_btn:
        data, le = label_encoder_function(data)
        data, oe= ordinal_encoder_function(data, COLS)
        X,y = encode_data(data, COLS)
        model = train_model(X,y)

        x_pred = [odor, 
                    gill_size, 
                    gill_color, 
                    stalk_surface_above_ring, 
                    stalk_surface_below_ring, 
                    stalk_color_above_ring, 
                    stalk_color_below_ring, 
                    ring_type, 
                    spore_print_color]

        clean_x_pred = [item[0] for item in x_pred]
        x_pred_final = oe.transform([clean_x_pred])

        pred = predict(model, x_pred_final)
        pred = le.inverse_transform(pred)

        if pred=="e":
            text = "The muhroom is edible"
        else:
            text = "The mushroom is poisonous"


        st.write(text)
        
    # 5. Make a prediction
    # 6. Format the prediction to be a nice text
    # 7. Output it to the screen
    





