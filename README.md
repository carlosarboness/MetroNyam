# MetroNyam
Choose your restaurant and go by metro!

## Getting Started

This project is divided in four parts: 

* `restaurant.py` : Contains all the code related to obtaining the list of restaurants and related searches.

* `metro.py` : Contains all the code related to the construction of the subway graph.


* `city.py` : Contains all the code related to the construction of the city graph and the search for routes between points in the city.


* `bot.py` : Contains all the code related to the Telegram bot and uses the city and restaurant modules. Its task is to react to user commands in order to guide them.


### Prerequisites

You will need to have `python3` and `pip3` updated. Check it with:
```
pip3 install --upgrade pip3
pip3 install --upgrade python3
```

To use the bot you will need a `Telegram` account as well as the `Telegram` app. It is available in [Play Store](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=ca), [App Store](https://apps.apple.com/es/app/telegram-messenger/id686449807) or in [Telegram's website](https://telegram.org).

In addition to this, in order to make a good usage of the project, you will need to create your own bot and save your acess token in a file called `token.txt`. To do that follow the _**Requirements**_ steps in [Lliçons de bots de Telegram](https://xn--llions-yua.jutge.org/python/telegram.html)

### Installing

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


## Usage

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

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

