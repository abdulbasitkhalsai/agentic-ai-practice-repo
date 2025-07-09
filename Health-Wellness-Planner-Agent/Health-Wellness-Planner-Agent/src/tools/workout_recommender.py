# tools/workout_recommender.py
from pydantic import BaseModel
from typing import Dict
from agents import function_tool

class WorkoutInput(BaseModel):
    experience_level: str  # beginner, intermediate, advanced

class WorkoutOutput(BaseModel):
    plan: Dict[str, str]  # e.g., { "Monday": "Pushups and Squats" }

@function_tool
async def workout_recommender(input: WorkoutInput) -> WorkoutOutput:
    """Recommends a weekly workout plan based on experience level."""
    plan = {
        "Monday": "Pushups + Squats",
        "Tuesday": "Rest",
        "Wednesday": "Planks + Lunges",
        "Thursday": "Cardio (Jump Rope)",
        "Friday": "Pushups + Squats",
        "Saturday": "Yoga or Stretching",
        "Sunday": "Rest"
    }
    return WorkoutOutput(plan=plan)
