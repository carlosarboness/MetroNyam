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

### Installing

The packages needed for this bot are:
* `networkx` to manipulate graphs.
* `osmnx` to obtain city graphs (Barcelona in this case).
* `haversine` for calculating distances between coordinates.
* `staticmap` to draw and plot maps.
* `python-telegram-bot` to create and interact with a Telegram bot.
* `pandas` to read CSV files.
* `fuzzysearch` to do diffuse searches.


To install all the packages used in this bot you can execute the following command:
```
pip3 install -r requirements.txt
```

If you have problems with it you can install the packages one by one with `pip3 install` followed by the package name.

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

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

