import matplotlib.pyplot as plt
import os
import csv
from utils.constants import DATASETS

import tensorflow as tf

tfk = tf.keras

# ---------------------------------------------------------------


def create_output(options, data, model, effective_epochs, score, emissions_kg, duration, project_id):
    """
    returns json like object with all info of experiment
    """

    metrics = dict(zip(model.metrics_names, score))
    dataset_type = options['dataset_type']
    original_data_size = DATASETS[dataset_type][options['dataset']]['original_data_size']
    data_type = DATASETS[dataset_type][options['dataset']]['data_type']
    num_classes = DATASETS[dataset_type][options['dataset']]['num_classes']
    sequence_length, dimensions = None, None
    if dataset_type == 'time_series':
        sequence_length, dimensions = DATASETS[dataset_type][options['dataset']]['input_shape']

    used_data_size = data['x_train'].shape[0]

    return {
        **options,
        **metrics,
        'effective_epochs': effective_epochs,
        'used_data_size': used_data_size,
        'actual_data_percentage_used': used_data_size/original_data_size,
        'original_data_size': original_data_size,
        'data_type': data_type,
        'num_classes': num_classes,
        'sequence_length': sequence_length,
        'dimensions': dimensions,
        'emissions_kg': emissions_kg,
        'duration': duration,
        'n_parameters': model.count_params(),
        'project_id': project_id
    }


def plot_history(history):

    plt.plot(history.history['categorical_accuracy'])
    plt.plot(history.history['val_categorical_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()


def save_results(options, result, dataset_type):
    if 'with_random_removal' in options:
        results_csv_path = f"./results/{dataset_type}/{options['experiment']}_new.csv"
    else:
        results_csv_path = f"./results/{dataset_type}/{options['experiment']}_missing_results.csv"
    result['ready'] = True

    file_exists = os.path.exists(results_csv_path)
    if not file_exists:
        with open(results_csv_path, 'a', newline='') as f:
            w = csv.DictWriter(f, result.keys())
            w.writeheader()

    with open(results_csv_path, 'a', newline='') as f:
        w = csv.DictWriter(f, result.keys())
        w.writerow(result)


def format_result(options, result):
    print(f"""
        Model: {options['model']}
        Dataset: {options['dataset']}
        Experiment: {options['experiment']}
        epochs: {result['effective_epochs']}
        duration: {result['duration']}
        result: {result['categorical_accuracy']}
        result_top_3: {result['top_3_accuracy']}
        result_top_5: {result['top_5_accuracy']}
        {result}
        ----------------------
    """)
