from playwright.sync_api import sync_playwright
import time
import re

def scrape():
    print("Scraping IIT Delhi Events...")

    url = "https://ocs.iitd.ac.in/"
    initial_results = []

    # starting browser in background mode
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # load full page and wait a bit so data actually appears
            page.goto(url, wait_until="networkidle", timeout=30000)

            # scrolling once to trigger some lazy content, not too much tho
            page.mouse.wheel(0, 1000)
            time.sleep(3)

            good_keywords = [
                "programme", "certificate", "cep", "course",
                "workshop", "internship", "jrf", "recruitment",
                "training", "fair", "interview", "event", "session"
            ]

            bad_keywords = [
                "ranking", "pledge", "gift", "alumnus",
                "award", "inauguration", "sports", "visit"
            ]

            # grabbing all links, later we filter them properly
            links = page.locator("a").all()

            for link in links:
                try:
                    title = link.text_content(timeout=1000)
                    href = link.get_attribute("href")
                except:
                    continue

                if not title or len(title.strip()) < 15 or not href:
                    continue

                # ignore useless clickable things like toggles etc
                if href.startswith('#') or 'javascript' in href.lower():
                    continue

                title = title.replace('►', '').strip()
                title_lower = title.lower()

                is_good = any(w in title_lower for w in good_keywords)
                is_bad = any(w in title_lower for w in bad_keywords)

                if is_good and not is_bad:
                    full_link = href if href.startswith("http") else f"https://ocs.iitd.ac.in/{href.lstrip('/')}"

                    # trying to get nearby text so we can guess context
                    parent_text = link.evaluate("el => el.parentElement ? el.parentElement.innerText : ''")
                    grandparent_text = link.evaluate("el => el.parentElement && el.parentElement.parentElement ? el.parentElement.parentElement.innerText : ''")

                    # simple date pattern, works most of the time but not always
                    date_pattern = re.compile(r'\d{1,2}\s+[A-Za-z]+\s+\d{4}')
                    date_match = date_pattern.search(parent_text)

                    if not date_match:
                        date_match = date_pattern.search(grandparent_text)

                    date_raw = date_match.group(0) if date_match else "Recent"

                    initial_results.append({
                        "title": title[:150],
                        "link": full_link,
                        "deadline_raw": date_raw,
                        "organization": "IIT Delhi",
                        "source": "IIT Delhi OCS",
                        "description": grandparent_text[:500]  # using nearby text, not perfect but works ok
                    })

            # remove duplicates based on link, otherwise too many repeats
            unique_results = list({v['link']: v for v in initial_results}.values())
            final_results = []

            print(f"Found {len(unique_results)} items, now opening each page...")

            for item in unique_results:

                # skipping pdf links, no point opening them here
                if item['link'].lower().endswith('.pdf'):
                    final_results.append(item)
                    continue

                try:
                    # opening detail page but not rushing it
                    page.goto(item['link'], wait_until="load", timeout=15000)
                    time.sleep(1.5)

                    # grabbing page text, just first part is enough
                    page_text = page.locator("body").text_content(timeout=2000) or ""
                    item['description'] = page_text[:1000]

                    # trying to find apply/register link inside page
                    sub_links = page.locator("a").all()
                    for sub_link in sub_links:
                        try:
                            sub_text = sub_link.text_content(timeout=500) or ""
                            if any(k in sub_text.lower() for k in ['apply', 'register', 'click here']):
                                final_href = sub_link.get_attribute("href")
                                if final_href:
                                    item['link'] = final_href if final_href.startswith('http') else f"https://ocs.iitd.ac.in/{final_href.lstrip('/')}"
                                    break
                        except:
                            continue

                    final_results.append(item)

                except Exception:
                    # if page fails, still keep basic info instead of dropping it
                    final_results.append(item)

        except Exception as e:
            print(f"IIT Delhi Error: {e}")

        finally:
            browser.close()  # always close browser or it eats memory slowly

    return final_results


if __name__ == "__main__":
    for item in scrape():
        print(f"\n{item['title']}")
        print(f"{item['link']}")
        print(f"{item['deadline_raw']}")