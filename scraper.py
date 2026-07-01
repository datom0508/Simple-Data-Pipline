import requests
import os
import re
from markdownify import markdownify as md

output_folder = "optisigns_articles"
os.makedirs(output_folder, exist_ok=True)

api_url = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json?per_page=30&sort_by=created_at&sort_order=asc"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    articles = data.get('articles', [])
        
    for article in articles:
        # get title and body of the article
        title = article.get('title', 'Untitled')
        html_body = article.get('body', '')
        
        # if the article doest has body
        if not html_body:
            continue
            
        # create slug to use as file name
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        
        # convert html to markdown
        markdown_content = md(html_body, heading_style="ATX")
        
        # add title to markdown file
        final_markdown = f"# {title}\n\n{markdown_content}"
        
        # save to file
        file_path = os.path.join(output_folder, f"{slug}.md")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_markdown)
            
        print(f"saved: {slug}.md")
        
    print("\nscrape completed")
else:
    print(response.status_code)