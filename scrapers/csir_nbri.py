import requests
from bs4 import BeautifulSoup

def scrape():
    print("Scraping CSIR-NBRI...")
    url = "https://www.csir.res.in/en/career-opportunities/recruitment"
    
    # Crucial: Spoofing full browser headers to bypass 403 Forbidden
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    results = []
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Look for table rows (common in Govt sites)
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 1:
                link_tag = row.find('a', href=True)
                if link_tag:
                    results.append({
                        "title": cols[0].text.strip() + " - " + cols[1].text.strip(),
                        "link": link_tag['href'],
                        "deadline_raw": cols[-1].text.strip(), # Usually the last column is the deadline
                        "organization": "CSIR-NBRI",
                        "source": "NBRI Recruitment"
                    })
        return results
    except Exception as e:
        print(f"NBRI Error: {e}")
        return []