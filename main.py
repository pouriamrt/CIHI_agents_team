import streamlit as st
from agents.create_team import initialize_team
import time
from agno.models.openai import OpenAIChat
import asyncio
import sys
from config import Config
from pathlib import Path
import glob

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

config = Config()

model = OpenAIChat(id=config.model_name, api_key=config.api_key)

if "team" not in st.session_state:
    if "team_session_id" not in st.session_state:
        st.session_state.team_session_id = f"streamlit-team-session-{int(time.time())}"
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    st.session_state.team = initialize_team(model, st.session_state)

st.title("CIHI Chatbot Team")
st.markdown("""
This AI team can help with:
- Data table analysis and visualization
- General Q&A and synthesis  
""")

# --- Place to show plots (live updating) ---
def get_plot_files(vis_folder):
    return sorted(Path(vis_folder).glob("*.*"))

with st.expander("Show Plots", expanded=False):
    vis_folder = Path(config.visualization_folder)
    
    # Use a session state to keep track of the last seen plot files
    if "last_plot_files" not in st.session_state:
        st.session_state.last_plot_files = []

    plot_files = get_plot_files(vis_folder)
    if plot_files != st.session_state.last_plot_files:
        st.session_state.last_plot_files = plot_files

    if plot_files:
        for plot_file in plot_files:
            file_suffix = plot_file.suffix.lower()
            if file_suffix in [".png", ".jpg", ".jpeg"]:
                st.image(str(plot_file), caption=plot_file.name)
            elif file_suffix in [".svg"]:
                with open(plot_file, "r", encoding="utf-8") as f:
                    svg_content = f.read()
                st.markdown(f'<div style="text-align:center">{svg_content}</div>', unsafe_allow_html=True)
            elif file_suffix in [".pdf"]:
                st.markdown(f"[{plot_file.name} (PDF)]({plot_file.as_posix()})")
            else:
                st.markdown(f"[{plot_file.name}]({plot_file.as_posix()})")
    else:
        st.info("No plots have been generated yet. When you ask for a chart or visualization, it will appear here.")

    # Add a refresh button instead of auto-refresh
    if st.button("🔄 Refresh Plots"):
        st.rerun()

# Display past messages (if any) from the session state
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for the user's query
user_query = st.chat_input("Ask the CIHI Chatbot Team anything...")

if user_query:
    # Log user message in history
    st.session_state.messages.append({"role": "user", "content": user_query})
    # Display user message immediately in chat
    with st.chat_message("user"):
        st.markdown(user_query)
    # Prepare to display team's answer
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # placeholder for streaming text
        full_response = ""
        # Run the team on the user query with streaming enabled
        try:
            # Check if tool logs should be captured
            capture_tool_logs = st.session_state.get("show_tool_logs", False)
            tool_logs = []
            
            response_stream = st.session_state.team.run(user_query, stream=True)
            for chunk in response_stream:
                if chunk.content and isinstance(chunk.content, str):
                    # Filter out tool execution messages from the main response
                    if "delegate_task_to_member" in chunk.content:
                        break
                    
                    if not (chunk.content.startswith(("datatable_")) or 
                            ") completed in " in chunk.content):
                        full_response += chunk.content
                        # Display the current accumulated response with a cursor
                        message_placeholder.markdown(full_response + "▌")
                    elif capture_tool_logs:
                        # Capture tool logs for debugging
                        tool_logs.append(chunk.content)
            
            # Store tool logs if captured
            if capture_tool_logs and tool_logs:
                st.session_state.tool_logs = "\n".join(tool_logs)
            
            # When done, display the final response (remove the blinking cursor)
            message_placeholder.markdown(full_response)
            # Add the final response to the messages history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            memories = []
            for memory in st.session_state.team.db.get_user_memories():
                memories.append(memory.memory)
            st.session_state.memory_dump = memories
            
        except Exception as e:
            # Error handling: show an error in the app and log to history
            st.error(f"An error occurred: {e}\nPlease check your API keys and try again.")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
            st.exception(e)  # for debug, print full traceback in the app
            
            
            
with st.sidebar:
    st.title("Team Settings")

    # Toggle to display team memory for debugging
    if st.checkbox("Show Team Memory Contents", value=False):
        st.subheader("Team Memory (Debug)")
        if "memory_dump" in st.session_state:
            # Pretty-print the memory message list
            from pprint import pformat
            memory_str = pformat(st.session_state.memory_dump, indent=2, width=80)
            st.code(memory_str, language="python")
        else:
            st.info("Interact with the team to see memory contents here.")
    
    # Toggle to show tool execution logs for debugging
    show_tool_logs = st.checkbox("Show Tool Execution Logs", value=False)
    st.session_state.show_tool_logs = show_tool_logs
    
    if show_tool_logs:
        st.subheader("Tool Execution Logs (Debug)")
        if "tool_logs" in st.session_state:
            st.code(st.session_state.tool_logs, language="text")
        else:
            st.info("Tool execution logs will appear here when enabled.")
    # Display current session info
    st.markdown(f"**Session ID**: `{st.session_state.team_session_id}`")
    st.markdown(f"**Model**: {config.model_name}")
    st.subheader("Memory & Session")
    st.markdown("This team remembers the conversation in this session. Use the reset button to clear memory.")
    # Button to clear chat history and reinitialize the team
    if st.button("Clear Chat & Reset Team"):
        st.session_state.messages = []
        st.session_state.team_session_id = f"streamlit-team-session-{int(time.time())}"
        st.session_state.team = initialize_team(model, st.session_state)  # start a fresh team instance
        if "memory_dump" in st.session_state:
            del st.session_state.memory_dump
        if "tool_logs" in st.session_state:
            del st.session_state.tool_logs
        st.rerun()  # reload the app
    st.title("About")
    st.markdown("""
    **How this works**:  
    - Chat with CIHI released data.
    """)