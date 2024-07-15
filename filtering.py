import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Ensure you have the necessary NLTK data files
nltk.download("punkt")
nltk.download("wordnet")

# Example known and new terms
known_terms = [
    "palazzo pants",
    "mom jeans",
    "skinny jeans",
    "crop tops",
    "linen undergarment",
    "Printed cotton pyjamas",
    "Printed cotton pyjamas",
    "Printed pyjamas",
    "5-pack printed boys’ briefs",
    "2-piece hoodie and leggings set",
    "Printed pyjamas",
    "Motif-detail cap",
    "Oversized printed T-shirt",
    "2-piece printed cotton set",
    "Printed sweatshirt",
    "2-piece printed cotton set",
    "Bow-detail dress",
    "Printed sweatshirt",
    "2-pack long-sleeved jersey tops",
    "Ribbed T-shirt",
    "Relaxed Fit Appliquéd Jeans",
    "5-pack patterned socks",
    "Ribbed T-shirt",
    "Printed pyjamas",
    "Printed pyjamas",
    "Motif-detail cap",
]
new_terms = [
    "balloon palazzo pants",
    "flared jeans",
    "tie-dye crop tops",
    "linen kerchiefs",
    "polo shirt",
    "sleeveless tank top",
]

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()


def preprocess(text):
    words = word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in words if word.isalnum()]
    return words


# Preprocess terms
preprocessed_known_terms = [preprocess(term) for term in known_terms]
preprocessed_new_terms = [preprocess(term) for term in new_terms]

# Combine all terms for training the Word2Vec model
all_terms = preprocessed_known_terms + preprocessed_new_terms

# Train Word2Vec model
model = Word2Vec(all_terms, vector_size=100, window=5, min_count=1, workers=4)


def get_vector(term):
    words = preprocess(term)
    term_vector = np.mean(
        [model.wv[word] for word in words if word in model.wv], axis=0
    )
    return term_vector


# Calculate similarity scores
similarity_scores = {}
for new_term in new_terms:
    new_vector = get_vector(new_term)
    scores = {}
    for known_term in known_terms:
        known_vector = get_vector(known_term)
        score = cosine_similarity([new_vector], [known_vector])[0][0]
        scores[known_term] = score
    similarity_scores[new_term] = scores

# Output similarity scores
for new_term, scores in similarity_scores.items():

    for known_term, score in scores.items():

        if score > 0.50:
            print(new_term)
            break
