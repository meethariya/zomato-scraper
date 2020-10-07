# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 21:07:40 2020

@author: Meet Hariya
"""


from bs4 import BeautifulSoup
import requests
import csv


dictionary = []
page_counter = 1
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
url = "https://www.zomato.com/ncr/connaught-place-delhi-restaurants?page="
while page_counter <= 10:
    new_url = url + str(page_counter)
    print("Connecting to page", page_counter)
    raw = requests.get(new_url, headers=HEADERS)
    soup = BeautifulSoup(raw.text, 'html5lib')
    boxes = soup.findAll("div", {"class": "search-card"})
    for data in boxes:
        temp = []
        name = data.findAll("a", {"class": "fontsize0"})
        if not name:
            continue
        name = name[0].text.replace("\t", "")
        name = name.replace("\n", "")
        temp.append(name.strip())
        number = data.findAll("a", {"class": "item res-snippet-ph-info"})
        number = number[0]['data-phone-no-str'].replace("\t", "")
        number = number.replace("\n", "")
        number = number.split(",")
        if len(number) == 2:
            temp.append(number[0])
            temp.append(number[1])
        else:
            temp.append(number[0])
            temp.append("")
        address = data.findAll("div", {"class": "ln22"})
        address = address[0].text.replace("\t", "")
        address = address.replace("\n", "")
        temp.append(address.strip())
        dictionary.append(temp)
    print("Page ", page_counter, "Extracted")
    page_counter += 1
fields = ['Name', 'Phone number 1', 'Phone number 2', 'address']
print("Writting in excel sheet....Please wait")
with open("hotels2.csv", "w", encoding="utf-8", newline="") as scribble:
    csvwriter = csv.writer(scribble)
    csvwriter.writerow(fields)
    csvwriter.writerows(dictionary)
print("Written in excel sheet successfully!")
