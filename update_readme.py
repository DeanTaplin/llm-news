import os
import json
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

def search_brave(query, count=20):
    api_key = os.environ.get('BRAVE_API_KEY')
    headers = {'X-Subscription-Token': api_key}
    url = 'https://api.search.brave.com/res/v1/web/search'
    params = {
        'q': query,
        'count': count
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def generate_readme_content(news_data):
    current_date = datetime.now().strftime("%B %Y")
    
    content = f"""# LLM News Tracker

A curated collection of the latest developments, breakthroughs, and news in the field of Large Language Models (LLMs).

## Latest Updates ({current_date})

### Major Model Releases & Improvements
"""
    
    # Process and categorize news here
    model_releases = []
    innovations = []
    market_trends = []
    
    # Categorize news based on content
    for item in news_data.get('web', {}).get('results', []):
        title = item.get('title', '')
        description = item.get('description', '')
        url = item.get('url', '')
        
        # Simple categorization based on keywords
        content_text = f"{title} {description}".lower()
        
        news_item = f"- **{title}**\n  - {description}\n  - [Source]({url})\n"
        
        if any(keyword in content_text for keyword in ['release', 'launch', 'version', 'model', 'gpt', 'claude', 'gemini']):
            model_releases.append(news_item)
        elif any(keyword in content_text for keyword in ['breakthrough', 'innovation', 'research', 'discover']):
            innovations.append(news_item)
        elif any(keyword in content_text for keyword in ['market', 'growth', 'trend', 'industry', 'adoption']):
            market_trends.append(news_item)
    
    # Add model releases section
    if model_releases:
        content += "\n### Major Model Releases & Improvements\n\n"
        content += "\n".join(model_releases[:5])  # Limit to top 5
    
    # Add innovations section
    if innovations:
        content += "\n### Notable Innovations\n\n"
        content += "\n".join(innovations[:5])  # Limit to top 5
    
    # Add market trends section
    if market_trends:
        content += "\n### Market Trends\n\n"
        content += "\n".join(market_trends[:5])  # Limit to top 5
    
    # Add the standard sections
    content += """
## Contributing

To contribute to this news tracker:

1. Fork the repository
2. Add your news item in the appropriate section
3. Include:
   - Clear, concise summary
   - Date of announcement/development
   - Reliable source link
   - Any relevant technical details
4. Submit a pull request

## News Categories

- Model Releases
- Research Breakthroughs
- Industry Applications
- Market Developments
- Technical Innovations
- Policy & Regulation
- Open Source Developments

## Update Schedule

This repository is updated weekly with the latest developments in the LLM space. Each update includes verification from multiple sources when available.

## Disclaimer

The information provided in this repository is compiled from various sources and may not be comprehensive. Always refer to the original sources for complete details and verify information independently.

## License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""
    
    return content

def main():
    # Search for latest LLM news
    query = "LLM AI language model news last week"
    news_data = search_brave(query)
    
    # Generate new README content
    new_content = generate_readme_content(news_data)
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
