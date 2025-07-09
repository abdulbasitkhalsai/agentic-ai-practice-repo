# tools/tracker.py
from pydantic import BaseModel
from agents import function_tool

class ProgressInput(BaseModel):
    update: str

class ProgressOutput(BaseModel):
    message: str

@function_tool
async def progress_tracker(input: ProgressInput) -> ProgressOutput:
    """Logs user progress and suggests next steps."""
    text = input.update.lower()
    if "lost" in text:
        return ProgressOutput(message="Great job! Keep going!")
    elif "tired" in text:
        return ProgressOutput(message="Thanks for the update. Consider adjusting your diet or rest cycle.")
    else:
        return ProgressOutput(message="Thanks for the update. Logging your progress.")
