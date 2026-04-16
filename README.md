<h1>🚀 OppHub</h1>

OppHub is basically a smart system that collects useful opportunities from across the internet and puts them in one place. Instead of checking different websites for internships, hackathons, or jobs, this does that work for you.

It runs automatically, scrapes public data, cleans it, and shows everything in a fast, simple dashboard where you can search and filter easily.

<h2>🤔 What is the use of this?</h2>

If you're a student (or even just someone looking for opportunities), you probably know this problem:

internships are on one site
hackathons somewhere else
research openings hidden on university pages
jobs scattered everywhere

So most people either miss deadlines or never even find good opportunities.

👉 This project solves that.

It collects everything into one place so you can:

quickly find opportunities
filter by type (internship, hackathon, job, etc.)
check deadlines easily
avoid missing important stuff

In short, it saves time and makes things way less messy.

<h2>How the system works</h2>

<h3>The project is split into 3 simple parts:</h3>

1. Backend (Scrapers)

These are Python scripts that go to different websites and collect data.

Uses Playwright for modern sites (React/JS heavy)
Uses BeautifulSoup for simpler pages
Handles scrolling, popups, dynamic content etc

Basically, it behaves like a real user and pulls useful info.

2. Database (Supabase / PostgreSQL)

All scraped data goes into Supabase.

Stores everything in one place
avoids duplicates using upsert
acts like the central storage

Think of this as the "brain" of the system.

3. Frontend (HTML + JS)

This is the UI you actually see.

simple static webpage
fetches data directly from Supabase
fast and lightweight
supports search + filters

No heavy backend needed here, which is kinda nice.

<h2>⚡ How everything connects</h2>
Scrapers collect raw data
Cleaner processes and formats it
Data gets stored in Supabase
Frontend fetches and displays it

That's it — simple flow, but quite effective.

<h2>💡 Why this project is useful</h2>
saves time (no need to check multiple sites)
helps students discover hidden opportunities
reduces chance of missing deadlines
clean and organized view of scattered data
<h2>🧠 Final thought</h2>

This is not just a scraper — it’s more like a personal opportunity tracker.

You can also extend it later:

add alerts
add AI recommendations
add more sources
🚀 Future ideas (optional)
email notifications for new opportunities
personalized recommendations
better ranking system
mobile-friendly UI

## 📂 Folder Structure

```text
│── main.py                                    
│── index.html              
│── requirements.txt        
│
├── scrapers/                    
│   ├── iit_delhi.py       
│   ├── iit_roorkee.py            
│   ├── ncs_india.py
│   ├── buddy4study.py
│   ├── csir_nbri.py
│   ├── unstop.py       
│   ├── linkedin.py         
│   └── devfolio.py         
│
└── utils/                      
    └── cleaner.py
    └── scorer.py
    └── supabase_client.py
