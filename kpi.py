import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def show():

    # Load the data
    df = pd.read_csv('dados_combinados.csv')

    # Convert dates to datetime format
    df['calendar_date'] = pd.to_datetime(df['calendar_date'])
    df['creation_date'] = pd.to_datetime(df['creation_date'])

    # Create widgets for user input
    location = st.sidebar.selectbox('Selecione a localização', np.append(df['location'].unique(), 'Todos'))
    property_id = st.sidebar.selectbox('Selecione o ID da propriedade', np.append(df['property_id'].unique(), 'Todos'))

    # Create date input widget and convert date objects to datetime
    date_range = st.sidebar.date_input('Selecione o intervalo de datas', [df['calendar_date'].min(), df['calendar_date'].max()])
    date_range = pd.to_datetime(date_range)

    # Filter data based on user input
    if location != 'Todos':
        df = df[df['location'].str.strip().str.lower() == location.lower()]
    if property_id != 'Todos':
        df = df[df['property_id'] == property_id]  # Compare property_id as string
    df = df[(df['calendar_date'] >= date_range[0]) & (df['calendar_date'] <= date_range[1])]

    # If the DataFrame is empty after filtering, display a message
    if df.empty:
        st.write("No data available for the selected filters.")
    else:
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

        # Get today's date
        today = pd.to_datetime(datetime.today())

        # Get the first date from the selected range and add one day
        start_date = date_range[0] + pd.DateOffset(days=1)

        # Calculate the number of booked dates in the future
        num_booked_future = df[(df['calendar_date'] >= start_date) & (df['calendar_date'] <= date_range[1]) & (df['occupancy'] == 1) & (df['blocking'] == 0)].shape[0]

        # Calculate the future revenue
        revenue_future = df[(df['calendar_date'] >= start_date) & (df['calendar_date'] <= date_range[1]) & (df['occupancy'] == 1) & (df['blocking'] == 0)]['last_daily_price'].sum()

        # Add a title
        st.title('KPI Dashboard')

        # Add a subtitle
        st.subheader('Key Performance Indicators')

        # Display KPIs in columns
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(label="Número de datas ocupadas", value=f"{num_occupied}")

        with col2:
            st.metric(label="Número de datas bloqueadas", value=f"{num_blocked}")

        with col3:
            st.metric(label="Número de check-ins", value=f"{num_checkins}")

        with col4:
            st.metric(label="Número de datas reservadas", value=f"{num_booked_future}")

        with col5:
            st.metric(label="Número de datas disponíveis", value=f"{num_available}")

        # Display KPIs in separate containers
        container1 = st.container()
        container2 = st.container()
        container3 = st.container()

        with container1:
            data = df[df['calendar_date'].between(date_range[0], date_range[1])]
            # Group by date and calculate sum of specific columns
            data = data.groupby('calendar_date')[['last_daily_price', 'occupancy']].sum()
            st.metric(label="Receita total", value=f"R${total_revenue:,.2f}")
            # Create line chart for total revenue with matplotlib
            fig, ax = plt.subplots()
            ax.plot(data.index, data['last_daily_price'] * data['occupancy'], color='darkblue')
            ax.yaxis.set_major_formatter('${x:1.2f}')
            # Rotate date labels on x-axis
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with container2:
            data = df[df['calendar_date'].between(date_range[0], date_range[1])]
            # Group by date and calculate sum of specific columns
            data = data.groupby('calendar_date')[['last_daily_price', 'occupancy']].sum()
            st.metric(label="Porcentagem da receita região", value=f"{percentage_revenue:.2f}%")
            # Create line chart for percentage revenue with matplotlib
            fig, ax = plt.subplots()
            ax.plot(data.index, data['last_daily_price'] * data['occupancy'] / data['last_daily_price'].sum() * 100, color='darkblue')
            ax.yaxis.set_major_formatter('{x:1.2f}%')
            # Rotate date labels on x-axis
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with container3:
            data = df[(df['calendar_date'] >= start_date) & (df['calendar_date'] <= date_range[1]) & (df['occupancy'] == 1) & (df['blocking'] == 0)]
            # Get all column names except 'calendar_date'
            columns_to_sum = df.select_dtypes(include=[np.number]).columns
            # Group by 'calendar_date' and sum only specified columns
            data = data.groupby('calendar_date')[columns_to_sum].sum()
            st.metric(label="Receita gerada datas reservadas", value=f"R${revenue_future:,.2f}")
            # Create line chart for future revenue with matplotlib
            fig, ax = plt.subplots()
            ax.plot(data.index, data['last_daily_price'], color='darkblue')
            ax.yaxis.set_major_formatter('${x:1.2f}')
            # Rotate date labels on x-axis
            plt.xticks(rotation=45)
            st.pyplot(fig)
