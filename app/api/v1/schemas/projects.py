

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    """Base schema for Project."""

    name: str = Field(..., min_length=1, max_length=30, description="Project name")
    description: str = Field(
        ..., min_length=1, max_length=150, description="Project description"
    )


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "My Project",
                "description": "A detailed description of my project",
            }
        }
    )


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=30, description="Project name"
    )
    description: Optional[str] = Field(
        None, min_length=1, max_length=150, description="Project description"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Project Name",
                "description": "Updated project description",
            }
        }
    )


class ProjectResponse(ProjectBase):
    """Schema for project response."""

    id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Project creation timestamp")

    model_config = ConfigDict(from_attributes=True)
