from fastapi import UploadFile
import numpy as np
import random
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler

from constants import REDUCING_METHODS
from utils.numpy_encoder import NumpyEncoder

class DatasetAnalizer:
    def __init__(self, file: UploadFile):
        self.file = file
        self.x_train = None
        self.y_train = None


    async def load_train_data(self):
        contents = await self.file.read()
        as_array = np.array([i.split() for i in contents.decode('utf-8').split('\n')][:-1], dtype='float')
        self.x_train, self.y_train = np.expand_dims(as_array[:, 1:], axis=-1), as_array[:, 0]
    
    def dataset_metadata(self):
        """
        Gets:
            - (w, h, dimension)
            - num_classes
            - Training size
        """

        classes, classes_counts = np.unique(self.y_train, return_counts=True)
        classes_counts_original = dict(zip(classes, classes_counts))

        train_size, w, dimensions = self.x_train.shape
        h = 1

        return {
            'num_classes': classes.shape[0],
            'classes_counts': NumpyEncoder(classes_counts_original),
            'original_data_size': train_size,
            'datapoint_w': w,
            'datapoint_h': h,
            'dimensions': dimensions,
        }
    

    def dataset_completeness(self):
        return 1 - np.count_nonzero(np.isnan(self.x_train))/np.prod(self.x_train.shape)

    def dataset_consistency(self):
        amount_of_duplicates = np.sum(np.unique(self.x_train, axis=0, return_counts=True)[1] - 1)

        # Assuming the duplicates have different classes
        return 1 - amount_of_duplicates/self.x_train.shape[0]


    def dataset_quality(self):
        """
        Gets:
            - completeness
            - accuracy: NO
            - consistency
        """

        return {
            'completeness': self.dataset_completeness(),
            'consistency': self.dataset_consistency(),
        }

    def clean_dataset(self, dataset_percent, reducing_method: REDUCING_METHODS):

        
        goal_size = int(self.x_train.shape[0]*dataset_percent)

        # In order of most important DQ dimensions

        # Consistency
        current_consistency = self.dataset_consistency()
        if current_consistency < 1:
            left_to_remove = self.x_train.shape[0] - goal_size


            repeats = filter(lambda x: x.shape[0] > 1, pd.DataFrame(self.x_train).groupby([0]).indices.values())
            current_number_take_out = 0
            take_out_indices = []

            for repeat_index in repeats:
                current_number_take_out += repeat_index.shape[0]

                take_out_indices = [*take_out_indices, *repeat_index]

                if current_number_take_out > left_to_remove:
                    break


            self.x_train = np.delete(self.x_train, take_out_indices, axis=0)
            self.y_train = np.delete(self.y_train, take_out_indices, axis=0)


        
        # Completeness
        left_to_remove = self.x_train.shape[0] - goal_size


        nan_mask = np.squeeze(np.any(np.isnan(self.x_train), axis=1))
        number_to_drop_from_nan_mask = np.sum(nan_mask)

        if number_to_drop_from_nan_mask > left_to_remove:
            # If the number of values with nan is greater than how many we need to remove based on goal
            # Turn some of the nan mask to false, to keep some nans
            change_to_false_indices = random.sample(
                np.where(nan_mask == True)[0].tolist(),
                number_to_drop_from_nan_mask - left_to_remove)

            nan_mask[change_to_false_indices] = False

        self.x_train = self.x_train[~nan_mask]
        self.y_train = self.y_train[~nan_mask]


        # Remove till get goal
        if self.x_train.shape[0] > goal_size:

            if reducing_method == 'keep_distributions':
                # randomly remove data
                dropped_percentage = (self.x_train.shape[0] - goal_size)/self.x_train.shape[0]
                drop_mask = np.random.choice(
                    [True, False],
                    self.x_train.shape[0],
                    p=[1 - dropped_percentage, dropped_percentage])


                # Border Case - Ignore
                if not np.any(drop_mask):
                    drop_mask[0] = True

                self.x_train = self.x_train[drop_mask]
                self.y_train = self.y_train[drop_mask]
            elif reducing_method == 'balance_classes':
                total_to_drop = self.x_train.shape[0] - goal_size
                classes, classes_counts = np.unique(self.y_train, return_counts=True)
                classes_counts_original = dict(zip(classes, classes_counts))

                classes_counts = classes_counts_original.copy()

                sampling_strategy = {i: 0 for i in classes}

                while total_to_drop > 0:
                    class_to_drop = max(classes_counts, key=classes_counts.get)
                    sampling_strategy[class_to_drop] += 1
                    classes_counts[class_to_drop] -= 1
                    total_to_drop -= 1

                resulting_strategy = {}
                for class_ in classes_counts_original.keys():
                    resulting_strategy[class_] = classes_counts_original[class_] - sampling_strategy[class_]

                sampler = RandomUnderSampler(sampling_strategy=resulting_strategy)

                rebalanced_x_train, rebalanced_y_train = sampler.fit_resample(np.squeeze(self.x_train), self.y_train)

                permutations = np.random.permutation(rebalanced_x_train.shape[0])
                self.x_train = np.expand_dims(rebalanced_x_train[permutations], -1)
                self.y_train = rebalanced_y_train[permutations]


        full_dataset_train = np.concatenate((np.expand_dims(self.y_train, axis=1), np.squeeze(self.x_train)), axis=1, dtype='str')
        text_dataset = "\n".join([" ".join(i) for i in full_dataset_train])

        return {
            **self.dataset_metadata(),
            **self.dataset_quality(),
            'text_dataset': text_dataset,
        }


