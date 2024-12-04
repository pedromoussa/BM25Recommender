import requests

API_BASE_URL = "https://api.stackexchange.com/2.3"

# Mapeamento de rotas da API
ENDPOINTS = {
  "posts": "/posts",
  "user_posts": "/users/{id}/posts?order=desc&sort=activity&site=stackoverflow",
  "user_comments": "/users/{id}/comments?order=desc&sort=creation&site=stackoverflow",
  "user_favorites": "/users/{id}/favorites?order=desc&sort=added&site=stackoverflow",
  "user_tags": "/users/{id}/tags?order=desc&sort=popular&site=stackoverflow",
  # "tag_preferences": "/users/{id}/tag-preferences?site=stackoverflow",
}

# Faz uma chamada genérica à API do Stack Exchange
def fetch_data(endpoint, user_id=None, params=None, access_token=None):
  if params is None:
    params = {}
  if user_id:
    endpoint = endpoint.format(id=user_id)
  if access_token:
    params["access_token"] = access_token
  url = f"{API_BASE_URL}{endpoint}"
  response = requests.get(url, params=params)
  response.raise_for_status()
  return response.json()

def parse_posts(posts):
  print("Posts fetched:", posts)
  if not posts or not isinstance(posts, dict) or "items" not in posts:
    return []
  return [{"title": post.get("title", ""), "body": post.get("body", "")} for post in posts.get("items", [])]

def parse_comments(comments):
  print("Comments fetched:", comments)
  if not comments or not isinstance(comments, dict) or "items" not in comments:
    return []
  return [comment.get("body", "") for comment in comments.get("items", [])]

def parse_favorites(favorites):
  print("Favorites fetched:", favorites)
  if not favorites or not isinstance(favorites, dict) or "items" not in favorites:
    return []
  return [{"title": fav.get("title", ""), "body": fav.get("body", "")} for fav in favorites.get("items", [])]

def parse_tags(tags):
  print("Tags fetched:", tags)
  if not tags or not isinstance(tags, dict) or "items" not in tags:
    return []
  return [tag.get("name", "") for tag in tags.get("items", [])]

def parse_tag_preferences(tag_preferences):
  print("Tag Preferences fetched:", tag_preferences)
  if not tag_preferences or not isinstance(tag_preferences, dict) or "items" not in tag_preferences:
    return []
  return [pref.get("tag_name", "") for pref in tag_preferences.get("items", [])]
