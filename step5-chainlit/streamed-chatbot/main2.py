import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

@cl.on_chat_start
async def handle_chat_start():
    config = RunConfig(
        model = model,
        model_provider = external_client,
        tracing_disabled = True
    )
    agent = Agent(
        name = "Assistant",
        instructions = "You are helpful Assistant"
    )
    cl.user_session.set("history", [])
    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)
    await cl.Message(content = "Welcome to Panabot, How may I help you?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content" : message.content})
    msg = cl.Message(content = "")
    await msg.send()
    agent : Agent = cast(Agent, cl.user_session.get("agent"))
    config : RunConfig = cast(RunConfig, cl.user_session.get("config"))

    try:

        result = Runner.run_streamed(agent, history, run_config = config)

        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr (event.data, "delta"):
                token = event.data.delta
                await msg.stream_token(token)
                print(f"Token is {token}")

        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("history", history)
    
    except Exception as e:
        await msg.update(content=f"Error: {str(e)}")