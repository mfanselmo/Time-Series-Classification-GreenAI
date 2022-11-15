import numpy as np
from imblearn.under_sampling import RandomUnderSampler

from utils.constants import DATASETS

import tensorflow as tf

tfk = tf.keras

# ---------------------------------------------------------------

def load_dataset(options):
    dataset_type = options['dataset_type']
    dataset_info = DATASETS[dataset_type][options['dataset']]

    if dataset_type == 'time_series':
        train_data = np.loadtxt(f"./datasets/time_series/{dataset_info['name']}/{dataset_info['train_file']}")
        test_data = np.loadtxt(f"./datasets/time_series/{dataset_info['name']}/{dataset_info['test_file']}")

        return np.expand_dims(train_data[:, 1:],axis=-1), train_data[:, 0], np.expand_dims(test_data[:, 1:], axis=-1), test_data[:, 0] - extra
    else:
        (x_train, y_train), (x_test, y_test) = dataset_info['data']()
        (x_train, y_train), (x_test, y_test) = (x_train.copy(), y_train.copy()), (x_test.copy(), y_test.copy())

        return x_train, y_train, x_test, y_test


## DROPPING DATA: DROPS DATA
def reduce_data_volume(x_train, y_train, options):
    completeness_percentage = options['data_quality_dimension_percentage']
    method = options['experiment_method']

    dropped_percentage = 1 - completeness_percentage

    if method == 'uniform':
        drop_mask = np.random.choice([True, False], x_train.shape[0], p=[1 - dropped_percentage, dropped_percentage])
        return x_train[drop_mask], y_train[drop_mask]

    n_original = x_train.shape[0]
    total_to_drop = int(n_original*dropped_percentage)
    classes, classes_counts = np.unique(y_train, return_counts=True)
    classes_counts_original = dict(zip(classes, classes_counts))

    classes_counts = classes_counts_original.copy()

    sampling_strategy = {i: 0 for i in classes}
    class_to_drop = max(classes_counts_original, key=classes_counts_original.get)

    sampling_strategy[class_to_drop] += total_to_drop
    classes_counts[class_to_drop] -= total_to_drop

    resulting_strategy = {}
    for class_ in classes_counts_original.keys():
        resulting_strategy[class_] = classes_counts_original[class_] - sampling_strategy[class_]

    sampler = RandomUnderSampler(sampling_strategy=resulting_strategy)

    rebalanced_x_train, rebalanced_y_train = sampler.fit_resample(np.squeeze(x_train), y_train)

    permutations = np.random.permutation(rebalanced_x_train.shape[0])
    return np.expand_dims(rebalanced_x_train[permutations], -1), rebalanced_y_train[permutations]


## ACCURACY: CHANGES LABELS
def reduce_accuracy(x_train, y_train, options):

    accuracy_percentage = options['data_quality_dimension_percentage']
    method = options['experiment_method']
    corrupted_percentage = 1 - accuracy_percentage
    total_amount = x_train.shape[0]
    class_list = set(np.unique(y_train))

    if method == 'uniform':
        for i in range(total_amount):
            if np.random.random() < corrupted_percentage:
                y_value = y_train[i]
                new_y_value = np.random.choice(list(class_list.difference({y_value})))
                y_train[i] = new_y_value

        return x_train, y_train

    classes, classes_counts = np.unique(y_train, return_counts=True)
    classes_counts_original = dict(zip(classes, classes_counts))
    class_to_corrupt = max(classes_counts_original, key=classes_counts_original.get)
    class_percentage = classes_counts_original[class_to_corrupt]/total_amount
    other_classes = list(class_list.difference({class_to_corrupt}))

    class_percentage_to_corrupt = corrupted_percentage/class_percentage
    for i in range(total_amount):
        y_value = y_train[i]
        if y_value == class_to_corrupt and np.random.random() < class_percentage_to_corrupt:

            new_y_value = np.random.choice(other_classes)
            y_train[i] = new_y_value

    return x_train, y_train


## COMPLETENESS: Deletes inner points
def reduce_completeness(x_train, y_train, options):
    accuracy_percentage = options['data_quality_dimension_percentage']
    method = options['experiment_method']
    inner_missing_percentage = 0.4

    number_of_sequences, length_of_sequence, dimensions = x_train.shape
    number_of_missing_points_per_sequence = int(inner_missing_percentage*length_of_sequence)

    total_amount = x_train.shape[0]

    if method == 'uniform':
        while True:
            affected_percentage = (1 - accuracy_percentage)/inner_missing_percentage
            if affected_percentage <= 1:
                break

            inner_missing_percentage *= 1.02
        for i in range(total_amount):
            if np.random.random() < affected_percentage:
                start = np.random.randint(0, length_of_sequence-number_of_missing_points_per_sequence)
                x_train[i][start: start + number_of_missing_points_per_sequence] = np.mean(x_train[i])

        return x_train, y_train

    class_list = set(np.unique(y_train))
    classes, classes_counts = np.unique(y_train, return_counts=True)
    classes_counts_original = dict(zip(classes, classes_counts))
    class_to_corrupt = max(classes_counts_original, key=classes_counts_original.get)
    class_percentage = classes_counts_original[class_to_corrupt]/total_amount
    affected_class_percentage = min(1, (1 - accuracy_percentage)/(inner_missing_percentage*class_percentage))
    while True:
        actual_accuracy_percentage = 1 - inner_missing_percentage*class_percentage*affected_class_percentage

        if actual_accuracy_percentage <= accuracy_percentage:
            break

        inner_missing_percentage *= 1.02
        affected_class_percentage = min(1, (1 - accuracy_percentage)/(inner_missing_percentage*class_percentage))

    number_of_missing_points_per_sequence = int(inner_missing_percentage*length_of_sequence)
    for i in range(total_amount):
        y_value = y_train[i]
        if y_value == class_to_corrupt and np.random.random() < affected_class_percentage:
            start = np.random.randint(0, length_of_sequence-number_of_missing_points_per_sequence)
            x_train[i][start: start + number_of_missing_points_per_sequence] = np.mean(x_train[i])

    return x_train, y_train



## CONSISTENCY: DUPLICATES AND CHANGES LABELS
def reduce_consistency(x_train, y_train, options):
    
    consistency_percentage = options['data_quality_dimension_percentage']
    method = options['experiment_method']
    class_list = set(np.unique(y_train))
    original_total = x_train.shape[0]
    n_to_add = int((original_total - consistency_percentage*original_total)/consistency_percentage)
    if method == 'uniform':
        indices = np.arange(0, original_total)
    else:
        classes, classes_counts = np.unique(y_train, return_counts=True)
        classes_counts_original = dict(zip(classes, classes_counts))
        class_to_corrupt = max(classes_counts_original, key=classes_counts_original.get)
        indices = np.squeeze(np.argwhere(y_train == class_to_corrupt))

        
    inconsistent_indices = np.random.choice(indices, n_to_add)
    x_train_duplicates, y_train_duplicates = x_train[inconsistent_indices].copy(), y_train[inconsistent_indices].copy()

    for i in range(x_train_duplicates.shape[0]):
        y_value = y_train_duplicates[i]
        new_y_value = np.random.choice(list(class_list.difference({y_value})))
        y_train_duplicates[i] = new_y_value


    new_x_train, new_y_train = np.concatenate(
        (x_train, x_train_duplicates)), np.concatenate(
        (y_train, y_train_duplicates))
    permutations = np.random.permutation(new_x_train.shape[0])
    

    return new_x_train[permutations], new_y_train[permutations]


def create_data(options):
    if options['dataset'] == None:
        raise Exception('none dataset_name')
    elif options['dataset_type'] == None:
        raise Exception('None dataset_type')

    dataset_info = DATASETS[options['dataset_type']][options['dataset']]

    x_train, y_train, x_test, y_test = load_dataset(options)

    if options['experiment'] == 'e00':
        pass
    elif options['experiment'] in ["e11", "e12"]:
        x_train, y_train = reduce_data_volume(x_train, y_train, options)
    elif options['experiment'] in ["e21", "e22"]:
        x_train, y_train = reduce_accuracy(x_train, y_train, options)
    elif options['experiment'] in ["e23", "e24"]:
        x_train, y_train = reduce_completeness(x_train, y_train, options)
    elif options['experiment'] in ["e31", "e32"]:
        x_train, y_train = reduce_consistency(x_train, y_train, options)
    else:
        raise Exception("DANGER: NO experiment")

    if 'with_random_removal' in options:
        x_train, y_train = reduce_data_volume(x_train, y_train, options)
    
    # convert class vectors to binary class matrices
    y_train = tfk.utils.to_categorical(y_train, dataset_info['num_classes'])
    y_test = tfk.utils.to_categorical(y_test, dataset_info['num_classes'])

    return {
        "x_train": x_train,
        "x_test": x_test,
        "y_train": y_train,
        "y_test": y_test
    }
