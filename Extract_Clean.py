import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import pickle


MAIN_PATH = "."
DATA_PATH = "data"


def clean_post(text:str)->str:
    soup = BeautifulSoup(text, "html.parser")
    sent = soup.get_text()
    cleaned_text = re.sub(r'\s+', ' ', sent).strip()
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text).lower()

    return cleaned_text

def extract_data(datapath: str) -> pd.DataFrame:
    posts = pd.read_xml(os.path.join(datapath, 'Posts.xml'), parser="etree", encoding="utf8")
    posts['cleaned_body'] = posts.Body.fillna('').apply(clean_post)
    posts['cleaned_title'] = posts.Title.fillna('').apply(clean_post)

    return posts


if __name__ == '__main__':
    posts = extract_data(DATA_PATH)

    with open(os.path.join(DATA_PATH, 'posts.pkl'), 'wb') as f:
        pickle.dump(posts, f)

    #with open(os.path.join(DATA_PATH, 'posts.pkl'), 'rb') as f:
    #    posts = pickle.load(f)

    votes = pd.read_xml(os.path.join(DATA_PATH, 'Votes.xml'), parser="etree", encoding="utf8")
    users = pd.read_xml(os.path.join(DATA_PATH, 'Users.xml'), parser="etree", encoding="utf8")

    # Now we merge both of them to identify the votes based score for each post, it will be important later on
    votes_posts = pd.merge(votes, posts, left_on='PostId', right_on='Id', how='left')

    print(posts)
    print(votes_posts["Score"])
