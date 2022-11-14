import pandas as pd
import os
import numpy as np
from tool.constants import DATA_LOCATION, COLS_TO_DROP, RUNS_FILE, EXPERIMENT_DESCRIPTORS, DATASET_ESTIMATORS, METRICS, MODEL_TYPES, DATA_TYPES
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error


def show_percentage(number):
    return str(100*number)[:4] + "%"

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


def load_runs(dataset_type):
    """
        Takes all runs from results folders and loads it for analysis
        Return dataframe with runs
    """
    total_df = pd.DataFrame()
    for _, _, files in os.walk(f"{DATA_LOCATION}/{dataset_type}/filtered"):
        for file in files:
            if file.endswith(RUNS_FILE):
                total_df = pd.concat([total_df, pd.read_csv(f"{DATA_LOCATION}/{dataset_type}/filtered/{file}")])

    return total_df


def get_unique_experiments(runs_df):
    """
        given the runs, returns an array of dataset-model pairs
    """
    return list(runs_df[['dataset', 'model']].drop_duplicates().to_records(index=False))


def get_unique_datasets(runs_df):
    return runs_df['dataset'].unique()


def get_reduction_curve(runs_df, metric, linear_regressor):
    assert runs_df['model'].unique().shape[0] == 1
    assert runs_df['dataset'].unique().shape[0] == 1

    X = np.log(runs_df[['data_quality_dimension_percentage']])
    y = runs_df[metric]

    reg = linear_regressor()
    reg.fit(X, y)

    return {
        "slope": reg.coef_[0],
        "intercept": reg.intercept_
    }


def get_single_experiment_runs(runs_df, model, dataset):
    return runs_df.query(f"model == '{model}' and dataset == '{dataset}'")


def get_train_test_datasets(dataset_list, percentage):
    test_datasets = list(np.random.choice(dataset_list, int(percentage*len(dataset_list))))
    train_datasets = list(set(dataset_list) - set(test_datasets))

    return train_datasets, test_datasets


def split_runs_df(runs_df, percentage):

    dataset_list = get_unique_datasets(runs_df)

    datasets_train, datasets_test = get_train_test_datasets(dataset_list, percentage)
    train_runs_df = runs_df.query(f"dataset in {datasets_train}")
    test_runs_df = runs_df.query(f"dataset in {datasets_test}")

    return train_runs_df, test_runs_df


def load_experiments_df(runs_df, linear_regressor, metrics=None):
    unique_experiments = get_unique_experiments(runs_df)
    result = []
    for dataset, model in unique_experiments:
        experiment_runs_df = get_single_experiment_runs(runs_df, model, dataset)
        base_data = {
            attribute: experiment_runs_df[attribute].unique()[0]
            for attribute in EXPERIMENT_DESCRIPTORS + DATASET_ESTIMATORS}
        for metric in metrics or METRICS:
            curve_data = get_reduction_curve(experiment_runs_df, metric, linear_regressor)
            result.append({**base_data, 'metric': metric, **curve_data})

    return pd.DataFrame(result)


def train_regressor_model(experiments_df, metric, regressor, cat_estimators, num_estimators):
    estimating_column = 'slope'
    experiments_df = experiments_df.query(f"metric == '{metric}'")

    X_data_cat = None
    X_data_num = None
    encoder = None
    if len(cat_estimators):
        X_data_cat = experiments_df[cat_estimators]
        categories = []
        if 'model_type' in cat_estimators:
            categories.append(MODEL_TYPES)
        if 'data_type' in cat_estimators:
            categories.append(DATA_TYPES)

        encoder = OneHotEncoder(handle_unknown='error', categories=categories)
        encoder.fit(X_data_cat)
        X_data_cat = encoder.transform(X_data_cat).toarray()

    if len(num_estimators):
        X_data_num = experiments_df[num_estimators]

    X_data = None
    if X_data_cat is not None:
        X_data = X_data_cat
    if X_data_num is not None:
        if X_data is not None:
            X_data = np.concatenate([X_data, X_data_num], axis=1)
        else:
            X_data = X_data_num

    y_data = experiments_df[estimating_column]

    regressor = regressor()
    regressor.fit(X_data, y_data)

    return regressor, encoder


def evaluate_test_experiment_df(test_experiments_df, metric, encoder, regressor, cat_estimators, num_estimators):
    estimating_column = 'slope'
    test_experiments_df = test_experiments_df.query(f"metric == '{metric}'")

    X_test_cat = None
    X_test_num = None
    if len(cat_estimators):
        X_test_cat = test_experiments_df[cat_estimators]
        X_test_cat = encoder.transform(X_test_cat).toarray()

    if len(num_estimators):
        X_test_num = test_experiments_df[num_estimators]

    X_test = None
    if X_test_cat is not None:
        X_test = X_test_cat
    if X_test_num is not None:
        if X_test is not None:
            X_test = np.concatenate([X_test, X_test_num], axis=1)
        else:
            X_test = X_test_num

    y_true = test_experiments_df[estimating_column]
    y_pred = regressor.predict(X_test)

    return mean_squared_error(y_true, y_pred)
