import telebot, flask, reply_gen
from config import token, webhook_host, webhook_port

replier = reply_gen.Generator()
webhook_url_base = webhook_host+':'+webhook_port
webhook_url_path = "/{}/".format(token)

bot = telebot.TeleBot(token, threaded=False)  
bot.remove_webhook()

bot.set_webhook(url=webhook_url_base+webhook_url_path)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который отправляет предложение из других лексем, но с теми же грамматическими характеристиками.")


@bot.message_handler(func=lambda m: True)  
def send_reply(message):
	bot.send_message(message.chat.id, replier.reply(message.text))


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

 
@app.route(webhook_url_path, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
