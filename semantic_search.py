import math

def encode_query(query : str, model) -> torch.Tensor:
    return model.encode([query], normalize_embeddings=True, convert_to_tensor=True)

def similarity(query: str, model: SentenceTransformer, embeddings: torch.Tensor, batch_size: int = 1024) -> np.array:
    query_embedding = encode_query(query, model)
    # query_embedding = torch.stack([query_embedding])
    scores = []
    for i in range(0, len(embeddings), batch_size):
        key_embedding = torch.stack(embeddings[i:i+batch_size])
        with torch.no_grad():
            score = torch.cosine_similarity(query_embedding, key_embedding)
        scores.extend(score.cpu().detach().numpy())

    return np.array(scores)

def similarity_order(matrix_similarity) -> List[int]:
    return list(np.argsort(-np.array(matrix_similarity)))

def closest_semantic_doc(query: str, model: SentenceTransformer, embeddings: torch.Tensor, top_n: int = 10) -> pd.DataFrame:
    matrix_similarity = similarity(query, model, embeddings)
    ordre = similarity_order(matrix_similarity)
    # ordre is index, return clean_posts at indices ordre
    return posts.iloc[ordre[:top_n]]


def similarities_title(query: str, model: SentenceTransformer, embeddings: torch.Tensor = embeddings_titles, batch_size: int = 1024) -> np.array:
    query_embedding = encode_query(query, model)
    scores = []
    for i in range(0, len(embeddings)):
        title_id = posts['ParentId'].iloc[i]
        if math.isnan(title_id) :
            key_embedding = embeddings[i]
        else :
            title_id = int(title_id)
            index_parent = posts[posts['Id'] == title_id].index.values.tolist()[0]
            key_embedding = embeddings[index_parent]
        with torch.no_grad():
            score = torch.cosine_similarity(query_embedding, key_embedding)
        scores.extend(score.cpu().detach().numpy())

    return np.array(scores)


def order_similarity(matrix_similarity):
    return list(np.argsort(-np.array(matrix_similarity)))


