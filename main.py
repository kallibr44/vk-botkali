# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import *
import bot
import time

exams =[]
data =[]
value1 = 0
count = 0
i = 0
counter = 0
new_exams = []
def get_html(url):
    request = requests.get(url)
    return request.text


def main():
    parse(get_html('http://coko.tomsk.ru/exam2018/default.aspx'))

def parse(html):
    global data
    global exams
    global value1
    global count
    print("Обновляю базу...")
    soup = BeautifulSoup(html, "lxml")
    table = soup.find('table',id='ctl00_ContentPlaceHolder1_ExamSummary')
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if re.search('-11', cols[0].nobr.text):
            ex_date = str(cols[0].nobr.text)[-11::]
            date = datetime.strptime(str(ex_date[1:]), "%d.%m.%Y")
            start_date = datetime.strptime('20180525', "%Y%m%d")
            if start_date < date:
             exams.append({
              "Экзамен" : cols[0].nobr.text,
              "Работ" :cols[1].nobr.text,
              "Результатов" : cols[2].nobr.text
            })
             count = count + 1
    print ("всего строк: %d" % count)
    if value1 == 0:
     for t in exams:
            rez = t['Результатов']
            data.append({
                'Результат': rez
            })
    print("База обновлена!")
    update(html)
        #bot.send_message(str(text))

def update(html):
    global exams
    global new_exams
    global counter
    while True:
     soup = BeautifulSoup(html, "lxml")
     table = soup.find('table', id='ctl00_ContentPlaceHolder1_ExamSummary')
     for row in table.find_all('tr')[1:]:
         cols = row.find_all('td')
         if re.search('-11', cols[0].nobr.text):
             ex_date = str(cols[0].nobr.text)[-11::]
             date = datetime.strptime(str(ex_date[1:]), "%d.%m.%Y")
             start_date = datetime.strptime('20180525', "%Y%m%d")
             if start_date < date:
                 new_exams.append({
                     "Экзамен": cols[0].nobr.text,
                     "Работ": cols[1].nobr.text,
                     "Результатов": cols[2].nobr.text
                 })
     while True:
         pass

def check(id):
    global count
    global exams
    global new_exams
    global counter
    i = count
    co = 0
    for q in range(0, i):
        if (exams[q]['Результатов'] == new_exams[q]['Результатов']):
            co = co + 1
        else:
            counter = 1
            bot.success("Обновление результатов по %s : Было результатов: %s | Стало результатов: %s" % (
            new_exams[q]['Экзамен'], str(exams[q]['Результатов']), str(new_exams[q]['Результатов'])))
    if counter == 0:
        bot.send_message("Ничего нового...",1,id)
    if counter == 1:
        main()
        counter = 0

if __name__ == '__main__':
 bot.init()
 bot.hello()
 main()
