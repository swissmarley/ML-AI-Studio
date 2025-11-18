"""Dataset endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os
import pandas as pd
from pathlib import Path

from app.core.database import get_db
from app.core.config import settings
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.project import Project

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class DatasetResponse(BaseModel):
    """Dataset response schema"""
    id: int
    name: str
    description: str = None
    file_format: str
    file_size: int
    row_count: int = None
    column_count: int = None
    schema: dict = None
    tags: List[str]
    project_id: int = None
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class DatasetUpdate(BaseModel):
    """Dataset update schema"""
    name: str = None
    description: str = None
    tags: List[str] = None


def detect_file_format(filename: str) -> str:
    """Detect file format from extension"""
    ext = Path(filename).suffix.lower()
    format_map = {
        '.csv': 'csv',
        '.json': 'json',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.parquet': 'parquet',
        '.pkl': 'pickle',
        '.h5': 'hdf5'
    }
    return format_map.get(ext, 'unknown')


def analyze_dataset(file_path: str, file_format: str) -> dict:
    """Analyze dataset and extract metadata"""
    try:
        if file_format == 'csv':
            df = pd.read_csv(file_path, nrows=1000)  # Sample for analysis
        elif file_format == 'json':
            df = pd.read_json(file_path)
        elif file_format == 'excel':
            df = pd.read_excel(file_path, nrows=1000)
        elif file_format == 'parquet':
            df = pd.read_parquet(file_path)
        else:
            return {}
        
        schema = {
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "shape": list(df.shape)
        }
        
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "schema": schema
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/", response_model=List[DatasetResponse])
async def get_datasets(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all datasets for current user"""
    query = db.query(Dataset).filter(Dataset.owner_id == current_user.id)
    
    if project_id:
        query = query.filter(Dataset.project_id == project_id)
    
    datasets = query.offset(skip).limit(limit).all()
    return datasets


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    project_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new dataset"""
    # Validate project if provided
    if project_id:
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
    
    # Detect file format
    file_format = detect_file_format(file.filename)
    if file_format == 'unknown':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format"
        )
    
    # Save file
    file_path = UPLOAD_DIR / f"{current_user.id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large"
            )
        f.write(content)
    
    # Analyze dataset
    analysis = analyze_dataset(str(file_path), file_format)
    
    # Create dataset record
    dataset = Dataset(
        name=name or file.filename,
        description=description,
        file_path=str(file_path),
        file_format=file_format,
        file_size=len(content),
        row_count=analysis.get("row_count"),
        column_count=analysis.get("column_count"),
        schema=analysis.get("schema"),
        project_id=project_id,
        owner_id=current_user.id
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    return dataset


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific dataset"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    return dataset


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a dataset"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Delete file
    if os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)
    
    db.delete(dataset)
    db.commit()
    return None

