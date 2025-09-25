from dataclasses import dataclass
from dotenv import load_dotenv
import os
from pathlib import Path
from agno.models.openai import OpenAIChat
from agno.db.in_memory import InMemoryDb

load_dotenv()

@dataclass
class Config:
    data_folder: str = "data"
    agents_folder: str = "agents"
    api_key: str = os.getenv("OPENAI_API_KEY")
    db = InMemoryDb()
    model_name: str = os.getenv("MODEL_NAME")
    
    def get_data_tables(self):
        return [file for file in Path(self.data_folder).glob("*.csv")]
    
    def get_model(self):
        model = self.model_name
        return OpenAIChat(id=model, api_key=self.api_key)
    