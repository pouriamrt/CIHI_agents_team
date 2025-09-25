from agno.tools.crawl4ai import Crawl4aiTools
from agno.agent import Agent
from config import Config

config = Config()

model = config.get_model()
db = config.db

cihi_web_agent = Agent(name="CIHI Web Agent",
    model=model,
    db=db,
    tools=[Crawl4aiTools(max_length=None)],  # no content length limit
    add_history_to_context=True,
    num_history_runs=3,
    description="Extracts content from specific websites based on the question.",
    instructions=[
        f"Use web_crawler to extract content from the URLs {config.web_urls}.",
        "Summarize key points based on the question and include the source URL."
    ],
    markdown=True,
    exponential_backoff=True
)