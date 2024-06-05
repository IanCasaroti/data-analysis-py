import streamlit as st
import pandas as pd

def color_cells(val):
    """
    Colors cells with 1.0 and removes the number.
    """
    if pd.isna(val):
        return ''
    elif isinstance(val, (int, float)) and val == 1.0:
        return 'background-color: green'
    else:
        return ''

def color_alternate_rows(row):
    """
    Colors alternate rows with orange, dark blue, and green.
    """
    colors = ['background-color: navy', 'background-color: salmon', 'background-color: black']
    color_index = int(row.name) % 3 if row.name.isdigit() else 0
    color = colors[color_index]  # Use the row index to alternate colors
    return [color if val == 1.0 else '' for val in row]

def show():
    # Load your data
    df = pd.read_csv('dados_combinados.csv')

    # Convert 'calendar_date' to datetime
    df['calendar_date_datetime'] = pd.to_datetime(df['calendar_date'])

    # Create separate columns for the month/year and the day
    df['month_year'] = df['calendar_date_datetime'].dt.to_period('M')
    df['day'] = df['calendar_date_datetime'].dt.day

    # Convert the date to a string
    df['calendar_date'] = df['calendar_date_datetime'].dt.strftime('%Y-%m-%d')

    # Pivot the DataFrame with a MultiIndex for the columns
    pivot_df = df.pivot(index='property_id', columns=['month_year', 'day'], values='occupancy')

    # Convert the MultiIndex to datetime
    pivot_df.columns = pd.to_datetime(pivot_df.columns.get_level_values(0).astype(str) + '-' + pivot_df.columns.get_level_values(1).astype(str))

    # Create lists for the month/year and the day of the week
    month_year = pivot_df.columns.strftime('%B %Y')
    day_weekday = pivot_df.columns.strftime('%d %A')

    # Create a new MultiIndex using the lists
    pivot_df.columns = pd.MultiIndex.from_arrays([month_year, day_weekday], names=['month_year', 'day_weekday'])

    # Sort the MultiIndex
    pivot_df = pivot_df.sort_index(axis=1)

    # Replace None or NaN with an empty string
    pivot_df = pivot_df.fillna('')

    # Create a filter for the property with the option to select all
    property_ids = pivot_df.index.unique().tolist()
    property_ids.insert(0, 'All')
    selected_property = st.sidebar.selectbox('Select the property', options=property_ids)

    # # Assuming min_date and max_date are derived from 'calendar_date'
    # min_date = pd.to_datetime(df['calendar_date']).min()
    # max_date = pd.to_datetime(df['calendar_date']).max()

    # start_date, end_date = st.sidebar.date_input('Select the period', [min_date, max_date])
    # Apply the filters to the DataFrame
    if selected_property != 'All':
        filtered_df = pivot_df.loc[[selected_property]]
    else:
        filtered_df = pivot_df



    # Apply the style to the DataFrame
    styled_df = filtered_df.style.applymap(color_cells)
    styled_df = styled_df.apply(color_alternate_rows, axis=1)

    # Remove the numbers
    styled_df = styled_df.format({col: '' for col in styled_df.columns})

    # Display the styled DataFrame in Streamlit
    st.dataframe(styled_df)