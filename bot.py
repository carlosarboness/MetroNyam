from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from staticmap import StaticMap, CircleMarker
import telegram
import random
import os
import restaurants as rs
import metro as mt
import city as cy 
import datetime
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Union


def init_city() -> None: 
    """ Inicializes the necessaty tools to set up the bot in the correct way """

    global restaurants
    restaurants = rs.read()  # We read the list of all restaurants

    global metro_graph
    metro_graph = mt.get_metro_graph()
    mt.plot(metro_graph, 'filename.png')

    global bcn_graph
    bcn_graph = cy.get_osmnx_graph()

    global city_graph
    city_graph = cy.build_city_graph(bcn_graph, metro_graph)


def start(update, context):
    """ Inicializes the bot and sends an introductory message to help the users start using it """

    init_city()

    user = update.effective_chat.first_name  # We get the user's first name

    salute = ''' 

Hola %s! Aquest bot t'ajudarà a trobar el restaurant més adient per a tú i t'hi portarà fins allà en el menor temps possible. 

Si necessites informació sobre totes les comandes disponibles escriu */help*. 

⚠️ *És important que enviis la teva ubicació actual per tal de que et puguem guiar correctament* ⚠️ 

Que vagi bé 🧡 

''' % (user)

    send_markdown(update, context, salute)


def help(update, context):
    """ Sends a message to the user with all the available commands the bot can use 
    and a breive explaination and some examples of them"""

    info = ''' 

*Soc un bot amb les comandes següents:* 

🚩 Amb */start* s'inicialitza el bot i podràs començar la conversa

🚩 Escriu */author* si vols saber els creadors del projecte 

🚩 Amb */find* podràs accedir a una llista de restaurants segons les teves preferències. Només has d'escriure la comanda i una o diverses sol·licituds al costat.

*Exemple: /find* pizza sants 

🚩 Si necessites informació sobre qualsevol dels restaurants de la llista, escriu */info* i el número del restaurant que estiguis interessat. 

*Exemple: /info* 4 

🚩 Si ja t'has decidit pel restaurant al que vols anar, escriu */guide* i el número del restaurant de la llista

*Exemple: /guide* 8 

🚩 La comanda */linies_metro* mostra una imatge de totes les linies de metro disponibles de Barcelona '''
    
    send_markdown(update, context, info)


def author(update, context): 
    """ Sends an informative text of the developers of the project and how to contact them"""

    info = '''

*Els creadors d'aquest projecte son 👨‍💻 :* 

📌 *Carlos Arbonés Sotomayor*
📪 carlos.arbones@estudiantat.upc.edu 

📌 *Benet Ramió Comas*
📪 benet.ramio@estudiantat.upc.edu
    
'''
    send_markdown(update, context, info)


def get_filtered_restaurants(update, context) -> rs.Restaurants:
    "Returns a list of restaurants that fulfill the requirements of the query"

    query: str = ""

    for i in range(0, len(context.args)):
        query += " " + str(context.args[i])

    return rs.find(query, restaurants)


def send_not_found_message(update, context) -> None: 
    """ Sends a message that no restaurants have been found """

    txt = '''

Ups! Sembla que no hi ha restaurants que coincideixen amb aquestes característiques.
            
*Intenta generalitzar una mica més per tal que de que puguem ajudar-te*.
            
'''
    send_markdown(update, context, txt)


def send_list_restaurants(update, context, filter: rs.Restaurants, selected_restaurants: dict) -> None: 
    """ Sends a list of 12 restaurants (or less if there are not 12) to the user, with a number
    in front to refer them and use other functions """

    txt = '''*Tria el teu Restaurant!* 👩🏻‍🍳🍽️ \n \n'''

    if len(filter) > 12: 
        j = 13
    else: 
        j = len(filter) + 1

    for i in range(1, j): 
        
        rest = filter[i-1]
        txt +=  '''〽️ *''' + str(i) + '''.* _''' + rest.get_name().replace("*", "") + '''_ \n'''
        selected_restaurants[i] = rest

    if 'rest' in context.user_data:
        del context.user_data['rest']
        
    context.user_data['rest'] = selected_restaurants

    send_markdown(update, context, txt)


def find(update, context): 
    """ Reads one or more requirements form the user and finds restaurants that 
    suit the conditions, if there are not restaurants that fulfill them, it sends 
    a message that there are no restaurants available and to try with other requirements,
    If it finds one or more restaurants, it prints their name """

    try:

        selected_restaurants: dict = {}
        filter: rs.Restaurants = get_filtered_restaurants(update, context)

        if len(filter) == 0: 

            send_not_found_message(update, context)

        else: 
            
            send_list_restaurants(update, context, filter, selected_restaurants)

    except Exception as e:

        error = ''' 
        
        🚨​ *Hi ha hagut un error, torna-ho a provar* 🚨​
        
        ''' 

        send_markdown(update, context, error)


def info(update, context): 
    """ Sends to the user information about the restaurant their decide. It prints
    an error message if the restaurant selected is not in the showed list.
    Prec: the /find command has already been used and it has been displayed the 
    list of available restaurants """

    try:
        n = int(context.args[0]) #  número del restaurant escollit
        rest: rs.Restaurant = context.user_data['rest'][n] #  accedim al restaurant escollit

        info = ''' ⚜️ *Informació del restaurant* ⚜️ \n \n'''
        info += '''ℹ️ *Nom:*  ''' + rest.get_name().replace("*", "") + '''\n'''
        info += '''ℹ️ *Adreça:*  ''' + rest.get_adress()[0] + ''', nº ''' + (rest.get_adress()[1])[:-2] + '''\n'''
        info += '''ℹ️ *Barri:*  ''' + rest.get_neighborhood() + '''\n'''
        info += '''ℹ️ *Districte:*  ''' + rest.get_district() + '''\n'''
        info += '''ℹ️ *Telèfon:*  ''' + rest.get_tel()
        
        send_markdown(update, context, info)

    except Exception as e:

        error = ''' 
        
        *Has de triar un número de la llista!!* 🤬
        
        ''' 
        send_markdown(update, context, error)


def random_name() -> str: 
    """ Returns a random name for the photo """

    return "%d.png" % random.randint(1000000, 9999999)  


def get_restaurant_location(update, context, n: int) -> Tuple[float, float]:
    """ Returns the location (coordinates) of the restaurant in position n """

    restaurant: rs.Restaurant = context.user_data['rest'][n]
    coordinates = restaurant.get_coord()
    return (float(coordinates[1]), float(coordinates[0]))


def save_photo_and_remove_file(update, context, fitxer: str) -> None: 
    """ Sends to telegram the photo in the file <fitxer> and removes the file """

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(fitxer, "rb"))
    os.remove(fitxer)


def calculate_end_time(journey_duration: int) -> str: 
    """ Returns the time is going to be by adding to the real time the
    journey duration, the output is a string in format hour:minutes """

    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=journey_duration)
    future_time_str = future_time.strftime('%m-%d-%Y %H:%M:%S.%f')

    return future_time_str[10:16]


def guide(update, context):
    """ Guides the user to the restaurant they select from the list"""

    try:

        fitxer: str = random_name() 
        n: int = int(context.args[0]) #  number of the restaurant the user wants to go

        ori_coord: cy.Coord = context.user_data['location']
        dst_coord: cy.Coord = get_restaurant_location(update, context, n)

        shortest_path: cy.Path = cy.find_path(bcn_graph, city_graph, ori_coord, dst_coord)
        cy.plot_path(city_graph, shortest_path, ori_coord, dst_coord, fitxer) #  we plot the path in file <fitxer>

        journey_duration: int = int(cy.time(city_graph, shortest_path)) #  time the user is going to spend travelling
        journey_end_time: str = calculate_end_time(journey_duration) #  calulates the time the user is going to arrive to the restaurant

        txt = ''' 
        
        🗺 *Informació del trajecte* 🗺

    El temps estimat que trigaràs és _d'aproximadament_ %d minuts. 

    Si surts ara arribaràs a les %s 🕐
        
    *Bon viatge !!* 🚆😁 
        
        ''' % (journey_duration, journey_end_time) 

        save_photo_and_remove_file(update, context, fitxer)
        
        send_markdown(update, context, txt)

    except Exception as e:
        print(e)
        error = ''' 
        
        📍 *Envia primer la teva localització* 📍
        
        ''' 
        send_markdown(update, context, error)

def linies_metro(update, context):
    """ Mostra una imatge de les linies del metro disponibles """

    try:

        fitxer: str = random_name()
        save_photo_and_remove_file(update, context, fitxer)

    except Exception as e:

        error = ''' 
        
        🚨​ *Hi ha hagut un error, torna-ho a provar* 🚨​
        
        ''' 

        send_markdown(update, context, error)


def your_location(update, context):
    """Stores the location of the user. """

    try:
        context.user_data['location'] = [
            update.message.location.longitude,
            update.message.location.latitude,
        ]
    except:

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your location wasn't shared succesfully",
        )


def send_markdown(update, context, info) -> None:
    """ Sends a message containing the given text in markdown format. """

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=info,
        parse_mode=telegram.ParseMode.MARKDOWN)


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
dispatcher.add_handler(MessageHandler(Filters.location, your_location))


updater.start_polling()