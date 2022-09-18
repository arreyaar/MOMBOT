# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 22:35:00 2022

@author: iaman
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendMail(fileName):
    mail_content = '''Hello,
Please find the Minutes of Meeting attached.
Thank You,
MOMBOT
'''
    #The mail addresses and password
    sender_address = 'aman.chauhan@outlook.in'
    sender_pass = 'T38t!ngM@!l'
    receiver_address = 'vikash.wadhwani@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Minutes of Meeting attached'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = fileName
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment; filename={}'.format(attach_file_name))
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp-mail.outlook.com',587) #use gmail with port
    session.ehlo()
    session.starttls() #enable security
    session.ehlo()
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
