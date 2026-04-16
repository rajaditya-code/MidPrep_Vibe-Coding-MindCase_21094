from playwright.sync_api import sync_playwright
import time

def scrape():
    print("Scraping Buddy4Study scholarships...")

    url = "https://www.buddy4study.com/scholarships"
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # open page and wait, this site takes time to load properly
            page.goto(url, wait_until="networkidle", timeout=45000)

            # scrolling few times so more cards appear, otherwise limited data comes
            for _ in range(3):
                page.mouse.wheel(0, 1000)
                time.sleep(1.5)

            # targeting links which look like scholarship detail pages
            links = page.locator("a[href*='/page/'], a[href*='/scholarship/']").all()

            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        continue

                    # skip login or register stuff, not useful for us
                    if "login" in href.lower() or "register" in href.lower():
                        continue

                    # try getting text directly from link
                    title = link.text_content(timeout=1000).strip()

                    # sometimes link has only image so we check parent text
                    if len(title) < 10:
                        parent_text = link.evaluate("el => el.parentElement ? el.parentElement.innerText : ''").strip()
                        title = parent_text.split('\n')[0] if parent_text else ""

                    if len(title) < 10:
                        continue

                    full_link = href if href.startswith("http") else f"https://www.buddy4study.com{href}"

                    # grabbing nearby card text to later find deadline etc
                    card_text = link.evaluate('''el => {
                        let card = el.closest('article') || el.closest('div[class*="card"]');
                        return card ? card.innerText : el.parentElement.innerText;
                    }''')

                    results.append({
                        "title": title[:150].strip(),
                        "link": full_link,
                        "deadline_raw": card_text,
                        "organization": "Buddy4Study Partner",
                        "source": "Buddy4Study UI",
                        "description": card_text[:500].replace('\n', ' | ')
                    })

                except:
                    # if one card fails, just skip it and move on
                    continue

        except Exception as e:
            print(f"Buddy4Study Error: {e}")

        finally:
            browser.close()

    # removing duplicates, same links can appear multiple times
    unique_results = list({v['link']: v for v in results}.values())

    print(f"Found {len(unique_results)} scholarships")

    return unique_results


if __name__ == "__main__":
    data = scrape()

    for item in data:
        print(f"\n{item['title']}")
        print(f"{item['link']}")
        print(f"{item['description'][:100]}...")