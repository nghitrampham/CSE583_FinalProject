# Design Documents - Component Specification
### Software Components

#### Data Manager
Our data is stored on Github, and imported into Python modules. All data needed to be concatenated and was loaded into the python module as a Pandas Dataframe. The data from the EPA is relatively clean.  The data from the CDC needs to be concatenated by year and also contains NaN values. The two datasets can be concatenated by county code, but both columns need to be made to be the same type. All US counties are not represented by the data. The inputs are the raw data files and the outputs are the cleaned, selected, and organized Pandas dataframes.

#### Visualization  Manager
The analyzed and raw time series data is presented in an interactive U.S. map using the Dash and Plotly libraries. Clicking on a U.S. county displays: 1) the correlation between respiratory deaths and air pollution since 2000 (upper right), 2) the predicted air quality index given the prior respiratory deaths and air pollution (text under interactive map), 3) the air quality index (measure of air pollution) since 2000 (lower left), and 4) the percent of respiratory deaths since 2000 (lower right) for that county. The inputs to the visualization is the Pandas dataframe that contains all of the air pollution, death rates, correlations, and air quality index data by year and county, and the output is the interactive map and the line plots.

#### Website manager
We implement the Plotly and Dash python libraries to visualize the U.S. map showing the the correlations of the respiratory death rates and air pollution across counties. 

#### Mathematical model for the correlation between respiratory death rates and air pollution 
The air quality index (AQI) and the respiratory death rates data for each county is first loaded into python as a pandas dataframes and then correlated using the scipy.signal.correlate() function in the scipy python package. The output is a pandas data frame with correlation by county for each year. 

#### Sequential Keras predictive model for predicting the future AQI.
The inputs are Pandas dataframes with the AQI data for the past several months organized by county, and the output is a dataframe with the predictive index for each county for the next day.

### Interactions
#### Use Case 1 
The prospective user is a public health official who is interested in determining if air pollution in the United States is causing deaths due to respiratory illness. Broadly, the interactions are between the user and the interface, the interface and the webpage, the interface and the mathematical and predictive models, the interface and the data manager, and the models and the data manager. Upon initiation, the webpage interacts with the visualization manager, which is pulling data from the mathematical model and the data manager. When the user first sees the webpage, they can read the title and the information at the top which gives some directions about how to use the visualization. Next they can look at the chloropleth map and pan and zoom to states or regions in the US that are of interest to them (have high or low correlations). Then they select a county of interest by clicking on the county. The visualization manager will call the specified data from the data manager and the machine learning model, and display them on the webpage. The user can keep clicking on different counties of interest and the dis play of data will update with each new county, pulled from the data manager and the predictive model.

#### Use Case 2
The interactions for User 2 are similar to those for User 1. In this case, User 2 is a public resident of the United States who wants to find out their respiratory death risk in the county they live in. Again, upon starting, the webpage interacts with the visualization manager, which is pulling data from the mathematical and predictive models. When the user first sees the webpage, they can read the title and the information at the top which gives some directions about how to use the visualization. Next they can look at the chloropleth map and pan and zoom to the state and county they live in. Then they can click on that county and the visualization manager will call the specified data from the data manager and the machine learning model, and display them on the webpage as plots and text.

### Work Plan
Find the data. Clean and organize the data.<br /> 
Try different math modules and find the best module for the data. Store the result.<br /> 
Make line plots of time series of pollutions and death rates.<br /> 
Set up the visualization manager and visualize the data.<br /> 
Set up the webpage and host our visualization.<br /> 
Connect the backend data manager to the front end visualization.<br />
Make the visualization interactive.