from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math
import nltk
from collections import Counter

nltk.download('punkt_tab')
nltk.download('stopwords')

def process_text(text):
	tokens = word_tokenize(text.lower())
	stop_words = set(stopwords.words("english"))
	return [word for word in tokens if word.isalnum() and word not in stop_words]

def calculate_idf(documents):
	N = len(documents)
	term_doc_count = Counter()

	for doc in documents:
		unique_terms = set(doc)
		for term in unique_terms:
			term_doc_count[term] += 1

	idf = {
		term: math.log((N + 1) / (count + 1)) + 1
		for term, count in term_doc_count.items()
	}
	return idf

def calculate_bm25(query_tokens, documents, idf, k1=1.5, b=0.75):
	scores = []
	avg_doc_len = sum(len(doc) for doc in documents) / len(documents)

	for doc in documents:
		doc_len = len(doc)
		score = 0
		for term in query_tokens:
			tf = doc.count(term)
			term_idf = idf.get(term, 0)
			numerator = tf * (k1 + 1)
			denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))
			score += term_idf * (numerator / denominator)
		scores.append(score)
	return scores
