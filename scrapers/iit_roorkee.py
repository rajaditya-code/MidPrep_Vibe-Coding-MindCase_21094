import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress the annoying SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape():
    print("Scraping IIT Roorkee...")
    url = "https://iitr.ac.in/Careers/Project%20Jobs.html"
    
    # Enhanced headers to perfectly mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }
    
    results = []

    try:
        # Increased timeout to 30s and disabled strict SSL verification
        res = requests.get(url, headers=headers, timeout=30, verify=False)
        res.raise_for_status() # This will throw a clear error if the page is 404 Not Found
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # IITR often uses <p> or <li> tags for notices containing "Advertisement"
        for item in soup.find_all(['p', 'li']):
            text = item.text.strip()
            
            # Filter for job-related keywords
            if "Advertisement" in text or "JRF" in text or "Project" in text:
                link_tag = item.find('a', href=True)
                if not link_tag: 
                    continue
                
                href = link_tag['href']
                
                # Fix relative links
                if href.startswith("http"):
                    full_link = href
                elif href.startswith("/"):
                    full_link = f"https://iitr.ac.in{href}"
                else:
                    full_link = f"https://iitr.ac.in/Careers/{href}"
                
                results.append({
                    "title": text[:150].replace('\n', ' ') + "...", # Clean up newlines
                    "link": full_link,
                    "deadline_raw": text, 
                    "organization": "IIT Roorkee",
                    "source": "IITR Careers"
                })
                
        # Deduplicate based on link
        unique_results = list({v['link']: v for v in results}.values())
        print(f"✅ Found {len(unique_results)} project jobs at IIT Roorkee.")
        
        return unique_results

    except requests.exceptions.Timeout:
        print("❌ IITR Error: The server took too long to respond. It might be down for maintenance.")
        return []
    except Exception as e:
        print(f"❌ IITR Error: {e}")
        return []
    
if __name__ == "__main__":
    data = scrape()
    for item in data:
        print(f"\n💼 {item['title']}")
        print(f"   Link: {item['link']}")