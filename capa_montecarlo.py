import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit app title
st.title('Sprint Capacity Planner with Monte Carlo Simulation')

# Number of developers
num_devs = st.number_input('Number of developers', min_value=1, value=4)

# Number of simulations
num_simulations = st.number_input('Number of simulations', min_value=100, value=1000)

# Input for developers' data
dev_data = {}
for i in range(1, num_devs + 1):
    st.subheader(f'Developer {i}')
    name = st.text_input(f'Name of Developer {i}', value=f'Dev{i}')
    capacity = st.text_input(f'Historical capacities for {name} (comma-separated)', value='15,20')
    story_points = st.text_input(f'Historical story points for {name} (comma-separated)', value='12,18')
    next_PI_capacity = st.number_input(f'Predicted capacity for next PI - {name}', min_value=0.0, value=20.0, step=0.1)
    
    # Parsing the input data
    capacity = list(map(float, capacity.split(',')))
    story_points = list(map(int, story_points.split(',')))
    
    dev_data[name] = {
        'capacity': capacity,
        'story_points': story_points,
        'next_PI_capacity': next_PI_capacity,
    }

# Function for Monte Carlo simulation
def run_monte_carlo_simulation(dev_data, num_simulations):
    total_story_points_results = []
    individual_results = {name: [] for name in dev_data}

    for _ in range(num_simulations):
        total_story_points = 0

        for name, data in dev_data.items():
            # Randomly select a historical capacity and story point pair
            idx = np.random.randint(0, len(data['capacity']))
            selected_capacity = data['capacity'][idx]
            selected_story_points = data['story_points'][idx]

            # Use the ratio of story points to capacity for this simulation
            ratio = selected_story_points / selected_capacity
            
            # Use the predicted capacity for the next PI, but introduce some randomness to account for uncertainty (e.g., +/- 20%)
            variability = np.random.uniform(0.8, 1.2)  # This represents potential variation in capacity
            adjusted_next_PI_capacity = data['next_PI_capacity'] * variability

            simulated_story_points = ratio * adjusted_next_PI_capacity
            
            total_story_points += simulated_story_points
            individual_results[name].append(simulated_story_points)
        
        total_story_points_results.append(total_story_points)
    
    return individual_results, total_story_points_results


# Run simulations and display results
if st.button('Run Simulations'):
    individual_simulation_results, total_simulation_results = run_monte_carlo_simulation(dev_data, num_simulations)
    
    st.subheader('Simulation Results per Developer')
    for name, results in individual_simulation_results.items():
        st.write(f'{name} - Mean Predicted Story Points: {np.mean(results):.2f}')
        st.write(f'{name} - Standard Deviation: {np.std(results):.2f}')
        st.write(f'{name} - Median: {np.median(results):.2f}')
        st.write(f'{name} - 90th Percentile: {np.percentile(results, 90):.2f}')

        # Plot individual results
        fig, ax = plt.subplots()
        sns.histplot(results, kde=True, ax=ax)
        ax.set_title(f'Distribution of Predicted Story Points for {name}')
        ax.set_xlabel('Predicted Story Points')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
    
    st.subheader('Total Team Capacity')
    st.write(f'Mean Predicted Story Points: {np.mean(total_simulation_results):.2f}')
    st.write(f'Standard Deviation: {np.std(total_simulation_results):.2f}')
    st.write(f'Median: {np.median(total_simulation_results):.2f}')
    st.write(f'90th Percentile: {np.percentile(total_simulation_results, 90):.2f}')

    # Plot total team capacity results
    fig, ax = plt.subplots()
    sns.histplot(total_simulation_results, kde=True, color="blue", ax=ax)
    ax.set_title('Total Team Predicted Story Points Distribution')
    ax.set_xlabel('Total Predicted Story Points')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
