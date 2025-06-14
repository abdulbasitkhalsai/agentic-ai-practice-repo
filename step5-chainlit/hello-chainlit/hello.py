import chainlit as cl
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    provider = provider
)


@cl.on_message
async def handle_message(message: cl.Message):
    await cl.Message(content=f"Hello {message.content}").send()