# Springboard Capstone - Buttersbot

## Purpose 
The Buttersbot chatbot was intended to help moderate chat rooms in discord using machine learning to help identify hate speech nonobvious offensive speech. Most bots currently have simple wordlist filters that can find obvious violations whereas language is more complex. 

## Warning
The repo may contain obscene speech and possibly even racial slurs.  These are intended for training/testing purposes ONLY they do not reflect any support from the author.  Please disregard and be advised. 


## What is here
In this repository:
* Capstone Proposal: Original document describing the project
* All jupyter notebooks for the various protype experiments as well as training.  Key ones:
** [Capstone - Data Wrangling](https://github.com/jeffnb/springboard-capstone/blob/master/Capstone%20-%20Deep%20Learning.ipynb)
** [Capstone - PreProcessing](https://github.com/jeffnb/springboard-capstone/blob/master/Capstone%20-%20PreProcessing.ipynb)
** [Capstone - Features](https://github.com/jeffnb/springboard-capstone/blob/master/Capstone%20-%20Features.ipynb)
** [Capstone - Machine Learning](https://github.com/jeffnb/springboard-capstone/blob/master/Capstone%20-%20Machine%20Learning.ipynb)
** [Capstone - Deep Learning](https://github.com/jeffnb/springboard-capstone/blob/master/Capstone%20-%20Deep%20Learning.ipynb)
* main.py: Entry point to start application locally
* src/: python source directory containing the chat bot
* model_data/: data allowing chatbot machine learning classifier to run

## How to run
The jupyter notebooks can easily be run in order above locally.  Be aware they run long and take a good deal of memory. 

### Bot
In order to run the bot in discord a new app has to be created with permissions to send messages, manage essages, view channels, and kick memebers.
Once added it is also required to allow the bot into the server you want.  Then using the key the bot can start running.


### Docker
The fastest way to get the system to run is with Docker.  You will need to create an app key with discord to fully run the system
* `docker build .` in the root directory
* `docker run -i -t --env DISCORD_KEY=<your discord key> <image hash>`

### Local
Locally, the bot is straight foward to set up but some requirements such as xgboost can be painful on Mac
* `pip install -r requirements.txt`
* `python3 main.py`

## What the bot does
* The bot monitors all communication and runs each message through a trained machine learning classifier.  The classifier tries to determine if it is Hate Speech, Offensive or Clean.  Depending on the settings for the running bot it will determine if the message is an issue.  If it is then the bot will delete the message with a warning in the channel and also DM the user asking them to avoid it in the future.  On exceeding the `infraction_limit` they will be kicked from the server.
* Commands:
** `!ping`: Just says `pong`
** `!hello`: greets back

