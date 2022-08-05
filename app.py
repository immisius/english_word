import csv
from random import choices
from urllib import response
import pandas as pd
import datetime
import streamlit as st
import re
from st_aggrid import AgGrid
import requests
import json

columns=['単語','訳語','類語','タイプ','時刻']
df=pd.read_csv('words.csv',encoding='utf-8')
df=df.reindex(columns=columns).drop_duplicates()
df=df.reset_index(drop=True)
# 修正が反映される

# AgGrid(df,theme='streamlit', fit_columns_on_grid_load=True)
api="https://script.google.com/macros/s/AKfycbwHh0TXb4dvjRHuPOmQ24HXpyr-C4TSbDiFmK8b66YSBhIHsoGuPFMRP9tITght-W6ocA/exec"

st.dataframe(df)

with st.sidebar:
    words=st.text_input(label='単語')
    words=words.strip()
    api=api+'?'+'text='+words+'&source=en&target=ja'
    response=requests.get(api).json()
    google=response['text']
    reibun,cap=st.columns(2)
    if google != 'Bad Request':
        with reibun:
            st.markdown('**'+google+'**')
        with cap:
            st.caption('Translated by Google')
with st.sidebar.form('追加'):
    japa=st.text_input(label='訳語')
    st.markdown('多義を登録する場合は『、（読点）』で区切って下さい')
    ruigo=st.text_input(label='類語')
    ruigo=ruigo.split(',')
    st.markdown('多語を登録する場合は『,（カンマ）』で区切って下さい')
    if type=='知らない単語':
        japa=re.sub('(\s*)','',japa)
    japa=japa.split('、')
    st.markdown('覚えたい表現には訳語はつきません。')
    col1,col2=st.columns(2)
    with col1:
        imi = st.form_submit_button("知らない単語")
    with col2:
        not_imi=st.form_submit_button("覚えたい表現")
    if imi:
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if japa ==[""]:
            japa=google.split('、')
        df=pd.concat([pd.DataFrame([[words,"知らない単語",japa,dt_now,ruigo]],columns=['単語','タイプ','訳語','時刻','類語']),df])
        df.to_csv('words.csv',index=False,encoding='utf-8')
        words=st.empty()
        japa=st.empty()
        st.experimental_rerun()
    if not_imi:
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df=pd.concat([pd.DataFrame([[words,"覚えたい表現",japa,dt_now,ruigo]],columns=['単語','タイプ','訳語','時刻','類語']),df])
        df.to_csv('words.csv',index=False,encoding='utf-8')
        words=st.empty()
        japa=st.empty()
        st.experimental_rerun()
with st.sidebar.form('del'):
    choice=st.number_input('削除する番号を選択して下さい',step=1)
    delete = st.form_submit_button("削除")
    if delete:
        if len(df)!=0:
            df=df.drop(df.index[[choice]])
            df.to_csv('words.csv',index=False,encoding='utf-8')
            st.experimental_rerun()
csv=df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button('単語帳をダウンロード',data=csv,file_name='word-list.csv')
with st.sidebar.form('upload'):
    uploaded_file=st.file_uploader('単語帳をアップロードして追加',accept_multiple_files=False,type='csv')
    send=st.form_submit_button('アップロード')
    if send:
        df_add=pd.read_csv(uploaded_file,encoding='utf-8')
        df=pd.concat([df_add,df])
        df.to_csv('words.csv',index=False,encoding='utf-8')
        uploaded_file=st.empty()
        st.experimental_rerun()

