from main import main
from utils import get_all_repo_name
import streamlit as st

if __name__=='__main__':
    # text = st.text_input('Enter the github url')
    # text = input('Enter the github url')
    # text = 'https://github.com/cmooredev/RepoReader'
    # username = input('Enter the github username : ')
    st.title('GitHub Analyzer')
    username = st.text_input('Enter the github username : ')
    if username:
        repos = get_all_repo_name(username)

        for repo in repos:
            github_url = 'https://github.com/'+username+'/'+repo
            st.write(f'Repo Name {repo}')
            ans = main(github_url)
            st.write(f'Model says : \n')
            st.write(ans)
            st.write(github_url)
            st.write('-'*30)
            