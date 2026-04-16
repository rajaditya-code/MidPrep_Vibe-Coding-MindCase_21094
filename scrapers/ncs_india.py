import json
import time
from playwright.sync_api import sync_playwright

def scrape():
    print("Scraping NCS jobs...")

    url = "https://betacloud.ncs.gov.in/job-listing"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # open page and wait a bit, this site loads slowly sometimes
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)

            # trying to close any popup if it shows up
            page.keyboard.press("Escape")
            time.sleep(1)
            page.keyboard.press("Escape")

            try:
                page.locator("button:has-text('Close'), button:has-text('X'), button[aria-label='Close']").first.click(timeout=2000)
            except:
                pass

            # scroll few times so job cards actually load
            for _ in range(3):
                page.mouse.wheel(0, 1000)
                time.sleep(2)

            print("Extracting job data...")

            # using JS to pull data directly, easier than parsing messy html
            extracted_jobs = page.evaluate('''() => {
                let results = [];

                let elements = Array.from(document.querySelectorAll('*')).filter(el => {
                    let text = (el.innerText || "").toLowerCase();
                    return text.includes('applicants') && text.includes('experience');
                });

                let cards = elements.filter(el => {
                    return !Array.from(el.children).some(child => {
                        let cText = (child.innerText || "").toLowerCase();
                        return cText.includes('applicants') && cText.includes('experience');
                    });
                });

                cards.forEach(card => {
                    let allLinks = Array.from(card.querySelectorAll('a'));
                    let bestLink = "";

                    for (let a of allLinks) {
                        let href = a.getAttribute('href') || "";
                        if (href && href.length > 5 && !href.includes('javascript') && !href.includes('#')) {
                            bestLink = href;
                            break;
                        }
                    }

                    let titleEl = card.querySelector('h2, h3, h4, h5, strong, p.fw-bold');
                    let title = titleEl ? titleEl.innerText : card.innerText.split('\\n')[0];

                    results.push({
                        title: title ? title.trim() : "Unknown Job Title",
                        link: bestLink,
                        raw_text: card.innerText || ""
                    });
                });

                return results;
            }''')

            final_results = []

            for job in extracted_jobs:
                # fixing link if its relative, happens sometimes here
                link = job['link']
                if link:
                    link = link if link.startswith("http") else f"https://betacloud.ncs.gov.in{link}"
                else:
                    link = url

                final_results.append({
                    "title": job['title'][:150],
                    "link": link,
                    "deadline_raw": job['raw_text'][:100].replace('\n', ' '),
                    "organization": "NCS Employer",
                    "source": "NCS Beta Cloud",
                    "description": job['raw_text'][:500].replace('\n', ' | ')
                })

            # removing duplicates, sometimes same card comes twice
            unique_results = list({v['link'] + v['title']: v for v in final_results}.values())

            print(f"Extracted {len(unique_results)} jobs")

            # saving locally just to quickly check output
            with open("ncs_jobs_output.json", "w", encoding="utf-8") as f:
                json.dump(unique_results, f, indent=4, ensure_ascii=False)

            return unique_results

        except Exception as e:
            print(f"NCS Error: {e}")
            return []

        finally:
            browser.close()


if __name__ == "__main__":
    scrape()