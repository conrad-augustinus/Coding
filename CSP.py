# Web application for tracking a company's carbon footprint

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# Import the streamlit for web app creation, numpy for numerical operations, and matplotlib for plotting

class Footprint:
    def __init__(self):
        # Initialize dictionaries to store sector data, benchmark values, and user input values
        self.sectors = {}
        self.benchmark = {}
        self.value = {}

    def emission_sector(self, sector, use_cases):
        # Define a sector within the Footprint object
        self.sectors[sector] = {use_case: {} for use_case in use_cases}
        self.benchmark[sector] = {use_case: 0 for use_case in use_cases}
        self.value[sector] = {use_case: {} for use_case in use_cases}

    def input_value(self, sector, use_case, year):
        # Get user input for emission value for a use case within a sector for a year
        if sector in self.sectors and use_case in self.sectors[sector]:
            value = st.number_input(f"Enter Value for {use_case} in tCO2eq for {year}", value=None, key=f"{sector}_{use_case}_{year}")
            if value is not None:
                # Store user input in session state and Footprint object
                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                self.value[sector][use_case][year] = value

    def emission_benchmark(self, sector, use_case, value):
        # Set benchmark emission value for a use case within a sector
        if sector in self.benchmark and use_case in self.sectors[sector]:
            self.benchmark[sector][use_case] = value

    def total_emissions_by_year(self, year):
        # Calculate total emissions for a specific yea
        total_emissions = 0
        for sector in self.value.keys():
            for use_case in self.value[sector].keys():
                # Check if user input exists for the year in session state
                if st.session_state.get(sector, {}).get(use_case, {}).get(year):
                    total_emissions += st.session_state[sector][use_case][year]
        return total_emissions

    def display_values(self, sector, selected_year):
        # Display emission values and comparisons to benchmarks for a chosen sector and year
        if sector in self.sectors:
            total = 0
            for use_case, year_values in st.session_state.get(sector, {}).items():
                value = year_values.get(selected_year, 0)
                benchmark = self.benchmark[sector][use_case]
                st.write(f"{use_case}: {value} (Standard Emissions: {benchmark})")
                if value > benchmark:
                    st.warning(f"  - Excess Emissions compared to Standard of {value - benchmark} tCO2eq")
                elif value < benchmark:
                    st.success(f"  - Below Standard Emissions by {benchmark - value} tCO2eq")
                total += value

            st.write(f"Total Emissions for {sector}: {total} tCO2eq")
            st.caption("Benchmark Approximation Source: https://data.europa.eu/doi/10.2760/028705")
            # Calculate and display number of trees to offset emissions
            num_trees = int(self.total_emissions_by_year(selected_year) * 45)
            st.write(f"Number of Trees to Offset Emissions per Year: {num_trees}")
            # Generate and plot forest visualization based on number of trees
            forest = generate_forest(num_trees)
            plot_forest(forest)
            st.caption("Approximately 45 Trees per Ton of GHGs Emitted")

def generate_forest(num_trees):
    # Function to create virtual forest
    forest = []
    for _ in range(num_trees):
        x = np.random.rand()
        y = np.random.rand()
        tree = {"x": x, "y": y}
        forest.append(tree)
    return forest

def plot_forest(forest):
    # Function to plot the generated forest data
    fig, ax = plt.subplots()
    for tree in forest:
        # Plot each tree as a triangle marker on the scatter plot
        ax.scatter(tree["x"], tree["y"], marker="^", s=50, color="green")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")

    ax.axis("off")

    # Display the forest plot in Streamlit
    st.pyplot(fig)

def initialize_sectors(footprint_manager):
    # Define a dictionary mapping sectors to their use cases
    sectors_data = {
        "Energy": ["Electricity", "Fuel Combustion", "Thermal Energy"],
        "Production and Manufacturing": ["Production Processes"],
        "Transportation and Storage": ["Logistics"],
        "Water Supply and Waste Management": ["Water Treatment"],
        "Wholesale and Retail Trade": ["Distribution Centers"],
        "Agriculture": ["Livestock", "Farming"],
    }

    # Populate sectors and benchmark values in the Footprint object
    for sector, use_cases in sectors_data.items():
        footprint_manager.emission_sector(sector, use_cases)

    footprint_manager.emission_benchmark("Energy", "Electricity", 12.1)
    footprint_manager.emission_benchmark("Energy", "Fuel Combustion", 42)
    footprint_manager.emission_benchmark("Production and Manufacturing", "Production Processes", 18.3)
    footprint_manager.emission_benchmark("Transportation and Storage", "Logistics", 10.8)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Water Treatment", 0.8)
    footprint_manager.emission_benchmark("Wholesale and Retail Trade", "Distribution Centers", 2.2)
    footprint_manager.emission_benchmark("Agriculture", "Livestock", 48.55)
    footprint_manager.emission_benchmark("Agriculture", "Farming", 17.32)

def plot_total_emissions(footprint_manager):
    # Function to calculate and plot total emissions over time
    years = list(range(2010, 2050))
    total_emissions_data = [footprint_manager.total_emissions_by_year(year) for year in years]

    # Filter years and emissions data for non-zero values
    non_zero_years = [year for year, emissions in zip(years, total_emissions_data) if emissions > 0]
    non_zero_emissions = [emissions for emissions in total_emissions_data if emissions > 0]

    fig, ax = plt.subplots()
    # Plot total emissions over the years using Matplotlib
    ax.plot(non_zero_years, non_zero_emissions, marker="o", linestyle="-", color="g")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Emissions (in tCO2eq)")
    st.pyplot(fig)

def main_menu(footprint_manager):
    # Streamlit sidebar for user interaction
    st.sidebar.title("Carbon Footprint Tracker")
    options = ["Add/Update Values", "Display Emissions", "Plot Total Emissions"]

    choice = st.sidebar.selectbox("Select Option", options)

    # Functionality for adding/updating emission values
    if choice == "Add/Update Values":
        st.title("Add/Update Values")
        year = st.selectbox("Choose Year", list(range(2010, 2050)))
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        st.session_state.selected_sector = sector
        for use_case in footprint_manager.sectors.get(sector, {}):
            footprint_manager.input_value(sector, use_case, year)
    # Functionality for displaying emissions for a chosen sector and year
    elif choice == "Display Emissions":
        st.title("Display Emissions")
        selected_year = st.selectbox("Choose Year", list(range(2010, 2050)))
        total_emissions = footprint_manager.total_emissions_by_year(selected_year)
        st.subheader(f"Total Emissions for {selected_year}: {total_emissions} tCO2eq")
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        footprint_manager.display_values(sector, selected_year)
    # Functionality for plotting the emissions
    elif choice == "Plot Total Emissions":
        st.title("Plot Total Emissions")
        plot_total_emissions(footprint_manager)

if __name__ == "__main__":
    footprint_manager = Footprint()
    initialize_sectors(footprint_manager)
    main_menu(footprint_manager)