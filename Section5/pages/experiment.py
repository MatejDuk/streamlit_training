import streamlit as st
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif

# Set page config:
# The title is "Experiment"
# Choose an icon for the page
# The layout is centered
# The sidebar is set to "auto"
st.set_page_config(page_title = "Experiment", page_icon = "☢️", layout = "centered", initial_sidebar_state = "auto")

if "model" not in st.session_state:
    st.session_state["model"] = []

if "num_features" not in st.session_state:
    st.session_state["num_features"] = []

if "score" not in st.session_state:
    st.session_state["score"] = []
# Write a function to load the wine dataset from sklearn
# Should you cache it?
@st.cache_data
def load_data():
    df = load_wine(as_frame = True).frame
    return df
# Run the function to load the data
df = load_data()

# Write a function for train/test split.
# Use stratification, and keep 30% of the data for the test set
# Should you cache it?
@st.cache_data
def train_test(df):
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=df["target"]
    )
    X_train = X_train.to_numpy()
    X_test  = X_test.to_numpy()
    y_train  = y_train.to_numpy()
    y_test = y_test.to_numpy()
    return X_train, X_test, y_train, y_test


# Run your train/test split function
X_train, X_test, y_train, y_test = train_test(df)

# Write a function to select features using SelectKbest and mutual_info_classif
# Should you cache it?
@st.cache_data
def selection_of_cols(X_train, y_train, X_test, k=5):
    selector = SelectKBest(score_func=mutual_info_classif, k=k)
    X_train_selected = selector.fit_transform(X_train, y_train)
    X_test_selected = selector.transform(X_test)
    return X_train_selected, X_test_selected


# Write a function that fits the selected model and computes the F1-score
# The function must return the F1-Score
# Inside this function, you must run feature selection
# Should you cache it?
@st.cache_data
def f1_score_calc(X_train, X_test, y_train, y_test, model_type):
    if model_type == "Baseline":
        model = DummyClassifier()
    elif model_type == "Decision Tree":
        model = DecisionTreeClassifier()
    elif model_type == "Random Forest":
        model = RandomForestClassifier()
    elif model_type == "Gradient Boosted Classifier":
        model = GradientBoostingClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return f1_score(y_test, y_pred, average = "micro")
    


# Write a callback function that runs the model fitting and scoring function
# The callback appends the model, number of features, and score to the state.
# The callback takes 2 arguments: the model and the number of features to keep
@st.cache_data
def append_new_model(model, num_features):
    X_train_selected, X_test_selected = selection_of_cols(X_train, y_train, X_test, num_features)
    f1 = f1_score_calc(X_train_selected, X_test_selected, y_train, y_test, model)
    st.session_state["score"].append(f1)
    st.session_state["model"].append(model)
    st.session_state["num_features"].append(num_features)


if __name__ == "__main__":
    
    with st.container():
        st.title("🧪 Experiments")

    col1, col2 = st.columns(2)

    with col1:
        model = st.selectbox("Choose a model", ["Baseline", "Decision Tree", "Random Forest", "Gradient Boosted Classifier"])
    with col2:
        k = st.number_input("Choose the number of features to keep", 1, 13)

    # Plug in your callback and define the arguments
    st.button("Train", type="primary", on_click = append_new_model, kwargs = {"model":model,
                                                                              "num_features":k})

    # Display the full dataset inside an expander
    with st.expander(label = "See full dataset"):
        st.dataframe(df)

    if len(st.session_state["score"]) != 0:
        st.subheader(f"The model has an F1-Score of: {st.session_state['score'][-1]}")