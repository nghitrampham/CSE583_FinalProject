import warnings

from ..Scripts.Air_Pollution import main_aqi

warnings.filterwarnings('ignore')

ROOT = r"""air_pollution_death_rate_related/data/air_pollution/
        county_features_data/county_features_train/florida_bay_feature.csv"""

def test_load_data():

    [x_train, y_train, x_test, y_test], _ = main_aqi.load_data(ROOT)

    assert x_train.shape == (821, 1, 38)
    assert y_train.shape == (821,)
    assert x_test.shape == (205, 1, 38)
    assert y_test.shape == (205,)
