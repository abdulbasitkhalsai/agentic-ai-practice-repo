# import sys
# import os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from agents import Agent
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.workout_recommender import workout_recommender
from tools.scheduler import checkin_scheduler
from tools.tracker import progress_tracker
from specialized_agents.nutrition_expert_agent import nutrition_agent
from specialized_agents.injury_support_agent import injury_support_agent
from specialized_agents.escalation_agent import escalation_agent
# from specialized_agents.general_assistant_agent import general_assistant_agent

from config.agent.base_client import model, external_client
from guardrails.health_guardrails import health_guardrail
from agents import InputGuardrail


planner_agent = Agent(
    name="PlannerAgent",
    instructions="""
You are the Health & Wellness Planner Agent. Your job is to guide users toward their fitness goals through personalized planning and encouragement.

- Start by understanding their health goal (e.g., lose weight, build muscle).
- Use the GoalAnalyzerTool to extract structured goals.
- Recommend meals based on dietary preferences using MealPlannerTool.
- Suggest weekly workouts using WorkoutRecommenderTool.
- Track progress with ProgressTrackerTool and schedule check-ins using CheckinSchedulerTool.
- Use guardrails to validate inputs and ensure safe, structured outputs.
- If a user has complex dietary or injury-related needs, escalate to the relevant agent.
- Always respond with empathy, clarity, and structured plans.
""",
    tools=[
        goal_analyzer,
        workout_recommender,
        progress_tracker,
        meal_planner,
        checkin_scheduler
    ],
    handoffs=[
        nutrition_agent,
        injury_support_agent,
        escalation_agent,
        # general_assistant_agent
    ],
    input_guardrails=[
            InputGuardrail(guardrail_function= health_guardrail)
        ]
)

