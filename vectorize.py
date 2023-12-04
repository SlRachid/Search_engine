# Save and Load your Index(es) in Pickle format
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
import pickle
import os
import pandas as pd





nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

def clean_post_vectorize(text: str) -> str:
    text=str(text)
    text = text.replace('"', '')
    text = text.lower()
    text = text.replace('\n', ' ')
    text = text.replace('<p>', '')
    text = text.replace('</p>', '')
    text = re.sub(r'[^\w\s]', '', text)
    sentence = text
    new_string = ""
    for word in sentence.split():
        pos_tag = nltk.pos_tag([word])[0][1][0].lower()
        try:
            new_word = lemmatizer.lemmatize(word, pos = pos_tag)
        except KeyError:
            new_word = lemmatizer.lemmatize(word)
        new_string = new_string + " " + new_word
    return new_string


def filter_vectorize(documents):
    stops = set(stopwords.words('english'))

    filtered_documents = []
    for doc in documents:
        words = doc.split()  # Divise le document en mots
        filtered_words = [word for word in words if word.lower() not in stops]  # Filtrer les mots qui ne sont pas des stop words
        filtered_document = " ".join(filtered_words)  # Rejoindre les mots filtrés pour reconstituer le document
        filtered_documents.append(filtered_document)



    # Create an instance of CountVectorizer
    vectorizer = CountVectorizer()

    # Fit the vectorizer to the documents and transform the documents into a matrix of token counts
    X = vectorizer.fit_transform(filtered_documents)


    # Print the feature names (tokens)
    feature_names = vectorizer.get_feature_names_out()

    return feature_names,X


def save_vectorizer(posts: pd.DataFrame, savepath: str):
    posts['cleaned_body_vectorize'] = posts.Body.apply(clean_post_vectorize)
    vocab, docs_matrix =filter_vectorize(posts['cleaned_body_vectorize'])

    # save as Vocabulaire.pkl and docs_matrix.pkl pickle files
    with open(os.path.join(savepath, 'Vocabulaire.pkl'), 'wb') as f:
        pickle.dump(vocab, f)

    with open(os.path.join(savepath, 'docs_matrix.pkl'), 'wb') as f:
        pickle.dump(docs_matrix, f)
