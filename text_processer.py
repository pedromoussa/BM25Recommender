import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def process_text(text):
	# Tokenize and clean the text: lowercasing, stopword removal, and lemmatization
	tokens = word_tokenize(text.lower())
	stop_words = set(stopwords.words("english"))
	tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

	lemmatizer = WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(word) for word in tokens]

	return " ".join(tokens)

def build_user_query(user_data):
	all_text = []
	
	# Process user posts
	if "posts" in user_data:
		for post_data in user_data["posts"]:
			processed_text = process_text(post_data)
			all_text.append(processed_text)  # Process each post content

	# Process user tags
	if "tags" in user_data:
		tags_text = " ".join(user_data["tags"])  # Join tags into a string and process
		processed_tags = process_text(tags_text)
		all_text.append(processed_tags)
	
	combined_text = " ".join(all_text)
	word_counts = Counter(combined_text.split())
	
	# Get the most common 5 words
	most_common_words = [word for word, _ in word_counts.most_common(5)]

	# Combine the processed texts into one query
	user_query = " ".join(most_common_words)  # Adjust based on your requirement
	print(f"Processed User Query: {user_query}")
	
	return user_query

def build_user_query_tfidf(user_data):
	all_text = []

	if "posts" in user_data:
		for post_data in user_data["posts"]:
			processed_text = process_text(post_data)
			all_text.append(processed_text)
	
	if "tags" in user_data:
		tags_text = " ".join(user_data["tags"])
		processed_tags = process_text(tags_text)
		all_text.append(processed_tags)
	
	combined_text = " ".join(all_text)
	
	documents = [combined_text]
	
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform(documents)
	feature_names = vectorizer.get_feature_names_out()
	
	user_tfidf_vector = tfidf_matrix[0].toarray()[0]
	tfidf_scores = {feature_names[i]: user_tfidf_vector[i] for i in range(len(feature_names))}
	
	sorted_terms = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
	most_important_terms = [term for term, score in sorted_terms[:5]]
	
	user_query = " ".join(most_important_terms)
	print(f"Processed User Query with TF-IDF: {user_query}")
	
	return user_query

def calculate_idf(documents):
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform(documents)
	idf = vectorizer.idf_
	vocab = vectorizer.get_feature_names_out()

	idf_dict = {vocab[i]: idf[i] for i in range(len(vocab))}
	return idf_dict
