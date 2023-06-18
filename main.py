import os
import tempfile
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from constants import openai_key, model
from file_handler import clone_github_repo, load_and_index_files
from utils import format_documents


os.environ['OPENAI_API_KEY'] = openai_key


def main(url):
    github_url = url
    repo_name = github_url.split('/')[-1]
    print('Clonning the repositories.....')


    with tempfile.TemporaryDirectory() as local_path:
        if clone_github_repo(github_url, local_path):
            index, documents, file_type_counts, filenames = load_and_index_files(local_path)
            numbered_documents = format_documents(documents)

            '''
            print('\n\n\n\n')
            print('index', index)
            print()
            print('documents', documens)
            print()
            print('file type counts', file_type_counts)
            print()
            print('filenames', filenames)
            '''

            if index is None:
                print("Couldn't load documents Exiting")
                exit()
            
            print("Repositiries cloned and indexed")

            llm = OpenAI(temperature=0.2, model=model, verbose=True)

            template = """
            
            Repo: {repo_name} ({github_url}) | Docs: {numbered_documents} | FileCont: {file_type_counts} | FileNames: {filenames}

            What is the technical complexity of this repo in the range of 1 to 100? Also state the reason.

            """

            prompt = PromptTemplate(
                template=template,
                input_variables=['repo_name', 'github_url', 'numbered_documents', 'file_type_counts', 'filenames']
            )

            llm_chain = LLMChain(prompt=prompt, llm=llm)

            answer = llm_chain.run({'repo_name': repo_name, 'github_url': github_url, 'numbered_documents': numbered_documents[50:70], 'file_type_counts': file_type_counts, 'filenames': filenames})

            return answer

        else:
            print("\n\nCouldn't clone github repo\n\n")

        