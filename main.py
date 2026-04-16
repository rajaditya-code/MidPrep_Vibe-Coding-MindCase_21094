import time
import random
from scrapers import iit_roorkee, iit_delhi, csir_nbri, unstop_ui, linkedin, ncs_india, buddy4study, devfolio
from utils.cleaner import parse_date, detect_type, detect_location, extract_tags
from utils.scorer import calculate_score
from utils.supabase_client import insert_data

# list of all scrapers
SCRAPERS = [
    iit_roorkee.scrape,
    iit_delhi.scrape,
    csir_nbri.scrape,
    unstop_ui.scrape,
    linkedin.scrape,
    buddy4study.scrape,
    ncs_india.scrape,
    devfolio.scrape
]

def main():
    print("Starting Opportunity Aggregator...")
    total_added = 0

    for scraper in SCRAPERS:
        # small delay between sites so we dont hit servers too fast
        time.sleep(random.uniform(2, 5))

        raw_items = scraper()
        if not raw_items:
            continue

        for item in raw_items:
            # cleaning basic fields, sometimes data is messy so we normalize here
            title = item.get("title", "")
            desc = item.get("description", "")

            clean_data = {
                "title": title,
                "type": detect_type(title),
                "source": item.get("source"),
                "organization": item.get("organization"),
                "location": detect_location(desc),
                "deadline": parse_date(item.get("deadline_raw")),
                "description": desc[:500],  # keeping it short, full text not needed anyway
                "tags": extract_tags(title + " " + desc),
                "link": item.get("link"),
            }

            # calculating score based on urgency and keywords
            clean_data["score"] = calculate_score(clean_data)

            # inserting into db storage, and skip if already exists
            if insert_data(clean_data):
                total_added += 1

    print(f"Pipeline done, added {total_added} new opportunities")


if __name__ == "__main__":
    main()