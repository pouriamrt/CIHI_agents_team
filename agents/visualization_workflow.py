from agno.agent import Agent
from agno.tools.visualization import VisualizationTools
from agents.nursing_datatable_agent import agent_datatable
from agno.tools.workflow import WorkflowTools
from agno.workflow import Step, Workflow
from config import Config

config = Config()

config.clear_visualization_folder()
model = config.get_model()
db = config.db

visualization_agent = Agent(
    name="VisualizationAgent",
    model=model,
    db=db,
    instructions=[
        "You are a data visualization assistant that creates charts and plots",
        "Generate clear, informative visualizations based on the given data",
        "Save charts to files and provide insights about the data",
        "Choose appropriate chart types for different data patterns",
    ],
    tools=[VisualizationTools(output_dir=config.visualization_folder)],
    add_datetime_to_context=True, 
    markdown=True,
    exponential_backoff=True
)


visualization_workflow = Workflow(
    name="Visualization Workflow",
    db=db,
    description="A workflow that creates a visualization based on the data table analysis",
    steps=[
        Step(name="DataTable Analysis Phase", agent=agent_datatable),
        Step(name="Visualization Phase", agent=visualization_agent),
    ]
)


workflow_tools = WorkflowTools(
    workflow=visualization_workflow,
)

visualization_workflow_agent = Agent(
    model=model,
    db=db,
    name="VisualizationWorkflowAgent",
    instructions=[
        "You are a visualization workflow assistant that creates a visualization based on the data table analysis",
        "First delegate the task to the DataTableAgent to get the data",
        "Then delegate the task to the VisualizationAgent to create the visualization",
        "Provide insights about the visualization",
        "Save the visualization to the visualization folder",
        "Don't return the errors from the tool calls.",
        "Keep doing the task until the visualization is created and saved to the visualization folder."
    ],
    tools=[workflow_tools],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True, 
    markdown=True,
    exponential_backoff=True
)