import streamlit as st

# #Challenge from Section 2 video 10

# with st.form("key", clear_on_submit = False, border = True, width="stretch", height = "content"):
#     apetizers = st.selectbox("Apetizers", options = ["Choice1", "Choice2"])
#     main_course = st.selectbox("Main course", options = ["Choice1", "Choice2"])
#     dessert = st.selectbox("Dessert", options = ["Choice1", "Choice2"])
#     wine = st.checkbox("Are you bringing your own wine?")
#     day_of_coming = st.date_input("When are you coming?", value = None, min_value = "today")
#     time_of_coming = st.time_input("At what time are you coming?", value = "now")
#     allergies = st.text_area("Any allergies?", value = "Leave us a note for allergies")

#     submit_button = st.form_submit_button("Submit")
#     if submit_button:
#         st.write(f"""Your order summary:
                 
#         Appetizer: {apetizers}

#         Main course: {main_course}

#         Dessert: {dessert}

#         Are you bringing your own wine: {"yes" if wine else "no"}

#         Date of visit: {day_of_coming}

#         Time of visit: {time_of_coming}

#         Allergies: {allergies}""")

#Capstone project Section 2

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df = pd.read_csv(URL, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})

st.title("Population of Canada")
st.markdown(f"Source table can be found [here]({URL})")

with st.form("key"):
    cols = st.columns(3)
    #First column
    cols[0].write("Choose a starting date")
    start_quarter = cols[0].selectbox("Quarter", index = 0, options= ["Q1", "Q2", "Q3", "Q4"])
    start_year = cols[0].slider("Year",key= 0, min_value = 1991, max_value = 2023, step = 1)


    #Second column
    cols[1].write("Choose an end date")
    end_quarter = cols[1].selectbox("Quarter", index = 1, options= ["Q1", "Q2", "Q3", "Q4"])
    end_year = cols[1].slider("Year", key=1, min_value = 1991, max_value = 2023, step = 1)

    #Third column
    cols[2].write("Choose a location")
    location = cols[2].selectbox("Choose a location", options = df.columns[1:].tolist())

    submit_button = st.form_submit_button("Analyze")

if (start_year == 1991 and (start_quarter == "Q1" or start_quarter == "Q2")) or (end_year == 2023 and (end_quarter == "Q2" or end_quarter == "Q3" or end_quarter == "Q4")):
    st.error("No data available. Check your quarter and year selection")
elif end_year < start_year:
    st.error("Dates don't work. Start date must come before end date.")
elif end_year == start_year and start_quarter[1] > end_quarter[1]:
    st.error("Dates don't work. Start date must come before end date.")
else:
    start_date = f"{start_quarter} {start_year}"
    end_date = f"{end_quarter} {end_year}"
    
    tab1, tab2 = st.tabs(["Population change", "Compare"])
    
    #First tab 
    tab1.subheader(f"Population change from {start_date} to {end_date}")
    cols = tab1.columns(2)
    
    start_index = df[df["Quarter"] == start_date].index.item()
    end_index = df[df["Quarter"] == end_date].index.item()
    

    start_pop = df[df["Quarter"] == start_date][location].item()
    end_pop = df[df["Quarter"] == end_date][location].item()

    cols[0].metric(start_date, start_pop)
    cols[0].metric(start_date, end_pop, delta = f"{str(round((end_pop/start_pop-1)*100,2))} %")

    x_vals = df.iloc[start_index:end_index]["Quarter"].tolist()
    y_vals = df.iloc[start_index:end_index][location].tolist()

    fig, ax = plt.subplots(figsize=(5,3))

    ax.plot(x_vals, y_vals)

    ax.set_xticks([0, len(x_vals) - 1])
    ax.set_xticklabels([x_vals[0], x_vals[-1]])

    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    plt.xticks(rotation=45) # Rotates x-labels if they overlap

    cols[1].pyplot(fig)

    #Second tab
    tab2.subheader("Compare with other locations")
    locations = tab2.multiselect("Choose other locations", options = df.columns[1:], default = location, max_selections = len(df.columns)-1)
    x_vals = df.iloc[start_index:end_index]["Quarter"].tolist()
    fig2, ax2 = plt.subplots(figsize=(5,3))
    for col_name in locations:
        y_vals = df.iloc[start_index:end_index][col_name].tolist()
        ax2.plot(y_vals, label=col_name)


    ax2.plot(x_vals, y_vals)

    ax2.set_xticks([0, len(x_vals) - 1])
    ax2.set_xticklabels([x_vals[0], x_vals[-1]])

    ax2.set_xlabel("Time")
    ax2.set_ylabel("Population")
    ax2.legend()
    plt.xticks(rotation=45) # Rotates x-labels if they overlap

    tab2.pyplot(fig2)

            

