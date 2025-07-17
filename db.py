# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///instance/game_metrics.db"  # תוכל להחליף ל־PostgreSQL בהמשך

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # רק אם זה SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
