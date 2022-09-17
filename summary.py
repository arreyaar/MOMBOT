# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 13:03:27 2022

@author: vikas
"""

import streamlit as st
from results import *
import requests
import pandas as pd

uploaded_file = st.file_uploader('Please upload a file to get minutes')

if uploaded_file is not None:
    st.audio(uploaded_file,start_time = 0)
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
            st.dataframe(chapters_df)

            