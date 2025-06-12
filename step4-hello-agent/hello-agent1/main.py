import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set")

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client = external_client,
    model = "gemini-2.0-flash",
)

config = RunConfig(
    model = model,
    model_provider= external_client,
    tracing_disabled=True
)

async def main():
    agent = Agent(
        name="Travel Advisor",
        instructions="You are helpful Travel Advisor"
    )
    # agent = Agent(
    #     name="Assistant",
    #     instructions="You are helpful Assistant"
    # )
    user_input = input("What do you want to ask from Travel Advisor? ")
    result = await Runner.run(agent, user_input, run_config=config)
    print(result.final_output)
    print("Thanks for using LLM")


if __name__ == '__main__':
    asyncio.run(main())

