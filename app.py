import csv
from random import choices
import pandas as pd
import datetime
df=pd.read_csv('words.csv')
import streamlit as st
st.dataframe(df)
import re
with st.sidebar.form('追加'):
    words=st.text_input('単語', '')
    type=st.radio('どのタイプですか',('知らない単語','覚えたい表現'))
    japa=st.text_input('訳語', '')
    japa=re.sub('(\s*)','',japa)
    japa=japa.split('、')
    submitted = st.form_submit_button("Submit")
    if submitted:
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df=pd.concat([pd.DataFrame([[words,type,japa,dt_now]],columns=['単語','タイプ','訳語','時刻']),df])
        df.to_csv('words.csv',index=False)
        st.experimental_rerun()
with st.sidebar.form('del'):
    choice=st.number_input('Delete',step=1)
    delete = st.form_submit_button("Delete")
    if delete:
        df=df.drop(df.index[[choice]])
        df.to_csv('words.csv',index=False)
        st.experimental_rerun()
csv=df.to_csv().encode('utd-8')
st.sidebar.download_button('単語帳をダウンロード',data=csv,file_name='wordlist.csv')
uploaded_file=st.sidebar.file_uploader('単語帳をアップロードして追加')
if uploaded_file is not None:
    df_add=pd.read_csv(uploaded_file)
    df=pd.concat([df_add,df])
    df.to_csv('words.csv',index=False)
    st.experimental_rerun()