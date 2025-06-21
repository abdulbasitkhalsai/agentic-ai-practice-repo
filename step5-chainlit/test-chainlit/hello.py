import chainlit as cl
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

run_config = RunConfig(
    model = model,
    model_provider=external_client
)

agent = Agent(
    name= "Assistant",
    instructions="You are helpful assistant"
)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Welcome to Panaversity Chatbot. How may I help you?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({
        "role" : "user",
        "content": message.content
    })
    result = await Runner.run(
        agent,
        history,
        run_config = run_config
    )

    history.append({
        "role" : "assistant",
        "content" : result.final_output
    })

    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()