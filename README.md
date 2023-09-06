# formula1-map-dash

## Overview
- This app is a demo designed for fans of the FIA Formula One World Championship (F1).
- The app not only allows users to visually explore race locations and circuit layouts, but also provides the schedule for each Grand Prix session. Users can engage in strategy simulations themselves and view both race results and winning predictions made by the app.
- The app is accessible at https://formula1-map-dash-74a62ff12fb4.herokuapp.com/.
- Please note that the above URL may become invalid without prior notice.

## Circuit geo data source and license
- The geodata located in the `.data/` directory has been borrowed from the [bacinger](https://github.com/bacinger/f1-circuits/tree/master/circuits). I would like to express my gratitude to the contributors.
- The original code from which the geodata was borrowed is under the [MIT License](https://github.com/bacinger/f1-circuits/blob/master/LICENSE.md)

## Circuit Information Collection
- The script `scripts/make_data_for_strategy_simulator.py` is responsible for gathering and analyzing information related to various F1 circuits.
- This script estimates the rate of tire degradation and race pace for each circuit through the following steps:
    - Retrieves information about the most recent dry-weather race at the target circuit, utilizing the ChatGPT API to read Wikipedia pages on past races.
    - Determines the pace of the winning driver by averaging their lap times. Subsequently, a simple linear regression is conducted to ascertain the rate of lap time degradation.
- The resulting data is saved in a designated directory, and the application utilizes this information to simulate race strategies.

## Prediction Model Pipeline
- An AWS Lambda function is set up to prepare feature variables for the predictive model. This process takes place every Monday, and the results are stored in an S3 bucket (with the prefix `features/features_{}``).
- The script `predictor.py` loads a pre-trained LightGBM model from an S3 bucket. The model is initially trained in the Jupyter Notebook `notebooks/create_model.ipynb`.
- `predictor.py` also imports the feature variables generated by the Lambda function as described above.
- Utilizing the loaded model and feature set, `predictor.py` predicts outcomes for future Grand Prix races.

## Deployment
- The `master` branch is designated for deployment on Heroku.
- The app is accessible at https://formula1-map-dash-74a62ff12fb4.herokuapp.com/.
- Please note that the above URL may become invalid without prior notice.