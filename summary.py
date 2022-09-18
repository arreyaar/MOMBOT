# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 13:03:27 2022

@author: vikas
"""

import createPdf as pdf
import sendMail as mail
import streamlit as st
from results import *
import requests
import pandas as pd

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

uploaded_file = st.file_uploader('Please upload a file to get minutes')

if uploaded_file is not None:
    st.audio(uploaded_file,start_time = st.session_state['start_point'])
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

            for index , row in chapters_df.iterrows():
                with st.expander(row['gist']):
                    st.write(row['summary'])
                    f.write(row['gist'] + "\n")
                    f.write(row['summary'] + "\n")
                    st.button(row['start_str'], on_click=update_start, args=(row['start'],))
            f.close()
            pdf.createPDF("minutes.txt")
            
            if st.button('Send summary on mail'):
                mail.sendMail("minutes.pdf")