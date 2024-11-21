import requests
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import nltk
from collections import Counter

# Certifique-se de que as dependências estão instaladas
# pip install requests nltk rank_bm25

nltk.download('punkt')  # Necessário para tokenização

# Função para obter dados relevantes de um usuário
def get_user_data(user_id):
    url = f"https://api.stackexchange.com/2.3/users/{user_id}/answers?site=stackoverflow&filter=withbody"
    response = requests.get(url)
    data = response.json()
    
    # Extrair respostas e perguntas com o título e o corpo
    user_data = []
    for item in data['items']:
        user_data.append(item['title'] + " " + item['body'])
    
    # Você pode adicionar outras informações, como comentários e favoritos, aqui.
    return user_data

# Função para extrair palavras-chave e fazer a tokenização
def process_text(text):
    tokens = word_tokenize(text.lower())  # Tokenizar e normalizar para minúsculas
    return tokens

# Função para construir a query do BM25 com base no histórico do usuário
def build_query(user_data):
    all_tokens = []
    
    # Concatenar todos os textos do histórico e tokenizar
    for text in user_data:
        all_tokens.extend(process_text(text))
    
    # Criar a consulta ponderada, considerando a frequência dos termos
    term_freq = Counter(all_tokens)
    query_tokens = list(term_freq.keys())
    
    return query_tokens

# Função para buscar postagens relacionadas à consulta do usuário
def search_related_posts(query_tokens):
    query = " ".join(query_tokens)
    url = f"https://api.stackexchange.com/2.3/search/advanced?key=rl_wwWRdoSYMyF8Ldpzt42FFPruH&q={query}&site=stackoverflow"
    response = requests.get(url)
    data = response.json()
    posts = data.get('items', [])
    
    return posts

# Função para aplicar o BM25 para ranquear postagens
def rank_with_bm25(query_tokens, posts):
    # Tokenizar o conteúdo das postagens
    documents = []
    
    for post in posts:
        if 'body' in post:  # Se for uma resposta
            document = post['body']
        else:  # Caso contrário, deve ser uma pergunta
            document = post.get('title', '')  # Utiliza o título da pergunta

    # Processamento do texto (tokenização, remoção de stopwords, etc)
    processed_text = process_text(document)
    documents.append(processed_text)

    # Inicializar o BM25
    bm25 = BM25Okapi(documents)
    
    # Calcular as pontuações BM25 para cada postagem
    scores = bm25.get_scores(query_tokens)
    
    # Classificar postagens com base nas pontuações BM25
    ranked_posts = sorted(zip(posts, scores), key=lambda x: x[1], reverse=True)
    
    return ranked_posts

# Função principal para o sistema de recomendação
def recommend_posts(user_id):
    # Obter dados do usuário
    user_data = get_user_data(user_id)
    
    # Construir a query para o BM25
    query_tokens = build_query(user_data)
    
    # Buscar postagens relacionadas
    related_posts = search_related_posts(query_tokens)
    
    # Aplicar o BM25 para ranquear as postagens
    ranked_posts = rank_with_bm25(query_tokens, related_posts)
    
    # Exibir as postagens recomendadas, da maior para a menor pontuação
    print("Top 5 Postagens Recomendadas:")
    for i, (post, score) in enumerate(ranked_posts[:5]):
        print(f"{i+1}. {post['title']} - Pontuação BM25: {score}")
        print(f"   Link: {post['link']}\n")

# Exemplo de uso: fornecer o ID do usuário
user_id = 10  # Substitua pelo ID de um usuário real
recommend_posts(user_id)
