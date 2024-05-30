**Carbon Footprint Tracker**
This Python script using Streamlit creates a web application to track and visualize your carbon footprint. 
**Features:**
- Define sectors and use cases for your carbon footprint (e.g., Energy, Transportation).
- Set benchmark emission values for each use case.
- Enter your emission values for each use case within a chosen sector and year.
- View your total emissions for a specific sector and year, along with comparisons to benchmarks.
- Visualize your total emissions trend over time.
**Running the application:**

1. Ensure you have Python 3 and the required libraries (`streamlit`, `numpy`, `matplotlib`) installed.
pip install streamlit numpy matplotlib
2. Run the script from your terminal.
3. This will open a web browser window where you can interact with the Carbon Footprint Tracker application.
**Using the application:**
The application provides a sidebar menu with three options:
1. **Add/Update Values:** Enter your emission values for specific use cases within a chosen sector and year.
2. **Display Emissions:** Select a year and view your total emissions for a chosen sector, along with comparisons to benchmark values for each use case.
3. **Plot Total Emissions:** View a graph showing your total emissions trend over the years (2010-2049).
**Code Structure:**
The code is organized into several functions:
1. `Footprint`: This class manages the carbon footprint data, including sectors, use cases, benchmark values, and user-entered emission values.
2. Helper functions: These functions handle tasks like initializing sectors and benchmarks, plotting the forest visualization, and calculating total emissions by year.
3. `main_menu`: This function creates the Streamlit user interface and handles user interactions based on their selections.
**Additional Notes:**
Benchmark emission values used in the code are based on secondary research but can be modified within the code.
The forest visualization is a basic representation to indicate the number of trees needed to offset emissions. It doesn't account for specific tree species or their carbon sequestration capacity.
**Disclaimer:**
This code was partially created with the help of AI especially for purposes of troubleshooting.
This application is not intended to be a comprehensive carbon footprint calculator and may not capture all aspects of a company's carbon footprint.
