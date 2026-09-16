import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./taptym.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
class Base(DeclarativeBase):
    pass

def ensure_car_columns() -> None:
    if 'cars' not in inspect(engine).get_table_names():
        return
    existing = {column['name'] for column in inspect(engine).get_columns('cars')}
    additions = {
        'category': 'VARCHAR(80)', 'action': 'VARCHAR(40)', 'price': 'INTEGER',
        'location': 'VARCHAR(120)', 'description': 'VARCHAR(2000)',
        'detailimg': 'VARCHAR(500)', 'name': 'VARCHAR(120)', 'avatar': 'VARCHAR(500)',
        'owner_email': 'VARCHAR(160)',
    }
    with engine.begin() as connection:
        for column, column_type in additions.items():
            if column not in existing:
                connection.execute(text(f'ALTER TABLE cars ADD COLUMN {column} {column_type}'))
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
