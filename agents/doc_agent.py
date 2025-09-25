from agno.knowledge.knowledge import Knowledge
from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.db.sqlite import SqliteDb
from config import Config

config = Config()

model = config.get_model()
db = config.db

embedder = OpenAIEmbedder(id="text-embedding-3-small", api_key=config.api_key)

contents_db = SqliteDb(db_file="data/tmp/methodology_notes.db")
vector_db = ChromaDb(collection="methodology_notes", path="data/tmp/chromadb_meth_notes", persistent_client=True, embedder=embedder)
knowledge_base_methodology_notes = Knowledge(
    vector_db=vector_db,
    contents_db=contents_db
)

methodology_notes_agent = Agent(
    name="MethodologyNotesAgent",
    model=model,
    knowledge=knowledge_base_methodology_notes,
    db=db,
    description="Uses knowledge base to answer questions about methodology notes.",
    instructions=[
        "Answer questions comprehensively based on the knowledge base.",
        "Summarize key points and include the reference of the methodology notes.",
        "If the question is not in the knowledge base, say so and ask the user to provide more information about the methodology notes.",
        "If the question is not clear, ask the user to provide more information about the methodology notes.",
        "Make the response nice and beautifully formatted as well with sections and inline citations."
    ],
    expected_output="Answer the question comprehensively based on the context provided with citations and references. If the information is not available, say 'I don't know'.",
    add_history_to_context=True,
    num_history_runs=3,
    read_chat_history=True,
    markdown=True,
    add_knowledge_to_context=True,
    search_knowledge=True,
    enable_agentic_knowledge_filters=True,
    exponential_backoff=True,
    # debug_mode=True,
)


contents_db = SqliteDb(db_file="data/tmp/data_dictionary.db")
vector_db = ChromaDb(collection="data_dictionary", path="data/tmp/chromadb_data_dictionary", persistent_client=True, embedder=embedder)
knowledge_base_data_dictionary = Knowledge(
    vector_db=vector_db,
    contents_db=contents_db
)

data_dictionary_agent = Agent(
    name="DataDictionaryAgent",
    model=model,
    knowledge=knowledge_base_data_dictionary,
    db=db,
    description="Uses knowledge base to answer questions about data dictionary and data elements.",
    instructions=[
        "Answer questions comprehensively based on the knowledge base.",
        "Summarize key points and include the reference of the data dictionary and data elements.",
        "If the question is not in the knowledge base, say so and ask the user to provide more information about the data dictionary and data elements.",
        "If the question is not clear, ask the user to provide more information about the data dictionary and data elements.",
        "Make the response nice and beautifully formatted as well with sections and inline citations."
    ],
    expected_output="Answer the question comprehensively based on the context provided with citations and references. If the information is not available, say 'I don't know'.",
    add_history_to_context=True,
    num_history_runs=3,
    read_chat_history=True,
    markdown=True,
    add_knowledge_to_context=True,
    search_knowledge=True,
    enable_agentic_knowledge_filters=True,
    exponential_backoff=True,
    # debug_mode=True,
)
