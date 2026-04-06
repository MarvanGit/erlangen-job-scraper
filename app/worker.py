from celery import Celery
from .database import SessionLocal
from .scraper import scrape_erlangen_jobs


# 1. Initialize the Celery App
# We point the broker (the queue) and the backend (to store results) to our new Redis container.
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",  # Channel 1: The Queue                  FastAPI --> Redis(broker)  -->   Celery
    backend="redis://redis:6379/0"  # Channel 2: The Results                FastAPI <-- Redis(backend) <--   Celery 
)


# --- NEW: The Alarm Clock Configuration ---
celery_app.conf.beat_schedule = {
    "test-scraper-every-30-seconds": {
        "task": "run_scraper_task", # The name of our task below
        "schedule": 30.0,           # Run every 30 seconds for testing!

        # NOTE: In production, you would delete the line above and use a cron job:
        # "schedule": crontab(hour=8, minute=0), # Runs at 8:00 AM daily

    }
}

celery_app.conf.timezone = "Europe/Berlin"
# ------------------------------------------




@celery_app.task(name="run_scraper_task")
def run_scraper_task():
    # 3. Manually open a database connection for this background worker
    db = SessionLocal()
    try:
        # 4. Call the exact same scraper function you already wrote!
        result = scrape_erlangen_jobs(db)
        return result
    finally:
        # 5. Always close the connection when the task finishes
        db.close()