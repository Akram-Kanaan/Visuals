

import streamlit as st
import pandas as pd
import plotly.express as px
 
# Load the health dataset
@st.cache_data
def load_health_data():
    data = pd.read_csv(r'https://raw.githubusercontent.com/Akram-Kanaan/Visuals/main/Health.csv')
    data.columns = data.columns.str.strip()  # Clean column names
    data['Nb of Covid-19 cases'] = pd.to_numeric(data['Nb of Covid-19 cases'], errors='coerce')
    data['Percentage of cases out of national total'] = pd.to_numeric(data['Percentage of cases out of national total'], errors='coerce')
   
    # Composite Chronic Disease Score
    data['Chronic Disease Score'] = (data['Existence of chronic diseases - Hypertension'] +
                                     data['Existence of chronic diseases - Cardiovascular disease'] +
                                     data['Existence of chronic diseases - Diabetes'])
    return data
 
df = load_health_data()
 
# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Tree Map", "Line Chart", "Bubble Chart"])
 
# ------------------- Tree Map Page -------------------
if page == "Tree Map":
    st.title("COVID-19 Cases Distribution in Lebanon")
    st.write("""
    **Purpose**: This tree map shows the distribution of COVID-19 cases across different regions and towns in Lebanon.
    Each region contains towns, and the size of the boxes represents the number of COVID-19 cases in that town.
   
    **Key Insights**:
    - The larger the box, the more COVID-19 cases in that town.
    - This chart allows us to easily compare regions and towns with the highest number of COVID-19 cases, highlighting the areas most affected by the pandemic.
    """)
 
    # Sidebar Filters for Tree Map
    st.sidebar.header("Filter Options")
 
    # Dropdown for selecting a region
    regions = df['refArea'].unique()
    selected_region = st.sidebar.selectbox("Select a Region:", regions)
 
    # Slider for filtering the number of COVID-19 cases
    min_cases, max_cases = st.sidebar.slider("Select Range of COVID-19 Cases", 0, int(df['Nb of Covid-19 cases'].max()), (0, 100))
 
    # Filter data based on the selected region and case range
    filtered_data = df[(df['refArea'] == selected_region) &
                       (df['Nb of Covid-19 cases'].between(min_cases, max_cases))]
 
    # Tree Map Visualization
    st.subheader(f"Tree Map of COVID-19 Cases in {selected_region}")
    fig = px.treemap(filtered_data, path=['refArea', 'Town'], values='Nb of Covid-19 cases',
                     title=f'Tree Map of COVID-19 Cases in {selected_region}',
                     labels={'Nb of Covid-19 cases': 'COVID-19 Cases'},
                     height=600)
    st.plotly_chart(fig)
 
# ------------------- Line Chart Page -------------------
elif page == "Line Chart":
    st.title("COVID-19 Cases Over Towns")
    st.write("""
    **Purpose**: This line chart shows how the number of COVID-19 cases varies across different towns in Lebanon.
    By visualizing the data as a line, we can observe patterns and trends in how cases are distributed geographically.
   
    **Key Insights**:
    - The chart reveals any trends in the number of cases across towns, such as sudden spikes or steady increases.
    - Comparing multiple towns allows us to identify which towns are more or less affected by COVID-19.
    """)
 
    # Sidebar Filters for Line Chart
    st.sidebar.header("Line Chart Filter Options")
 
    # Dropdown for selecting towns (allow multiple selections)
    towns = df['Town'].unique()
    selected_towns = st.sidebar.multiselect("Select Town(s):", towns, default=towns)
 
    # Slider for filtering the number of COVID-19 cases
    case_range = st.sidebar.slider("Select Range of COVID-19 Cases", 0, int(df['Nb of Covid-19 cases'].max()), (0, 100))
 
    # Filter data based on the selected towns and case range
    filtered_data_line = df[(df['Town'].isin(selected_towns)) &
                            (df['Nb of Covid-19 cases'].between(case_range[0], case_range[1]))]
 
    # Line Chart Visualization
    st.subheader("Line Chart of COVID-19 Cases by Town")
    fig5 = px.line(filtered_data_line, x='Town', y='Nb of Covid-19 cases',
                   title='COVID-19 Cases Over Towns',
                   labels={'Nb of Covid-19 cases': 'Number of COVID-19 Cases', 'Town': 'Town'},
                   height=400)
    st.plotly_chart(fig5)
 
# ------------------- Bubble Chart Page -------------------
elif page == "Bubble Chart":
    st.title("COVID-19 Cases vs. Percentage of Cases with Chronic Disease")
    st.write("""
    **Purpose**: This bubble chart visualizes the relationship between the percentage of COVID-19 cases (out of the national total) and the number of cases, with the bubble size representing the chronic disease score.
    It helps us understand which towns have both high COVID-19 cases and a high burden of chronic diseases.
   
    **Key Insights**:
    - Larger bubbles indicate towns with more chronic diseases, revealing the additional health burden on those areas.
    - The chart highlights towns that may need more healthcare resources due to both high COVID-19 cases and chronic disease prevalence.
    """)
 
    # Sidebar Filters for Bubble Chart
    st.sidebar.header("Bubble Chart Filter Options")
 
    # Dropdown for selecting towns (allow multiple selections)
    towns_bubble = df['Town'].unique()
    selected_towns_bubble = st.sidebar.multiselect("Select Town(s):", towns_bubble, default=towns_bubble)
 
    # Slider for filtering the number of COVID-19 cases
    bubble_case_range = st.sidebar.slider("Select Range of COVID-19 Cases", 0, int(df['Nb of Covid-19 cases'].max()), (0, 100))
 
    # Filter data based on the selected towns and case range
    filtered_data_bubble = df[(df['Town'].isin(selected_towns_bubble)) &
                              (df['Nb of Covid-19 cases'].between(bubble_case_range[0], bubble_case_range[1]))]
 
    # Bubble Chart Visualization
    st.subheader("Bubble Chart: COVID-19 Cases vs. Percentage of National Cases")
    bubble_chart = px.scatter(filtered_data_bubble, x='Percentage of cases out of national total',
                              y='Nb of Covid-19 cases',
                              size='Chronic Disease Score',
                              color='Town',
                              hover_name='Town',
                              title="Bubble Chart: Covid-19 Cases vs. Percentage of Cases with Chronic Disease",
                              labels={'Percentage of cases out of national total': 'Percentage of National Cases',
                                      'Nb of Covid-19 cases': 'Number of Covid-19 Cases',
                                      'Chronic Disease Score': 'Chronic Disease Score (Sum)'},
                              height=600)
    st.plotly_chart(bubble_chart)
