from db import Base, engine
from models import Game  # הוסף כאן את כל שאר המודלים שלך

def init_database():
    print("Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init_database()
