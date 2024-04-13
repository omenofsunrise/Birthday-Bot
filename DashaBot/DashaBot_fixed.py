from email import message
from pickle import NONE
from re import S
from tokenize import maybe
import telebot
import random
from PIL import Image
import io
import os
import sqlite3
from telebot import TeleBot, types
from threading import Lock
import datetime
from datetime import timedelta, datetime
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

bot = telebot.TeleBot('***')

myID = 000;
waiting_email = {}
waiting_birthday = {}
waiting_code = {}
code = {}
current_email = {}
db_lock = Lock() 

def SendYanMail(recepients_emails: list, msg_text: str):
    login = "funnydouble.kirill@gmail.com"
    password = "***"
    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header('Очень важное сообщение!!!', 'utf-8')
    msg['From'] = login
    msg['To'] = ','.join(recepients_emails)
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    s.starttls()
    s.login(login, password)
    s.sendmail(msg['From'], recepients_emails, msg.as_string())
    s.quit()

def CreateCursor():
    connect = sqlite3.connect('Users_data.db', timeout=100)
    cursor = connect.cursor()
    return connect, cursor
    
connect, cursor = CreateCursor()  
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
email TEXT,
date TEXT            
)        
''')   
        
@bot.message_handler(commands=["start"])
def StartMessage(message):
    bot.reply_to(message, 'Привет, я - бот поздравляющий с днём рождения. Используйте /help чтобы посмотреть все команды.')
    
@bot.message_handler(commands=['help'])
def Help(message):
        bot.reply_to(message, '/help - ты тут \n/MyEmail - посмотреть свой email \n /MyBirthday - посмотреть свой день рождения \n/RewriteEmail - записать/переписать email \n/RewriteBirthday - записать/переписать день рождения')
    
@bot.message_handler(commands=["MyEmail"], func=lambda message: message.chat.type == 'private')
def CheckDBEmail(message):
    with db_lock: 
        connect, cursor = CreateCursor()  
        cursor.execute('''
        SELECT email FROM Users WHERE id = ?
                       ''', (message.from_user.id,))
        currentEmail = cursor.fetchone()
        if currentEmail and not currentEmail == (None,):
            bot.reply_to(message, f"your email {currentEmail}")
        else: 
            waiting_email[message.from_user.id] = True
            bot.reply_to(message, "I dont have your email in data base, send your email and i save it") 
            
@bot.message_handler(commands=["RewriteEmail"], func=lambda message: message.chat.type == 'private')
def RewriteEmail(message):
        waiting_email[message.from_user.id] = True
        bot.reply_to(message, "send your email and i save it") 
        
@bot.message_handler(func=lambda message: waiting_email.get(message.from_user.id) == True and message.chat.type == 'private')
def CheckCorrectnessOfEmail(message):
            waiting_email[message.from_user.id] = False
            email = message.text.split("@")
            if len(email) != 2:
                bot.reply_to(message, 'incorrect email') 
                return
            email = message.text.split(".")
            if len(email) < 2:
                bot.reply_to(message, 'incorrect email') 
                return
            
            current_email[message.from_user.id] = message.text
            code[message.from_user.id] = str(random.randint(100, 999))                             
            body = f'Hello! Send it to bot to accept your email {code[message.from_user.id]}'   
            SendYanMail(recepients_emails = [message.text], msg_text = body)
                        
            waiting_code[message.from_user.id] = True
            bot.reply_to(message, "I sent message with code to email you gave me. Send it to me")           

@bot.message_handler(func=lambda message: waiting_code.get(message.from_user.id) == True and message.chat.type == 'private')
def SaveEmail(message):   
    if message.text == code[message.from_user.id]:
        waiting_code[message.from_user.id] = False
        CreateOrCompleteAccount(message.from_user.id, None, current_email[message.from_user.id])
        bot.reply_to(message, "your email has been saved") 
    else:
        bot.reply_to(message, "Code is wrong") 
    

@bot.message_handler(commands =["MyBirthday"],func=lambda message: message.chat.type == 'private')
def CheckBirthday(message):
    with db_lock: 
        connect, cursor = CreateCursor()  
        cursor.execute('''
        SELECT date FROM Users WHERE id = ?
                       ''', (message.from_user.id,))
        currentBirthday = cursor.fetchone()
        if currentBirthday and not currentBirthday == (None,):
            bot.reply_to(message, f"your birthday {currentBirthday}")
        else: 
            bot.reply_to(message, "use next form to send me yourth birth - day month year \n use numbers, for example - 23 10 2005") 
            waiting_birthday[message.from_user.id] = True
        
@bot.message_handler(commands=["RewriteBirthday"], func=lambda message: message.chat.type == 'private')
def RewriteBirthday(message):
           bot.reply_to(message, "use next form to send me yourth birth - day month year \n use numbers, for example - 23 10 2005") 
           waiting_birthday[message.from_user.id] = True     
    

@bot.message_handler(func=lambda message: waiting_birthday.get(message.from_user.id) == True and message.chat.type == 'private' )
def SaveBirthday(message):   
    birthday = message.text.split(" ")

    if len(birthday) != 3:
        bot.send_message(message.chat.id, "Use right form to send yourth message")
        return
    try:
        day = int(birthday[0])
        month = int(birthday[1])
        year = int(birthday[2])

    except:
        bot.send_message(message.chat.id, "Use right form to send yourth message")
        return 
    if day < 1 or day > 31 or month < 1 or month > 12 or len(str(year)) < 4 or len(str(year)) > 4 :
        bot.send_message(message.chat.id, "Use right form to send yourth message")
        return
    birthdate = datetime(year, month, day).date()
    now = datetime.now() 
    age = now.year - birthdate.year
    if age < 0:
         bot.reply_to(message, "Wrong birthday")
         return
    if age < 6:
        bot.reply_to(message, "I don't believe you are under 6 years old")
        return
    
    waiting_birthday[message.from_user.id] = False
    CreateOrCompleteAccount(message.from_user.id, birthdate, None)
    bot.send_message(message.chat.id, "nice")
    
def CreateOrCompleteAccount(id, date, email):
    connect, cursor = CreateCursor()
    cursor.execute("SELECT id FROM Users WHERE id = ?", (id,))
    result = cursor.fetchone()

    if result is not None:
        if email is not None:
            cursor.execute('UPDATE Users SET email = ? WHERE id = ?', (email, id))
        if date is not None:
            cursor.execute('UPDATE Users SET date = ? WHERE id = ?', (date, id))
    else:
        cursor.execute('INSERT OR IGNORE INTO Users (id, date, email) VALUES (?, ?, ?)', (id, date, email))
    connect.commit() 

def SendCongratulations(id):
    bot.send_message(myID, f"{id}He has bd today")
    bot.send_message(id, "HappyBirthday!")
    
    connect, cursor = CreateCursor()  
    cursor.execute('''
        SELECT email FROM Users WHERE id = ?
                       ''', (id,))
    x = cursor.fetchall()
    SendYanMail(recepients_emails = x, msg_text = 'Happy Birthday!!!')
def CheckBirthday():
    now = datetime.now() 
    connect, cursor = CreateCursor()  
    cursor.execute('''
        SELECT id FROM Users WHERE date = ?
                       ''', (now,))
    results = cursor.fetchall()
    if results:
        for result in results:
            SendCongratulations(result)
    else:
        bot.send_message(myID, "Today is no one's birthday")

def CheckTime():
    while True:
        now = datetime.now()
        if now.hour == 3: 
            CheckBirthday()
            time.sleep(83000) 
        else:
            time.sleep(1200) 
            
t = threading.Thread(target=CheckTime)
t.start()
     
bot.polling()