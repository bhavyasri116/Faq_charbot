import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load English model
nlp = spacy.load("en_core_web_sm")

# Sample FAQs and answers
questions = [
    "Where is my order?",
    "How can I track my order?",
    "Can I get a refund?",
    "How do I return a product?",
    "Do you ship internationally?",
    "What is the return policy?"
]

answers = [
    "You can track your order using the tracking number sent to your email.",
    "You can track your order using the tracking number sent to your email.",
    "You can return any item within 30 days of purchase.",
    "Visit our returns page and follow the instructions to return a product.",
    "Yes, we ship to most countries worldwide.",
    "You can return any item within 30 days if it’s unused and in original condition."
]

# Preprocessing function using spaCy
def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Preprocess questions
preprocessed_questions = [preprocess(q) for q in questions]

# Vectorize questions
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(preprocessed_questions)

print("🤖 Welcome to the spaCy FAQ Chatbot! (Type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("🤖 Goodbye!")
        break

    processed_input = preprocess(user_input)
    input_vector = vectorizer.transform([processed_input])
    similarity = cosine_similarity(input_vector, faq_vectors)

    max_index = similarity.argmax()
    max_score = similarity[0][max_index]

    if max_score > 0.3:
        print("🤖", answers[max_index])
    else:
        print("🤖 I'm sorry, I don't understand. Could you rephrase?")
