from agents import Runner, Agent
from pydantic import BaseModel
from config.agent.session_config import config
from agents import GuardrailFunctionOutput


class health_output(BaseModel):
    is_health : bool
    reasoning : str

health_guardrail_agent = Agent(
    name= "Health Guardrail Agent",
    instructions= "Check the user is asking about Health",
    output_type=health_output
)


async def health_guardrail(ctx, agent, input_data):
    print(f"Health guardrail activated")
    result = Runner.run_sync(health_guardrail_agent, input_data, run_config=config, context=ctx.context)
    final_output = result.final_output_as(health_output)
    return GuardrailFunctionOutput(
        output_info = final_output,
        tripwire_triggered = not final_output.is_health
    )