#-_- coding: utf-8 -_-

import random
import time
import bot
import threading
import requests
import json

access_token = '961d5074c23cd79fccac08e2d8f2b28f599b8b148d303733801785bdadbd176e0fe6de6181102a3be00c1'
cards = ['6','7','8','9','10','Валет','Дама','Король','Туз']
mast = ['пики','черви','крести','буби']
koloda = [6,7,8,9,10,2,3,4,11] * 4
cache1 = []
cache2 = []
s1 = 0
s2 = 0
s3 = ''
server = []
ts = ''
timestamp = 0

def game(id):
 global cache1
 global cache2
 prepare(id)
 global s1
 global s2
 global s3
 global timestamp
 while True:
   bot.send_message("У вас %d очков\n" % (s1),1,id)
   #bot.send_message("У бота %d очков\n" % (s2))
   time.sleep(1)
   if s1 <=21 :
    if s1 == 21:
       bot.send_message("Поздравляем! вы набрали 21! ",1,id)
       clear(id)
       s3 = ''
       break
    bot.send_message("Берёте карту y/n ?",1,id)
    timestamp = int(time.time())
    s3 = pool_server(id)
    if s3 == 'y':
      temp = take()
      s1 = s1 + temp
      bot.send_message("Вы получили карту '%s' достоинством %d !" % (str(card(temp)),temp),1,id)
      s3 = ''
    elif s3 == 'n':
        if s1 <= 21:
            bot.send_message("Поздравляем! Вы выиграли!",1,id)
        bot.send_message("Досрочно закончена игра со счетом %d" % s1,1,id)
        clear(id)
        s3 = ''
        break
    else:
        bot.send_message("Неверный выбор! ",0,id)
        pass
   else:
       bot.send_message("Вы проиграли!",1,id)
       clear(id)
       s3 = ''
       break

def clear(id):
    global cache1
    global cache2
    global s1
    global s2
    cache1.clear()
    cache2.clear()
    s1 = 0
    s2 = 0
    bot.rabota(id,1)

def take():
    return koloda.pop()


def prepare(id):
    global cache2
    global cache1
    global s1
    bot.send_message("Раздаю карты...",1,id)
    for i in range(0, 2):
       s1 = s1 + koloda.pop()
       # cache1[i] = koloda.pop()
       # cache2[i] = koloda.pop()
       time.sleep(1)

def card(s1):
    global cards
    if s1 == 6:
        return cards[0]
    elif s1 == 7:
        return cards[1]
    elif s1 == 8:
        return cards[2]
    elif s1 == 9:
        return cards[3]
    elif s1 == 10:
        return cards[4]
    elif s1 == 2:
        return cards[5]
    elif s1 == 3:
        return cards[6]
    elif s1 == 4:
        return cards[7]
    elif s1 == 11:
        return cards[8]

def init(id):
    global cache1
    global cache2
    print("Поток игры начал работу с id: " + str(id))
    random.shuffle(koloda)
    game(id)

def start(id):
    init(id)

def mast(s1):
    global mast
    if s1 == 1:
        return mast[0]
    elif s1 == 2:
        return mast[1]
    elif s1 == 3:
        return mast[2]
    elif s1 == 4:
        return mast[3]

def karta():
    s1 = random.randint(1,9)
    return s1

def pool_server(id):
  global timestamp
  global s5
  s5 = ""
  while s5 != "y" and s5 !="n":
   messages = bot.take_message()
   for i in messages:
      if i["timestamp"] > timestamp and i["id"] == id and (i["text"] == "y" or i["text"] == "n"):
          print("Блок игры ответа: " + str(i))
          s5 = i["text"]
          ss = bot.get_user(id,1)
          print ("Игрок %s %s сделал ход!" % (ss[0],ss[1]))
          return i["text"]