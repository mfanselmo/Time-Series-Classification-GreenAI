from typing import List
from typing_extensions import get_args

from joblib import dump, load
from constants import DATA_TYPES, DATASET_ESTIMATORS, DATASET_TYPE_NAMES, METRICS, MODEL_TYPES, REGRESSORS_PATH
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import os
from db.models import Experiment
import numpy as np

class Regressor:
    def __init__(self, dataset_type: DATASET_TYPE_NAMES, metric: METRICS):
        self.dataset_type = dataset_type
        self.metric = metric
        self.model_path = f"{REGRESSORS_PATH}/{self.dataset_type}_{self.metric}.joblib"
        self.encoder_path = f"{REGRESSORS_PATH}/{self.dataset_type}_{self.metric}_encoder.joblib"
        self.regressor = None
        self.encoder = None

        self.load_model()

    def save_model(self):
        dump(self.regressor, self.model_path)
        dump(self.encoder, self.encoder_path)

    def load_model(self):

        if os.path.exists(self.model_path):
            self.regressor = load(self.model_path)
            self.encoder = load(self.encoder_path)



    def fit(self, experiments: List[Experiment]):
        self.regressor = RandomForestRegressor()
        X, y = self.preprocess_data(experiments)

        self.regressor.fit(X, y)
        self.save_model()

    def predict(
        self, 
        model_type: MODEL_TYPES, 
        data_type: DATA_TYPES, 
        n_parameters: int, 
        datapoint_w: int, 
        datapoint_h: int, 
        dimensions: int, 
        num_classes: int, 
        original_data_size: int
    ):
        X_cat = self.encoder.transform([[model_type, data_type]]).toarray()
        X_num = [[n_parameters, datapoint_w, datapoint_h, dimensions, num_classes, original_data_size]]

        return self.regressor.predict(np.concatenate([X_cat, X_num], axis=1))[0]

    def preprocess_data(self, experiments: List[Experiment]):
        X_cat = []
        X_num = []
        y = []
        for experiment in experiments:
            x_cat = []
            x_num = []
            for estimator in DATASET_ESTIMATORS:
                if estimator in ['model_type', 'data_type']:
                    x_cat.append(getattr(experiment, estimator))
                else:
                    x_num.append(getattr(experiment, estimator))


            metric_coefficient = next(
                (x for x in experiment.completeness_curves if x.metric == self.metric)).coefficient
            y.append(metric_coefficient)
            X_cat.append(x_cat)
            X_num.append(x_num)

        self.encoder = OneHotEncoder(handle_unknown='error', categories=[get_args(MODEL_TYPES), get_args(DATA_TYPES)])
        self.encoder.fit(X_cat)
        X_cat = self.encoder.transform(X_cat).toarray()

        return np.concatenate([X_cat, X_num], axis=1), y
