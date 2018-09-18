import tweepy
import html
from textblob import TextBlob # make sure you have text blob installed in your python config
import re
import pandas as pd
import numpy as np
import os
import shutil
%run ~/twitter_credentials.py
auth = tweepy.OAuthHandler(consumer_key=con_key, consumer_secret=con_secret)
auth.set_access_token(acc_token, acc_secret)
api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Helper method to URL encode for the Twitter API
# Hashtag (#) HTML encoded is %23
# Ampersand (@) HTML encoded is %40
# Space ( ) HTML encoded is %20
def URLEncode(string):
    string = string.replace("@", "%40")
    string = string.replace("#", "%23")
    string = string.replace(" ", "%20")
    return string

# Utility function to clean the text in a tweet by removing links and special characters using regex.
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Utility function to classify the polarity of a tweet using textblob.
def analize_sentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity

# Defining the custom object for NFL teams
class NFLTeam(object):
    __twitter_handle = ""
    __team_name = ""
    __team_hashtags = []
    
    def __init__(self, twitter_handle, team_name, team_hashtags):
        self.__twitter_handle = twitter_handle
        self.__team_name = team_name
        self.__team_hashtags = team_hashtags
        
    def get_team_handle(self):
        return self.__twitter_handle
    
    def get_team_name(self):
        return self.__team_name
    
    def get_team_hashtags(self):
        return self.__team_hashtags

# Declaring an instance of every NFL team
ArizonaCardinals = NFLTeam("@AZCardinals", "Arizona Cardinals", ["#AZCardinals", "#ArizonaCardinals"])
ChicagoBears = NFLTeam("@ChicagoBears", "Chicago Bears", ["#ChicagoBears"])
GreenBayPackers = NFLTeam("@packers", "Green Bay Packers", ["#packers", "#GreenBayPackers"])
NewYorkGiants = NFLTeam("@Giants", "New York Giants", ["#NYGiants", "#newyorkgiants"])
DetroitLions = NFLTeam("@Lions", "Detroit Lions", ["#DetroitLions"])
WashingtonRedskins = NFLTeam("@Redskins", "Washington Redskins", ["#Redskins", "#WashingtonRedskins"])
PhiladelphiaEagles = NFLTeam("@Eagles", "Philadelphia Eagles", ["#Eagles", "#FlyEaglesFly", "#PhilidelphiaEagles"])
PittsburghSteelers = NFLTeam("@steelers", "Pittsburgh Steelers", ["#Steelers", "#pittsburghsteelers"])
LosAngelesRams = NFLTeam("@RamsNFL", "Los Angeles Rams", ["#LARams"])
SanFrancisco49ers = NFLTeam("@49ers", "San Francisco 49ers", ["#49ers", "#SanFransisco49ers"])
ClevelandBrowns = NFLTeam("@Browns", "Cleveland Browns", ["#Browns", "#ClevelandBrowns"])
IndianapolisColts = NFLTeam("@Colts", "Indianapolis Colts", ["#Colts", "#IndianapolisColts"])
DallasCowboys = NFLTeam("@dallascowboys", "Dallas Cowboys", ["#DallasCowboys", "#CowboysNation"])
KansasCityChiefs = NFLTeam("@Chiefs", "Kansas City Chiefs", ["#Chiefs", "#ChiefsKingdom"])
LosAngelesChargers = NFLTeam("@Chargers", "Los Angeles Chargers", ["#Chargers", "#LAChargers", "#losangeleschargers"])
DenverBroncos = NFLTeam("@Broncos", "Denver Broncos", ["#BroncosCountry", "#DenverBroncos"])
NewYorkJets = NFLTeam("@nyjets", "New York Jets", ["#Jets"])
NewEnglandPatriots = NFLTeam("@Patriots", "New England Patriots", ["#GoPats", "#Patriots" "#NEPatriots"])
OaklandRaiders = NFLTeam("@RAIDERS", "Oakland Raiders", ["#Raiders", "#oaklandraiders"])
TennesseeTitans = NFLTeam("@Titans", "Tennessee Titans", ["#TitanUp"])
BuffaloBills = NFLTeam("@buffalobills", "Buffalo Bills", ["#BuffaloBills"])
MinnesotaVikings = NFLTeam("@Vikings", "Minnesota Vikings", ["#Vikings", "#VikingsNation"])
AtlantaFalcons = NFLTeam("@AtlantaFalcons", "Atlanta Falcons", ["#AtlantaFalcons"])
MiamiDolphins = NFLTeam("@MiamiDolphins", "Miami Dolphins", ["#MiamiDolphins"])
NewOrleansSaints = NFLTeam("@Saints", "New Orleans Saints", ["#Saints", "#neworleansaints"])
CincinnatiBengals = NFLTeam("@Bengals", "Cincinnati Bengals", ["#Bengals", "#CincinnatiBengals"])
SeattleSeahawks = NFLTeam("@Seahawks", "Seattle Seahawks", ["#GoHawks", "#Seahawks"])
TampaBayBuccaneers = NFLTeam("@Buccaneers", "Tampa Bay Buccaneers", ["#GoBucs"])
CarolinaPanthers = NFLTeam("@Panthers", "Carolina Panthers", ["#CarolinaPanthers"])
JacksonvilleJaguars = NFLTeam("@Jaguars", "Jacksonville Jaguars", ["#DUUUVAL", "#JacksonvilleJaguars"])
BaltimoreRavens = NFLTeam("@Ravens", "Baltimore Ravens", ["#RavensFlock", "#BaltimoreRavins"])
HoustonTexans = NFLTeam("@HoustonTexans", "Houston Texans", ["#WeAreTexans", "#HoustonTexans"])

AllNFLTeams = [
    ArizonaCardinals,
    ChicagoBears,
    GreenBayPackers,
    NewYorkGiants,
    DetroitLions,
    WashingtonRedskins,
    PhiladelphiaEagles,
    PittsburghSteelers,
    LosAngelesRams,
    SanFrancisco49ers,
    ClevelandBrowns,
    IndianapolisColts,
    DallasCowboys,
    KansasCityChiefs,
    LosAngelesChargers,
    DenverBroncos,
    NewYorkJets,
    NewEnglandPatriots,
    OaklandRaiders,
    TennesseeTitans,
    BuffaloBills,
    MinnesotaVikings,
    AtlantaFalcons,
    MiamiDolphins,
    NewOrleansSaints,
    CincinnatiBengals,
    SeattleSeahawks,
    TampaBayBuccaneers,
    CarolinaPanthers,
    JacksonvilleJaguars,
    BaltimoreRavens,
    HoustonTexans
]

tweetsByTeam = {}

for team in AllNFLTeams:    
    # adding the team handle
    queryString = URLEncode(team.get_team_handle()) + "+OR+"
    # adding the team name
    teamName = team.get_team_name()
    queryString += URLEncode(teamName) + "+OR+"
    # adding the team hashtags
    team_hashtags = team.get_team_hashtags()
    for hashtag in team_hashtags:
        queryString += URLEncode(hashtag) + "+OR+"
    # trimming of the last +OR+
    queryString = queryString[:-4]
    
    # getting the tweets by team
    numNeeded = 10000
    tweets = []
    last_id = -1 # id of last tweet seen
    while len(tweets) < numNeeded:
        try:
            new_tweets = api.search(q=queryString + '-filter:retweets', count=100, max_id = str(last_id - 1))
        except tweepy.TweepError as e:
            print("Error", e)
            break
        else:
            if not new_tweets:
                print("Could not find any more tweets!")
                break
            tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
    
    print("Number of tweets: " + str(len(tweets)))
    
    # extracting the text from the tweets
    tweetsDF = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Raw Tweets'])
    
    # cleaning the tweet
    tweetsDF["Clean Tweets"] = [clean_tweet(tweet) for tweet in tweetsDF['Raw Tweets']]
    
    # sentiment analysis on the tweet
    tweetsDF["Sentiment"] = [analize_sentiment(tweet) for tweet in tweetsDF['Clean Tweets']]
    
    # organizing the tweets by team
    tweetsByTeam[teamName] = tweetsDF
    
    # notify console
    print("Finished " + teamName)

print("Finished collecting tweets... Saving to files.\n")

# Saving the tweets to a file
directory = "tweets"

# removing the contents of the tweets directory if the program was run before
if os.path.exists(directory):
    shutil.rmtree(directory)

# creating the directory for the CSV files
if not os.path.exists(directory):
    os.makedirs(directory)

# writing the tweets to files
for key, value in tweetsByTeam.items():
    path = directory + "/" + key + ".csv"
    value.to_csv(path, index=False)
    
print("Saving to files complete.")