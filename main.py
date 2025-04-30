import uvicorn
from app.api import app
from dotenv import load_dotenv
from app.database import engine, Base  # Import engine and Base

load_dotenv()

Base.metadata.create_all(bind=engine)  # Create the database tables

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)