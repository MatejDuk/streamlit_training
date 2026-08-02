import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, AgglomerativeClustering

# hashed_passwords = stauth.Hasher().hash_list(["marketing", "datascience"])
# st.write(hashed_passwords)

# Read config file
with open('Section6/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
# Function to read the data


@st.cache_data
def read_data():
    df = pd.read_csv('Section6/data/segmentation data.csv')
    return df

# Read data
# Assign the features to the variable "X"
df = read_data()
X = df

# Function to calculate the silhouette for each algo, for each number of cluster
# Returns a Dataframe with 3 columns [n_clusters, algo1, algo2]


@st.cache_data(show_spinner="Running experiment")
def run_experiment(X):
    results = []
    for i in range(2,11):
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(X)
        kmeans_silhouette = silhouette_score(X, kmeans.labels_)

        agglomerative = AgglomerativeClustering(n_clusters=i)
        agglomerative.fit(X)
        agglomerative_silhouette = silhouette_score(X, agglomerative.labels_)

        results.append([i, round(kmeans_silhouette,2), round(agglomerative_silhouette,2)])
    
    return pd.DataFrame(results, columns=['n_clusters', 'kmeans', 'agglomerative'])



@st.cache_data
def display_group_metrics(df, num_clusters):
    for i in range(num_clusters):
        f_df = df[df['labels'] == i]

        male_percentage = round(len(f_df[f_df['Sex'] == 0])/len(f_df), 2)*100
        female_percentage = 100 - male_percentage

        marital_percentage = round(
            len(f_df[f_df['Marital status'] == 0])/len(f_df), 2)*100

        mean_age = round(f_df['Age'].mean(), 0)
        min_age = f_df['Age'].min()
        max_age = f_df['Age'].max()

        high_school = round(len(f_df[f_df['Education'] == 1])/len(f_df), 2)*100
        university = round(
            len(f_df[(f_df["Education"] == 2) | (f_df["Education"] == 3)])/len(f_df), 2)*100

        mean_income = round(f_df['Income'].mean(), 0)
        max_income = f_df['Income'].max()
        min_income = f_df['Income'].min()

        employment_num = f_df['Occupation'].mode().values

        if employment_num == 0:
            employment = 'Unemployed'
        elif employment_num == 1:
            employment = 'Skilled employee'
        else:
            employment = 'Highly skilled employee'

        city_num = f_df['Settlement size'].mode().values

        if city_num == 0:
            city = 'Small city'
        elif city_num == 1:
            city = "Mid-sized city"
        else:
            city = "Large city"

        with st.container():
            st.header(f"Group {i+1}")

            st.subheader("Demographics")
            st.write(f"Percentage of men: {male_percentage}%")
            st.write(f"Percentage of female: {female_percentage}%")

            st.subheader("Marital status")
            st.write(f"Percentage of married clients: {marital_percentage}%")

            st.subheader("Age")
            st.write(f"Mean age: {mean_age}")
            st.write(f"Max age: {max_age}")
            st.write(f"Min age: {min_age}")

            st.subheader("Education")
            st.write(f"High school: {high_school}%")
            st.write(f"University: {university}%")

            st.subheader("Income")
            st.write(f"Mean income: {mean_income}$")
            st.write(f"Max income: {max_income}$")
            st.write(f"Min income: {min_income}$")

            st.subheader("Employment")
            st.write(f"The majority is: {employment}")

            st.subheader("City size")
            st.write(f"The majority is: {city}")

# Function to display content for DS


def display_ds_content():
    # Write the dataframe
    st.dataframe(df)
    # Button to run the function run_experiment
    exp_btn = st.button("Run experiment")

    if exp_btn:
        # Run the experiment
        results = run_experiment(X)

        st.write("Silhouette scores")

        # Write the df of the results
        st.dataframe(results)


def display_marketing_content():
    st.write(df)

    num_clusters = st.slider("Number of groups", 2, 10)

    run_clustering = st.button("Generate groups")

    if run_clustering:
        c_df = df.copy()

        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(X)

        c_df['labels'] = kmeans.predict(X)

        c_df = c_df.sort_values(by=['labels'], ascending=True)

        display_group_metrics(c_df, num_clusters)

# Logic to authenticate user
# Render the login widget
authenticator.login(location="sidebar")
if st.session_state.get('authentication_status'):
    authenticator.logout(location="sidebar")
    name = st.session_state.get("username")
    if name == "datascience":
        st.write(f"Welcome *Data Science Team*")
        st.title("Data Science content")
        display_ds_content()
    elif name == "marketing":
        st.write(f"Welcome *Marketing Team*")
        st.title("Marketing content")
        display_marketing_content()
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')

# Authenticate users
# Put login in sidebar