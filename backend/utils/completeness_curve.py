import pandas as pd
from sklearn.linear_model import LinearRegression
from constants import METRICS
from db.models import Experiment

def get_experiment_completeness_curve(experiment: Experiment, metric: METRICS):
    regression = LinearRegression()
    X = list(map(lambda x: [x.data_quality_dimension_percentage], experiment.runs))
    y = list(map(lambda x: getattr(x, metric), experiment.runs))
    regression.fit(X, y)

    return {"metric": metric, "coefficient": regression.coef_[0], "intercept": regression.intercept_}

