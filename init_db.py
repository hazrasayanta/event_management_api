from app.database import engine, Base

# Create all tables in the SQLite database
Base.metadata.create_all(bind=engine)

print("Database and tables created successfully!")
