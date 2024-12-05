from bs4 import BeautifulSoup
import requests

def scrape_post_content(post_link):
	try:
		# Fetch the page content
		response = requests.get(post_link)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, 'html.parser')

		# Extract the question title
		title_tag = soup.find("a", class_="question-hyperlink")
		question_title = title_tag.get_text(strip=True) if title_tag else ""

		# Combine all content (title, question body, and answers)
		content = [question_title]

		# Extract all text from "s-prose js-post-body" (question body and answers)
		prose_tags = soup.find_all("div", class_="s-prose js-post-body")
		for tag in prose_tags:
			paragraphs = [p.get_text(strip=True) for p in tag.find_all("p")]
			content.extend(paragraphs)

		# Combine into a single string
		full_text = " ".join(content)
		return full_text, question_title, post_link

	except requests.RequestException as e:
		print(f"Error fetching the page: {e}")
		return "", "", ""