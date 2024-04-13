#-*- coding: utf-8 -*-

import telebot
import random

bot = telebot.TeleBot('6661673544:AAEuPVGWiDxsUgKFNsVgRvEksyoVvPLIsr8')
vuvaID = 1679627120
vuvaIsAllowed = False
admonitionsAmount = 0

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def reply_to_private_message(message):
    bot.reply_to(message, 'i love pigs')
    
@bot.message_handler(content_types=['text', 'document', 'audio'])

def get_text_messages(message):
    chat_id = message.chat.id
    if message.from_user.id == vuvaID: 
        if vuvaIsAllowed:
            bot.send_message(message.chat_id, "Ofh, fucker, im so tired of your barking, that's enough for today")
            vuvaIsAllowed = False
        elif message.text == "please let me speak my lady pls pls":
            vuvaIsAllowed = True
            bot.send_message(message.chat_id, "Okay, fucker, you can send mmmm ONE message")
        elif admonitionsAmount == 0:
            bot.send_message(message.chat_id, "fuck you slave I didnt let you speak. Youv got first ADMONTION before Il craple your eggs. print \"/please let me speak my lady pls pls\" and Il think ")
            admonitionsAmount =+ 1
        elif admonitionsAmount == 1:
            admonitionsAmount =+ 1
            bot.send_message(message.chat_id, "fuck you are so stupid wtf fucker. Shut up and dont interrupt our discussion. Youv got second ADMONTION ")
        elif admonitionsAmount == 2:
            admonitionsAmount =+ 1
            bot.send_message(message.chat_id, "Are you nuts? Dirty slave, I promise, one more word and you'll regret having a dick")
        else:       
             bot.kick_chat_member(chat_id, vuvaID)
             admonitionsAmount = 0

    elif message.text == "hello":
        bot.send_message(message.chat_id, "aaa hello hello !!")
    elif message.text == "/help":
        bot.send_message(message.chat_id, "/help - you r pidr\n/please let me speak my lady pls pls - ask to get right to speak\n/check Kirusha - you can assure yourself KIrusha is not under your bed... or vice versa...")
    elif message.text == "/please let me speak my lady pls pls" and not message.from_user.id == vuvaID:
        bot.send_message(message.chat_id, "oh, kitty, dont worry. You are too pretty so you even dont need allow to speak.")
    elif message.text == "/check Kirusha":
        case = random.randint(0, 11)
        if case == 0:
            bot.send_message(message.chat_id, "Right now Kirusha is cleaning pumps")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\CleaningPump', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 1:
            bot.send_message(message.chat_id, "Right now Kirusha in Sochi")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\sochi', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 2:
            bot.send_message(message.chat_id, "Kirusha is hunting")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\Hunting', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 3:
            bot.send_message(message.chat_id, "Kirusha in vuva`s locker")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\locker', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 4:
            bot.send_message(message.chat_id, "Kirusha enjoys by watching Vova in bath")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\bath', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 5:
            bot.send_message(message.chat_id, "Actually Kirusha is an Allseeing eye")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\eye', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 6:
            bot.send_message(message.chat_id, "Kirusha is eating after successful hunting")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\succses', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 7:
            bot.send_message(message.chat_id, "meow")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\kitty', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 8:
            bot.send_message(message.chat_id, "Kirusha is coming to you")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 9:
            bot.send_message(message.chat_id, "Kirusha after unsuccessful hunting")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\succses', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 10:
            bot.send_message(message.chat_id, "Kirusha is on bitch")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\bitch', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        elif case == 11:
            bot.send_message(message.chat_id, "I LOVE paRNis")
            with open('C:\Users\Кирилл\Pictures\DashaBotPictures\paris', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
                
bot.polling()