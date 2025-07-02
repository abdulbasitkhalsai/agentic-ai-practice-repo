from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio
from agents.run import RunConfig
from config import model, external_client

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


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context, run_config = config)
    final_output = result.final_output_as(HomeworkOutput)

    print("🎯 Raw Output from guardrail_agent:", result.final_output)
    print("📦 Parsed HomeworkOutput:", final_output)
    if final_output is None:
         # You must return a valid GuardrailFunctionOutput even in failure
        return GuardrailFunctionOutput(
            output_info=HomeworkOutput(is_homework=False, reasoning="Could not determine intent."),
            tripwire_triggered=False,
        )
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    # input_guardrails=[
    #     InputGuardrail(guardrail_function=homework_guardrail),
    # ],
)

async def main():
    result = await Runner.run(triage_agent, "first president of US?", run_config = config)
    print(f"Strat of Result 1: {result.final_output} ----------------The End Result 1---------------")

    result = await Runner.run(triage_agent, "how is life in US in 2017?", run_config = config)
    print(f"Strat of Result 2: {result.final_output} ----------------The End Result 2---------------")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())