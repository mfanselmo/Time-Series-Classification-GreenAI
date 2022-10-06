# from constants import DATASET_ESTIMATORS

# def get_query_string(experiment):
#     type_mappings = {
#         'model': 'str', 'dataset': 'str', 'dataset_type': 'str', 'data_type': 'str', 'n_parameters': 'int',
#         'datapoint_w': 'int', 'datapoint_h': 'int', 'dimensions': 'int', 'num_classes': 'int',
#         'original_data_size': 'int', 'model_type': 'str'}
#     list_with_each = []
#     for estimator in DATASET_ESTIMATORS:
#         if type_mappings[estimator] == 'str':
#             list_with_each.append(f"{estimator} == '{getattr(experiment, estimator)}'")
#         else:
#             list_with_each.append(f"{estimator} == {getattr(experiment, estimator)}")

#     return " and ".join(list_with_each)
