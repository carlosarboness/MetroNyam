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
mt.plot(m, 'filename.png')


g1 = cy.get_osmnx_graph()
g2 = cy.get_metro_graph()
g = cy.build_city_graph(g1, g2)

def start(update, context):
    txt = "Hola! Aquest bot t'ajudarà a trobar el restaurant més adient per a tú i "
    txt += "t'hi portarà fins allà en el menor temps possible. Si necessites informació sobre"
    txt += "totes les comandes disponibles escriu /help. \n⚠️ És important que enviis la teva ubicació actual"
    txt +=  " per tal de que et puguem guiar correctament ⚠️ \nQue vagi bé 🧡"
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)


def help(update, context):
    txt = "Soc un bot amb les comandes següents: \n\n"
    txt += "• Amb /start s'inicialitza el bot i podràs començar la conversa\n\n"
    txt += "• Escriu /author si vols saber els creadors del projecte \n\n"
    txt += "• Amb /find podràs accedir a una llista de restaurants segons les teves preferències, "
    txt += "només has d'escriure la comanda i una o diverses sol·licituds al costat. \nExemple: "
    txt += "/find pizza sants \n\n"
    txt += "• Si necessites informació sobre qualsevol dels restaurants de la llista, "
    txt += "escriu /info i el número del restaurant que estiguis interessat. \nExemple: /info 4 \n\n"
    txt += "• Si ja t'has decidit pel restaurant al que vols anar, escriu /guide i el número del restaurant de la llista \n"
    txt += "Exemple: /guide 8 \n\n"
    txt += "• La comanda /linies_metro mostra una imatge de totes les linies de metro disponibles de Barcelona"
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)


def author(update, context): 
    txt = "Els creadors d'aquest projecte son: \n\n"
    txt += "• Carlos Arbonés Sotomayor \n"
    txt += "• Benet Ramió Comas"
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

def find(update, context):
    try:
        rest_dict = {}
        query = ""
        for i in range(0, len(context.args)):
            query += " " + str(context.args[i])
        filter = rs.find(query, restaurants)

        if len(filter) == 0: 
            txt = "Sembla que no hi ha restaurants amb aquestes característiques, intenta "
            txt += "generalitzar una mica més per tal que de que puguem ajudar-te."
            context.bot.send_message(chat_id=update.effective_chat.id, text=str(txt))
        else: 
            txt = "Tria el teu Restaurant! \n\n"

            j = 0

            if len(filter) > 12: 
                j = 13
            else: 
                j = len(filter) + 1

            for i in range(1, j): 
                rest = filter[i-1]
                txt += str(i) + ". " + rest.get_name() + "\n"
                rest_dict[i] = rest
            
            context.user_data['rest'] = rest_dict

            context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')


def info(update, context):
    try:
        n = int(context.args[0])
        rest: rs.Restaurant = context.user_data['restaurants'][n]
        txt = "Informació del restaurant \n\n"
        txt += "Nom:  " + rest.get_name() + "\n"
        txt += "Adreça:  " + rest.get_adress()[0] + ", nº " + (rest.get_adress()[1])[:-2] + "\n"
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
    try:
        fitxer = "%d.png" % random.randint(
            1000000, 9999999
        )  # generate a random name for the photo
        
        n = int(context.args[0])
        rest: rs.Restaurant = context.user_data['rest'][n]
        coord = rest.get_coord()
        dst = (float(coord[1]), float(coord[0]))
        location = context.user_data['loc']
        s = cy.find_path(g1, g, location, dst)
        cy.plot_path(g, s, location, dst, fitxer)
        time = int(cy.time(g, s)/60)
        txt = "El temps estimat que trigaràs és de: " + str(time) + " minuts. Bon viatge 😁"
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

def linies_metro(update, context):
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open('filename.png', "rb")
        )
    except Exception as e:
        print(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='💣')

def your_location(update, context):
    """Stores the location of the user.
    Complexity O(1)."""

    # stores in a map the location of the user
    try:
        context.user_data['loc'] = [
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
    context.user_data['loc'] = origin


def where(update, context):
    """Sends a photo of the location of the user
    Precondition: location has to be send previously or function /pos has to be used.
    Complexity O(1)."""

    try:
        location = context.user_data['loc']
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
dispatcher.add_handler(CommandHandler('linies_metro', linies_metro))
dispatcher.add_handler(CommandHandler('pos', pos))
dispatcher.add_handler(CommandHandler('where', where))
dispatcher.add_handler(MessageHandler(Filters.location, your_location))


updater.start_polling()