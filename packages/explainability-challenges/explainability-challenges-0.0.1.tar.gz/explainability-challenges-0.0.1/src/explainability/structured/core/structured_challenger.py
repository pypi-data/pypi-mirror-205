from abc import ABC, abstractmethod
from typing import Dict, Optional

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, clone
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .structured_manipulator import StructuredManipulator


class SKChallenger(ABC):
    """
    Base class for challenges to explainability methods for supervised learning
    tasks using structured tabular data and scikit-learn models.
    """

    def __init__(self, model: BaseEstimator,
                 df: pd.DataFrame, label_column: str,
                 random_state: Optional[int] = None) -> None:
        """
        :param model: The model to implement challenges on.
        :param df: The dataset to implement challenges on.
        :param label_column: The target prediction column for the dataset.
        :param random_state: A random state for reproducibility in stochastic
            operations.
        :return: None
        """
        self.df = df
        self.label_column = label_column
        self.random_state = random_state
        self._model = model
        self.challenges: Dict[str, StructuredManipulator] = {
            "base": StructuredManipulator(df, label_column, random_state)
        }
        self.models: Dict[str, Pipeline] = {}

    @abstractmethod
    def generate_challenges(self) -> None:
        """
        Abstract method for populating `self.challenges` with
        `StructuredManipulator` objects representing each modified dataset
        for the challenge.

        :return: None
        """
        raise NotImplementedError

    def train_models(self, interpret: bool = False) -> None:
        """
        Train a model on each dataset for the challenge.

        :param interpret: Indicator for whether model is from interpret
            package.
        :return: None
        """
        for challenge_name, sm in self.challenges.items():
            x, y, _, _ = sm.train_test_split()
            model = clone(self._model)
            preprocessor = ColumnTransformer(transformers=[
                ("onehot",
                 OneHotEncoder(sparse_output=False),
                 x.select_dtypes(exclude=np.number).columns),
                ("scaler",
                 StandardScaler(),
                 x.select_dtypes(include=np.number).columns)],
                remainder="passthrough",
                verbose_feature_names_out=False)
            if interpret:
                preprocessor.fit(x, y)
                feature_names = preprocessor.get_feature_names_out()
                model.set_params(feature_names=feature_names)

            pipeline = Pipeline([("preprocessor", preprocessor),
                                 ("model", model)])

            # noinspection PyTypeChecker
            self.models[challenge_name] = pipeline.fit(x, y)  # noqa
