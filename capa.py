import streamlit as st
import pandas as pd
import numpy as np

# Function to simulate story points based on input data and capacity
def simulate_story_points(data, next_PI_capacity, n_simulations=1000):
    developer_story_points = {dev: [] for dev in data}
    total_story_points = []

    for _ in range(n_simulations):
        sprint_story_points = 0

        for dev, records in data.items():
            ratio = np.mean(np.array(records["story_points"]) / np.array(records["capacity"]))
            future_presence = next_PI_capacity[dev]
            future_story_points = future_presence * ratio
            developer_story_points[dev].append(future_story_points)
            sprint_story_points += future_story_points

        total_story_points.append(sprint_story_points)

    return developer_story_points, np.mean(total_story_points)

# Streamlit app title
st.title('Sprint Capacity Planner')

# Number of developers
num_devs = st.number_input('Number of developers', min_value=1, value=4)

# Input for developers' data
dev_data = {}
next_PI_capacity = {}
for i in range(1, num_devs + 1):
    st.subheader(f'Developer {i}')
    name = st.text_input(f'Developer {i} name', value=f'Dev{i}')
    capacity = st.text_input(f'Historical capacities for {name} (comma-separated)', value='15,20')
    story_points = st.text_input(f'Historical story points for {name} (comma-separated)', value='12,18')
    next_capacity = st.number_input(f'Next PI capacity for {name} (man-days)', value=15)
    
    # Parsing the input data
    capacity = list(map(float, capacity.split(',')))
    story_points = list(map(int, story_points.split(',')))

    dev_data[name] = {"capacity": capacity, "story_points": story_points}
    next_PI_capacity[name] = next_capacity

# Run simulation button
if st.button('Calculate Capacity'):
    dev_story_points, total_capacity = simulate_story_points(dev_data, next_PI_capacity)
    st.subheader('Predicted story points per developer')
    for dev, points in dev_story_points.items():
        st.text(f'{dev}: {np.mean(points):.2f} story points')

    st.subheader('Total team capacity for next PI')
    st.text(f'{total_capacity:.2f} story points')
