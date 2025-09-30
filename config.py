from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
from pathlib import Path
from agno.models.openai import OpenAIChat
from agno.db.in_memory import InMemoryDb
import glob

load_dotenv(override=True)

@dataclass
class Config:
    data_folder: str = "data"
    agents_folder: str = "agents"
    api_key: str = os.getenv("OPENAI_API_KEY")
    db = InMemoryDb()
    model_name: str = os.getenv("MODEL_NAME")
    visualization_folder: str = "data/visualizations"
    web_urls: list[str] = field(default_factory=lambda: ['https://www.cihi.ca/en/registered-nurses', 
                                                         'https://www.cihi.ca/en/licensed-practical-nurses',
                                                         'https://www.cihi.ca/en/registered-psychiatric-nurses', 
                                                         'https://www.cihi.ca/en/nurse-practitioners'])
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri: str = os.getenv("REDIRECT_URI")
    
    def get_data_tables(self):
        return [file for file in Path(self.data_folder).glob("*.csv")]
    
    def get_model(self):
        model = self.model_name
        return OpenAIChat(id=model, api_key=self.api_key, temperature=0.0)
    
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

    