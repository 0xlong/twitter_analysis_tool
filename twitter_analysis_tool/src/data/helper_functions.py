import tweepy

def get_tweets(api, tweeter_user, tweets):
    
    # Specify the Twitter account you want to check
    #username = 'CryptoTubylec'

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
    
    # Count total number of tweets account has published to retrieve from
    user = api.get_user(screen_name=tweeter_user)
    max_user_tweets = user.statuses_count
    print(max_user_tweets)

    # List for storing all tweets
    all_tweets = []

    # first tweet id needed to start iteration over tweets with max_id param from user_timeline
    oldest_tweet_id = api.user_timeline(screen_name=tweeter_user, count=1)[0].id

    while len(all_tweets) < max_user_tweets:
        
        # max tweets to get from API is 200
        new_tweets = api.user_timeline(screen_name=tweeter_user, count=200, max_id=oldest_tweet_id)
        
        all_tweets.extend(new_tweets)
        
        oldest_tweet_id = all_tweets[-1].id
        
    return all_tweets

#all_tweets = get_tweets('CryptoTubylec')

def get_tweets():
    
    # Specify the Twitter account you want to check
    #username = 'CryptoTubylec'

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
        
    return all_tweets