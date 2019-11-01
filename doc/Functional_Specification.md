# Design Documents
### Back grounds

Air pollution is an increasing concern across the globe as it has been linked to the development of respiratory illness. Although, government legislation and public awareness campaigns have addressed this health concern, an interactive platform for the public to visualize and predict the relationship between geographic respiratory death rates and air pollution does not exist. We aim to develop such a tool in order to illustrate: 1) how it correlates with geographic respiratory death rates and 2) if we could predict respiratory death rates given prior and current pollution levels. This tool will make it possible for individuals to determine their respiratory illness risk factor given the correlation between air quality and death rate where they live.  

### User profile

We anticipate that public health officials, medical researchers, and  citizens who want to know their risk of living certain places will use this system.

No programming knowledge will be necessary to use our system.  We will have an interactive mapping interface that anyone familiar with a smart phone (for example) would be comfortable interacting with.  It will be clickable with a mouse, but otherwise does not expect any prior technological knowledge of the user.

### Data source

We will have pollution data from the EPA from 2000 - 2017.<br />https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI

We will have death rates due to respiratory illness from the CDC from 2000-2017 as well.  The data is organized as .csv files which have columns of county in the United States, the number of deaths per year, and total population.<br />https://www.nber.org/data/vital-statistics-mortality-data-multiple-cause-of-death.html

### USE CASE
#### __USE CASE 1__
##### Medical researchers<br />
  a. The objective is to test a type of method to reduce the impact of the air pollution. Firstly they would want to find a place to test. The area that has bad air quality and high death correlation coefficient will be the ideal place for them to start the test.  <br />
  b. The researchers,  find desired place on our system by screen the data according to their specification. They go there to test the medical method and monitor the data during the implementation. The data will show if the method takes effect.

#### __USE CASE 2__
##### Any public citizen<br />
  a. The objective is for a user (any public citizen) to choose a geographic county in order to see a graphical representation of the correlation between respiratory death rate and air pollution as well as a predictive measure of respiratory death rate risk given this prior correlation. <br />
  b. The expected interaction between the user (any public citizens) and our system is as follows: <br />1) The user chooses a county by clicking first on the state they are interested in and then on the county within the state on a map programmed by us, <br />2) once a county is chosen, a graph displaying the respiratory death rate, air pollution, and the correlation between the two within that county will appear, <br />3) a risk factor will also appear that corresponds to the prediction of the respiratory death rate for a week given the correlation between air pollution and respiratory death rate, and <br />4) given this risk factor, people can modify their behavior (i.e. wearing a air filter mask) to reduce their risk for respiratory illness.   

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

