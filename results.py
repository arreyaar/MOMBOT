# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 13:06:17 2022

@author: vikas
"""

import requests
from config import *

headers = {
    "authorization": auth_token,
    "content_type": "application/json"
}

def upload_to_AI(f_audio):
    
    transcript_pt = "https://api.assemblyai.com/v2/transcript"
    upload_pt = "https://api.assemblyai.com/v2/upload"
    
    print('uploading file - start')
    
    up_resp = requests.post(
        upload_pt,
        headers=headers, data = f_audio
    )
    
    if up_resp.status_code != 200:
        print('Check Auth XXXX')
        exit        

    print(up_resp.json())
    audio_url = up_resp.json()['upload_url']

    print('uploading file - done')
    
    json = {
        "audio_url": audio_url,
        "iab_categories": True,
        "auto_chapters": True
    }
    
    resp = requests.post(transcript_pt, json=json, headers=headers)
    
    poll_end_pt = transcript_pt + "/" + resp.json()['id']

    return poll_end_pt

def toMiliSec(mili_start):
    sec = int((mili_start / 1000) % 60)
    min = int((mili_start / ( 1000 * 60)) % 60)
    hrs = int((mili_start / (1000 * 60 * 60)) % 24)
    btn_caption = ''

    if hrs > 0:
        btn_caption += f'{hrs:02d}:{min:02d}:{sec:02d}'
    else:
        btn_caption += f'{min:02d}:{sec:02d}'

    return btn_caption