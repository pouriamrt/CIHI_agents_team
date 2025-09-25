import asyncio

if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from dotenv import load_dotenv
import os

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from asyncio import Semaphore
from tqdm import tqdm

embedder = OpenAIEmbedder(id="text-embedding-3-small", api_key=OPENAI_API_KEY)

reader = PDFReader(
    split_on_pages=True, 
    read_images=True, 
    chunk=True, 
    chunking_strategy=RecursiveChunking(
        chunk_size=800,
        overlap=80
    )
)

model = OpenAIChat(id=os.getenv("MODEL_NAME"), api_key=OPENAI_API_KEY)

contents_db = SqliteDb(db_file="data/tmp/data_dictionary.db")

vector_db = ChromaDb(collection="data_dictionary", path="data/tmp/chromadb_data_dictionary", persistent_client=True, embedder=embedder)

knowledge_base_data_dictionary = Knowledge(
    vector_db=vector_db,
    contents_db=contents_db
)

files = ['data/health-workforce-information-minimum-data-set-data-submission-manual-en.pdf', 'data/nursing-in-canada-2024-meth-notes-en.pdf']

knowledge_base_data_dictionary.add_content(
    name="Data Dictionary",
    path=files[0],
    metadata={"doc_type": "data dictionary and data elements"},
    reader=reader,
    upsert=True,
    skip_if_exists=True
)

###########################################################################

reader = PDFReader(
    split_on_pages=True, 
    read_images=True, 
    chunk=True, 
    chunking_strategy=RecursiveChunking(
        chunk_size=800,
        overlap=80
    )
)

contents_db = SqliteDb(db_file="data/tmp/methodology_notes.db")

vector_db = ChromaDb(collection="methodology_notes", path="data/tmp/chromadb_meth_notes", persistent_client=True, embedder=embedder)

knowledge_base_methodology_notes = Knowledge(
    vector_db=vector_db,
    contents_db=contents_db
)

knowledge_base_methodology_notes.add_content(
    name="Methodology Notes",
    path=files[1],
    metadata={"doc_type": "methodology notes"},
    reader=reader,
    upsert=True,
    skip_if_exists=True
)



agent = Agent(knowledge=knowledge_base_data_dictionary)
agent.print_response("what are the data elements for place of work?", markdown=True, stream=True)

agent = Agent(knowledge=knowledge_base_methodology_notes)
agent.print_response("Is Manitoba workforce data available for 2024?", markdown=True, stream=True)

