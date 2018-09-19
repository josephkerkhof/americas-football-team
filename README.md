# America's Football Team

A Data Science project to quantitatively determine which NFL team is America's favorite with data from Twitter.

The Python code fetches the data from Twitter, cleans it, and performs sentiment analysis on each tweet. The R code produces graphs that show which team was favored most highly at the time of the tweets capture. Data for this project was captured just before the start of the 2018 NFL draft.

## Data Capture [Python]

My first step was to determine how to capture tweets and to which keywords I would look for inside a tweet. I decided to search for the team’s Twitter handle, main hashtag(s), and the team’s name spelled out in (ex. #GreenBayPackers). Once I had each of these team objects created, I queried Twitter to get a count of 10,000 tweets for each team.

## Data Cleaning & Sentiment Analysis [Python]

After collecting the tweets, I cleaned the text by stripping out special characters. Then I ran the tweets thru the sentiment analysis tool called [TextBlob](https://github.com/sloria/TextBlob/). Each team had a data frame stored in a separate object, which eased the exporting to a CSV file.

## Results [R]

Once this data was cleaned and processed, it was time to bring it into R for further analysis. Once in R, I created a sentiment mean for each team, sorted, and plotted them. As you can see in Figure 1, the Seattle Seahawks was the top performer sitting high and mighty with an average of about .2.

Unfortunately, my favorite team (the Green Bay Packers) were just coming off a hard season losing Aaron Rodgers to a season ending injury. This is my guess as to why the Packers mean sentiment analysis was so low.

_Figure 1_

![NFL Mean Sentiment - Figure 1.](https://i.imgur.com/ynXPHS5.png)

A graph of each NFL team's average sentiment analysis. A sentiment analysis ranges between -1 and 1, where -1 is a poor sentiment and 1 is a good sentiment.
