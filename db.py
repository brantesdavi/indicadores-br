from dotenv import load_dotenv
from sqlalchemy import create_engine
import os


load_dotenv()

def get_engine():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("A variavel DATABASE_URL não foi encontrada no .env")
    
    return create_engine(database_url)