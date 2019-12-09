"""
This module is used to predict the Air Quality Index model for 2019 for all counties.
"""
import pickle
import warnings

import pandas as pd
import numpy as np
from keras.models import load_model

import helpers

warnings.filterwarnings("ignore")

def main():

    data2019_raw = pd.read_csv("""air_pollution_death_rate_related/data/air_pollution/
                                data_air_raw/daily_aqi_by_county_2019.csv""")
    data2019 = helpers.data_cleaning(data2019_raw)
    predicted_date = "2019-03-12"

    file = open("temp.csv", "w")
    file.write("date,state_county,AQI\n")

    # for county in list(data2019["state_county"].unique()):
    for county in list(data2019["state_county"].unique())[:5]:

        ## load model to predict AQI
        print("---> Loading model for county {} ...".format(county))

        try:
            scaler_path = ("air_pollution_death_rate_related/trained_model/min_scaler_model/" +
                           county + "_scaler.pickle")

            model_path = ("air_pollution_death_rate_related/trained_model/county_aqi/" +
                          county + "_model.h5")

            model = load_model(model_path)
            mm_scaler = pickle.load(open(scaler_path, "rb"))

            ### feature engineering for model
            data_feature_temp = helpers.data_feature_engineering_for_test(
                                data2019,
                                county,
                                predicted_date)
            x_test, y_test = helpers.load_test_data(data_feature_temp["data"], mm_scaler)

            ## predicting AQI
            predictions = helpers.predict_point_by_point(model, x_test)
            # helpers.plot_results(predictions, y_test)

            ## keep prediction for all counties
            print("Predicting ....")
            y_pred = np.append(x_test, predictions.reshape(1, 1, 1)).reshape(1, 39)
            y_scale = mm_scaler.inverse_transform(y_pred)[-1][-1]

            file.write(predicted_date+","+county+","+str(y_scale)+"\n")

            del data_feature_temp, scaler_path,\
                model_path, model, mm_scaler, x_test, y_test, predictions, y_pred, y_scale

        except Exception as exp:
            print(exp)
            exp.args += ('Path and list_year must not be empty', "check read_raw_data function")

    file.close()

    ## creating dataframe containing county, state, predicted AQI,
    ## predicted date for interactive visualization map
    county_code = pd.read_csv("""air_pollution_death_rate_related/data/air_pollution/
                                data_misc/county_with_code.csv""")
    df_prediction = pd.read_csv("temp.csv")

    df_result = (pd.merge(county_code, df_prediction,
                          how='inner',
                          left_on=["state_county"],
                          right_on=["state_county"])
                )
    df_result.to_csv("predicted_AQI" + predicted_date + ".csv", index=False)

if __name__ == '__main__':
    main()
