from typing import List, Union

from pydantic import BaseModel


class RunBase(BaseModel):

    iteration: int
    data_quality_dimension_percentage: float
    loss: float
    categorical_accuracy: float
    categorical_crossentropy: float
    top_3_accuracy: float
    top_5_accuracy: float
    precision: float
    recall: float
    auc: float
    f1_score: float
    effective_epochs: int
    used_data_size: int
    actual_data_percentage_used: float
    emissions_kg: float
    duration: float



class Run(RunBase):
    id: int
    experiment_id: int

    class Config:
        orm_mode = True


class CompletenessCurveBase(BaseModel):
    metric: str
    coefficient: float
    intercept: float



class CompletenessCurve(CompletenessCurveBase):
    id: int
    experiment_id: int

    class Config:
        orm_mode = True


class ExperimentBase(BaseModel):
    dataset: str
    model: str
    model_type: str
    dataset_type: str
    data_type: str
    n_parameters: int
    datapoint_w: int
    datapoint_h: int
    dimensions: int
    num_classes: int
    original_data_size: int



class Experiment(ExperimentBase):
    id: int
    runs: List[Run] = []
    completeness_curve: CompletenessCurve = None

    class Config:
        orm_mode = True
