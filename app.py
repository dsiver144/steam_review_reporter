import requests
from bs4 import BeautifulSoup
import re

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