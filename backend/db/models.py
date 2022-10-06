from code import interact
from ctypes.wintypes import INT
from sqlalchemy import Float, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    dataset = Column(String)
    model = Column(String)
    dataset_type = Column(String)
    data_type = Column(String)
    original_data_size = Column(Integer)
    num_classes = Column(Integer)
    model_type = Column(String)
    datapoint_w = Column(Integer)
    datapoint_h = Column(Integer)
    dimensions = Column(Integer)
    n_parameters = Column(Integer)


    cons_1 = UniqueConstraint(dataset, model, name="unique_constraint_on_dataset_model", sqlite_on_conflict='IGNORE')
    runs = relationship("Run", back_populates="experiment")
    completeness_curves = relationship("CompletenessCurve", back_populates="experiment")


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    iteration = Column(Integer)
    data_quality_dimension_percentage = Column(Float)
    loss = Column(Float)
    categorical_accuracy = Column(Float)
    categorical_crossentropy = Column(Float)
    top_3_accuracy = Column(Float)
    top_5_accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    auc = Column(Float)
    f1_score = Column(Float)
    effective_epochs = Column(Integer)
    used_data_size = Column(Integer)
    actual_data_percentage_used = Column(Float)
    emissions_kg = Column(Float)
    duration = Column(Float)


    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    experiment = relationship("Experiment", back_populates="runs")
    cons2 = UniqueConstraint(experiment_id, iteration,
                             data_quality_dimension_percentage, 
                             name="unique_constraint_on_experiment_iteration_and_completeness_percentage",
                             sqlite_on_conflict='IGNORE')



class CompletenessCurve(Base):
    __tablename__ = "completenes_curves"

    
    id = Column(Integer, primary_key=True, index=True)
    metric = Column(String)
    coefficient = Column(Float)
    intercept = Column(Float)
    
    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    experiment = relationship("Experiment", back_populates="completeness_curves")
    cons3 = UniqueConstraint(experiment_id, metric,
                             name="unique_constraint_on_metric_for_experiment", sqlite_on_conflict='REPLACE')
