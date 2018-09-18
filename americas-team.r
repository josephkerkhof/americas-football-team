# Begin helper functions

readFile <- function(fileName){
  path = paste(paste("/tweets/", fileName, sep = ""), ".csv", sep = "")
  file = read.csv(path)
  return(file)
}

# End helper functions

# Begin execution

# Setting the team names
teams = c(
  "Arizona Cardinals",
  "Chicago Bears",
  "Green Bay Packers",
  "New York Giants",
  "Detroit Lions",
  "Washington Redskins",
  "Philadelphia Eagles",
  "Pittsburgh Steelers",
  "Los Angeles Rams",
  "San Francisco 49ers",
  "Cleveland Browns",
  "Indianapolis Colts",
  "Dallas Cowboys",
  "Kansas City Chiefs",
  "Los Angeles Chargers",
  "Denver Broncos",
  "New York Jets",
  "New England Patriots",
  "Oakland Raiders",
  "Tennessee Titans",
  "Buffalo Bills",
  "Minnesota Vikings",
  "Atlanta Falcons",
  "Miami Dolphins",
  "New Orleans Saints",
  "Cincinnati Bengals",
  "Seattle Seahawks",
  "Tampa Bay Buccaneers",
  "Carolina Panthers",
  "Jacksonville Jaguars",
  "Baltimore Ravens",
  "Houston Texans"
)

# Reading in the contents of the CSV files
Cardinals = readFile(teams[1])
Bears = readFile(teams[2])
Packers = readFile(teams[3])
Giants = readFile(teams[4])
Lions = readFile(teams[5])
Redskins = readFile(teams[6])
Eagles = readFile(teams[7])
Steelers = readFile(teams[8])
Rams = readFile(teams[9])
Fourty_Niners = readFile(teams[10])
Browns = readFile(teams[11])
Colts = readFile(teams[12])
Cowboys = readFile(teams[13])
Chiefs = readFile(teams[14])
Chargers = readFile(teams[15])
Broncos = readFile(teams[16])
Jets = readFile(teams[17])
Patriots = readFile(teams[18])
Raiders = readFile(teams[19])
Titans = readFile(teams[20])
Bills = readFile(teams[21])
Vikings = readFile(teams[22])
Falcons = readFile(teams[23])
Dolphins = readFile(teams[24])
Saints = readFile(teams[25])
Bengals = readFile(teams[26])
Seahawks = readFile(teams[27])
Buccaneers = readFile(teams[28])
Panthers = readFile(teams[29])
Jaguars = readFile(teams[30])
Ravens = readFile(teams[31])
Texans = readFile(teams[32])

# Computing the sentiment means for each team removing the NAs that appeared
team_means = c(
  mean(Cardinals$Sentiment, na.rm=TRUE),
  mean(Bears$Sentiment, na.rm=TRUE),
  mean(Packers$Sentiment, na.rm=TRUE),
  mean(Giants$Sentiment, na.rm=TRUE),
  mean(Lions$Sentiment, na.rm=TRUE),
  mean(Redskins$Sentiment, na.rm=TRUE),
  mean(Eagles$Sentiment, na.rm=TRUE),
  mean(Steelers$Sentiment, na.rm=TRUE),
  mean(Rams$Sentiment, na.rm=TRUE),
  mean(Fourty_Niners$Sentiment, na.rm=TRUE),
  mean(Browns$Sentiment, na.rm=TRUE),
  mean(Colts$Sentiment, na.rm=TRUE),
  mean(Cowboys$Sentiment, na.rm=TRUE),
  mean(Chiefs$Sentiment, na.rm=TRUE),
  mean(Chargers$Sentiment, na.rm=TRUE),
  mean(Broncos$Sentiment, na.rm=TRUE),
  mean(Jets$Sentiment, na.rm=TRUE),
  mean(Patriots$Sentiment, na.rm=TRUE),
  mean(Raiders$Sentiment, na.rm=TRUE),
  mean(Titans$Sentiment, na.rm=TRUE),
  mean(Bills$Sentiment, na.rm=TRUE),
  mean(Vikings$Sentiment, na.rm=TRUE),
  mean(Falcons$Sentiment, na.rm=TRUE),
  mean(Dolphins$Sentiment, na.rm=TRUE),
  mean(Saints$Sentiment, na.rm=TRUE),
  mean(Bengals$Sentiment, na.rm=TRUE),
  mean(Seahawks$Sentiment, na.rm=TRUE),
  mean(Buccaneers$Sentiment, na.rm=TRUE),
  mean(Panthers$Sentiment, na.rm=TRUE),
  mean(Jaguars$Sentiment, na.rm=TRUE),
  mean(Ravens$Sentiment, na.rm=TRUE),
  mean(Texans$Sentiment, na.rm=TRUE)
)

# Computing which team had the max sentiment value
indexOfMaxSentiment = which(team_means == max(team_means))
teamNameOfMaxSentiment = teams[indexOfMaxSentiment]

# Bar plot of team sentiments
par(mai=c(1,2,1,1))
barplot(team_means, main="NFL Team Sentiments", horiz=TRUE, names.arg=teams, las=1, xlim = c(-.05, .25))

# Sorting the team names and sentiment data
sortedTeamMeans = sort(team_means)
sortedTeamNames = teams[order(team_means)]
barplot(sortedTeamMeans, main="NFL Team Sentiments", horiz=TRUE, xlab = "Average Sentiment Value", names.arg=sortedTeamNames, las=1, xlim = c(-.05, .25))

# T-test to get the p-value of Seattle's sentiments are higher than Green Bay's sentiment
# H0: mu_packers = mu_seattle
# HA: mu_packers < mu_seattle
t.test(Packers$Sentiment, Seahawks$Sentiment, alternative = "less", conf.level = 0.95)

# End execution