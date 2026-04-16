from playwright.sync_api import sync_playwright
import time

def scrape():
    print("Scraping Unstop hackathons...")

    url = "https://unstop.com/hackathons"
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # open page and wait till things load properly
            page.goto(url, wait_until="networkidle", timeout=30000)

            # scroll a bit so lazy cards show up, otherwise it looks empty
            page.mouse.wheel(0, 1500)
            time.sleep(3)

            # grabbing hackathon cards based on url pattern
            cards = page.locator("a[href*='/hackathons/']").all()

            for card in cards:
                try:
                    # getting all visible text inside card
                    full_text = card.text_content(timeout=1000)
                except:
                    continue

                # skip small useless links, only big cards matter
                if not full_text or len(full_text.strip()) < 40:
                    continue

                href = card.get_attribute("href")
                full_link = href if href.startswith("http") else f"https://unstop.com{href}"

                # first line usually works as title most of the time
                lines = [line.strip() for line in full_text.splitlines() if line.strip()]
                title = lines[0] if lines else "Unstop Hackathon"

                results.append({
                    "title": title[:150],
                    "link": full_link,
                    "deadline_raw": full_text,
                    "organization": "Unstop Host",
                    "source": "Unstop UI"
                })

        except Exception as e:
            print(f"Unstop Error: {e}")

        finally:
            browser.close()

    return results


if __name__ == "__main__":
    for item in scrape():
        print(item['title'], "-", item['link'])