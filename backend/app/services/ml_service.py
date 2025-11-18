"""ML Model training and prediction services"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from pathlib import Path


class MLService:
    """Service for ML model operations"""
    
    def __init__(self, model_storage_path: str = "models"):
        self.model_storage_path = Path(model_storage_path)
        self.model_storage_path.mkdir(parents=True, exist_ok=True)
    
    def train_classification_model(
        self,
        dataset_path: str,
        target_column: str,
        algorithm: str = "random_forest",
        test_size: float = 0.2,
        random_state: int = 42,
        hyperparameters: dict = None
    ):
        """Train a classification model"""
        # Load data
        df = pd.read_csv(dataset_path)
        
        # Prepare features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Handle categorical variables
        X = pd.get_dummies(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Train model
        if algorithm == "random_forest":
            model = RandomForestClassifier(
                n_estimators=hyperparameters.get("n_estimators", 100),
                max_depth=hyperparameters.get("max_depth", None),
                random_state=random_state
            )
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, average="weighted")),
            "recall": float(recall_score(y_test, y_pred, average="weighted")),
            "f1_score": float(f1_score(y_test, y_pred, average="weighted"))
        }
        
        return model, metrics
    
    def train_regression_model(
        self,
        dataset_path: str,
        target_column: str,
        algorithm: str = "random_forest",
        test_size: float = 0.2,
        random_state: int = 42,
        hyperparameters: dict = None
    ):
        """Train a regression model"""
        # Load data
        df = pd.read_csv(dataset_path)
        
        # Prepare features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Handle categorical variables
        X = pd.get_dummies(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Train model
        if algorithm == "random_forest":
            model = RandomForestRegressor(
                n_estimators=hyperparameters.get("n_estimators", 100),
                max_depth=hyperparameters.get("max_depth", None),
                random_state=random_state
            )
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        metrics = {
            "mse": float(mean_squared_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "r2_score": float(r2_score(y_test, y_pred))
        }
        
        return model, metrics
    
    def save_model(self, model, model_id: int, version: str):
        """Save a trained model"""
        model_path = self.model_storage_path / f"model_{model_id}_v{version}.pkl"
        joblib.dump(model, model_path)
        return str(model_path)
    
    def load_model(self, model_path: str):
        """Load a saved model"""
        return joblib.load(model_path)
    
    def predict(self, model, data):
        """Make predictions with a model"""
        return model.predict(data)

