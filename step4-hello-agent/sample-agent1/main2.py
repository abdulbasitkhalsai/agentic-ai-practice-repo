import os
from dotenv import load_dotenv
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from pydantic import BaseModel
import asyncio
from agents.exceptions import InputGuardrailTripwireTriggered


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

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

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

fallback_agent = Agent(
    name="Fallback Agent",
    instructions="""
    Respond politely and clearly when a user asks a question that is outside the intended scope (homework-related).
    Explain that this assistant is only meant for homework help.
    Provide suggestions to ask a relevant question.
    """,
)

async def homework_guardrail(ctx, agent, input_data):
    # print("\n🔍 Guardrail Context Info:")
    # print("➡️ ctx.context:", ctx.context)
    # print("➡️ ctx:", ctx)
    result = await Runner.run(guardrail_agent, input_data, run_config=config, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    # print("✅ Guardrail agent response:", final_output)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    try:
        result = await Runner.run(triage_agent, "who was the first president of the united states? in short", run_config=config)
        print(result.final_output)
    except Exception as e:
        print("Error during first question:", e)

    try:
        result = await Runner.run(triage_agent, "what is life", run_config=config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        # Run fallback agent
        fallback_response = await Runner.run(fallback_agent, "What is life", run_config=config)
        print(f"\n⚠️ Fallback response to: \n{fallback_response.final_output}\n")
    except Exception as e:
        print("Error during second question:", e)

if __name__ == "__main__":
    asyncio.run(main())

# 🔍 Guardrail Context Info:

# ➡️ ctx: RunContextWrapper(context=None, usage=Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0))
# ✅ Guardrail agent response: is_homework=True reasoning='The question is a straightforward factual question about history, specifically asking about th
# e first president of the United States. This is a common topic covered in history classes in school. Hence it looks like a homework question.'        
# The first president of the United States was **George Washington**. He served from 1789 to 1797.


# 🔍 Guardrail Context Info:
# ➡️ ctx.context: None
# ➡️ ctx: RunContextWrapper(context=None, usage=Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0))
# ✅ Guardrail agent response: is_homework=False reasoning='The user is asking a philosophical question, not related to schoolwork.'

# ⚠️ Fallback response to:
# That's an interesting question! However, this assistant is designed to help with homework-related questions.

# If you have any questions about your homework, feel free to ask! For example, you could ask about a specific concept in your textbook, a difficult problem you're trying to solve, or a topic you're researching for a school project.


# (sample-agent1) PS C:\Users\abdulbasit.khalsai\Documents\WD\agentic-ai\beginner\repo-practice\step4-hello-agent\sample-agent1> 