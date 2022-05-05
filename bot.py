#https://t.me/arbonesbot.

# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler
import restaurants as rs
from metro import* 
from city import* 


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! T'ajudaré a trobar el millor restaurant per a tú =)")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Soc un bot amb comandes: \n /start \n /help \n  /author \n  /find \n  /info \n  /guide.")

def author(update, context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Carlos Arbonés Sotomayor i Benet Ramió Comas")

rest_dict: dict = {}

def find(update, context): 
    try:
        restaurants = rs.read()
        query = str(context.args[0])
        filter = rs.find(query, restaurants)
        txt = "Tria el teu Restaurant!"

        for i in range(1, 13): 
            rest = filter[i-1]
            txt += str(i) + ". " + rest.get_name() + "\n"
            rest_dict[i] = rest
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(txt))

    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def info(update, context): 
    try:
        n = int(context.args[0])
        rest: rs.Restaurant = rest_dict[n]
        txt = "Informació del restaurant"
        txt += "Nom:  " + rest.get_name() + "\n"
        txt += "Adreça:  " + rest.get_adress()[0] + ", " + rest.get_adress()[1] + "\n"
        txt += "Barri:  " + rest.get_neighborhood() + "\n"
        txt += "Districte:  " + rest.get_district() + "\n"
        txt += "Telèfon:  " + rest.get_tel()
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(txt))

    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def guide(update, context): ...



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('find', find))
dispatcher.add_handler(CommandHandler('info', info))


updater.start_polling()
