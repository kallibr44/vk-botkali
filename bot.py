import requests
import time
import os, sys
import json
import traceback
import threading
import main
import igra

access_token = 'здесь User API'
server = []
users = []
ch = 0
event = []
messages = []
pts = 0
queue = []
def hello():
  print("Начал работу...\n")
  send_message("Я включился! ",3,"kallibr44")

def pool_server(timer):
    pool()
    global server
    global users
    global ch
    global event
    global messages
    global pts
    pooll = requests.get(
        "https://%s?act=a_check&key=%s&ts=%s&wait=%s&mode=32&version=3" % (server[0], server[1], server[2], timer))
    response = json.loads(pooll.text)
    pts = response["pts"]
    while True:
     print ("PTS : " + str(pts))
     print("TIMESTAMP : " + str(server[2]))
     time.sleep(2)
     event.clear()
     messages.clear()
     req = requests.get("https://api.vk.com/method/messages.getLongPollHistory?v=5.52&access_token=%s&ts=%s&pts=%s&lp_version=3" %(access_token,server[2],pts))
     mes = json.loads(req.text)
     try:
      j=0
      #print(mes)
      for i in range(0,mes["response"]["messages"]["count"]):
          block = mes["response"]["messages"]["items"][i]
        #  print("Блок сообщения: " + str(block))
          res = get_user(mes["response"]["messages"]["items"][i]["user_id"],4)
         # print("Сообщение от %s %s с текстом: '%s'" % (res[0],res[1],mes["response"]["messages"]["items"][i]["body"]))
          event.append(mes["response"]["history"][i])
          j = i+1
     except Exception as e:
         print(traceback.format_exc())
     history(req)
     pts = mes["response"]["new_pts"]
    #print("К серверу long pool подключен! Жду команду... Таймаут через %s секунд" % (timer))
     time.sleep(2)
     pool()

def history(hist):
    global messages
    req = hist
    mes = json.loads(req.text)
    try:
        for i in range(0, mes["response"]["messages"]["count"]):
         res = get_user(mes["response"]["messages"]["items"][i]["user_id"],4)
         if mes["response"]["messages"]["items"][i]["out"] == 0:
          print("Сообщение от %s %s с текстом: '%s'" % (
             res[0], res[1], mes["response"]["messages"]["items"][i]["body"]))
          messages.append({"id" : mes["response"]["messages"]["items"][i]["user_id"],
                          "text" : mes["response"]["messages"]["items"][i]["body"],
                          "timestamp" : mes["response"]["messages"]["items"][i]["date"]})
        else:
            print("исходящее сообщение, игнорируем...")
    except Exception as e:
        print(traceback.format_exc())
    events()

def events():
   global event
   global messages
   response = event
   for i in response:
    if i[0] == 4:
        pass
    elif i[0] == 8:
        user = get_user(i[1],1)
        print("Пользователь %s %s появился в сети %s" % (user[0],user[1], datetime.datetime.fromtimestamp(int(i[2])).strftime('%Y-%m-%d %H:%M:%S')))
    elif i[0] == 61:
        user = get_user(i[1],1)
        print("Пользователь %s %s набирает сообщение..." % (user[0],user[1]))
    sort()

'''
Падежи для ответа:
Именительный - nom
родительный – gen
дательный – dat
винительный – acc
творительный – ins
предложный – abl
'''
def get_user(id,type):
   if type == 1:
    req = requests.get("https://api.vk.com/method/users.get?v=5.52&access_token=%s&user_ids=%s&name_case=nom" % (
    access_token, id))
    res = json.loads(req.text)
    return res["response"][0]["first_name"], res["response"][0]["last_name"]
   elif type == 2:
       req = requests.get("https://api.vk.com/method/users.get?v=5.52&access_token=%s&user_ids=%s&name_case=gen" % (
           access_token, id))
       res = json.loads(req.text)
       return res["response"][0]["first_name"], res["response"][0]["last_name"]
   elif type == 3:
       req = requests.get("https://api.vk.com/method/users.get?v=5.52&access_token=%s&user_ids=%s&name_case=dat" % (
           access_token, id))
       res = json.loads(req.text)
       return res["response"][0]["first_name"], res["response"][0]["last_name"]
   elif type == 4:
       req = requests.get("https://api.vk.com/method/users.get?v=5.52&access_token=%s&user_ids=%s&name_case=acc" % (
           access_token, id))
       res = json.loads(req.text)
       return res["response"][0]["first_name"], res["response"][0]["last_name"]
   elif type == 5:
       req = requests.get("https://api.vk.com/method/users.get?v=5.52&access_token=%s&user_ids=%s&name_case=ins" % (
           access_token, id))
       res = json.loads(req.text)
       return res["response"][0]["first_name"], res["response"][0]["last_name"]
   elif type == 6:
       req = requests.get("https://api.vk.com/method/users.get?v=5.52&access_token=%s&user_ids=%s&name_case=abl" % (
           access_token, id))
       res = json.loads(req.text)
       return res["response"][0]["first_name"], res["response"][0]["last_name"]

def pool():
    #получаем ключ и тс
    global server
    server.clear()
    req = requests.get('https://api.vk.com/method/messages.getLongPollServer?v=5.52&access_token=%s' % (access_token))
    t = json.loads(req.text)
    server.append (t["response"]["server"])
    server.append (t["response"]["key"])
    server.append (t["response"]["ts"])
    #print ("Данные для пула: \n" + req.text + "\n---------------")

def success(text):
    global users
    for i in users:
        send_message(text,1,i)

def send_message(text,type,id):
    # структура запроса: url/method/type_method?v=5.2&access_token&parameters
    # тип: 1=личное сообщение 2=сообщение в группу 3= сообщение по домену
     if type == 1:
      requests.get('https://api.vk.com/method/messages.send?v=5.52&access_token=%s&message=%s&user_id=%s' % (access_token, text,id))
     elif type == 2:
      requests.get('https://api.vk.com/method/messages.send?v=5.52&access_token=%s&message=%s&chat_id=%s' % (access_token, text,id))
     elif type == 3:
      requests.get('https://api.vk.com/method/messages.send?v=5.52&access_token=%s&message=%s&domain=%s' % (access_token, text,id))

def timer():
 i = 3600
 while i > 0:
   i = i-1
   time.sleep(1)

def rabota(id,s1):
   global t2
   global v
   if s1 == 0:
    t2 = threading.Thread(target=igra.init, args=(id,))
    t2.start()
   elif s1 == 1:
     try:
       v = t2.isAlive()
       if v == False:
           print("Поток с игроком %s окончен" % str(id))
           que(id)
       elif v == True:
           print("поток по-прежнему запущен!")
     except Exception as e:
         print(traceback.format_exc(e))

def que(id):
    global queue
    if len(queue) > 0:
     queue.reverse()
     id = queue.pop()
     rabota(id,0)
     queue.reverse()
    else:
        send_message("Вы первый в очереди!",0,id)


def init():
    os.system("clear")
    t = threading.Thread(target=pool_server, args=(25,))
    t.start()
    t1 = threading.Thread(target=commands)
    t1.start()

def sort():
    global event
    global queue
    for i in messages:
      check = i["text"]
      if check == "проверка" or check == "Проверка":
          res = get_user(i["id"],3)
          send_message("Привет! Эта команда работает!", 1, i["id"])
          print(("Сказал %s %s текст: %s \n" % (res[0], res[1], "Привет! Эта команда работает!")))
      elif check == "результат" or check == "Результат":
          res = get_user(i["id"],2)
          send_message("Сейчас проверим...", 1, i["id"])
          print(("Проверил результаты для %s %s \n" % (res[0], res[1])))
          main.check(i["id"])
      elif check == "игра" or check == "Игра":
          try:
             if len(queue) > 0:
              queue.append(i["id"])
              send_message("Ожидайте, вы %d в очереди! " % queue.index(i["id"]),1,i["id"])
             rabota(i["id"], 0)
          except Exception as e:
              print(traceback.format_exc(e))
      elif check == "/help":
          res = get_user(i["id"],3)
          send_message(
              "'результат'- я посмотрю, были ли изменения \n 'проверка'-проверить работоспособность бота \n 'игра'- сыграть в 21",
              1, i["id"])
          print(("Помог %s %s \n" % (res[0], res[1])))
      elif check == "чат" or check == "Чат":
          chat()
      else:
          pass

def chat():
    while True:
        pass

def commands():
   while True:
    text = input()
    id = input("Введите id: ")
    send_message(text,1,id)
    user = get_user(id,3)
    print("Сообщение %s %s с текстом '%s' отправлено! " % (user[0],user[1],text))

def take_message():
    return messages
