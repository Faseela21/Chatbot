import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Load the stopwords
stop_words = set(stopwords.words('english'))

# Function to preprocess text (tokenization and stop word removal)
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    
    # Remove stop words
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Join the tokens back into a string
    return " ".join(filtered_tokens)

# Load the JSON data
with open('data.json', 'r') as f:
    data = json.load(f)

# Extract all keywords, and answers
keywords = []
answers = []

for section in data:
    for category in data[section]:
        for qa in data[section][category]:
            # Preprocess the keywords using NLTK
            preprocessed_keywords = preprocess_text(" ".join(qa['Keywords']))
            keywords.append(preprocessed_keywords)  # Add the preprocessed keywords to the list
            answers.append(qa['Answer'])

# Fit the vectorizer to the preprocessed keywords
vectorizer = TfidfVectorizer()
vectorizer.fit(keywords)

def find_best_match(query):
    # Preprocess the query using NLTK
    preprocessed_query = preprocess_text(query)
    
    # Vectorize the preprocessed query using the fitted vectorizer
    query_vec = vectorizer.transform([preprocessed_query])

    # Compute cosine similarity
    cosine_similarities = cosine_similarity(query_vec, vectorizer.transform(keywords)).flatten()

    # Find the index of the best match
    best_match_idx = np.argmax(cosine_similarities)

    # Check if the best match is above a certain threshold
    threshold = 0.2  # Adjust this based on your needs
    if cosine_similarities[best_match_idx] > threshold:
        return best_match_idx
    else:
        return None

def chatbot_response(query):
    match_idx = find_best_match(query)
    if match_idx is not None:
        return answers[match_idx]
    else:
        return "I couldn't find a relevant answer. Please try rephrasing your query or providing more context."


