import os
import arxiv
import openai
from jinja2 import Environment, FileSystemLoader
import time
import requests
import ssl
import urllib.request
import certifi

# Define search query and parameters
query = "cat:astro-ph.HE"  # Modify this to your interest
max_results = 10

# Set up arXiv client
client = arxiv.Client()

# Search for papers
search = arxiv.Search(
    query=query,
    max_results=max_results,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

# Set up an SSL context with certifi's CA bundle
context = ssl.create_default_context(cafile=certifi.where())
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
urllib.request.install_opener(opener)

papers = []

for result in client.results(search):
    try:
        abstract = result.summary
        # Create prompt for summarization
        prompt = f"Summarize this abstract in one sentence: {abstract}"
        # Call OpenAI API for summarization
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 9014dee5-9a23-44d1-b4fb-cc59c9ad0b6b"
        }
        data = {
            "model": "deepseek-r1-250120",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()
        summary = response_data['choices'][0]['message']['content'].strip()
        # Collect paper data
        paper_data = {
            'title': result.title,
            'authors': ', '.join(author.name for author in result.authors),
            'published': result.published.strftime('%Y-%m-%d'),
            'url': result.entry_id,
            'summary': summary
        }
        papers.append(paper_data)
        time.sleep(1)  # Delay to respect API rate limits
    except Exception as e:
        print(f"Error processing paper {result.entry_id}: {e}")

# Render HTML using Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')
html_content = template.render(papers=papers)

# Save the HTML content to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)