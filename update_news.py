import requests
import json
from datetime import datetime, timedelta
import os
from dateutil.parser import parse

def fetch_news():
    headers = {
        'Accept': 'application/json',
        'X-Subscription-Token': 'BSAHUTubNaMWRSSxHZv4f6j4aOTODeX'
    }
    
    params = {
        'q': 'LLM AI news ChatGPT Claude Gemini -site:reddit.com',
        'count': 20,
        'freshness': 'pw' # past week
    }
    
    response = requests.get(
        'https://api.search.brave.com/res/v1/web/search',
        headers=headers,
        params=params
    )
    
    return response.json()

def format_news(articles):
    now = datetime.now()
    
    # Archive current README content
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        # Create archives directory if it doesn't exist
        os.makedirs('archives', exist_ok=True)
        
        # Save to archive with date
        archive_path = f'archives/news-{now.strftime("%Y-%m-%d")}.md'
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(old_content)
    except FileNotFoundError:
        pass
    
    # Create new content
    content = f"# LLM News Update - {now.strftime('%B %Y')}\n\n"
    content += "A curated collection of the latest developments in Large Language Models (LLMs) and AI.\n\n"
    content += f"Last updated: {now.strftime('%B %d, %Y')}\n\n"
    content += "## Latest Developments\n\n"
    
    for article in articles.get('web', {}).get('results', []):
        title = article.get('title', '').replace('|', '-')
        description = article.get('description', '')
        url = article.get('url', '')
        
        content += f"### {title}\n"
        content += f"**Summary:** {description}\n\n"
        content += f"**Source:** [{url.split('/')[2]}]({url})\n\n"
    
    content += "---\n\n"
    content += "## Previous Updates\n\n"
    content += "Previous news updates are archived in the [archives](./archives) directory.\n\n"
    content += "---\n\n"
    content += "## Contributing\n\n"
    content += "Feel free to submit pull requests with new articles or updates. Please ensure all submissions include:\n"
    content += "- Clear headline\n"
    content += "- Brief summary\n"
    content += "- Reliable source link\n"
    content += "- Date of publication"
    
    return content

def main():
    try:
        # Fetch news
        news_data = fetch_news()
        
        # Format content
        content = format_news(news_data)
        
        # Write to README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
