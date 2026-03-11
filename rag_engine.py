from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

def build_index(text):

    chunks = text.split(". ")
    vectors = vectorizer.fit_transform(chunks)

    return chunks, vectors


def search(query,chunks,vectors):

    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec,vectors)

    idx = sims.argmax()

    return chunks[idx]