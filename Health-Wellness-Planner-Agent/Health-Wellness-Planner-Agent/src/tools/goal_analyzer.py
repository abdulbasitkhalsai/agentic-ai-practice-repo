# from pydantic import BaseModel
# import re
# from agents import function_tool  

# class GoalInput(BaseModel):
#     raw_input: str

# class GoalOutput(BaseModel):
#     quantity: float
#     metric: str
#     duration_days: int

# @function_tool
# async def goal_analyzer(input: GoalInput) -> GoalOutput:
#     """Analyzes user fitness goal and converts it into a structured format."""
#     text = input.raw_input.lower()
#     match = re.search(r"(\d+)\s*(kg|lbs|pounds).*(\d+)\s*(day|week|month|months)", text)
#     if not match:
#         raise ValueError("Goal format not recognized. Try: 'lose 5kg in 2 months'")

#     quantity, metric, duration, unit = match.groups()
#     metric = "kg" if metric in ["kg", "kilogram"] else "lbs"
#     duration_days = int(duration) * 30 if "month" in unit else int(duration) * 7

#     return GoalOutput(
#         quantity=float(quantity),
#         metric=metric,
#         duration_days=duration_days
#     )
from pydantic import BaseModel
import re
from agents import function_tool  

class GoalInput(BaseModel):
    raw_input: str

class GoalOutput(BaseModel):
    quantity: float
    metric: str
    duration_days: int

@function_tool
async def goal_analyzer(input: GoalInput) -> GoalOutput:
    """Analyzes user fitness goal and converts it into a structured format."""
    print(f"[goal_analyzer] Called with input: {input}")
    
    text = input.raw_input.lower()
    match = re.search(r"(\d+)\s*(kg|lbs|pounds).*(\d+)\s*(day|week|month|months)", text)
    if not match:
        raise ValueError("Goal format not recognized. Try: 'lose 5kg in 2 months'")

    quantity, metric, duration, unit = match.groups()
    metric = "kg" if metric in ["kg", "kilogram"] else "lbs"
    duration_days = int(duration) * 30 if "month" in unit else int(duration) * 7

    output = GoalOutput(
        quantity=float(quantity),
        metric=metric,
        duration_days=duration_days
    )
    print(f"[goal_analyzer] Output: {output}")
    return output
