

import streamlit as st
import pandas as pd
from streampy_console import Console
from streamlit_deferrer import st_deferrer
from streamlit_ace import st_ace
from io import StringIO
from github import Github
from github import Auth
from code_editor import code_editor

# using an access token

g = None

def replaceVariables(text):
    result = text 
    for i in edited_df.index:
        result = result.replace("{{" + edited_df['Name'][i] + "}}",edited_df['Value'][i])
    return result


st.set_page_config(page_title="Moving Python", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
variables_df = pd.DataFrame(columns=['Name','Value'])
fileNames = []
repoNames = []

saveFileName = ""
selectedFileName = ""
selectedRepoName = None
selectedCode = "print('HelloWorld')"
def convert_df(df):
    return df.to_csv().encode('utf-8')
if 'token' not in st.session_state:
    st.session_state.token = ''
token = ""
with st.expander("GitHub Access", expanded=False):

    token = st.text_input("Access Token",token, key="token",type="password")
    
    if token != "":
        auth = Auth.Token("access_token")
        g = Github(token)
        l = g.get_user().login
        print("get user repos",l)
        fileNames = []
        repoNames = []
        for repo in g.get_user().get_repos():
            repoNames.append(repo.name)
        selectedRepoName = st.selectbox('Select Repository',repoNames)
        
        if selectedRepoName is not None:
            repository = g.get_user().get_repo(selectedRepoName)
         
            repocontents = repository.get_contents("")
            fileNames = []
            for content_file in repocontents:
                if ".py" in str(content_file):
                    fileNames.append(str(content_file).replace('ContentFile(path="',"").replace('")',""))
            selectedFileName = st.selectbox('Select File',fileNames)
            if selectedFileName != "":
                print(selectedFileName)
                if selectedFileName:
                    file_content = repository.get_contents(selectedFileName)
                    selectedCode = file_content.decoded_content.decode()
                    content = selectedCode
                

with st.expander("Global Variables", expanded=False):
    uploaded_file = st.file_uploader("Upload variables:",label_visibility="collapsed")
    if uploaded_file is not None:
        savedVariables = pd.read_csv(uploaded_file,index_col=[0])
        for i in savedVariables.index:
            variables_df.loc[i] = [savedVariables['Name'][i],savedVariables['Value'][i]]

    edited_df = st.data_editor(variables_df, num_rows="dynamic",hide_index=False)

    st.download_button(label="Download Variables",data= convert_df(edited_df),file_name='variables.csv',mime='text/csv',)

saveFileName = st.text_input('File Name',selectedFileName)

if selectedRepoName is not None:
    repo = g.get_user().get_repo(selectedRepoName)
    if saveFileName is not None:
        if saveFileName != selectedFileName:
            if st.button("Save '" + saveFileName + "' to '" + repo.name + "' repo"):
                repo.create_file(saveFileName, "committing files", content, branch="main")
                print("save")
        else:
            if st.button("Update '" + saveFileName + "' in '" + repo.name + "' repo"):
                contents = repo.get_contents(saveFileName)
                selectedFileName = saveFileName
                repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")


std = st_deferrer()

console = Console(std,startup="startup.py")
content = ""


btn_settings_editor_btns = [{
  
    "name": "Run",
    "feather": "Play",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"bottom": "0rem", "right": "0.4rem"}
  }
  ]

response_dict  = code_editor(selectedCode, height = [5, 16],lang="python", buttons=btn_settings_editor_btns)
if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    content = response_dict['text']
    newCode = replaceVariables(content)
    console.run(newCode)


         






