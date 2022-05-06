#https://t.me/arbonesbot.
#https://t.me/benetraco_bot


# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from staticmap import StaticMap, CircleMarker
import random
import os
import restaurants as rs
import metro as mt
import city as cy 


restaurants = rs.read()

m = mt.get_metro_graph()

g1 = cy.get_osmnx_graph()
g2 = cy.get_metro_graph()
g = cy.build_city_graph(g1, g2)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! T'ajudaré a trobar el millor restaurant per a tú =)")


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Soc un bot amb comandes:\n/start\n/help\n/author\n/find\n/info\n/guide\n/carrers_bcn\n/linies_metro.")


def author(update, context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Carlos Arbonés Sotomayor i Benet Ramió Comas")


rest_dict: dict = {}


def find(update, context): 
    try:
        query = str(context.args[0])
        filter = rs.find(query, restaurants)
        txt = "Tria el teu Restaurant! \n"

        j = 0

        if len(filter) > 12: 
            j = 13
        else: 
            j = len(filter) + 1

        for i in range(1, j): 
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
        txt = "Informació del restaurant \n"
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


def guide(update, context):
    key = update.effective_chat.id  # we use the user id as the key of the map
    try:
        fitxer = "%d.png" % random.randint(
            1000000, 9999999
        )  # generate a random name for the photo
        
        n = int(context.args[0])
        rest: rs.Restaurant = rest_dict[n]
        coord = rest.get_coord()
        dst = (float(coord[1]), float(coord[0]))
        location = context.user_data[key]
        s = cy.find_path(g1, g, location, dst)
        cy.plot_path(g, s, location, dst, fitxer)
        time = int(cy.time(g, s)/60)
        txt = "El temps estimat que trigaràs és de: " + str(time) + " minuts"
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(fitxer, "rb")
        )
        os.remove(fitxer)
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        # photo is made, send, and then removed
    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def carrers_bcn(update, context):
    try:
        fitxer = "%d.png" % random.randint(
            1000000, 9999999
        )  # generate a random name for the photo
        
        cy.plot1(g, fitxer)
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(fitxer, "rb")
        )
        os.remove(fitxer)
        # photo is made, send, and then removed
    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def linies_metro(update, context):
    try:
        fitxer = "%d.png" % random.randint(
            1000000, 9999999
        )  # generate a random name for the photo
        
        mt.plot(m, fitxer)
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(fitxer, "rb")
        )
        os.remove(fitxer)
        # photo is made, send, and then removed
    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def your_location(update, context):
    """Stores the location of the user.
    Complexity O(1)."""

    # stores in a map the location of the user using the id
    # of the user as the key
    try:
        key = update.effective_chat.id
        context.user_data[key] = [
            update.message.location.longitude,
            update.message.location.latitude,
        ]
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your location wasn't shared succesfully",
        )


def pos(update, context):
    """Stores the location of a user without sharing the location
    Precondition: if the location is send in coordinates, first parameter must be the latitude and the second one must be longitude.
    Complexity O(l), l being the length of context.args list."""

    try:
        origin = [float(context.args[1]), float(context.args[0])]
        # latitude and longitude are changed because in i_go module,
        # longitude is the first parameter and latitude is the second one
    except:
        street = context.args[0]
        for i in range(1, len(context.args)):
            street = " "
            street = context.args[i]
        street += ", Barcelona"  # if we add ", Barcelona" at the end,
        # geocode function becomes much more accurate
        coord = ox.geocode(street)
        origin = [coord[1], coord[0]]
        # latitude and longitude are changed because in i_go module,
        # longitude is the first parameter and latitude is the second one
    key = update.effective_chat.id
    context.user_data[key] = origin


def where(update, context):
    """Sends a photo of the location of the user
    Precondition: location has to be send previously or function /pos has to be used.
    Complexity O(1)."""

    key = update.effective_chat.id  # we use the user id as the key of the map
    try:
        location = context.user_data[key]
        fitxer = "%d.png" % random.randint(
            1000000, 9999999
        )  # generate a random name for the photo

        mapa = StaticMap(500, 500)
        mapa.add_marker(CircleMarker((location[0], location[1]), "blue", 10))
        imatge = mapa.render()
        imatge.save(fitxer)
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(fitxer, "rb")
        )
        os.remove(fitxer)
        # photo is made, send, and then removed

    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Your location must be sent"
        )


TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('find', find))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(CommandHandler('guide', guide))
dispatcher.add_handler(CommandHandler('carrers_bcn', carrers_bcn))
dispatcher.add_handler(CommandHandler('linies_metro', linies_metro))
dispatcher.add_handler(CommandHandler('pos', pos))
dispatcher.add_handler(CommandHandler('where', where))
dispatcher.add_handler(MessageHandler(Filters.location, your_location))


updater.start_polling()