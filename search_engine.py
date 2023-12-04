import torch
from Extract_Clean import clean_post
import numpy as np 
import math
from embeddings import load_embeddings_and_models   
import os
import pickle
from semantic_search import encode_query, order_similarity



MAIN_PATH = ".\Search_engine"
DATA_PATH = ".\Search_engine\data"

with open(os.path.join(DATA_PATH, 'posts.pkl'), 'rb') as f:
    posts = pickle.load(f)

with open(DATA_PATH + '/lda_model.pkl', 'rb') as f:
    lda_model = pickle.load(f)

with open(DATA_PATH + '/vectorizer_lda.pkl', 'rb') as f:
    vectorizer_lda = pickle.load(f)

question_query_model, answer_query_model, embeddings_titles, embeddings_answer = load_embeddings_and_models()



coeff1 = 0.3
coeff2 = 0.2
coeff3 = 0.5

def vectorizer_search_clustering(query,docs_matrix, Vocabulaire) -> list:
    Vector_query=vectorize_query_clustering(query, docs_matrix, Vocabulaire)
    L=[]
    Vector_query=torch.Tensor(Vector_query).to("cuda")
    Acoo = docs_matrix.tocoo()
    aa = torch.sparse.LongTensor(torch.LongTensor([Acoo.row.tolist(), Acoo.col.tolist()]),
                                 torch.LongTensor(Acoo.data.astype(np.int32))).to("cuda")
    L = []
    for i in range(0, docs_matrix.shape[0]):
        with torch.no_grad():
            L.extend(torch.cosine_similarity(Vector_query, aa[i].to_dense().unsqueeze(0)).cpu().numpy())
    return(L)
#vectorizer_search("how to learn AI",docs_matrix)

def vectorize_query_clustering(query, matrix_docs, Vocabulaire):
    L=[]
    query = clean_post(query)
    L=query.split()

    vector_L=[0]*len(Vocabulaire)
    for i in L:
        if i in Vocabulaire:
            index = np.where(Vocabulaire == i)[0][0]
            vector_L[index]+=1
    return vector_L

def similarity_clustering(query, model, relevant_posts, embeddings=embeddings_answer, batch_size=1024):
    query_embedding = encode_query(query, model)
    relevant_id = list(relevant_posts["Id"])
    filtered_embeddings = {post_id : embeddings[post_id] for post_id in relevant_id}
    # query_embedding = torch.stack([query_embedding])
    scores = []
    for i in range(0, len(filtered_embeddings), batch_size):
        id = int(relevant_posts['Id'].iloc[i])
        key_embedding = torch.stack(list(filtered_embeddings.values())[i:i+batch_size])
        with torch.no_grad():
            score = torch.cosine_similarity(query_embedding, key_embedding)
        scores.extend(list(score.cpu().detach().numpy()))
    return np.array(scores)

def similarities_title_clustering(query, model, relevant_posts, embeddings = embeddings_titles, batch_size = 1024) :
    query_embedding = encode_query(query, model)
    scores = []
    relevant_id = list(relevant_posts["Id"])
    filtered_embeddings = [embeddings[post_id] for post_id in relevant_id]
    for i in range(0, len(filtered_embeddings), batch_size):
        # title_id = relevant_posts['Id'].iloc[i]
        # if math.isnan(title_id) :
        #     id = int(relevant_posts['ParentId'].iloc[i])
        #     key_embedding = filtered_embeddings[id]
        # else :
        #     title_id = int(title_id)
        #     index_parent = relevant_posts[relevant_posts['Id'] == title_id]['Id'].iloc[0]
        #     key_embedding = filtered_embeddings[index_parent]
        key_embedding = torch.stack(filtered_embeddings[i:i+batch_size])
        with torch.no_grad():
            score = torch.cosine_similarity(query_embedding, key_embedding)
        scores.extend(score.cpu().detach().numpy())

    return np.array(scores)

def search_engine_clustering(query, vectorizer=vectorizer_lda, lda_model=lda_model, top_n=None) :
    #topic_query = get_topic_query(query, vectorizer, lda_model)
    #relevant_docs = topic_documents[topic_query]

    relevant_posts = posts#[posts['Id'].isin(relevant_docs)]
    # Vocabulaire, matrix_docs=filter_vectorize(relevant_posts['cleaned_body'])

    similarity_semantic_answer = similarity_clustering(query, answer_query_model, relevant_posts, embeddings=embeddings_answer, batch_size=1024)
    # similarity_vectorize = np.array(vectorizer_search_clustering(query, matrix_docs, Vocabulaire))
    similarity_title = similarities_title_clustering(query, question_query_model, relevant_posts, embeddings = embeddings_titles, batch_size = 1024)

    similarity_pond = similarity_semantic_answer * coeff1 + similarity_title * coeff3

    ordre = order_similarity(similarity_pond)
    top_posts = relevant_posts.iloc[ordre]

    top_posts["ParentId"] = top_posts["ParentId"].fillna(top_posts["Id"])
    top_posts_id = top_posts["ParentId"]
    # drop duplicates top_posts
    top_posts_id = top_posts_id.drop_duplicates(keep='first')

    # get top_posts where id is top_posts_id
    top_posts = top_posts[top_posts["ParentId"].isin(top_posts_id)]

    if top_n is not None:
      top_posts = top_posts.iloc[:top_n]

    return top_posts






if __name__ == "__main__":
    query = "how to learn AI"
    result = search_engine_clustering(query, top_n= 20 )
    print(result["Title"])
