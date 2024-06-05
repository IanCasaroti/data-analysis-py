import streamlit as st
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('dados_combinados.csv')

# Convert dates to datetime format
df['calendar_date'] = pd.to_datetime(df['calendar_date'])
df['creation_date'] = pd.to_datetime(df['creation_date'])

# Create widgets for user input
location = st.sidebar.selectbox('Select Location', np.append(df['location'].unique(), 'All'))
property_id = st.sidebar.selectbox('Select Property ID', np.append(df['property_id'].unique(), 'All'))

# Create date input widget and convert date objects to datetime
date_range = st.sidebar.date_input('Select Date Range', [df['calendar_date'].min(), df['calendar_date'].max()])
date_range = pd.to_datetime(date_range)

# Filter data based on user input
if location != 'All':
    df = df[df['location'] == location]
if property_id != 'All':
    df = df[df['property_id'] == property_id]
df = df[df['calendar_date'].between(date_range[0], date_range[1])]

# Calculate KPIs
num_occupied = df['occupancy'].sum()
num_blocked = df['blocking'].sum()
num_occupied_and_blocked = df[(df['occupancy'] == 1.0) & (df['blocking'] == 1.0)].shape[0]
num_available = len(df) - num_occupied_and_blocked - ((num_occupied - num_occupied_and_blocked) + (num_blocked - num_occupied_and_blocked))

# Add a new column with the creation date and property ID of the previous row
df['previous_creation_date'] = df['creation_date'].shift()
df['previous_property_id'] = df['property_id'].shift()

# Filter rows where occupancy is 1.0, blocking is 0 and creation date is different from the creation date of the previous row or property ID is different from the property ID of the previous row
check_ins = df[(df['occupancy'] == 1.0) & (df['blocking'] == 0) & ((df['creation_date'] != df['previous_creation_date']) | (df['property_id'] != df['previous_property_id']))]

# Count the number of check-ins
num_checkins = len(check_ins)

avg_precedence = (df['calendar_date'] - df['creation_date']).mean().days
total_revenue = (df['last_daily_price'] * df['occupancy']).sum()
percentage_revenue = total_revenue / df['last_daily_price'].sum() * 100
num_booked_future = df[(df['calendar_date'] > df['calendar_date'].max()) & (df['occupancy'] == 1)].shape[0]
revenue_future = df[(df['calendar_date'] > df['calendar_date'].max()) & (df['occupancy'] == 1)]['last_daily_price'].sum()

# Display KPIs
st.write(f"Number of occupied dates: {num_occupied}")
st.write(f"Number of blocked dates: {num_blocked}")
st.write(f"Number of available dates: {num_available}")
st.write(f"Number of check-ins: {num_checkins}")
st.write(f"Average precedence of the bookings: {avg_precedence} days")
st.write(f"Total revenue of the booked dates: {total_revenue}")