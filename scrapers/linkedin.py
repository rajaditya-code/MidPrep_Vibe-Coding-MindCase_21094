import json
import time
from playwright.sync_api import sync_playwright

def scrape(keyword="internship", location="India"):
    print(f"Scraping LinkedIn for: {keyword} in {location}...")

    # using public job search page, no login needed
    url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={location}&f_TPR=r86400"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # setting a normal browser look so it doesnt look like bot instantly
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )

        page = context.new_page()

        try:
            # open page and wait a bit, linkedin loads stuff slowly sometimes
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)

            # scrolling few times to load more jobs, not too aggressive
            for _ in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # sometimes there is a button instead of scroll
                try:
                    page.locator("button.infinite-scroller__show-more-button").click(timeout=1000)
                    time.sleep(2)
                except:
                    pass

            print("Extracting job details...")

            # grabbing data directly from DOM using JS, faster and cleaner
            jobs_data = page.evaluate('''() => {
                let results = [];
                let jobCards = document.querySelectorAll('ul.jobs-search__results-list > li');

                jobCards.forEach(card => {
                    let titleEl = card.querySelector('h3.base-search-card__title');
                    let companyEl = card.querySelector('h4.base-search-card__subtitle');
                    let locationEl = card.querySelector('span.job-search-card__location');
                    let linkEl = card.querySelector('a.base-card__full-link');
                    let dateEl = card.querySelector('time');

                    if (titleEl && linkEl) {
                        results.push({
                            title: titleEl.innerText.trim(),
                            company: companyEl ? companyEl.innerText.trim() : "Unknown",
                            location: locationEl ? locationEl.innerText.trim() : "Unknown",
                            link: linkEl.href.split('?')[0],
                            date_posted: dateEl ? dateEl.innerText.trim() : "Recent"
                        });
                    }
                });

                return results;
            }''')

            final_results = []

            for job in jobs_data:
                # linkedin gives "2 days ago" type info, so we dont treat it as deadline
                posted_time = job.get('date_posted', '')

                final_results.append({
                    "title": f"{job['title']} at {job['company']}",
                    "link": job['link'],
                    "deadline_raw": None,
                    "organization": job['company'],
                    "location": job['location'],
                    "source": "LinkedIn Public",
                    "description": f"Posted: {posted_time} | Location: {job['location']}"
                })

            # remove duplicates using link, happens sometimes
            unique_results = list({v['link']: v for v in final_results}.values())

            print(f"Scraped {len(unique_results)} jobs from LinkedIn")

            return unique_results

        except Exception as e:
            print(f"LinkedIn Scraper Error: {e}")
            return []

        finally:
            browser.close()


if __name__ == "__main__":
    scrape("software engineering internship", "India")