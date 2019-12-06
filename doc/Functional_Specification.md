# Design Documents - Functional Specification
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
##### Public Health Researchers<br />
  a. Public health researchers interested in the effects of air pollution on illness and death in the United States could use our interface to find areas that are especially problematic (have a high correlation between air pollution and respiratory death rates) or are the opposite (have a low correlation between air pollution and respiratory death rates). Researchers would also be interested in the time series plots that show the correlation, the air pollution data, and the respiratory death rates in that location over time. The researcher's objective could be to test a methods to reduce the impact of the air pollution, and they could use this visualization to find a place to test. The areas that have bad air quality and high death correlation coefficients will be the ideal places for them to start the test.  <br />
  b. The researchers will scan the chloropleth map for areas of interest, and pan and zoom in on counties that are of interest to them. They can click on counties of interest and examine the line plots of historical data in those regions. Then if they go there to test the intervention method and monitor the data during the implementation, once the data is updated, the visualization will show if the method takes effect.

#### __USE CASE 2__
##### Any public citizen<br />
  a. The objective is for a user (any public citizen) to choose a geographic county in order to see a representation of the correlation between respiratory death rate and air pollution as well as a predictive measure of respiratory death rate risk given this prior correlation. <br />
  b. The expected interaction between the user (any public citizens) and our system is as follows: <br />1) The user chooses a county by clicking first on the state they are interested in and then on the county within the state on a map programmed by us, <br />2) once a county is chosen, a graph displaying the respiratory death rate, air pollution, and the correlation between the two within that county will appear, <br />3) a risk factor will also appear that corresponds to the prediction of the respiratory death rate for a week given the correlation between air pollution and respiratory death rate, and <br />4) given this risk factor, people can modify their behavior (i.e. wearing an air filter mask) to reduce their risk for respiratory illness.   



