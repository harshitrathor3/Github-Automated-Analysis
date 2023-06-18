import re
import nltk
import os
import requests
from requests.auth import HTTPBasicAuth
# from constants import github_token
import json

def clean_and_tokenize(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\b(?:http|ftp)s?://\S+', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    return nltk.word_tokenize(text)




def format_documents(documents):
    numbered_docs = "\n".join([f"{i+1}. {os.path.basename(doc.metadata['source'])}: {doc.page_content}" for i, doc in enumerate(documents)])
    return numbered_docs


def get_all_repo_name(userid):
    response = requests.get('https://api.github.com/users/' + userid + '/repos')
    data = json.loads(response.text)
    repos = []
    for i in data:
        repos.append(i['name'])
        
    return repos
