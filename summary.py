# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 13:03:27 2022

@author: vikas
"""
import io
import createPdf as pdf
import sendMail as mail
import streamlit as st
from results import *
import requests
import pandas as pd
import shutil
from azure.storage.fileshare import ShareFileClient

PAGE_CONFIG = {"page_title":"Minutes of Meeting", 
               "layout":"centered", 
               "initial_sidebar_state":"auto"}

st.set_page_config(**PAGE_CONFIG)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

if 'start_point' not in st.session_state:
    st.session_state['start_point'] = 0
    
def update_start(start_t):
    st.session_state['start_point'] = int(start_t/1000)
    
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.postimg.cc/ZK2sxNFP/457.png");
             background-repeat: no-repeat;
             background-attachment: fixed;
             background-position: right bottom;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

connection_string = "DefaultEndpointsProtocol=https;AccountName=bootlogdfe5e392;AccountKey=JmRLd6ZuKoDpB3N47PQtZz0SVLM7QDCN1L8bM6ZhnF3Hvvw+cw+BgVkcYaINcTZOb4Z9YiFfI80k+AStEO99uw==;EndpointSuffix=core.windows.net"
dirfile_client = ShareFileClient.from_connection_string(conn_str=connection_string, share_name="minutes123", file_path="SE12.mp3")

DEST_FILE = './SE12.mp3'

def get_downloaded_file():
    with open(DEST_FILE, "wb") as file_handle:
        data = dirfile_client.download_file()
        #data.readinto(file_handle)
        file_handle.write(data.readall())
        print(print("Size of file is :", file_handle.tell(), "bytes"))
        return file_handle

uploaded_file = get_downloaded_file()
uploaded_file = io.open(DEST_FILE, "rb", buffering = 0)

if uploaded_file is not None:
    st.audio(DEST_FILE,start_time = st.session_state['start_point'])
    poll_end_pt = upload_to_AI(uploaded_file)
    
    status ='submitted'
    while status != 'completed':
        poll_resp = requests.get(poll_end_pt, headers=headers)
        status = poll_resp.json()['status']
        if status == 'completed':
            #print categories
            st.subheader('Main Topics')
            with st.expander('Themes'):
                categories = poll_resp.json()['iab_categories_result']['summary']
                for cat in categories:
                    st.markdown("* " + cat)
            
            
            #print chapters
            st.subheader('Summary points from the meeting')
            chapters = poll_resp.json()['chapters']
            chapters_df = pd.DataFrame(chapters)
            chapters_df['start_str'] = chapters_df['start'].apply(toMiliSec)
            chapters_df['end_str'] = chapters_df['end'].apply(toMiliSec)
            
            f = open("minutes.txt", "w")
            assigned = ""    
            for index , row in chapters_df.iterrows():
                with st.expander(row['gist']):
                    if(row['summary'].find('Dutch') != -1):
                        assigned = 'Dutch'
                    st.write(row['summary'] + "\n" + "Assigned to: " + assigned)
                    f.write(row['gist'] + "\n")
                    f.write(row['summary'] + "\n")
                    st.button(row['start_str'], on_click=update_start, args=(row['start'],))
            f.close()
            pdf.createPDF("minutes.txt")
            
            #auto send mail to intended participants
            mail.sendMail("minutes.pdf")
            
            #also send mail on click on send mail button on GUI
            if st.button('Send summary on mail'):
                mail.sendMail("minutes.pdf")