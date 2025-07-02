from agents import Agent
from config.agent.base_client import model, external_client
from specialized_agents.escalation_agent import escalation_agent
from specialized_agents.nutrition_expert_agent import nutrition_agent
from specialized_agents.injury_support_agent import injury_support_agent
from specialized_agents.general_assistant_agent import general_assistant_agent


def create_triage_agent():
    return Agent(
        name = "Query Router Agent",
        instructions = """You are the Query Router Agent. Your only responsibility is to evaluate the user’s input and hand it off to the most appropriate agent available in your handoff list.

        Follow this decision order:

        Prefer domain-specific agents like Nutrition, Injury Support, or Escalation if the query clearly fits.

        If no agent is a good match (e.g., the query is too general, simple, or unrelated), hand it off to the General Assistant Agent — which is listed at the end of your handoff list.

        Never respond to queries yourself. Route all queries based on relevance only.""",
        handoffs=[escalation_agent, nutrition_agent, injury_support_agent, general_assistant_agent]
    )
