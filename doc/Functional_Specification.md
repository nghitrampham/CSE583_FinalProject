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



