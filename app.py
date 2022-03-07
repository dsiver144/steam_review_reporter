import requests
from bs4 import BeautifulSoup
import re
from requests.api import get
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def getSteamReview():
    current_count = 0
    last_review_id = 0
    path = "current.txt"
    flag = False
    try:
        file = open(path, "r")
        result = file.readline().split(",")
        current_count = int(result[0])
        last_review_id = int(result[1])
        file.close()
    except:
        print("Cant open file!")
        flag = True

    URL = "https://store.steampowered.com/appreviews/1156360?json=1&review_type=all&language=all&filter=recent&num_per_page=1"
    data = requests.get(URL).json()
    summary = data['query_summary']
    pos_rv = summary['total_positive']
    neg_rv = summary['total_negative']
    current_review_id = data['reviews'][0]['recommendationid']
    review_score_desc = summary['review_score_desc'];

    if summary['total_reviews'] != current_count and last_review_id != current_review_id:
        current_count = summary['total_reviews']

        file = open(path, "w")
        file.write(str(current_count) + "," + str(current_review_id))
        file.close

        last_review = data['reviews'][0]
        last_text = "None."
        date = ""
        review_icon = "💬"
        if last_review is not None:
            last_text = last_review['review']
            date = time.ctime(last_review['author']['last_played'])
            review_icon = '⭕' if last_review['voted_up'] else '❌'
        
        subject = review_icon + "NEW REVIEW(S) FOR PEACEFUL DAYS!" + review_icon
        contents = "💬 Current Reviews: " + str(current_count) + " <" + review_score_desc + "> " + " (✅" + str(pos_rv) + " | ❎" + str(neg_rv) + ")"
        contents += "\n\n Last Review (" + date + "):\n\n" + last_text
        sendEmail(subject, contents)

def sendEmail(subject, mail_content):
    #The mail addresses and password
    sender_address = os.getenv('SENDER_ADDRESS')
    sender_pass = os.getenv('SENDER_PASSWORD')
    receiver_address = 'dsiver144@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

getSteamReview()
