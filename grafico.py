import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import matplotlib.dates as mdates
import matplotlib.ticker as mtick

def show():
    # Load your data
    df = pd.read_csv('dados_combinados.csv')

    # Convert 'calendar_date' to datetime
    df['calendar_date'] = pd.to_datetime(df['calendar_date'])

    # Create 'is_occupied', 'is_available', 'is_blocked' and 'future_occupied' columns
    df['is_occupied'] = ((df['occupancy'] == 1) & (df['blocking'] == 0)).astype(int)
    df['is_available'] = ((df['occupancy'] == 0) & (df['blocking'] == 0)).astype(int)
    df['is_blocked'] = (df['blocking'] == 1).astype(int)
    df['future_occupied'] = ((df['occupancy'] == 1) & (df['calendar_date'] > df['calendar_date'].max() - pd.DateOffset(days=30))).astype(int)

    # Group by 'calendar_date' and calculate the sum of 'is_occupied', 'is_available', 'is_blocked' and 'future_occupied'
    daily_data = df.groupby('calendar_date').agg({'is_occupied': 'sum', 'is_available': 'sum', 'is_blocked': 'sum', 'future_occupied': 'sum'}).reset_index()

    # Calculate total available dates for each day
    daily_data['total_available_dates'] = daily_data['is_available'] + daily_data['is_occupied']

    # Calculate occupancy rate
    daily_data['occupancy_rate'] = daily_data['is_occupied'] / daily_data['total_available_dates']

    # Get the last 30 days of data
    last_30_days = daily_data[daily_data['calendar_date'] >= daily_data['calendar_date'].max() - pd.DateOffset(days=30)]

        # Convert the selected start date to datetime
    start_date = pd.to_datetime(st.sidebar.date_input('Select the start date', daily_data['calendar_date'].max() - pd.DateOffset(days=60)))

    # Filter the data based on the selected start date
    filtered_data = daily_data[(daily_data['calendar_date'] >= start_date) & (daily_data['calendar_date'] < start_date + pd.DateOffset(days=30))]

    # Create line chart for occupancy rate with matplotlib
    fig, ax = plt.subplots(figsize=(15, 5))  # Increase the width of the figure
    ax.plot(filtered_data['calendar_date'], filtered_data['occupancy_rate'], color='darkblue')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))  # Format y-axis labels as percentages
    ax.xaxis.set_major_locator(mdates.DayLocator())  # Set x-axis major locator to a DayLocator
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format x-axis labels as dates
    ax.grid(True)  # Add grid lines
    # Rotate and decrease the size of date labels on x-axis
    plt.xticks(rotation=45, fontsize=8)
    st.pyplot(fig)

    # Create line chart for future bookings with matplotlib
    fig, ax = plt.subplots(figsize=(15, 5))  # Increase the width of the figure
    ax.plot(filtered_data['calendar_date'], filtered_data['future_occupied'], color='darkblue')
    ax.xaxis.set_major_locator(mdates.DayLocator())  # Set x-axis major locator to a DayLocator
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format x-axis labels as dates
    ax.grid(True)  # Add grid lines
    # Rotate and decrease the size of date labels on x-axis
    plt.xticks(rotation=45, fontsize=8)
    st.pyplot(fig)

    # Placeholder for the other plot
    st.empty()