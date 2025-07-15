from sentence_transformers import SentenceTransformer
import torch
import pandas as pd
import os
# from bs4 import BeautifulSoup
# import re
from typing import Tuple, Dict


DATAPATH = "./data"
QUESTION_QUERY_MODEL_NAME = "all-MiniLM-L6-v2"
ANSWER_QUERY_MODEL_NAME = "multi-qa-mpnet-base-cos-v1"


# os.environ['CURL_CA_BUNDLE'] = ''

def remove_tags(text:str)->str:
    text = text.replace('"', '')
    text = text.replace('\n', ' ')
    text = text.replace('<p>', '')
    return text

def save_embeddings(model_name: str, savepath: str):
    # device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model = SentenceTransformer(f'sentence-transformers/{model_name}', device='cuda')

    posts = pd.read_xml(os.path.join('Posts.xml'), parser="etree", encoding="utf8")
    clean_posts = posts[['Id', 'Body', 'Title']]
    clean_posts['Clean Body'] = clean_posts['Body'].fillna('').apply(remove_tags)
    clean_posts['Clean Title'] = clean_posts['Title'].fillna('').apply(remove_tags)

    embeddings_bodies = []
    embeddings_titles = []
    clean_bodies = list(clean_posts["Clean Body"])
    clean_titles = list(clean_posts['Clean Title'])
    postid = list(clean_posts['Id'])
    batch_size = 10000

    for i in range(0, len(clean_bodies), batch_size):
        embeddings_bodies.extend(model.encode(clean_bodies[i:i+batch_size], convert_to_tensor=True, normalize_embeddings=True))
        embeddings_titles.extend(model.encode(clean_titles[i:i+batch_size], convert_to_tensor=True, normalize_embeddings=True))
        print(i, flush=True)

    # save embeddings tensors as dict with id as key
    embeddings_bodies_dict = dict(zip(postid, embeddings_bodies))
    embeddings_titles_dict = dict(zip(postid, embeddings_titles))

    torch.save(embeddings_bodies_dict, f'{model_name}-embeddings_bodies_dict.pt')
    torch.save(embeddings_titles_dict, f'{model_name}-embeddings_titles_dict.pt')





def load_embeddings_and_models() -> Tuple[SentenceTransformer, SentenceTransformer, Dict[int, torch.Tensor], Dict[int, torch.Tensor]]:
    question_query_model = SentenceTransformer(QUESTION_QUERY_MODEL_NAME, device="cuda")
    answer_query_model = SentenceTransformer(ANSWER_QUERY_MODEL_NAME, device="cuda")

    # get embeddings from reading file embeddings_bodies_dict.pt
    embeddings_titles = torch.load(os.path.join(DATAPATH, f'{QUESTION_QUERY_MODEL_NAME}-embeddings_titles_dict.pt'))

    # get embeddings from reading file embeddings_bodies_dict.pt
    embeddings_answer = torch.load(os.path.join(DATAPATH, f'{ANSWER_QUERY_MODEL_NAME}-embeddings_bodies_dict.pt'))

    return question_query_model, answer_query_model, embeddings_titles, embeddings_answer


if __name__ == '__main__':
    save_embeddings()
