import streamlit as st
import numpy as np
from joblib import load

# Initialize the session state with an empty prediction
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None

# Function to load the model (use caching)
@st.cache_resource
def load_model():
    model = load("Section4/model.joblib")
    return model


# Callback function to make a prediction.
# Use kwargs to pass the model as an argument
# It updates the value of the prediction stored in the state
def make_prediction(pipe):
    miles = st.session_state["miles"]
    year = st.session_state["year"]
    make = st.session_state["make"]
    model = st.session_state["model"]
    engine_size = st.session_state["engine_size"]
    province = st.session_state["province"]

    X_pred = np.array([miles, year, make, model, engine_size, province]).reshape(1,-1)

    pred = pipe.predict(X_pred)
    pred = round(pred[0], 2)

    st.session_state["prediction"] = pred
    

if __name__ == "__main__":
    st.title("🍁Used car price calculator")

    # Load model
    model = load_model()

    with st.form(key="form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.number_input("Miles", value=86132.0, min_value=0.0, step=0.1, key="miles")
            st.selectbox("Model", index=0, key="model", options=['Prius', 'Highlander', 'Civic', 'Accord', 'Corolla', 'Ridgeline',
       'Odyssey', 'CR-V', 'Pilot', 'Camry Solara', 'Matrix', 'RAV4',
       'Rav4', 'HR-V', 'Fit', 'Yaris', 'Yaris iA', 'Tacoma', 'Camry',
       'Avalon', 'Venza', 'Sienna', 'Passport', 'Accord Crosstour',
       'Crosstour', 'Element', 'Tundra', 'Sequoia', 'Corolla Hatchback',
       '4Runner', 'Echo', 'Tercel', 'MR2 Spyder', 'FJ Cruiser',
       'Corolla iM', 'C-HR', 'Civic Hatchback', '86', 'S2000', 'Supra',
       'Insight', 'Clarity', 'CR-Z', 'Prius Prime', 'Prius Plug-In',
       'Prius c', 'Prius C', 'Prius v'])
        with col2:
            st.number_input("Year", value=2001, min_value=1886, step=1, key="year")
            st.number_input("Engine size (L)", value=1.5, key="engine_size", min_value=0.9, step=0.1)
        with col3:
            st.selectbox("Make", key="make", index=0, options=['toyota', 'honda'])
            st.selectbox("Province", index=0, key="province", options=['NB', 'QC', 'BC', 'ON', 'AB', 'MB', 'SK', 'NS', 'PE', 'NL', 'YT', 'NC', 'OH','SC'])
        st.form_submit_button("Calculate", type="primary", on_click = make_prediction, kwargs = {"pipe":model})

    # Display the prediction
    # If the value is empty, display a message to click on the button
    # Otherwise, display the prediction
    if st.session_state["prediction"] == None:
        st.write("Click on the button")
    else:
        st.write(f"Price of the car will be {st.session_state['prediction']}")

    st.write(st.session_state)