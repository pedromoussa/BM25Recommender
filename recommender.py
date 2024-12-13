from text_processer import process_text, calculate_idf
from rank_bm25 import BM25Okapi

def recommend_posts(user_query, recent_posts):
	documents = [process_text(content) for content in recent_posts.values()]
	
	print("Calculating IDF...")
	idf = calculate_idf(documents)

	query_tokens = user_query.split()  # Process the user query text

	print("Ranking posts...")
	scores = calculate_bm25(query_tokens, documents, idf)
	ranked_posts = sorted(zip(recent_posts.items(), scores), key=lambda x: x[1], reverse=True)[:5]

	print("\nRecommended Posts:")
	for i, ((question, post_link), score) in enumerate(ranked_posts, 1):
		print(f"{i}. {question} (Score: {score})")

def calculate_bm25(query_tokens, documents, idf, k1=1.5, b=0.75):
	scores = []
	avg_doc_len = sum(len(doc) for doc in documents) / len(documents)

	for doc in documents:
		doc_len = len(doc)
		score = 0
		for term in query_tokens:
			tf = doc.count(term)
			term_idf = idf.get(term, 0)  # Use the IDF for the term
			numerator = tf * (k1 + 1)
			denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))
			score += term_idf * (numerator / denominator)
		scores.append(score)
	return scores
