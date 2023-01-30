import tweepy
import re
import json



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


def get_tweets(twitter_api, tweeter_user, tweets):
   
    # Count total number of tweets account has published to retrieve from
    user = twitter_api.get_user(screen_name=tweeter_user)
    max_user_tweets = user.statuses_count
    print(max_user_tweets)

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

#all_tweets = get_tweets('CryptoTubylec')


def save_tweets_in_json(username, tweets):
    with open(f'../data/processed/{username}-tweets.json', "w") as file:
        tweets_json = [tweet._json for tweet in tweets]
        json.dump(tweets_json, file)
        
    
def make_tweeets_dataset(tweets_dataframe_raw):
    return tweets_dataframe_raw[['created_at','id','text','entities','retweet_count','favorite_count']]
    
    #from pandas.io.json import json_normalize
    #json_normalize(tweets_df['entities'])[['symbols']].apply(lambda x: [dic['text'] for dic in x if 'text' in dic])
    #json_normalize(tweets_df['entities'])[['symbols']]    

    
def find_all_tweets_with_symbol(tweets_df, symbol):
    #@tweets_df - tweets df processed, where one column, called text, contains tweets text
    
    symbol_tweets = []

    for index, row in tweets_df.iterrows():
        
        # Look for a tweet text containing symbol
        found = re.findall('\\'+symbol+'\\w+', row.text)
        
        # If symbol found in tweet
        if found != []:
            symbol_tweets.append([row.id, row.created_at, [x.strip(symbol) for x in found]])
    
    return symbol_tweets

#find_all_tweets_with_symbol(tweets_df.text,'$')