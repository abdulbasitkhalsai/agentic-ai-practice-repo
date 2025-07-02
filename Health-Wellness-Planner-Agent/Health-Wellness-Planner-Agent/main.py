import asyncio
import chainlit as cl
from agents import Runner, Agent
from agent import create_triage_agent
from config.agent.session_config import create_run_config
from agents.run import RunConfig
from typing import cast

@cl.on_chat_start
async def handle_chat_start():
    agent = create_triage_agent()
    config = create_run_config()
    
    cl.user_session.set("chat_history", [])
    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)

    await cl.Message(content="Welcome to the Health & Wellness Planner! How may I help you?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("chat_history") or []
    print(f"history before append {history}")
    history.append({"role": "user", "content" : message.content})
    msg = cl.Message(content = "")
    await msg.send()
    agent : Agent = cast(Agent, cl.user_session.get("agent"))
    config : RunConfig = cast(RunConfig, cl.user_session.get("config"))
    try:
        result = Runner.run_streamed(agent, history, run_config = config)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                token = event.data.delta
                # Skip function call argument deltas
                if getattr(event.data, "type", "") == "response.function_call_arguments.delta":
                    print("Skipping function call delta:", token)
                    continue
                await msg.stream_token(token)
        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)
    
    except Exception as e:
        await msg.update(content=f"Error: {str(e)}")

