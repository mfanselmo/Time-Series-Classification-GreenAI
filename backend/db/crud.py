from sqlalchemy.orm import Session, joinedload, lazyload
from typing_extensions import get_args

from constants import DATASET_ESTIMATORS, DATASET_TYPE_NAMES, DETAIL_LEVEL, METRICS, RUN_DESCRIPTORS

from db.models import Experiment, Run, CompletenessCurve
from utils.completeness_curve import get_experiment_completeness_curve
from utils.file_helpers import load_results
from utils.numpy_encoder import NumpyEncoder


def get_or_create(session, db_model, **kwargs):
    instance = session.query(db_model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = db_model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def reset_db(db: Session):

    db.query(Experiment).delete()
    db.query(Run).delete()
    db.query(CompletenessCurve).delete()


def load_runs_csvs(db: Session, dataset_type: DATASET_TYPE_NAMES):
    runs_df = load_results(dataset_type)
    group_by_descriptors = ['dataset_type', 'dataset', 'model'] + DATASET_ESTIMATORS
    db_experiments = []
    db_runs = []

        
    for group_by_values, values in runs_df.groupby(group_by_descriptors):
        grouped_in_dict = NumpyEncoder(dict(zip(group_by_descriptors, group_by_values)))
        
        experiment = get_or_create(db, Experiment, **grouped_in_dict)
        db_experiments.append(experiment)

        for index, value in values.iterrows():
            db_runs.append(Run(**{i: value[i] for i in RUN_DESCRIPTORS}, experiment=experiment))

    db.add_all(db_runs)
    db.commit()

    return db_experiments

def load_completeness_curves(db: Session, load_only_missing: bool = True):
    experiments_to_load_query = db.query(Experiment).options(lazyload(Experiment.completeness_curves))

    if load_only_missing:
        experiments_to_load_query = experiments_to_load_query.filter(Experiment.completeness_curves == None)


    db_completeness_curves = []
    for experiment in experiments_to_load_query:
        for metric in get_args(METRICS):
            experiment_completeness_curve = get_experiment_completeness_curve(experiment, metric)
            db_completeness_curves.append(CompletenessCurve(experiment=experiment, **experiment_completeness_curve))

    db.add_all(db_completeness_curves)
    db.commit()

    return db_completeness_curves


def get_experiment(db: Session, dataset_name: str, model_name: str, detail_level: DETAIL_LEVEL = "0"):
    basic_query = db.query(Experiment).filter_by(
        dataset=dataset_name,
        model=model_name
    )

    if detail_level == "1":
        basic_query =  basic_query.options(
            joinedload(Experiment.completeness_curves)
        )
    if detail_level == "2":
        basic_query =  basic_query.options(
            joinedload(Experiment.runs)
        )
    return basic_query.first()


def get_experiments(db: Session, detail_level: DETAIL_LEVEL = "0", dataset_type: DATASET_TYPE_NAMES | None = None):
    basic_query = db.query(Experiment)
    if dataset_type is not None:
        basic_query = basic_query.filter_by(dataset_type = dataset_type)
    if detail_level == "1":
        basic_query = basic_query.options(
            joinedload(Experiment.completeness_curves)
        )
    if detail_level == "2":
        basic_query = basic_query.options(
            joinedload(Experiment.runs)
        )
    return basic_query.all()


def get_runs(db: Session, dataset_type: DATASET_TYPE_NAMES | None = None, dataset_name: str | None = None, model_name: str | None = None):

    experiment_kwargs = {'dataset_type': dataset_type, 'dataset': dataset_name, 'model': model_name}
    experiment_kwargs = {k: v for k, v in experiment_kwargs.items() if v is not None}

    return db.query(Run).options(
        lazyload(Run.experiment)).filter(
        Run.experiment.has(**experiment_kwargs)).all()

