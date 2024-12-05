import requests
from web_scrapper import scrape_post_content
from datetime import datetime, timedelta

API_BASE_URL = "https://api.stackexchange.com/2.3"

# Mapeamento de rotas da API
ENDPOINTS = {
  "questions": "/questions",
  "user_posts": "/users/{id}/posts?order=desc&sort=activity&site=stackoverflow",
  "user_tags": "/users/{id}/tags?order=desc&sort=popular&site=stackoverflow",
}

# Faz uma chamada genérica à API do Stack Exchange
def fetch_data(endpoint, user_id=None, params=None):
  if params is None:
    params = {}
  if user_id:
    endpoint = endpoint.format(id=user_id)
  url = f"{API_BASE_URL}{endpoint}"
  response = requests.get(url, params=params)
  response.raise_for_status()
  return response.json()

def fetch_user_data(user_id):
  data = {}

  # Fetch posts and extract links
  posts = fetch_data(ENDPOINTS["user_posts"], user_id)
  post_links = parse_posts(posts)

  # Scrape content for each post
  data["posts"] = []
  for post in post_links:
    scraped_data = scrape_post_content(post["link"])
    if scraped_data:
      content, _, _ = scraped_data
      data["posts"].append(content)

  # Tags
  tags = fetch_data(ENDPOINTS["user_tags"], user_id)
  data["tags"] = parse_tags(tags)

  return data

def fetch_recent_posts():
  to_date = int(datetime.utcnow().timestamp())
  from_date = int((datetime.utcnow() - timedelta(days=7)).timestamp())
  params = {
    "fromdate": from_date,
    "todate": to_date,
    "order": "desc",
    "sort": "activity",
    "site": "stackoverflow"
  }
  posts = fetch_data(ENDPOINTS["questions"], None, params=params)
  post_links = parse_posts(posts)

  recent_posts = {}
  for post in post_links:
    scraped_data = scrape_post_content(post["link"])
    if scraped_data:
      content, question, post_link = scraped_data
      recent_posts[(question, post_link)] = content

  return recent_posts

def parse_posts(posts):
  if not posts or not isinstance(posts, dict) or "items" not in posts:
    return []
  
  # Extract only the post link
  return [{"link": post.get("link", "")} for post in posts.get("items", [])]

def parse_tags(tags):
  if not tags or not isinstance(tags, dict) or "items" not in tags:
    return []

  # Extract all tags under collectives -> tags
  unique_tags = set()
  for item in tags.get("items", []):
    collectives = item.get("collectives", [])
    for collective in collectives:
      tags_list = collective.get("tags", [])
      unique_tags.update(tags_list)

  return list(unique_tags)
