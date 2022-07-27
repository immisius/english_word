import csv
from random import choices
import pandas as pd
import datetime
import streamlit as st
import re

df=pd.read_csv('words.csv',encoding='utf-8')
df=df.reindex(columns=['単語', '訳語', 'タイプ','時刻'])
# 修正が反映される
st.table(df)

with st.sidebar.form('追加'):
    words=st.text_input(label='単語')
    type=st.radio('どのタイプですか',('知らない単語','覚えたい表現（訳語いらない）'))
    japa=st.text_input(label='訳語')
    st.markdown('多義を登録する場合は『、（読点）』で区切って下さい')
    if type=='知らない単語':
        japa=re.sub('(\s*)','',japa)
    japa=japa.split('、')
    submitted = st.form_submit_button("Submit")
    if submitted:
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if type=='覚えたい表現（訳語いらない）':
            japa=None
        df=pd.concat([pd.DataFrame([[words,type,japa,dt_now]],columns=['単語','タイプ','訳語','時刻']),df])
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
st.sidebar.download_button('単語帳をダウンロード',data=csv,file_name='wordlist.csv')
uploaded_file=st.sidebar.file_uploader('単語帳をアップロードして追加',accept_multiple_files=False,type='csv')
if uploaded_file is not None:
    df_add=pd.read_csv(uploaded_file,encoding='utf-8')
    df=pd.concat([df_add,df])
    df.to_csv('words.csv',index=False,encoding='utf-8')
    uploaded_file.close()
    st.experimental_rerun()