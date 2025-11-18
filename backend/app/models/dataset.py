"""Dataset model"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Dataset(Base):
    """Dataset model"""
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)
    file_format = Column(String, nullable=False)  # csv, json, excel, parquet, etc.
    file_size = Column(BigInteger, nullable=False)  # in bytes
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    schema = Column(JSON, nullable=True)  # Column names, types, etc.
    extra_metadata = Column(JSON, default=dict)  # Additional metadata (renamed from 'metadata' to avoid SQLAlchemy conflict)
    tags = Column(JSON, default=list)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="datasets")

