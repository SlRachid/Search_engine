from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

with open(DATAPATH + '/lda_model.pkl', 'rb') as f:
    lda_model = pickle.load(f)

with open(DATAPATH + '/vectorizer_lda.pkl', 'rb') as f:
    vectorizer_lda = pickle.load(f)

# Get the most probable topic for each document
train_data = vectorizer_lda.transform(posts.cleaned_body.values)
topic_assignments = lda_model.transform(train_data)
most_probable_topics = []
for sublist in topic_assignments:
    max_indices = sorted(enumerate(sublist), key=lambda x: x[1], reverse=True)[:3]
    most_probable_topics.append([index for index, _ in max_indices])

topic_documents = defaultdict(list)
for i, document in enumerate(posts.Id.values) :
    for j in range(3) :
        topic_documents[most_probable_topics[i][j]].append(document)


def get_topic_query(query, vectorizer=vectorizer_lda, lda_model=lda_model) -> int:
    vector = vectorizer_lda.transform([query])
    topic_assignement = lda_model.transform(vector)
    most_probable_topics = topic_assignments.argmax(axis=1)


    return most_probable_topics[0]