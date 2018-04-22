
from pymorphy2 import MorphAnalyzer
from flask import Flask
import flask
import random
import telebot
morph = MorphAnalyzer()
#['NOUN', 'PREP', 'VERB', 'ADJF', 'CONJ', 'PRTS', 'PRCL', 'ADVB', 'NPRO', 'INTJ', 'GRND', 'ADJS', 'INFN', 'PRED', None, 'PRTF', 'NUMR', 'COMP']

TOKEN = "564610441:AAGw836BFLfnsoVK_fSbZklgnzljI8v3DuI"
WEBHOOK_HOST = 'orlov.pythonanywhere.com'
WEBHOOK_PORT = '443'

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TOKEN)

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)


app = Flask(__name__)

def vocabulary():
    words = []
    with open('text.txt', 'r', encoding = 'utf-8') as t:
         text = t.read()
         text = text.split()
         for item in text:
            item = item.strip('[!?.,:;()\ufeff]').lower()
            if item != '—':
                words.append(item)
    return words

def partsofspeach(vocab):
    #создать словари, в каждом из которых массив слов нужных, нужной части речи. потом будем выбирать рандомное слово
    pos = {}
    for item in vocab:
        anna = morph.parse(item)
        first = anna[0]
        if str(first.tag).split()[0] not in pos:
            pos[str(first.tag).split()[0]] = [first.word]
        else:
            pos[str(first.tag).split()[0]].append(first.word)
    return pos

def new_one(vocab, pos, sent):
    grammar = GrammarSequence(vocab, pos, sent) #массив из двух в массивов: в первом по порядку все неизменные признаки слова, во втором - изменяемые
    response = ''
    for i in range(0, len(grammar[0])):
        if grammar[0][i] in pos and grammar[1] != []:
            word = random.choice(pos[grammar[0][i]])
            ann = morph.parse(word)[0]
            if (grammar[1][i] != ' ')  and (ann.tag.POS != 'NPRO') and (ann.tag.POS != 'PREP') and (ann.tag.POS != 'CONJ'):
                if ',' in grammar[1][i]:
                    a = grammar[1][i].split(',')
                for item in a:
                        print(ann)
                        ann = ann.inflect({item})
            response = response + ' ' + ann.word
        else:
            response  = response + ' ' + sent.split()[i]
    return response




def GrammarSequence(vocab, pos, sent):
    grammarobl= []
    grammaropt = []
    sent = sent.split()
    for item in sent:
        anna = morph.parse(item)
        grammar = str(anna[0].tag)
        grammarobl.append(grammar.split()[0])
        if ' ' in grammar:
            grammaropt.append(grammar.split()[1])
        else:
            grammaropt.append(' ')
    return [grammarobl, grammaropt]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это моё дз по проге.")

@bot.message_handler(func=lambda m: True)
def my_function(message):
    vocab = vocabulary()
    pos = partsofspeach(vocab)
    text = new_one(vocab, pos, message)
    bot.send_message(message.chat.id, text)  # отправляем в чат наш ответ

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)



