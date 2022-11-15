import os, json, itertools

def generate_combinations(all_options):
    if any([i is None for i in all_options.values()]):
        raise Exception('DANGER: None options')

    combinations = list(itertools.product(*all_options.values()))
    return [dict(zip(all_options.keys(), a)) for a in combinations]

def add_accuracy(combinations):
    for combination in combinations:
        combination['data_quality_dimension_percentage'] = 1 - combination['affected_percentage']*combination['inner_missing_percentage']

    return combinations


def save_into_json(combinations, path):
    if not os.path.exists(path):
        json_object = json.dumps(combinations, indent=4)

        with open(path, "w") as outfile:
            outfile.write(json_object)
        return


time_series_datasets = ["ChlorineConcentration", "PhalangesOutlinesCorrect", "StarLightCurves"]
models = ['FCN', 'RESNET', 'MLP']
percentages_base = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
percentages_1_class = [0.9, 0.8, 0.7, 0.6]

BASE_OPTIONS = {
    'model': models,
    'dataset': time_series_datasets,
    'dataset_type': ['time_series'],
    'experiment': None,
    'iteration': [0],
    'with_random_removal': [True, False],
}

# BASELINE
# E00: Baseline
e00_options_for_saving = BASE_OPTIONS.copy()
e00_options_for_saving['experiment'] = ['e00']


# Droppping data
# Experiment 11: dropping uniform
e11_options_for_saving = BASE_OPTIONS.copy()
e11_options_for_saving['experiment'] = ['e11']
e11_options_for_saving['experiment_method'] = ['uniform']
e11_options_for_saving['data_quality_dimension'] = ['none-droping']
e11_options_for_saving['data_quality_dimension_percentage'] = percentages_base

# Experiment 12: Dropping 1 class
e12_options_for_saving = BASE_OPTIONS.copy()
e12_options_for_saving['experiment'] = ['e12']
e12_options_for_saving['experiment_method'] = ['1_class']
e12_options_for_saving['data_quality_dimension'] = ['none-droping']
e12_options_for_saving['data_quality_dimension_percentage'] = percentages_1_class


# ACCURACY
# Experiment 21: change labels uniform
e21_options_for_saving = BASE_OPTIONS.copy()
e21_options_for_saving['experiment'] = ['e21']
e21_options_for_saving['experiment_method'] = ['uniform']
e21_options_for_saving['data_quality_dimension'] = ['accuracy']
e21_options_for_saving['data_quality_dimension_percentage'] = percentages_base

# ACCURACY
# Experiment 22: change labels 1 class
e22_options_for_saving = BASE_OPTIONS.copy()
e22_options_for_saving['experiment'] = ['e22']
e22_options_for_saving['experiment_method'] = ['1_class']
e22_options_for_saving['data_quality_dimension'] = ['accuracy']
e22_options_for_saving['data_quality_dimension_percentage'] = percentages_1_class


# completeness
# Experiment 31: inner change uniform
e31_options_for_saving = BASE_OPTIONS.copy()
e31_options_for_saving['experiment'] = ['e31']
e31_options_for_saving['experiment_method'] = ['uniform']
e31_options_for_saving['data_quality_dimension'] = ['completeness']
e31_options_for_saving['data_quality_dimension_percentage'] = percentages_base


# ACCURACY
# Experiment 32: inner_change 1 class
e32_options_for_saving = BASE_OPTIONS.copy()
e32_options_for_saving['experiment'] = ['e32']
e32_options_for_saving['experiment_method'] = ['1_class']
e32_options_for_saving['data_quality_dimension'] = ['completeness']
e32_options_for_saving['data_quality_dimension_percentage'] = percentages_1_class



# CONSISTENCY
# Experiment 41: completeness uniform
e41_options_for_saving = BASE_OPTIONS.copy()
e41_options_for_saving['experiment'] = ['e41']
e41_options_for_saving['experiment_method'] = ['uniform']
e41_options_for_saving['data_quality_dimension'] = ['consistency']
e41_options_for_saving['data_quality_dimension_percentage'] = percentages_base

# CONSISTENCY
# Experiment 42: completeness 1 class
e42_options_for_saving = BASE_OPTIONS.copy()
e42_options_for_saving['experiment'] = ['e42']
e42_options_for_saving['experiment_method'] = ['1_class']
e42_options_for_saving['data_quality_dimension'] = ['consistency']
e42_options_for_saving['data_quality_dimension_percentage'] = percentages_1_class



e00_combinations = generate_combinations(e00_options_for_saving)
e11_combinations = generate_combinations(e11_options_for_saving)
e12_combinations = generate_combinations(e12_options_for_saving)
e21_combinations = generate_combinations(e21_options_for_saving)
e22_combinations = generate_combinations(e22_options_for_saving)
e31_combinations = generate_combinations(e31_options_for_saving)
e32_combinations = generate_combinations(e32_options_for_saving)
e41_combinations = generate_combinations(e41_options_for_saving)
e42_combinations = generate_combinations(e42_options_for_saving)


save_into_json(e00_combinations, './settings/time_series/e00_options.json')
save_into_json(e11_combinations, './settings/time_series/e11_options.json')
save_into_json(e12_combinations, './settings/time_series/e12_options.json')
save_into_json(e21_combinations, './settings/time_series/e21_options.json')
save_into_json(e22_combinations, './settings/time_series/e22_options.json')
save_into_json(e31_combinations, './settings/time_series/e31_options.json')
save_into_json(e32_combinations, './settings/time_series/e32_options.json')
save_into_json(e41_combinations, './settings/time_series/e41_options.json')
save_into_json(e42_combinations, './settings/time_series/e42_options.json')
