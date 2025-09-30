from agents.nursing_datatable_agent import agent_datatable
from agents.general_agent import general_agent
from agents.visualization_workflow import visualization_workflow_agent
from agents.cihi_web_agent import cihi_web_agent
from agents.doc_agent import data_dictionary_agent, methodology_notes_agent
from agno.team import Team
from config import Config

config = Config()
db = config.db

def initialize_team(model, session_state):
    """Initializes or re-initializes the research assistant team."""
    return Team(
        name="CIHI Chatbot Team",
        model=model, 
        members=[
            agent_datatable,
            general_agent,
            visualization_workflow_agent,
            cihi_web_agent,
            data_dictionary_agent,
            methodology_notes_agent
        ],
        description="Coordinates a team of specialist agents to handle CIHI data analysis tasks.",
        instructions=[
            "Analyze the user query and decide which specialist(s) should handle it.",
            "Delegate tasks based on query type:",
            "- Data table analysis -> DataTableAgent",
            "- General or multi-step queries -> GeneralAssistant",
            "- Visualization creation -> VisualizationWorkflowAgent",
            "- Web extraction -> CIHI Web Agent",
            "- Data dictionary -> DataDictionaryAgent",
            "- Methodology notes -> MethodologyNotesAgent",
            "Gather all agents' findings and synthesize a coherent answer.",
            "Do not include the logs and errors from the tool calls in the response.",
            "Cite sources for any facts and maintain clarity in the final answer.",
            "Always check the conversation history (memory) for context or follow-up references.",
            "If the user asks something that was asked before, utilize remembered information instead of starting fresh.",
            "If the user asks for to create a chart or visualization, delegate the task to the VisualizationWorkflowAgent.",
            "When done with visualization, tell the user to refresh the plot section to see the new chart or visualization.",
            "For questions regarding key points, first try to use the CIHI Web Agent to extract the key points.",
            "For questions about the availability and quality of the data, delegate the task to the MethodologyNotesAgent.",
            "For questions about the data dictionary and data elements, delegate the task to the DataDictionaryAgent.",
            "RN is Registered Nurses, LPN is Licensed Practical Nurses, RPN is Registered Psychiatric Nurses, NP is Nurse Practitioners",
            "Continue delegating and researching until the query is fully answered.",
            "Avoid mentioning the function calls in the final response and make the final response beautifully formatted as well."
        ],
        db=db,
        session_state=session_state,
        expected_output="The user's query has been thoroughly answered with information from all relevant specialists.",
        enable_agentic_state=True,      # The coordinator retains its own context between turns
        share_member_interactions=True, # All agents see each other's outputs as context
        enable_agentic_memory=True,
        enable_user_memories=True,
        read_team_history=True,
        show_members_responses=False,   # Do not show raw individual agents' answers directly to the user
        markdown=True,
        add_member_tools_to_context=True,
        add_history_to_context=True,    # Maintain a shared history (memory) between coordinator and members
        num_history_runs=5,             # Limit how much history is shared (to last 5 interactions)
        add_session_state_to_context=True
    )