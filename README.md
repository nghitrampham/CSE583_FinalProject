# CSE 583 Final Project 

[![Build Status](https://travis-ci.org/nghitrampham/DEATH_and_POLLUTION.svg?branch=master)](https://travis-ci.org/nghitrampham/DEATH_and_POLLUTION)
[![Coverage Status](https://coveralls.io/repos/github/nghitrampham/DEATH_and_POLLUTION/badge.svg?branch=master)](https://coveralls.io/github/nghitrampham/DEATH_and_POLLUTION?branch=master)

![Alt text](logos/ReadMe.jpg?raw=true "Title")
## Air Pollution vs Respiratory Death Rates
Team: Brandon Pratt, Siting Wang, Marta Wolfshorndl, and Tram Nghi Pham | Course project for CSE 583 | Fall 2019

### Back grounds

Air pollution is an increasing concern across the globe as it has been linked to the development of respiratory illness. Although, government legislation and public awareness campaigns have addressed this health concern, an interactive platform for the public to visualize and predict the relationship between geographic respiratory death rates and air pollution does not exist. We aim to develop such a tool in order to illustrate: 1) how it correlates with geographic respiratory death rates and 2) if we could predict respiratory death rates given prior and current pollution levels. This tool will make it possible for individuals to determine their respiratory illness risk factor given the correlation between air quality and death rate where they live.  

### User profile

We anticipate that public health officials, medical researchers, and  citizens who want to know their risk of living certain places will use this system.

No programming knowledge will be necessary to use our system.  We will have an interactive mapping interface that anyone familiar with a smart phone (for example) would be comfortable interacting with.  It will be clickable with a mouse, but otherwise does not expect any prior technological knowledge of the user.

### Data source

We will have pollution data from the EPA from 2000 - 2017.<br />https://aqs.epa.gov/aqsweb/airdata/download_files.html#AQI

We will have death rates due to respiratory illness from the CDC from 2000-2017 as well.  The data is organized as .csv files which have columns of county in the United States, the number of deaths per year, and total population.<br />https://www.nber.org/data/vital-statistics-mortality-data-multiple-cause-of-death.html


### Interactive map 
For details on how to use Interative map. See Examples. 

### Organization of the project

The project has the following structure:

```
CSE583_FinalProject/
  |- README.md
  |- Death_Air_Pollution/
     |- Data/
        |-Respiratory_Death/
        	|- ...
        |-Air_Pollution/
        	|- ...
     |- Scripts/
        |- Model_AQI/
        	|- ...
        |- Correlation/
        	|- ...
        |- Respiratory_Death/
        	|- ...
     |- Tests/
        |- ...
     |- Trained_AQI_Model/ 
        |- ...
     |- Interactive_App/
     	|- interactive_map.py
     	|- associated_data/
     		|- ...
  |- examples
     |- User_Guide
  |- logos
     |- image.png  
  |- doc/
     |- FunctionalSpec
     |- ComponentSpec
     |- TechnologyReview
     |- Final presentation
  |- setup.py
  |- LICENSE
  |- requirements.txt
  |- environment.yml
```


### Installation

To install AirPollution_Death perform following steps:

* clone the repo: git clone https://github.com/nghitrampham/CSE583_FinalProject.git
* run the setup.py file: python setup.py install
* run requirements.txt to ensure all dependencies exist : pip install -r requirements.txt
* run interactive map: see Examples for user guide
* run train AQI model: open another terminal and go to Scripts/Airpollution/ folder
* run $python main_AQI.py to train model 
* run $python predict_AQI.py to predict (a server may need to run it)

<!-- * go to Scripts folder: cd UWHousing/Scripts
* properly set data path os.environ ["SALES_DATA_PATH"](\UWHousingTeam\data) and 
  os.environ["SALES_DATA_FILE"] ('Merged_Data.csv') follow instructions in the house_price_model_2.py file
* run bokeh server: bokeh serve --port 5001 part1_predict_price.py
* Open another terminal and go to Scripts folder: cd UWHousing/Scripts
* run bokeh server: bokeh serve --port 5002 part2_bid_price.py
* Open another terminal and go to Scripts folder: cd UWHousing/Scripts
* run bokeh server: bokeh serve --port 5003 part3_monthly_cost.py
* go to landing page http://housing-prediction.azurewebsites.net/UWHousingTeam/html_landing_page/
* follow the User_Guide in examples folder  -->






