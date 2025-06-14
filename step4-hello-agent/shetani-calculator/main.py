import os
import asyncio
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.run import RunConfig
from dotenv import load_dotenv
from tools.funny_calc import add, substract, multiply, divide

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set")

provider = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model= model,
    model_provider=provider,
    tracing_disabled=True
)


async def main():
    agent = Agent(
        name = "Shetani (Funny) Calculator",
        instructions="You are a Shetani (Funny) Calculator that respond mathematical calculation with tool calling. In tools, there is intentional addition of random value in answer",
        tools=[add, substract, divide, multiply]
    )

    user_input = input("Please ask any mathematical calculation? ")
    result = await Runner.run(agent, user_input, run_config=config)
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())
