# tools/scheduler.py
from pydantic import BaseModel
from datetime import datetime, timedelta
from agents import function_tool

class ScheduleInput(BaseModel):
    checkin_frequency: str  # e.g., "weekly"

class ScheduleOutput(BaseModel):
    next_checkin: str

@function_tool
async def checkin_scheduler(input: ScheduleInput) -> ScheduleOutput:
    """Schedules the next check-in based on frequency."""
    if input.checkin_frequency == "weekly":
        next_date = datetime.now() + timedelta(days=7)
    else:
        next_date = datetime.now() + timedelta(days=3)

    return ScheduleOutput(next_checkin=next_date.strftime("%Y-%m-%d"))
