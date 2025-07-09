# # tools/meal_planner.py
# from pydantic import BaseModel
# from typing import Dict, List
# from agents import function_tool

# class MealInput(BaseModel):
#     diet_type: str  # e.g., vegetarian, keto

# class MealOutput(BaseModel):
#     plan: Dict[str, List[str]]  # e.g., { "Monday": ["Breakfast", "Lunch", "Dinner"] }

# @function_tool
# async def meal_planner(input: MealInput) -> MealOutput:
#     """Creates a 7-day meal plan based on diet preference."""
#     sample_day = ["Oats with berries", "Lentil salad", "Grilled tofu"]
#     plan = {day: sample_day for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
#     return MealOutput(plan=plan)
# tools/meal_planner.py


from pydantic import BaseModel
from typing import Dict, List
from agents import function_tool

class MealInput(BaseModel):
    diet_type: str  # e.g., vegetarian, keto

class MealOutput(BaseModel):
    plan: Dict[str, List[str]]  # e.g., { "Monday": ["Breakfast", "Lunch", "Dinner"] }

@function_tool
async def meal_planner(input: MealInput) -> MealOutput:
    """Creates a 7-day meal plan based on diet preference."""
    print(f"[meal_planner] Called with input: {input}")
    
    sample_day = ["Oats with berries", "Lentil salad", "Grilled tofu"]
    plan = {day: sample_day for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
    
    output = MealOutput(plan=plan)
    print(f"[meal_planner] Output: {output}")
    
    return output
