import tweepy
import re
import json
import plotly.express as px
import requests
import pandas as pd
from datetime import datetime

def twitter_auth(choice=['user','app']):

    # Twitter API authorization
    # Authenticate to Twitter
    consumer_key = '4Ft8G39Py6aBoJCO0BSv8sgd2'
    consumer_secret = '6ijVxle8eCqFSnGzP6KejCeZR6skWJguoufj6YFbDR5pVZrQMX'
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAACHAlQEAAAAAJprTqqhmpTWpWHPPzwnt%2FIoBWpw%3DAs7igyoLU5tA2v8pian9sWggiMGFDJjwwko5cqNsWvJBMjXGTE'
    access_token ='937601962077573120-U1NOzPdCshnXsTFjUG7zOyTq3LObFVW'
    access_token_secret = 'YnO3eV6ENps3hLrSTH9o7Yl5wKpXDIwgS95pqCfumDBAy'
    
    # Authorisation for user and app (different limits for user and app)
    auth_user = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    auth_app = tweepy.AppAuthHandler(consumer_key, consumer_secret)

    # Create API object for user and app (different limits for user and app)
    api_user = tweepy.API(auth_user, wait_on_rate_limit = True)
    api_app = tweepy.API(auth_app, wait_on_rate_limit = True)
    
    if choice == 'user':
        return api_user
    else:
        return api_app


def get_tweets(twitter_api, tweeter_user):
   
   
    # Check if twitter user exist
    # ........................
    # ........................
   
    # Count total number of tweets account has published to retrieve from
    user = twitter_api.get_user(screen_name=tweeter_user)
    max_user_tweets = user.statuses_count

    # List for storing all tweets
    all_tweets = []

    # first tweet id needed to start iteration over tweets with max_id param from user_timeline
    oldest_tweet_id = twitter_api.user_timeline(screen_name=tweeter_user, count=1)[0].id

    while len(all_tweets) < max_user_tweets:
        
        # max tweets to get from API is 200
        new_tweets = twitter_api.user_timeline(screen_name=tweeter_user, count=200, max_id=oldest_tweet_id)
        
        all_tweets.extend(new_tweets)
        
        oldest_tweet_id = all_tweets[-1].id
        
    return all_tweets

#all_tweets = get_tweets(app,'CryptoTubylec')


def save_tweets_in_json(username, tweets):
    with open(f'../data/processed/{username}-tweets.json', "w") as file:
        tweets_json = [tweet._json for tweet in tweets]
        json.dump(tweets_json, file)
        
    
def make_tweets_dataset(tweets_dataframe_raw):
    return tweets_dataframe_raw[['created_at','id','text','entities','retweet_count','favorite_count']]
    
    #from pandas.io.json import json_normalize
    #json_normalize(tweets_df['entities'])[['symbols']].apply(lambda x: [dic['text'] for dic in x if 'text' in dic])
    #json_normalize(tweets_df['entities'])[['symbols']]    

    
def find_all_tweets_with_symbol(tweets_df, symbol):
    #@tweets_df - tweets df processed, where one column, called text, contains tweets text
    
    symbols_tweets = []

    for index, row in tweets_df.iterrows():
        
        # Look for a tweet text containing symbol
        found = re.findall('\\'+symbol+'\\w+', row.text)
        #print(found)
        # If symbol found in tweet
        if found != []:
            symbols_tweets.append([row.id, row.created_at, [x.strip(symbol) for x in found], row.text])
    
    return symbols_tweets

#find_all_tweets_with_symbol(tweets_df,'$')[0]


# This function finds token name (coin_id) based on symbol given - 'CAW' will return 'a-hunters-dream'
def find_token_symbol(token_name):
    
    # Get table of coins with maaping to symbols from coingecko
    response_list = requests.get(f'https://api.coingecko.com/api/v3/coins/list')
    coins_list = json.loads(response_list.text)
    
    # Get coin name based on symbol given
    for c in coins_list:
        if c['symbol']==token_name.lower():
            return(c['id'])

# collect only tweets where desired token is mentioned and return tweets date
# collect only tweets where desired token is mentioned and return tweets date
def specific_token_tweets(token_name, tweets_list):
    tweets_with_specific_token = []        
    for i in tweets_list:
        if token_name in i[2]:
            #print(i[0], " - ", i[1].strftime("%Y-%m-%d %H:%M"),'UTC')
            tweets_with_specific_token.append([i[1].strftime("%Y-%m-%d %H:%M"),i[0], i[3]])
    return tweets_with_specific_token

#specific_token_tweets('CAW', alltweets)


def token_tweets_mentions_graph(token_name, only_tweets_with_token_symbol):

    import plotly.express as px
    
    # Define dates and labels for vertical lines
    tweets_dates = [i[0] for i in specific_token_tweets(token_name, only_tweets_with_token_symbol)]
    tweets_dates_labels = [i[2] for i in specific_token_tweets(token_name, only_tweets_with_token_symbol)]

    # How many days back phas to be retrieved from API price chart
    days_back = (datetime.now() - datetime.strptime(tweets_dates[-1], "%Y-%m-%d %H:%M")).days+7

    # Replacing symbol with actual token name from coingecko API
    token_coingecko_name = find_token_symbol(token_name)

    # Get CAW data from CoinGecko API
    url = f"https://api.coingecko.com/api/v3/coins/{token_coingecko_name}/market_chart?vs_currency=usd&days={days_back}"
    data = requests.get(url).json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')


    # Plot the price chart and add vertical lines with labels
    fig = px.line(df, x='timestamp', y='price')

    for d, l in zip(tweets_dates, tweets_dates_labels):
        
        fig.add_shape(type='line', x0=d, x1=d, y0=0, y1=1, xref='x', yref='paper',
                    line=dict(color='red', width=3), layer='above')
        
        fig.add_annotation(x=d, y=1.4, xref='x', yref='paper', text=d, textangle=-90,
                        showarrow=False, font=dict(color='red', size=10), hovertext=f"{l}: {d}")


    fig.update_layout(margin=dict(l=100, r=100, t=120, b=50), yaxis=dict(tickformat='e'), xaxis=dict(title=None),
                      title={'text': f"Price of {token_name} and corresponding tweets mentioned from ...", 'y':0.03, 'x':0.5} )
    
    return fig

# If searching for CAW token with price action of 150 days from todays date and tweets_df with tweets for given token 'CAW' (last parameter)
# token_tweets_mentions_graph('CAW', 150, find_all_tweets_with_symbol(tweets_df, '$'))