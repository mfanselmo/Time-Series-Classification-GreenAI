import pandas as pd
import os

from constants import DATASET_TYPE_NAMES, RESULTS_PATH

cols_to_drop = ['ready', 'loss', 'categorical_crossentropy', 'top_3_accuracy',
                'top_5_accuracy', 'project_id', 'duration_per_epoch', 'emissions_per_epoch']


def load_results(dataset_type: DATASET_TYPE_NAMES) -> pd.DataFrame:
    total_df = pd.DataFrame()
    for _, _, files in os.walk(f"{RESULTS_PATH}/{dataset_type}"):

        for file in files:
            if file.endswith('results.csv'):
                total_df = pd.concat([total_df, pd.read_csv(f"{RESULTS_PATH}/{dataset_type}/{file}")])

    return total_df
