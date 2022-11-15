# FCN model
# when tuning start with learning rate->mini_batch_size ->
# momentum-> #hidden_units -> # learning_rate_decay -> #layers
import tensorflow as tf
import tensorflow_addons as tfa

from codecarbon import OfflineEmissionsTracker

from utils.constants import DATASETS
from utils.run_utils import plot_history, create_output
from utils.dataset_utils import create_data

import uuid
import numpy as np
import time


tfk = tf.keras
tfkl = tf.keras.layers


class Classifier_MLP:

    def __init__(self, options, verbose=False):
        self.options = options
        self.project_id = str(uuid.uuid4())
        self.verbose = verbose

        self.model = self.build_model()
        self.data = create_data(options)

        if (verbose == True):
            print(
                f"Experiment: \nModel: {options['model']}\nDataset: {options['dataset']} \nExperiment: {options['experiment']}")
            print(self.model.summary())
            print("Data shapes")
            print(f"X_train: {self.data['x_train'].shape}")
            print(f"y_train: {self.data['y_train'].shape}")
            print(f"X_test: {self.data['x_test'].shape}")
            print(f"y_test: {self.data['y_test'].shape}")

        self.measure_parameters = {
            'effective_epochs': 0,
            'effective_emissions_kg': 0,
            'effective_duration': 0
        }

    def build_model(self):
        dataset_type = self.options['dataset_type']

        input_shape = DATASETS[dataset_type][self.options['dataset']]['input_shape']
        num_classes = DATASETS[dataset_type][self.options['dataset']]['num_classes']

        input_layer = tfkl.Input(input_shape)

        input_layer_flattened = tfkl.Flatten()(input_layer)

        layer_1 = tfkl.Dropout(0.1)(input_layer_flattened)
        layer_1 = tfkl.Dense(500, activation='relu')(layer_1)

        layer_2 = tfkl.Dropout(0.2)(layer_1)
        layer_2 = tfkl.Dense(500, activation='relu')(layer_2)

        layer_3 = tfkl.Dropout(0.2)(layer_2)
        layer_3 = tfkl.Dense(500, activation='relu')(layer_3)

        output_layer = tfkl.Dropout(0.3)(layer_3)
        output_layer = tfkl.Dense(num_classes, activation='softmax')(output_layer)

        model = tfk.models.Model(inputs=input_layer, outputs=output_layer)

        model.compile(
            loss='categorical_crossentropy',
            optimizer=tfk.optimizers.Adadelta(),
            metrics=[
                tfk.metrics.CategoricalAccuracy(),
                tfk.metrics.CategoricalCrossentropy(),
                tfk.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy'),
                tfk.metrics.TopKCategoricalAccuracy(k=5, name='top_5_accuracy'),
                tfk.metrics.Precision(name="precision"),
                tfk.metrics.Recall(name="recall"),
                tfk.metrics.AUC(name="auc"),
                tfa.metrics.F1Score(num_classes=num_classes, average="micro", name="f1_score")
            ]

        )

        early_stopping = tfk.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=300,
            verbose=self.verbose,
            restore_best_weights=True,
        )

        reduce_lr = tfk.callbacks.ReduceLROnPlateau(
            monitor='loss',
            factor=0.5,
            patience=50,
            verbose=self.verbose,
            min_lr=0.1
        )

        self.callbacks = [reduce_lr, early_stopping]

        return model

    def fit(self):
        if not tf.test.is_gpu_available:
            print('error')
            exit()

        x_train, y_train = self.data['x_train'], self.data['y_train']

        batch_size = 16
        nb_epochs = 2000

        mini_batch_size = int(min(x_train.shape[0] / 10, batch_size))

        with OfflineEmissionsTracker(country_iso_code="ITA", project_name=self.project_id, log_level='warning') as tracker:
            start_time = time.time()

            history = self.model.fit(
                x_train,
                y_train,
                callbacks=self.callbacks,
                batch_size=mini_batch_size,
                epochs=nb_epochs,
                validation_split=0.1,
                verbose=self.verbose
            )
            self.measure_parameters['effective_duration'] += time.time() - start_time

        self.measure_parameters['effective_emissions_kg'] += tracker.final_emissions
        self.measure_parameters['effective_epochs'] += len(history.epoch)

        if self.verbose:
            plot_history(history)

    def predict(self):
        score = self.model.evaluate(self.data["x_test"], self.data["y_test"], verbose=0)

        output = create_output(
            self.options,
            self.data,
            self.model,
            self.measure_parameters['effective_epochs'],
            score,
            self.measure_parameters['effective_emissions_kg'],
            self.measure_parameters['effective_duration'],
            self.project_id
        )

        del self.data
        del self.model

        return output
