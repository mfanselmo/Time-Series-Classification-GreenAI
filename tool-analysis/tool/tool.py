import numpy as np
import math
from tool.utils import train_regressor_model, show_percentage
from tool.constants import DATASET_ESTIMATORS_CAT, DATASET_ESTIMATORS_NUM

def simulate_tool_usage(
        full_runs_df, train_experiment_curves_df, user_experiment, regressor,
        phase_one_hyperparameter_search_iterations=100, verbose=False, base_metric_result_percentage=0.5, performance_goal_increase=0.1):
    """
        Performs the whole pipeline the user would perform.
        - User inputs an experiment, a goal metric and a baseline 
        - Tool is trained with the whole dataset except user inputed one
    """
    metric = user_experiment['metric']

    phase_2_hyperparameter_search_iterations = 25
    

    """
        First we need to get the runs of the user experiment
        This is real data
    """
    user_experiment_runs_df = full_runs_df.query(
        f"dataset=='{user_experiment['dataset']}' and model=='{user_experiment['model']}'")
    base_user_experiment_runs_df = user_experiment_runs_df.query(
        f"data_quality_dimension_percentage == {base_metric_result_percentage}")  # Experiments done with 0.4
    # Experiments done with 100% of data, for comparison on classic method
    full_user_experiment_runs_df = user_experiment_runs_df.query(f"data_quality_dimension_percentage == {1.0}")

    base_experiment_metric_result = base_user_experiment_runs_df[metric].mean()
    full_experiment_metric_result = full_user_experiment_runs_df[metric].mean()
    base_experiment_kg_emissions = base_user_experiment_runs_df['emissions_kg'].mean()
    full_experiment_kg_emissions = full_user_experiment_runs_df['emissions_kg'].mean()

    goal_metric = base_experiment_metric_result + performance_goal_increase

    if goal_metric > full_experiment_metric_result:
        goal_metric = full_experiment_metric_result

    """
        This is the tool model, trained with the data of chosen metric (not including user experiment)
    """
    reg, enc = train_regressor_model(train_experiment_curves_df, metric, regressor,
                                     DATASET_ESTIMATORS_CAT, DATASET_ESTIMATORS_NUM)

    """
        Simulation part where the tool predicts the percentage of the dataset to be used to reach goal
    """

    # To input the data into the regressor, we need to encode it correctly with the same trained encoder
    X_test_cat = user_experiment[DATASET_ESTIMATORS_CAT].to_frame().T
    X_test_num = [user_experiment[DATASET_ESTIMATORS_NUM]]

    X_test_cat = enc.transform(X_test_cat).toarray()
    X_test = np.concatenate([X_test_cat, X_test_num], axis=1)

    # Predict coefficient using the regressor
    metric_coefficient = reg.predict(X_test)[0]

    # Now we use basic linear equation formulas to get the intercept of the curve with user input, then the % of the dataset needed
#     intercept = base_experiment_metric_result - metric_coefficient*base_metric_result_percentage
#     dataset_percent = (goal_metric - intercept)/metric_coefficient

    intercept = base_experiment_metric_result - metric_coefficient*math.log(base_metric_result_percentage)
    dataset_percent = math.exp((goal_metric - intercept)/metric_coefficient)

    """
        Now that we have the dataset percent out tool suggested, we can get the actual runs with that percentage
    """
    rounded_dataset_percent = min(round(dataset_percent, 1), 1)

    
    tool_suggested_runs = user_experiment_runs_df.query(
        f"data_quality_dimension_percentage == {rounded_dataset_percent}")
    tool_suggested_experiment_metric_result = tool_suggested_runs[metric].mean()
    tool_suggested_experiment_kg_emissions = tool_suggested_runs['emissions_kg'].mean()


    classic_method_emissions = phase_one_hyperparameter_search_iterations*full_experiment_kg_emissions
    our_method_emissions = phase_one_hyperparameter_search_iterations*base_experiment_kg_emissions + \
        phase_2_hyperparameter_search_iterations*tool_suggested_experiment_kg_emissions

    emissions_percentage_change = (our_method_emissions - classic_method_emissions)/classic_method_emissions

    if verbose:
        print(
            f"""
                On dataset {user_experiment['dataset']} model {user_experiment['model']} metric {user_experiment['metric']}
                    ----- User goals ------

                    User goal: {show_percentage(goal_metric)}
                    User Inputs: {show_percentage(base_experiment_metric_result)} on {show_percentage(base_metric_result_percentage)} of the data

                    ----- Prediction -----

                    Our model predicted to use {show_percentage(rounded_dataset_percent)} of dataset

                    ------ Results ----
                    With that amount of data, we got {show_percentage(tool_suggested_experiment_metric_result)}

                    ----- Emissions saved -----

                    Emissions (kg) saved: {classic_method_emissions - our_method_emissions} (negative value is bad)
                    Emissions percentage change: {show_percentage(emissions_percentage_change)} (Negative is a decrease, good)

                    ------ Errors -----
                    Error on goal: {show_percentage(goal_metric - tool_suggested_experiment_metric_result)} (values < 1% are good (and negative better))


                    ------ Extra errors ----
                    Error on classic method (100% of data): {show_percentage(full_experiment_metric_result - tool_suggested_experiment_metric_result)} (smaller is better) 
                \n\n\n
            """)

    return {
        # Experiment data
        'model': user_experiment['model'],
        'dataset': user_experiment['dataset'],
        'metric': user_experiment['metric'],
        'phase_one_hyperparameter_search_iterations': phase_one_hyperparameter_search_iterations,
        'base_metric_result_percentage': base_metric_result_percentage,
        'performance_goal_increase': 100*performance_goal_increase,
        'real_performance_goal_increase': 100*(base_experiment_metric_result - goal_metric),
        

        # User goal
        'base_experiment_metric_result': base_experiment_metric_result,
        'user_goal': goal_metric,
        'user_goal_error': 100*(goal_metric - tool_suggested_experiment_metric_result),

        # Results
        #         'estimated_coefficient': metric_coefficient,
        #         'real_coefficient':
        'tool_suggested_dataset_percent': rounded_dataset_percent,
        'tool_suggested_experiment_metric_result': tool_suggested_experiment_metric_result,

        # Emissions:
        'classic_method_emissions_kg': classic_method_emissions,
        'our_method_emissions_kg': our_method_emissions,
        'emissions_kg_reduction': classic_method_emissions - our_method_emissions,
        'emissions_percentual_change': 100*(emissions_percentage_change),
        'full_experiment_kg_emissions':full_experiment_kg_emissions,
        'base_experiment_kg_emissions':base_experiment_kg_emissions, 
        'tool_suggested_experiment_kg_emissions':tool_suggested_experiment_kg_emissions,
        
        # Extra
        'full_experiment_metric_result': full_experiment_metric_result,
        'performance_loss_vs_full_dataset': full_experiment_metric_result - tool_suggested_experiment_metric_result,
    }
