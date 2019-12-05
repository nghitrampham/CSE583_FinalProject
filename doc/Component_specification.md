### Component Specification
#### Data Manager
Our data will be stored in Google Drive, and we will import it into Python Jupyter notebooks.  The data from the EPA is relatively clean and will be stored as a Pandas dataframe.  The data from the CDC needs to be concatenated by year.
#### Visualization  Manager
It helps to visualize the data. The data will be presented in an interactive map. There are two inputs: 1) is the correlation between air pollution and the death rate by county. You can click the territory and the result will show up. The general result will also be presented by line graph. 2) is the predictive air quality index for the next seven days in the location specified.
#### Website manager
we are going to implement the visualized map showing the U.S. states and counties and the associated correlations of the respiratory death rates and air pollution at that geographic location. We plan to host the map on github. 

Mathematical model for the correlation between respiratory death rates and air pollution: The data of the air quality index (AQI) and the respiratory death rates will be loaded into python as a pandas dataframes. Then the two datasets will be filtered and grouped by county. The respiratory death rates and air pollution data grouped by country will be correlated in time (over the prior 15 years) using the scipy.signal.correlate() function in the scipy python package<br /> (see:https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html)

### Interactions
Overall, the interactions are between the user and the interface, the interface and the webpage, the interface and the mathematical model, the interface and the data manager, and the model and the data manager.
#### Use Case as a medical researcher
The user loads our webpage and our visualization manager starts to retrieve the data from the data manager and presents the data. The result of the rank of pollution severity will be present both in the form of numbers and a heat map. The user clicks the area of interest, the map will zoom in to the state level, and the user can click the county they’re interested in. The interface interacts with the data manager  and the mathematical model, and the plots of the pollution time series for the county will show up, as well as the correlation between pollution and death rate for that county.

### Preliminary plan. A list of tasks in priority order.
Find the data. Clean and organize the data.<br /> 
Try different math module and find the best module for the data.Store the result.<br /> 
Make line plots of time series of pollutions and death rates.<br /> 
Set up the visualization manager and visualize the data.<br /> 
Set up the webpage and host our visualization.<br /> 
Make the visualization interactive.