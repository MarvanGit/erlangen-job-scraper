from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal
from . import scraper
from .worker import run_scraper_task

# This single line is the magic. 
# It tells SQLAlchemy: "Look at all classes that inherit from Base, 
# and if the tables don't exist in Postgres yet, create them."
models.Base.metadata.create_all(bind=engine)



app = FastAPI()


# Root endpoint to check if the API is running. `app.get("/")` is a Decorator. It's a way to wrap a function with extra behavior. Here, it tells FastAPI: "Hey, whenever a GET request hits the `/` route, trigger the `read_root` function immediately below me."
@app.get("/")
def read_root():
    return {"status": "Erlangen Job Scraper API is running!"}

def get_db():
    db = SessionLocal() # 1. Open a new database workspace
    try:
        yield db        # 2. "Pause" here and hand the db to the API route
    finally:
        db.close()      # 3. When the API route finishes (or crashes), close the workspace!

# Create a clean type alias using Annotated
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/scrape")
def trigger_scraper(db: db_dependency):
    # Notice how we just pass 'db' straight into the function!
    # new_job = scraper.scrape_erlangen_jobs(db)
    # return {"status": "success", "data": new_job}

    # .delay() is the magic word! 
    # It means: "Don't run this now. Put a message in Redis for Celery to pick up."
    run_scraper_task.delay()
    # Notice we don't return the jobs anymore. We return instantly! [CHECK LINE 38]
    return {"message": "Scraping task successfully dispatched to the background worker!"}

@app.get("/jobs")
def get_all_jobs(db: db_dependency):
    # Because of dependency injection, 'db' is now a fully open, ready-to-use database session!
    jobs = db.query(models.Job).all()  
    return jobs


@app.delete("/jobs")
def clear_all_jobs(db: db_dependency):
    # Delete all rows in the jobs table
    db.query(models.Job).delete()
    db.commit()
    return{"message": "Database wiped clean!"}