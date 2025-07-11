import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, InputGuardrail, GuardrailFunctionOutput
from pydantic import BaseModel
from agents.run import RunConfig
import asyncio
import chainlit as cl
from typing import cast

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str



async def homework_guardrail(ctx, agent, input_data):
    # result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    config = cl.user_session.get("config")
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context, run_config=ctx.run_config)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

@cl.on_chat_start
async def handle_chat_start():
    agent = Agent(
        name = "Triage Agent",
        instructions = "You are triage agent & helpful assistant",
        handoffs=[history_tutor_agent, math_tutor_agent],
        input_guardrails=[
            InputGuardrail(guardrail_function=homework_guardrail),
        ],
    )
    config = RunConfig(
        model = model,
        model_provider = external_client,
        tracing_disabled = True
    )
    cl.user_session.set("chat_history", [])
    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)

    await cl.Message(content="Welcome to the Health & Wellness Planner! How may I help you?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("chat_history") or []
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
                    continue
                await asyncio.sleep(0.01)  
                await msg.stream_token(token)
        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)
    
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()

        # await msg.update(content=f"Error: {str(e)}")

# triage_agent = Agent(
#     name="Triage Agent",
#     instructions="You determine which agent to use based on the user's homework question",
#     handoffs=[history_tutor_agent, math_tutor_agent],
#     input_guardrails=[
#         InputGuardrail(guardrail_function=homework_guardrail),
#     ],
# )

# async def main():
#     result = await Runner.run(triage_agent, "who was the first president of the united states?")
#     print(result.final_output)

#     result = await Runner.run(triage_agent, "what is life")
#     print(result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())