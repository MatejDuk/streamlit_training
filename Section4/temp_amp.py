import streamlit as st

st.title("Exercise: State Management")

st.subheader("Temperature conversion")

if "celsius" not in st.session_state:
    st.session_state["celsius"] = 0

if "farenheit" not in st.session_state:
    st.session_state["farenheit"] = 32

if "kelvin" not in st.session_state:
    st.session_state["kelvin"] = 273.15

# Initialize state with temperatures.
# Use the freezing point of water

# Write a callback to convert the temperature in Celsius
# to Farenheit and Kelvin. Change the values in the state
# appropriately
def celsius_input():
    st.session_state["farenheit"] = st.session_state["celsius"]*9/5 + 32
    st.session_state["kelvin"] = st.session_state["celsius"] + 273.15

# Same thing, but converting from Farenheit to Celsius
# and Kelvin
def farenheit_input():
    st.session_state["celsius"] = (st.session_state["farenheit"]-32)*5/9
    st.session_state["kelvin"] = (st.session_state["farenheit"] -32)*5/9 + 273.15

# Same thing, but converting from Kelvin to Celsius
# and Farenheint
def kelvin_input():
    st.session_state["celsius"] = st.session_state["kelvin"]-273.15
    st.session_state["farenheit"] = (st.session_state["kelvin"] -273.15)*9/5 + 32

# Write a callback that adds whatever number the user
# inputs to the Celsius box. Use args.
def add_celsius(add):
    st.session_state["celsius"] += add
    celsius_input()

# Write a callback to sets the temperatures depending on
# which button the user clicks. Use kwargs.
def temp_change(type = "zero"):
    if type == "zero":
        st.session_state["celsius"] = 0
        celsius_input()
    elif type == "boil":
        st.session_state["celsius"] = 100
        celsius_input()
    elif type == "absolute_zero":
        st.session_state["kelvin"] = 0
        kelvin_input()

col1, col2, col3 = st.columns(3)

# Hook up the first 3 callbacks to the input widgets
col1.number_input("Celsius", step=0.01, key="celsius", on_change = celsius_input)
col2.number_input("Farenheit", step=0.01, key="farenheit", on_change = farenheit_input)
col3.number_input("Kelvin", step=0.01, key="kelvin", on_change = kelvin_input)

# Hook up the 4th callback to the button. Use args.
col1, _, _ = st.columns(3)
num = col1.number_input("Add to Celsius", step=1)
col1.button("Add", type="primary", on_click = add_celsius, args = [num])


col1, col2, col3 = st.columns(3)

# Hook up the last callback to each button. Use kwargs.
col1.button('🧊 Freezing point of water', on_click = temp_change, kwargs ={"type":"zero"})
col2.button('🔥 Boiling point of water', on_click = temp_change, kwargs = {"type":"boil"})
col3.button('🥶 Absolute zero', on_click = temp_change, kwargs = {"type":"absolute_zero"})

st.write(st.session_state)