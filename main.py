# user_id = 10  # Substitua pelo ID de um usuário real
# api_key = rl_wwWRdoSYMyF8Ldpzt42FFPruH
from datetime import datetime, timedelta
from api_handler import fetch_data, parse_posts, parse_comments, parse_favorites, parse_tags, parse_tag_preferences, ENDPOINTS
from text_processer import process_text, calculate_idf, calculate_bm25
from rank_bm25 import BM25Okapi

USER_ID = "12345"  # Substitua pelo ID real do usuário
# ACCESS_TOKEN = "rl_wwWRdoSYMyF8Ldpzt42FFPruH"

# Coleta todos os dados do usuário
def fetch_user_data(user_id):
  data = {}

  # Posts
  posts = fetch_data(ENDPOINTS["user_posts"], user_id)
  data["posts"] = parse_posts(posts)

  # Comments
  comments = fetch_data(ENDPOINTS["user_comments"], user_id)
  data["comments"] = parse_comments(comments)

  # Favorites
  favorites = fetch_data(ENDPOINTS["user_favorites"], user_id)
  data["favorites"] = parse_favorites(favorites)

  # Tags
  tags = fetch_data(ENDPOINTS["user_tags"], user_id)
  data["tags"] = parse_tags(tags)

  # Tag Preferences
  # tag_preferences = fetch_data(ENDPOINTS["tag_preferences"], user_id, access_token=access_token)
  # data["tag_preferences"] = parse_tag_preferences(tag_preferences)

  return data

# Coleta postagens recentes
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
  posts = fetch_data(ENDPOINTS["posts"], None, params=params)
  return parse_posts(posts)

# Realiza recomendação de postagens com base na consulta do usuário e BM25
def recommend_posts(user_query, recent_posts):
  documents = [
    process_text(post.get("title", "") + " " + post.get("body", ""))
    for post in recent_posts
  ]

  print("Calculating IDF...")
  idf = calculate_idf(documents)

  # Processar consulta do usuário
  query_tokens = process_text(user_query)

  # Calcular BM25 e ranquear
  print("Ranking posts...")
  scores = calculate_bm25(query_tokens, documents, idf)
  ranked_posts = sorted(zip(recent_posts, scores), key=lambda x: x[1], reverse=True)[:5]

  # Exibir resultados
  print("\nRecommended Posts:")
  for i, (post, score) in enumerate(ranked_posts, 1):
    print(f"{i}. {post['title']} (Score: {score})")
    print(post)
    # print(f"   Link: {post['link']}\n")

def main():
  print("Fetching user data...")
  user_data = fetch_user_data(USER_ID)

  print("Processing user data...")
  all_text = []
  for key, values in user_data.items():
    if isinstance(values, list):
      for item in values:
        if isinstance(item, dict):  # Títulos e corpos
          all_text.append(item.get("title", "") + " " + item.get("body", ""))
        elif isinstance(item, str):  # Comentários, tags
          all_text.append(item)

  print("Fetching recent posts...")
  recent_posts = fetch_recent_posts()

  # Criar uma consulta com base nos dados do usuário
  user_query = " ".join(all_text[:5])  # Combina os primeiros 5 textos processados
  print(f"User query: {user_query}")

  recommend_posts(user_query, recent_posts)

if __name__ == "__main__":
  main()
