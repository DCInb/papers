import requests
import feedparser

# Fetch the feed using requests
feed_url = "http://arxiv.org/rss/physics.plasm-ph"
response = requests.get(feed_url)

if response.status_code == 200:
    # Parse the content with feedparser
    feed = feedparser.parse(response.content)
    if feed.bozo == 0:
        print("Feed parsed successfully!")
    else:
        print(f"Error parsing feed: {feed.bozo_exception}")
else:
    print(f"Failed to fetch feed: {response.status_code}")

categories = ["physics.plasm-ph"]
base_url = "http://arxiv.org/rss/"
papers = []

for category in categories:
    feed_url = base_url + category
    try:
        feed = feedparser.parse(feed_url)
        if feed.bozo == 0:
            for entry in feed.entries:
                paper_data = {
                    'title': entry.title,
                    'authors': ', '.join(author.name for author in entry.authors),
                    'link': entry.link,
                    'summary': entry.summary,
                    'category': category
                }
                papers.append(paper_data)
        else:
            print(f"Error parsing feed for {category}: {feed.bozo_exception}")
    except Exception as e:
        print(f"Exception for {category}: {e}")