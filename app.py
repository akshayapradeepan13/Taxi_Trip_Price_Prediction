import streamlit as st
import pickle
import numpy as np

# Load the pickle file
model_path = 'C:/Users/LENOVO/OneDrive/Desktop/Taxi_Project/Taxi.pkl'  
with open(model_path, 'rb') as file:   # Opens the pickle file in binary read mode.
    model = pickle.load(file)

# with open('C:/Users/LENOVO/OneDrive/Desktop/Taxi_Project/scaler.pkl','rb') as file:
#     scaler = pickle.load(file)


# Streamlit app title
st.title("Taxi Fare Prediction App")

# App description
st.write("This App Predicts Taxi Fares Based On Trip Details. Please Enter The Required Information Below.")

# Input fields for user input
# step=0.1: Sets the increment or decrement step size for the input
trip_distance_km = st.number_input("Trip Distance (in km)", min_value=0.0, step=0.1, format="%.2f")
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6, step=1)
base_fare = st.number_input("Base Fare (in $)", min_value=0.0, step=0.1, format="%.2f")
per_km_rate = st.number_input("Rate per km (in $)", min_value=0.0, step=0.1, format="%.2f")
per_minute_rate = st.number_input("Rate per minute (in $)", min_value=0.0, step=0.1, format="%.2f")
trip_duration_minutes = st.number_input("Trip Duration (in minutes)", min_value=0.0, step=0.1, format="%.1f")

# Categorical features
time_of_day = st.selectbox("Time of Day", ["Morning", "Evening", "Night"])
day_of_week = st.selectbox("Day of Week", ["Weekday", "Weekend"])
traffic_conditions = st.selectbox("Traffic Conditions", ["Low", "Medium", "High"])
weather = st.selectbox("Weather", ["Clear", "Rain", "Snow"])

# Mapping categorical inputs to features
time_of_day_mapping = {"Morning": [1, 0, 0], "Evening": [0, 1, 0], "Night": [0, 0, 1]} # one hot
day_of_week_mapping = {"Weekday": [0], "Weekend": [1]}  # binary
traffic_conditions_mapping = {"Low": [1, 0], "Medium": [0, 1], "High": [0, 0]} # dummy
weather_mapping = {"Clear": [0, 0], "Rain": [1, 0], "Snow": [0, 1]} # dummy

time_of_day_encoded = time_of_day_mapping[time_of_day]
day_of_week_encoded = day_of_week_mapping[day_of_week]
traffic_conditions_encoded = traffic_conditions_mapping[traffic_conditions]
weather_encoded = weather_mapping[weather]

# Prediction button
if st.button("Predict Fare"): # the logic (code) runs when we click this button
    # Combine all inputs into a single array
    input_data = np.array([[
        trip_distance_km,
        passenger_count,
        base_fare,
        per_km_rate,
        per_minute_rate,
        trip_duration_minutes,
        *time_of_day_encoded,
        *day_of_week_encoded,
        *traffic_conditions_encoded,
        *weather_encoded
    ]])
    
    # Get prediction from the model
    prediction = model.predict(input_data)
    
    # Display the result
    st.success(f"Predicted Fare: ${prediction[0]:.2f}")
else:
    st.write("Click the 'Predict Fare' button to get the prediction.")

