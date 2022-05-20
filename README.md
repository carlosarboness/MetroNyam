# MetroNyam 🍲 🚇 
Choose your restaurant and go by metro!

## Getting Started ✍🏻

This project is divided in four parts: 

* `restaurant.py` : Contains all the code related to obtaining the list of restaurants and related searches.

* `metro.py` : Contains all the code related to the construction of the subway graph.


* `city.py` : Contains all the code related to the construction of the city graph and the search for routes between points in the city.


* `bot.py` : Contains all the code related to the Telegram bot and uses the city and restaurant modules. Its task is to react to user commands in order to guide them.


### Prerequisites 📃

You will need to have `python3` and `pip3` updated. Check it with:
```
pip3 install --upgrade pip3
pip3 install --upgrade python3
```

To use the bot you will need a `Telegram` account as well as the `Telegram` app. It is available in [Play Store](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=ca), [App Store](https://apps.apple.com/es/app/telegram-messenger/id686449807) or in [Telegram's website](https://telegram.org).

In addition to this, in order to make a good usage of the project, you will need to create your own bot and save your acess token in a file called `token.txt`. To do that follow the _**Requirements**_ steps in [Lliçons de bots de Telegram](https://xn--llions-yua.jutge.org/python/telegram.html)

### Installing 🛠

The packages needed for this bot are:
* `networkx` to manipulate graphs.
* `osmnx` to obtain city graphs (Barcelona in this case).
* `haversine` for calculating distances between coordinates.
* `staticmap` to draw and plot maps.
* `python-telegram-bot` to create and interact with a Telegram bot.
* `pandas` to read CSV files.
* `fuzzysearch` to do diffuse searches.
* `typing_extensions` to define a new name for a type.


To install all the packages used in this bot you can execute the following command:
```
pip3 install -r requirements.txt
```

If you have problems with it you can install the packages one by one with `pip3 install` followed by the package name.


## Usage 🤖 

**Note**: this bot is configured to work with _**Barcelona**_ street network by default, therefore, interaction with the user is made in _Catalan language_.
To use the bot you must first open your telegram account and select the chat of the bot you created. Then execute bot.py in the terminal using python3:
```
python3 bot.py
```

Now you are ready to use the MetroNyam bot!

Type `/start` in the chat and the bot will present itself and offer you some help on usage. To use the bot, you must share its location so it can guide you properly. If the location is not shared, a command will report an error.

These are commands that the bot has:
* `/start`: starts the conversation.

* `/help`: offers help with available commands.

* `/author`: shows the name of the project authors.

* `/find <query>`: Find which restaurants satisfy the search and write a numbered list (12 items at most). For example: /find pizza sants.

* `/info <numero>`: shows the restaurant information specified by its number (selected from the last numbered list obtained with /find). For example: /info 4

* `/guide <numero>`: shows a map with the shortest path from the current point where the user is to the restaurant specified by their number (chosen from the last numbered list obtained with /find). For example: /guide 8

* `metro_map`: shows a map with all the available metro lines in Barcelona.

Great! Now let's see a real example.

<p float="left">
  <img src="https://github.com/carlosarboness/MetroNyam/blob/main/tutorial1.png" width=30% height=30%> 
  <img src="https://github.com/carlosarboness/MetroNyam/blob/main/tutorial2.png" width=30% height=30%>
</p>
<p float="left">
  <img src="https://github.com/carlosarboness/MetroNyam/blob/main/tutorial3.png" width=30% height=30%> 
  <img src="https://github.com/carlosarboness/MetroNyam/blob/main/tutorial4.png" width=30% height=30%>
 </p>

If you want to see how to use the bot in more detail in a video, you can click [here](https://www.youtube.com/watch?v=x0kZpj33Yz0).
## Authors 👨🏼‍🎓 

Developed by [Carlos Arbonés Sotomayor](https://github.com/carlosarboness) and [Benet Ramió i Comas](https://github.com/benetraco).

For more information abot the project, please contact us at: `carlos.arbones@estudiantat.upc.edu` and `benet.ramio@estudiantat.upc.edu`.

Data Science and Engineering students at UPC, 2022
