from dataclasses import dataclass
from dotenv import load_dotenv
import os
from pathlib import Path
from agno.models.openai import OpenAIChat
from agno.db.in_memory import InMemoryDb
import glob

load_dotenv()

@dataclass
class Config:
    data_folder: str = "data"
    agents_folder: str = "agents"
    api_key: str = os.getenv("OPENAI_API_KEY")
    db = InMemoryDb()
    model_name: str = os.getenv("MODEL_NAME")
    visualization_folder: str = "data/visualizations"
    
    def get_data_tables(self):
        return [file for file in Path(self.data_folder).glob("*.csv")]
    
    def get_model(self):
        model = self.model_name
        return OpenAIChat(id=model, api_key=self.api_key)
    
    def clear_visualization_folder(self):
        try:
            vis_folder = self.visualization_folder
            files = glob.glob(f"{vis_folder}/*")
            for f in files:
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"Error deleting {f}: {e}")
                    
            print("Visualization folder cleared")
        except Exception as e:
            print(f"Error clearing visualization folder: {e}")

    