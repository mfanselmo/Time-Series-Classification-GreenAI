from pydantic.typing import Literal


# What defines an experiment: The datasettype, dataset and a model
EXPERIMENT_DESCRIPTORS = ['dataset_type', 'dataset', 'model']


# From what we are going to estimate the performance metric curve (accuracy, precision, f1, etc)
# Is the characteristics of the dataset
DATASET_ESTIMATORS = [
    'model_type', # SimpleCNN, RESNET, ...
    'data_type', # Spectogram, SensorData, ...
    'n_parameters',
    'datapoint_w', 
    'datapoint_h', 
    'dimensions', 
    'num_classes', 
    'original_data_size'
]

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

# class DatasetEstimatorsModel(BaseModel):
#     model_type: str
#     dataset_type: str
#     data_type: str
#     n_parameters: int
#     datapoint_w: int
#     datapoint_h: int
#     dimensions: int
#     num_classes: int
#     original_data_size: int



DATASET_TYPE_NAMES = Literal['images', 'time_series']
DATASET_NAMES = []
MODEL_NAMES = []

MODEL_TYPES = Literal['SIMPLE_CNN', 'SIMPLE_MLP', 'RESNET', 'Other']
DATA_TYPES = Literal['Sensor', 'Spectro', 'Image', 'Device', 'Motion', 'Other']
METRICS = Literal['f1_score', 'auc', 'categorical_accuracy', 'precision', 'recall']
REDUCING_METHODS = Literal['keep_distributions', 'balance_classes']


RESULTS_PATH = './static/experiment_results/'
REGRESSORS_PATH = './static/regressors/'


DETAIL_LEVEL = Literal["0", "1", "2"]
