"""ML Model models"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class MLModel(Base):
    """ML Model model"""
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    model_type = Column(String, nullable=False)  # classification, regression, clustering, etc.
    algorithm = Column(String, nullable=False)  # random_forest, xgboost, neural_network, etc.
    status = Column(String, default="draft")  # draft, training, trained, deployed, archived
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="models")
    versions = relationship("ModelVersion", back_populates="model", cascade="all, delete-orphan")
    experiments = relationship("ModelExperiment", back_populates="model", cascade="all, delete-orphan")


class ModelVersion(Base):
    """Model Version model"""
    __tablename__ = "model_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)  # e.g., "1.0.0"
    model_path = Column(String, nullable=False)  # Path to saved model file
    metrics = Column(JSON, default=dict)  # accuracy, precision, recall, f1, etc.
    hyperparameters = Column(JSON, default=dict)
    training_config = Column(JSON, default=dict)
    model_id = Column(Integer, ForeignKey("ml_models.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    model = relationship("MLModel", back_populates="versions")


class ModelExperiment(Base):
    """Model Experiment model"""
    __tablename__ = "model_experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    metrics = Column(JSON, default=dict)
    hyperparameters = Column(JSON, default=dict)
    status = Column(String, default="running")  # running, completed, failed
    model_id = Column(Integer, ForeignKey("ml_models.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    model = relationship("MLModel", back_populates="experiments")

