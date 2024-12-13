from api_handler import fetch_user_data, fetch_recent_posts
from text_processer import build_user_query, build_user_query_tfidf
from recommender import recommend_posts

USER_ID = "12345"

def main():
    print("Fetching user data...")
    user_data = fetch_user_data(USER_ID)

    print("Processing user data...")
    # user_query = build_user_query(user_data)
    user_query = build_user_query_tfidf(user_data)

    print("Fetching recent posts...")
    recent_posts = fetch_recent_posts()

    recommend_posts(user_query, recent_posts)

if __name__ == "__main__":
  main()
