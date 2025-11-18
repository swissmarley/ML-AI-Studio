"""Data visualization endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.dataset import Dataset

router = APIRouter()


class VisualizationRequest(BaseModel):
    """Visualization request schema"""
    dataset_id: int
    chart_type: str  # bar, line, scatter, histogram, heatmap, etc.
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    color_column: Optional[str] = None
    aggregation: Optional[str] = None  # sum, mean, count, etc.


@router.get("/{dataset_id}/summary")
async def get_dataset_summary(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistical summary of a dataset"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    try:
        # Load dataset
        if dataset.file_format == 'csv':
            df = pd.read_csv(dataset.file_path)
        elif dataset.file_format == 'json':
            df = pd.read_json(dataset.file_path)
        elif dataset.file_format == 'excel':
            df = pd.read_excel(dataset.file_path)
        elif dataset.file_format == 'parquet':
            df = pd.read_parquet(dataset.file_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format for visualization"
            )
        
        # Generate summary statistics
        summary = {
            "shape": list(df.shape),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
            "missing_values": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
        
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing dataset: {str(e)}"
        )


@router.post("/{dataset_id}/chart")
async def create_chart(
    dataset_id: int,
    request: VisualizationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a chart from dataset"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    try:
        # Load dataset
        if dataset.file_format == 'csv':
            df = pd.read_csv(dataset.file_path)
        elif dataset.file_format == 'json':
            df = pd.read_json(dataset.file_path)
        elif dataset.file_format == 'excel':
            df = pd.read_excel(dataset.file_path)
        elif dataset.file_format == 'parquet':
            df = pd.read_parquet(dataset.file_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format"
            )
        
        # Create chart based on type
        fig = None
        
        if request.chart_type == "bar" and request.x_column and request.y_column:
            if request.aggregation:
                df_agg = df.groupby(request.x_column)[request.y_column].agg(request.aggregation).reset_index()
                fig = px.bar(df_agg, x=request.x_column, y=request.y_column)
            else:
                fig = px.bar(df, x=request.x_column, y=request.y_column, color=request.color_column)
        
        elif request.chart_type == "line" and request.x_column and request.y_column:
            fig = px.line(df, x=request.x_column, y=request.y_column, color=request.color_column)
        
        elif request.chart_type == "scatter" and request.x_column and request.y_column:
            fig = px.scatter(df, x=request.x_column, y=request.y_column, color=request.color_column)
        
        elif request.chart_type == "histogram" and request.x_column:
            fig = px.histogram(df, x=request.x_column)
        
        elif request.chart_type == "heatmap":
            numeric_df = df.select_dtypes(include=['number'])
            if len(numeric_df.columns) > 0:
                fig = px.imshow(numeric_df.corr(), text_auto=True, aspect="auto")
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chart type or missing required columns"
            )
        
        if fig:
            return json.loads(fig.to_json())
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create chart"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating chart: {str(e)}"
        )

