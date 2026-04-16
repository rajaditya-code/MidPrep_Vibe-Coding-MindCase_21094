import json
import time
from playwright.sync_api import sync_playwright

def scrape():
    print("🚀 Scraping Devfolio (Subdomain Hunting Mode)...")
    url = "https://devfolio.co/hackathons"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5) 
            
            # Scroll down to trigger the lazy-loading for upcoming hackathons
            print("Scrolling to load hackathons...")
            for _ in range(5):
                page.mouse.wheel(0, 1000)
                time.sleep(1.5)

            # THE SUBDOMAIN HUNTER
            print("Extracting Hackathon URLs...")
            extracted_data = page.evaluate('''() => {
                let results = [];
                let allLinks = Array.from(document.querySelectorAll('a'));
                
                // Keep track of links we've already grabbed to avoid duplicates
                let seenLinks = new Set();
                
                allLinks.forEach(link => {
                    let href = link.href || "";
                    let text = (link.innerText || "").trim();
                    
                    // The Golden Rule: Look for subdomains like "xyz.devfolio.co"
                    // Ignore standard devfolio.co pages, twitter, mailto, etc.
                    if (href.includes('.devfolio.co') && !href.includes('www.devfolio.co') && href !== 'https://devfolio.co/') {
                        
                        // Clean off any tracking parameters like ?ref=...
                        let cleanLink = href.split('?')[0];
                        
                        if (!seenLinks.has(cleanLink)) {
                            seenLinks.add(cleanLink);
                            
                            // Try to grab the title. If the link text is empty (e.g. an image link), 
                            // we hunt for a heading tag nearby.
                            let title = text;
                            if (title.length < 3) {
                                let parentCard = link.closest('div');
                                let heading = parentCard ? parentCard.querySelector('h3, h2, h4, h5, p') : null;
                                title = heading ? heading.innerText : "Devfolio Hackathon";
                            }
                            
                            // Grab the surrounding card text to find the dates
                            let parentBox = link.closest('div') ? link.closest('div').innerText : text;
                            
                            results.push({
                                title: title.split('\\n')[0].trim(), // The first line is usually the name
                                link: cleanLink,
                                raw_text: parentBox
                            });
                        }
                    }
                });
                return results;
            }''')

            final_results = []
            for item in extracted_data:
                # Basic cleanup
                title = item['title']
                if len(title) < 3 or "Apply" in title:
                    # Fallback if the title extraction was messy: extract name from the URL
                    # e.g., https://hackout.devfolio.co -> "Hackout"
                    url_part = item['link'].replace('https://', '').split('.devfolio.co')[0]
                    title = url_part.replace('-', ' ').title()
                    
                final_results.append({
                    "title": title[:150],
                    "link": item['link'],
                    "deadline_raw": item['raw_text'][:100].replace('\n', ' '), 
                    "organization": "Devfolio",
                    "source": "Devfolio Hackathons",
                    "description": item['raw_text'][:300].replace('\n', ' | ')
                })

            print(f"✅ Successfully extracted {len(final_results)} hackathons from Devfolio.")
            
            with open("devfolio_hackathons.json", "w", encoding="utf-8") as f:
                json.dump(final_results, f, indent=4, ensure_ascii=False)
                
            return final_results

        except Exception as e:
            print(f"❌ Devfolio UI Error: {e}")
            return []
        finally:
            browser.close()

if __name__ == "__main__":
    data = scrape()
    for item in data[:5]:
        print(f"\n💻 {item['title']}")
        print(f"   Link: {item['link']}")