from agents.run import RunConfig
from config.agent.base_client import external_client, model

def create_run_config():
    return RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
    )
