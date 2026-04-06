from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from . import models

# 1. Import the synchronous version of Playwright
from playwright.sync_api import sync_playwright

def scrape_erlangen_jobs(db: Session):
    url = "https://realpython.github.io/fake-jobs/"
    scraped_count = 0

    # 2. Boot up the Playwright browser context
    with sync_playwright() as p:
        # Launch Chromium (headless=True means it runs invisibly!)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 3. Tell the browser to navigate to the URL and wait for the page to fully load
        page.goto(url)
        
        # We can even tell Playwright to wait for a specific CSS element to appear
        # before we grab the HTML, ensuring the JavaScript has finished!
        page.wait_for_selector(".card-content")

        # 4. Grab the final, fully-rendered HTML from the browser
        html_content = page.content()

        # 5. Shut down the browser to save memory
        browser.close()

    # --- From here down, it is exactly the same BeautifulSoup code you already wrote! ---
    soup = BeautifulSoup(html_content, "html.parser")

    for card in soup.select('.card-content'):
        title = card.select_one('.title').get_text(strip=True)
        company = card.select_one('.company').get_text(strip=True)
        location = card.select_one('.location').get_text(strip=True)
        
        existing_job = db.query(models.Job).filter(
            models.Job.title == title,
            models.Job.company == company
        ).first()

        if existing_job:
            print("STOPPED A DUPLICATE")
            pass
        else:
            new_job = models.Job(
                title=title,
                company=company,
                location=location,
                description=""
            )
            db.add(new_job)
            scraped_count += 1

    db.commit()
    return {"message": f"Successfully scraped and saved {scraped_count} jobs using Playwright!"}