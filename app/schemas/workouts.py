from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date
from typing import Dict, List

class WorkoutUpsertRequest(BaseModel):
    workout_date: date
    workout_names: List[str] = Field(..., min_items=1)
    workouts_duration_minutes: List[int] = Field(..., min_items=1)
    workouts_calories_burned: List[float] = Field(..., min_items=1)
    
    @field_validator('workouts_duration_minutes', 'workouts_calories_burned')
    def validate_positive_values(cls, v):
        if any(val <= 0 for val in v):
            raise ValueError("Все значения должны быть положительными")
        return v
    
    model_config = ConfigDict(from_attributes=True)

class WorkoutItemResponse(BaseModel):
    name: str
    duration: int
    calories: float

class WorkoutResponse(BaseModel):
    workout_date: date
    workout_items: List[WorkoutItemResponse]
    
    model_config = ConfigDict(from_attributes=True)

class WorkoutSearchItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    model_config = ConfigDict(from_attributes=True)


class DailyWorkoutsSummaryResponse(BaseModel):
    total_duration: int = 0
    total_calories_burned: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class DailyWorkoutsResponse(BaseModel):
    date: date
    workouts: List[WorkoutItemResponse]  