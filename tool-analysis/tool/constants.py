from sklearn.linear_model import LinearRegression, TheilSenRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR



EXPERIMENT_DESCRIPTORS = ['dataset', 'model']

DATASET_ESTIMATORS_CAT = ['model_type', 'data_type']
DATASET_ESTIMATORS_NUM = [
    'n_parameters',
    'datapoint_w',
    'datapoint_h',
    'dimensions',
    'num_classes',
    'original_data_size'
]

DATASET_ESTIMATORS = [*DATASET_ESTIMATORS_CAT, *DATASET_ESTIMATORS_NUM]


RUN_DESCRIPTORS = [
    'iteration',
    'data_quality_dimension_percentage',
    'loss',
    'categorical_accuracy',
    'categorical_crossentropy',
    'top_3_accuracy',
    'top_5_accuracy',
    'precision',
    'recall',
    'auc',
    'f1_score',
    'effective_epochs',
    'used_data_size',
    'actual_data_percentage_used',
    'emissions_kg',
    'duration',
]


DATASET_TYPE_NAMES = ['images', 'time_series']
DATASET_NAMES = []
MODEL_NAMES = []

MODEL_TYPES = ['SIMPLE_CNN', 'SIMPLE_MLP', 'RESNET', 'Other']
DATA_TYPES = ['Sensor', 'Spectro', 'Image', 'Device', 'Motion',
              'EOG', 'Traffic', 'ECG', 'Simulated', 'Spectrum', 'Other']


METRICS = ['f1_score', 'auc', 'categorical_accuracy', 'precision', 'recall']
REDUCING_METHODS = ['keep_distributions', 'balance_classes']
linear_regressors = {'linear': LinearRegression, 'theil': TheilSenRegressor}

regressors = {'random_forest': RandomForestRegressor, 'svr': SVR, 'xgboost': GradientBoostingRegressor}

skip_datasets = []  # ['ECG5000', 'ECGFiveDays', 'Coffee', 'CBF']
skip_models = []  # ['MLP']

SPLIT_PERCENTAGE = 0.3


COLS_TO_DROP = ['ready', 'loss', 'categorical_crossentropy', 'top_3_accuracy',
                'top_5_accuracy', 'project_id', 'duration_per_epoch', 'emissions_per_epoch']
DATA_LOCATION = './../tool/backend/static/experiment_results'

RUNS_FILE = 'all.csv'
