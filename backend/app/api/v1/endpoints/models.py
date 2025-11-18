"""ML Model endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import json

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.model import MLModel, ModelVersion, ModelExperiment
from app.models.project import Project
from app.models.dataset import Dataset

router = APIRouter()


class ModelCreate(BaseModel):
    """Model creation schema"""
    name: str
    description: str = None
    model_type: str  # classification, regression, clustering, etc.
    algorithm: str  # random_forest, xgboost, neural_network, etc.
    project_id: Optional[int] = None


class ModelUpdate(BaseModel):
    """Model update schema"""
    name: str = None
    description: str = None
    status: str = None


class TrainingConfig(BaseModel):
    """Training configuration schema"""
    dataset_id: int
    target_column: str
    test_size: float = 0.2
    random_state: int = 42
    hyperparameters: Dict[str, Any] = {}


class ModelResponse(BaseModel):
    """Model response schema"""
    id: int
    name: str
    description: str = None
    model_type: str
    algorithm: str
    status: str
    project_id: int = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ModelVersionResponse(BaseModel):
    """Model version response schema"""
    id: int
    version: str
    metrics: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[ModelResponse])
async def get_models(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all models for current user"""
    query = db.query(MLModel).filter(MLModel.owner_id == current_user.id)
    
    if project_id:
        query = query.filter(MLModel.project_id == project_id)
    
    models = query.offset(skip).limit(limit).all()
    return models


@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_data: ModelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new ML model"""
    # Validate project if provided
    if model_data.project_id:
        project = db.query(Project).filter(
            Project.id == model_data.project_id,
            Project.owner_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
    
    model = MLModel(
        name=model_data.name,
        description=model_data.description,
        model_type=model_data.model_type,
        algorithm=model_data.algorithm,
        project_id=model_data.project_id,
        owner_id=current_user.id
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific model"""
    model = db.query(MLModel).filter(
        MLModel.id == model_id,
        MLModel.owner_id == current_user.id
    ).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    return model


@router.post("/{model_id}/train", status_code=status.HTTP_202_ACCEPTED)
async def train_model(
    model_id: int,
    config: TrainingConfig,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Train a model"""
    model = db.query(MLModel).filter(
        MLModel.id == model_id,
        MLModel.owner_id == current_user.id
    ).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    # Validate dataset
    dataset = db.query(Dataset).filter(
        Dataset.id == config.dataset_id,
        Dataset.owner_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Create experiment
    experiment = ModelExperiment(
        name=f"Training {model.name}",
        model_id=model_id,
        hyperparameters=config.hyperparameters,
        status="running"
    )
    db.add(experiment)
    model.status = "training"
    db.commit()
    
    # TODO: Implement actual training logic in background task
    # background_tasks.add_task(train_model_task, model_id, config, experiment.id)
    
    return {
        "message": "Training started",
        "experiment_id": experiment.id,
        "model_id": model_id
    }


@router.get("/{model_id}/versions", response_model=List[ModelVersionResponse])
async def get_model_versions(
    model_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all versions of a model"""
    model = db.query(MLModel).filter(
        MLModel.id == model_id,
        MLModel.owner_id == current_user.id
    ).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    return model.versions


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    model_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a model"""
    model = db.query(MLModel).filter(
        MLModel.id == model_id,
        MLModel.owner_id == current_user.id
    ).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    db.delete(model)
    db.commit()
    return None

