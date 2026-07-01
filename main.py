import requests
import os
import re
import time
import json
import hashlib
from markdownify import markdownify as md
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

output_folder = "optisigns_articles"
state_file = "sync_state.json"
os.makedirs(output_folder, exist_ok=True)

# find previous state file
if os.path.exists(state_file):
    with open(state_file, "r", encoding="utf-8") as f:
        sync_state = json.load(f)
else:
    sync_state = {}

# for logging
counts = {"added": 0, "updated": 0, "skipped": 0}

print("Start daily checking")

# Scraping
api_url = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json?per_page=30&sort_by=created_at&sort_order=asc"
response = requests.get(api_url)

if response.status_code == 200:
    articles = response.json().get('articles', [])
    
    for article in articles:
        title = article.get('title', 'Untitled')
        html_body = article.get('body', '')
        
        if not html_body: continue
            
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        markdown_content = f"# {title}\n\n{md(html_body, heading_style='ATX')}"
        
        # create a MD5 hash code for currnet content
        current_hash = hashlib.md5(markdown_content.encode('utf-8')).hexdigest()

        # actions categorize
        action = None
        if slug not in sync_state:
            action = "added"
        elif sync_state[slug] != current_hash:
            action = "updated"
        else:
            counts["skipped"] += 1
            continue
            
        # Save / Update if there are new changes in the files
        file_path = os.path.join(output_folder, f"{slug}.md")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(markdown_content)
            
        print(f"({action}): {slug}.md")
        client.files.upload(
            file=file_path, 
            config={'display_name': f"{slug}.md", 'mime_type': 'text/plain'}
        )
        
        # update state and counters
        sync_state[slug] = current_hash
        counts[action] += 1
        time.sleep(2)

    # saved newst state for next run
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(sync_state, f, indent=4)
        
    # print result
    print("\n=== Daily Results ===")
    print(f"Added:   {counts['added']}")
    print(f"Updated: {counts['updated']}")
    print(f"Skipped: {counts['skipped']}")
    
else:
    print(response.status_code)