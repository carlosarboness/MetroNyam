#https://t.me/arbonesbot.

# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler
from restaurants import* 
from metro import* 
from city import* 


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! T'ajudaré a trobar el millor restaurant per a tú =)")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Soc un bot amb comandes /start, /help, /author, /find, /info i /guide.")

def author(update, context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Carlos Arbonés Sotomayor i Benet Ramió Comas")

def find(update, context): 
    try:
       query = str(context.args[0])
       
    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def info(update, context): ...


def guide(update, context): ...



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))


updater.start_polling()
