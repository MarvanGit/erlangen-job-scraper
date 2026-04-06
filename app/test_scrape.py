from bs4 import BeautifulSoup

# 1. The raw HTML string (normally we get this via requests.get)
html_doc = """
<html>
    <body>
        <div class="job-list">
            <div class="job-card">
                <h2 class="title">Junior AI Engineer</h2>
                <span class="company">Siemens Healthineers</span>
                <span class="location">Erlangen, Bavaria</span>
            </div>
            <div class="job-card">
                <h2 class="title">Data Scientist</h2>
                <span class="company">DATEV</span>
                <span class="location">Nuremberg, Bavaria</span>
            </div>
        </div>
    </body>
</html>
"""

# 2. Parse the HTML
soup = BeautifulSoup(html_doc, 'html.parser')
# 3. YOUR ASSIGNMENT:

# Write a loop that finds all "job-card" divs.
for div in soup.select('.job-card'):

    # For each card, extract the title, company, and location.
    title = div.select_one('.title').get_text(strip=True)
    company = div.select_one('.company').get_text(strip=True)
    location = div.select_one('.location').get_text(strip=True)

    # Print them out to the console so it looks like:
    # - Junior AI Engineer at Siemens Healthineers (Erlangen, Bavaria)
    # - Data Scientist at DATEV (Nuremberg, Bavaria)
    print(f"{title} at {company} ({location})")

# Write your extraction logic here:
# jobs = soup.select(...) 
# for job in jobs:
#    ...