import feedparser
from jinja2 import Environment, FileSystemLoader

# Define the arXiv categories you want to subscribe to
categories = ["physics.plasm-ph"]  # Change these to your preferred topics, e.g., "physics.optics"

# Base URL for arXiv RSS feeds
base_url = "http://arxiv.org/rss/"

# List to store paper details
papers = []

# Fetch and parse RSS feeds for each category
for category in categories:
    feed_url = base_url + category
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        paper_data = {
            'title': entry.title,
            'authors': ', '.join(author.name for author in entry.authors),
            'link': entry.link,
            'summary': entry.summary,
            'category': category
        }
        papers.append(paper_data)

# Render HTML using Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')
html_content = template.render(papers=papers)

# Save the HTML to index.html
with open('index.html', 'w') as f:
    f.write(html_content)