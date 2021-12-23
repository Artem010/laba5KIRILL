import telebot
from random import randint

token = '5034962954:AAGK81QU0MuDehyuYGbIWcxZ7_xRjKGxGKE'
bot = telebot.TeleBot(token);

slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'YO',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CH','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA'} # буква:транслит

userNum = {}
userStatus = {}


@bot.message_handler(commands=['start']) # отлавливаем команду /start от пользователя
def start_handler(message):
    bot.send_message(message.chat.id, f'*{message.from_user.first_name}*, привет! Это мой телеграм бот для 5 лабораторной работы. Напиши мне /info для ознакомления со всеми функциями', parse_mode= "Markdown")
    #отправляем в диалог c пользователем по message.chat.id текст вставив имея юзера, parse_mode отвечает за стили шрифта (жирный шрифт записывается *text*)
@bot.message_handler(commands=['info'])
def info_handler(message):
    text = "Бот умеет приветствовать пользователя, отправлять информаицю о боте (/info) Транслитировать строку (/func) играть в угадай число (/num)"
    bot.send_message(message.chat.id, text, parse_mode= "Markdown")
@bot.message_handler(commands=['func'])
def func_handler(message):
    userStatus[message.from_user.id] = 'func'
    bot.send_message(message.chat.id, "Введите текст:", parse_mode= "Markdown")
@bot.message_handler(commands=['num'])
def num_handler(message):
    if(message.text == '/num'):
        userStatus[message.from_user.id] = 'num' #записываем ифнормацию о статусе для данного пользователя по его ID {userid:number}
        userNum[message.from_user.id] = [str(randint(0, 99999)), ''] #записываем ифнормацию о загаданном числе и числе на этапе отгадывания для данного пользователя по его ID {userid:[number, numberNow]}
        for n in userNum[message.from_user.id][0]:
            userNum[message.from_user.id][1] += '-'
        bot.send_message(message.chat.id, text=f'Число *{userNum[message.from_user.id][1]}*\nВведите цифру:', parse_mode= "Markdown")



@bot.message_handler(content_types=['text'])
def get_text_message(message):
    userid = message.from_user.id
    if(userid in userStatus and userStatus[userid] == 'func'): #если статус пользователя == func
        t = message.text
        for key in slovar: #прогоняем через цикл каждую букву в строке
            t = t.replace(key, slovar[key]) # заменяем данную букву на значение по ключу словаря
        bot.send_message(message.chat.id, "Форматированный текст: *" +  t +  '*', parse_mode= "Markdown")
        del userStatus[userid]
    if(userid in userStatus and userStatus[userid] == 'num'):
        n = message.text
        if len(n) == 1:
            if n in userNum[message.from_user.id][0]:
                for i, nn in enumerate(userNum[message.from_user.id][0]): #проходим по каждому символу в загаданном числе i=index, тт=char
                    if(n == nn):
                        userNum[message.from_user.id][1] = userNum[message.from_user.id][1][:i] + nn + userNum[message.from_user.id][1][i+1:] #заменяем - на отгаданную букву по индексу в строке
        if(userNum[message.from_user.id][0] == userNum[message.from_user.id][1]):  #проверяем отгдал ли пользователь число
            bot.send_message(message.chat.id, text=f'Ура, вы отгадали число *{userNum[message.from_user.id][1]}*', parse_mode= "Markdown")
            del userStatus[userid] #удаляем ифнормацию о статусе
            del userNum[userid] #удаляем ифнормацию о числе
        else:
            bot.send_message(message.chat.id, text=f'Число *{userNum[message.from_user.id][1]}*\nВведите цифру:', parse_mode= "Markdown")

bot.polling(none_stop=True, interval=1); # запускаем бота и проверяем входящие сообщения каждую секунду
