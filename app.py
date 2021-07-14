import requests
from bs4 import BeautifulSoup
import re
from requests.api import get
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getSteamReview0():
    current_count = 0
    try:
        file = open("current.txt", "r")
        current_count = int(file.read)
        file = open("current.txt", "w")
    except:
        file = open("current.txt", "w")

    URL = "https://store.steampowered.com/app/1156360/Peaceful_Days"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_="summary column")
    x = re.findall(r"(\d+)", results.text)
    if x[0] != current_count:
        file.write(x[0])

    current_count = x[0]
    review_percent = x[1]

    print(current_count, review_percent)

    file.close()

def getSteamReview1():
    current_count = 0
    path = "D:/current.txt"
    flag = False
    try:
        file = open(path, "r")
        current_count = int(file.readline())
        file.close()
    except:
        print("Cant open file!")
        flag = True

    URL = "https://store.steampowered.com/appreviews/1156360?json=1&review_type=all&language=all"
    data = requests.get(URL).json()
    summary = data['query_summary']
    pos_rv = summary['total_positive']
    neg_rv = summary['total_negative']
    if summary['total_reviews'] != current_count:
        current_count = summary['total_reviews']

        file = open(path, "w")
        file.write(str(current_count))
        file.close

        last_review = data['reviews'][0]
        last_text = "None."
        date = ""
        review_icon = "💬"
        if last_review is not None:
            last_text = last_review['review']
            date = time.ctime(last_review['author']['last_played'])
            review_icon = '⭕' if last_review['voted_up'] else '❌'
        
        subject = "🔔 NEW REVIEW(S) FOR PEACEFUL DAYS! 🔔"
        contents = "💬 Current Reviews: " + str(current_count) + " (✅" + str(pos_rv) + " | ❎" + str(neg_rv) + ")"
        contents += "\n\n" + review_icon + " Last Review (" + date + "):\n\n" + last_text
        sendEmail(subject, contents)

def sendEmail(subject, mail_content):
    #The mail addresses and password
    sender_address = 'dsiver144@gmail.com'
    sender_pass = 'emphqfokzlecrwwd'
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

schedule.every().day.at("06:00").do(getSteamReview1)
schedule.every().day.at("09:00").do(getSteamReview1)
schedule.every().day.at("12:00").do(getSteamReview1)
schedule.every().day.at("15:00").do(getSteamReview1)
schedule.every().day.at("15:18").do(getSteamReview1)
schedule.every().day.at("18:00").do(getSteamReview1)
schedule.every().day.at("18:00").do(getSteamReview1)

getSteamReview1()

while True:
    schedule.run_pending()
    time.sleep(1)