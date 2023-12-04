import numpy as np
import torch
from Extract_Clean import clean_post





def vectorize_query(query: str, vocabulaire: np.ndarray):
    query = clean_post(query)
    L = query.split()

    vector_L=[0]*len(vocabulaire)
    for i in L:
        if i in vocabulaire:
            index = np.where(vocabulaire == i)[0][0]
            vector_L[index]+=1
    return vector_L

def vectorizer_search(query: str, vocabulaire: np.ndarray, docs_matrix: np.ndarray):
    Vector_query=vectorize_query(query, vocabulaire)
    Vector_query=torch.Tensor(Vector_query).to("cuda")
    L = []
    Acoo = docs_matrix.tocoo()
    sparse_docs_matrix = torch.sparse.LongTensor(torch.LongTensor([Acoo.row.tolist(), Acoo.col.tolist()]),
                                torch.LongTensor(Acoo.data.astype(np.int32))).to("cuda")
    for i in range(0, docs_matrix.shape[0]):
        with torch.no_grad():
            vector_key = sparse_docs_matrix[i].to_dense().unsqueeze(0)
            L.append(torch.cosine_similarity(Vector_query, vector_key).cpu().numpy()[0])

    return L

