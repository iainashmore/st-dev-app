#conda activate streamlit_env
import streamlit as st
import pandas as pd
import requests as rq
import json

session = rq.Session()

output = {"name":['myOutput']}


def __get(path,headers,username,password):
    session.auth = (username, password)
    res = session.get(path,headers=headers)
    return res.status_code,res.json()

def __convert_df():
    df = pd.DataFrame(output)
    return df.to_csv().encode('utf-8')

def __createDownload():
    if output != None:
        st.download_button(
            label="Download CSV",
            data=__convert_df(),
            file_name='output.csv',
            mime='text/csv',
        )

def __add(a,b):
    return a + b