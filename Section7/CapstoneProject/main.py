import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from supabase import create_client, Client
from statsforecast import StatsForecast
from statsforecast.models import CrostonOptimized

# Initialize connection to db
@st.cache_resource
def init_connection():
    db_pass = st.secrets["SUPABASE_URL"]
    api_key = st.secrets["SUPABASE_KEY"]
    client = create_client(db_pass, api_key)
    return client

# Run the function to make the connection
client = init_connection()

# Function to query the db
@st.cache_data(ttl=600)  # cache clears after 10 minutes
def run_query():
    # Return just the data list so Streamlit can cache it easily
    return client.table("table").select("*").execute().data

# Function to create a Dataframe
@st.cache_data(ttl=600)
def create_dataframe():
    raw_data = run_query()
    df = pd.json_normalize(raw_data)
    # Cast to integer here so it applies to the whole app safely
    df['volume'] = df['volume'].astype(int)
    return df

# Function to plot data (pass df as an argument)
@st.cache_data
def plot_volume(ids, df):
    fig, ax = plt.subplots()

    for id in ids:
        # Filter the dataframe for the specific ID
        subset = df[df['parts_id'] == id]
        # X and Y must come from the same subset
        ax.plot(subset['date'], subset['volume'], label=id) 
        
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.legend(loc='best')
    fig.autofmt_xdate()

    st.pyplot(fig)

# Function to format the dataframe
@st.cache_data
def format_dataset(ids, df):
    # Use .copy() to avoid mutating the original cached dataframe
    model_df = df[df['parts_id'].isin(ids)].copy()
    model_df = model_df.drop(['id'], axis=1, errors='ignore')
    model_df.rename(columns={"parts_id": "unique_id", "date": "ds", "volume": "y"}, inplace=True)
    return model_df

# Create the statsforecast object
# Removed the unused model_df argument
@st.cache_resource
def create_sf_object():
    sf = StatsForecast(
        models=[CrostonOptimized()],
        freq='D',
        n_jobs=-1
    )
    return sf

# Function to make predictions
@st.cache_data(show_spinner="Making predictions...")
def make_predictions(ids, horizon, df):
    model_df = format_dataset(ids, df)
    sf = create_sf_object()

    forecast_df = sf.forecast(df=model_df, h=horizon)
    forecast_df = forecast_df.reset_index() # Ensure unique_id is a column, not an index

    # Rename standard columns, and rename the model's output column to 'forecast'
    forecast_df.rename(columns={
        "unique_id": "parts_id", 
        "ds": "date",
        "CrostonOptimized": "forecast" 
    }, inplace=True)

    csv = forecast_df.to_csv(index=False).encode('utf-8')
    return csv


if __name__ == "__main__":
    st.title("Forecast product demand")

    df = create_dataframe()

    st.subheader("Select a product")
    product_ids = st.multiselect(
        "Select product ID", options=df['parts_id'].unique()
    )

    if len(product_ids) > 0:
        # Pass df into the plotting function
        plot_volume(product_ids, df)

    with st.expander("Forecast"):
        if len(product_ids) == 0:
            st.warning("Select at least one product ID to forecast")
        else:
            horizon = st.slider("Horizon", 1, 12, step=1)
            forecast_btn = st.button("Forecast", type="primary")

            # Fix for the nested button issue using session_state
            if forecast_btn:
                # Generate and save the CSV to session state
                st.session_state['forecast_csv'] = make_predictions(product_ids, horizon, df)

            # If the CSV exists in memory, show the download button
            if 'forecast_csv' in st.session_state:
                st.download_button(
                    label="Download forecast as CSV",
                    data=st.session_state['forecast_csv'],
                    file_name='forecast.csv',
                    mime='text/csv',
                )