from agno.agent import Agent
from config import Config

config = Config()
model = config.get_model()
db = config.db

# General Agent
general_agent = Agent(
    name="GeneralAssistant",
    model=model,
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    description="Handles general queries and synthesizes info from specialists.",
    instructions=[
        "Answer general questions or combine inputs from specialist agents.",
        "If specialists provide info, synthesize it into a clear answer.",
        "If a query doesn't fit other specialists, attempt to answer directly.",
        "Maintain a professional and clear tone.",
        "Make the response beautifully formatted as well."
    ],
    markdown=True,
    exponential_backoff=True
)