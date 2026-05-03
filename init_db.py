from app.database import engine, Base
from app import models

print("Creation des tables...")
Base.metadata.create_all(bind=engine)
print("Tables creees avec succes !")