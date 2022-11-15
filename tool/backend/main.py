from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile

from sqlalchemy.orm import Session

from db import crud, models
from db.database import SessionLocal, engine

from typing_extensions import get_args
import numpy as np

from constants import DATA_TYPES, DATASET_TYPE_NAMES, DETAIL_LEVEL, METRICS, MODEL_TYPES, REDUCING_METHODS
from utils.dataset_analyzer import DatasetAnalizer


from utils.regressor import Regressor

# SETUP
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="main app")


@app.get('/')
def api_root():
    return {'hello': 'world'}


@app.get("/load_experiments_on_db")
def load_experiments_on_db(reset_db: bool = False, db: Session = Depends(get_db)):
    """
        Loads csv present in static directory
        Optional param: Reset db
    """
    if reset_db:
        crud.reset_db(db)

    for dataset_type in get_args(DATASET_TYPE_NAMES):
        crud.load_runs_csvs(db, dataset_type)

    return {}


@app.get("/load_completeness_curves")
def load_completeness_curves(load_only_missing: bool = True, db: Session = Depends(get_db)):
    """
    """
    crud.load_completeness_curves(db, load_only_missing)
    return {}


@app.get("/train_regressors")
def train_regressor(db: Session = Depends(get_db)):
    """
    """
    for dataset_type in get_args(DATASET_TYPE_NAMES):
        for metric in get_args(METRICS):
            regressor = Regressor(dataset_type, metric)

            experiments = crud.get_experiments(db, detail_level="1", dataset_type=dataset_type)
            try:
                regressor.fit(experiments)
            except StopIteration:
                raise HTTPException(status_code=400, detail="Completeness curves not available")

            regressor.save_model()

    return {}


@app.get("/get_experiment")
def get_experiment(dataset_name: str, model_name: str, detail_level: DETAIL_LEVEL = "0", db: Session = Depends(get_db)):
    """
    """
    return crud.get_experiment(db, dataset_name, model_name, detail_level)


@app.get("/get_experiments")
def get_experiments(detail_level: DETAIL_LEVEL = "0", dataset_type: DATASET_TYPE_NAMES | None = None,
                    db: Session = Depends(get_db)):
    """
    """
    return crud.get_experiments(db, detail_level, dataset_type)


@app.get("/get_runs")
def get_runs(
        dataset_type: DATASET_TYPE_NAMES | None = None, dataset_name: str | None = None, model_name: str | None = None,
        db: Session = Depends(get_db)):
    """
    """
    return crud.get_runs(db, dataset_type, dataset_name, model_name)


@app.get("/get_prediction")
def get_prediction(
    dataset_type: DATASET_TYPE_NAMES,
    metric: METRICS,
    base_metric_result_percentage: float,  # (0.1 -> 1) How much of the data was used for base metric result
    base_metric_result: float,  # (0 -> 1): Result of given metric using base_metric_result_percentage
    goal_metric: float,
    model_type: MODEL_TYPES,
    data_type: DATA_TYPES,
    n_parameters: int,
    datapoint_w: int,
    datapoint_h: int,
    dimensions: int,
    num_classes: int,
    original_data_size: int,
    db: Session = Depends(get_db)
):
    """
    """
    regressor = Regressor(dataset_type, metric)

    if regressor.regressor is None:
        raise HTTPException(status_code=400, detail="Regressor not trained")

    metric_coefficient = regressor.predict(model_type, data_type, n_parameters,
                                           datapoint_w, datapoint_h, dimensions, num_classes, original_data_size)
    intercept = base_metric_result - metric_coefficient*np.log(base_metric_result_percentage)

    return {
        "metric_coefficient": metric_coefficient,
        "dataset_percent": (goal_metric - intercept)/metric_coefficient,
        "dataset_percent": np.exp((goal_metric - intercept)/metric_coefficient),
        "ready": True
    }


@app.post('/get_dataset_info')
async def get_dataset_info(file: UploadFile):
    print(file)
    dataset_analizer = DatasetAnalizer(file)
    await dataset_analizer.load_train_data()

    return {
        **dataset_analizer.dataset_metadata(),
        **dataset_analizer.dataset_quality()
    }


@app.post('/clean_dataset')
async def clean_dataset(file: UploadFile, dataset_percent: float, reducing_method: REDUCING_METHODS):
    dataset_analizer = DatasetAnalizer(file)
    await dataset_analizer.load_train_data()

    return dataset_analizer.clean_dataset(dataset_percent, reducing_method)


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", app)
