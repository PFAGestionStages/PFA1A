from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "#a remplir"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#connexion à connexion à PostgreSQL