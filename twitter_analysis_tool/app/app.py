# Adding path to libraries directories to import them
#import sys
#sys.path.append('c:/Users/Longin/Desktop/Projects/twitter_analysis_tool/twitter_analysis_tool/twitter_analysis_tool/src/data')

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json
import helper_functions as hf
from flask import Flask
import plotly.express as px
from datetime import datetime
import pickle

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # Launch twitter authorisation
    # twitter_auth = hf.twitter_auth('app')       
    
    selected_twitter_account = None
    
    print('Twitter user account NOT selected: ', selected_twitter_account)

    
    if request.method == 'POST':
        
        # Get input from html field
        selected_twitter_account = request.form.get('twitter_username')

        
        if selected_twitter_account:
            print('Twitter user account selected:', selected_twitter_account)
            
            #twitter_username_tweets = hf.get_tweets(twitter_auth, selected_twitter_account)
            #print('Tweets retrieved for ', selected_twitter_account)
        
            #hf.save_tweets_in_json(selected_twitter_account, twitter_username_tweets)
            #print('Tweets saved into json file ')
            
            tweets_from_json = pd.read_json(f'../data/processed/{selected_twitter_account}-tweets.json')
            print(datetime.now(), '- Tweets loaded from json file ')
            
            tweets_df = hf.make_tweets_dataset(tweets_from_json)
            print(datetime.now(), '- Dataset from tweets created')
            
            tweets_with_symbol = hf.find_all_tweets_with_symbol(tweets_df, '$')
            print(datetime.now(), '- Tweets with dollar symbol selected')
            
            unique_symbols = list(dict.fromkeys([x.upper() for x in sum(list([d[2] for d in tweets_with_symbol]), [])]))            
            print(datetime.now(), '- Unique tokens list created')
            
            with open(f'../data/processed/{selected_twitter_account}-data.pkl', 'wb') as handle:
                pickle.dump({'tweets_df': tweets_df, 'unique_symbols': unique_symbols}, handle, protocol=pickle.HIGHEST_PROTOCOL)       
                     
        return redirect(url_for('twitter_account_info', selected_twitter_account=selected_twitter_account))

    return render_template("index.html", twitter_username = '')


@app.route('/<selected_twitter_account>', methods=['GET', 'POST'])
def twitter_account_info(selected_twitter_account):
    
    
    print('Twitter info function: ', selected_twitter_account)
    

    with open(f'../data/processed/{selected_twitter_account}-data.pkl', 'rb') as handle:
        data = pickle.load(handle)
        
    tweets_df = data['tweets_df']
    unique_symbols = data['unique_symbols']     
    
    selected_coin = 'None'

    if request.method == 'POST':
        
        selected_coin = request.form.get('dropdown_choice')
        
        if selected_coin:
            
            print('Coin selected: ', selected_coin, 'for given user: ', selected_twitter_account)
            
            filtered_df = tweets_df[tweets_df['text'].str.lower().str.contains(selected_coin.lower(), na=False)]
            return render_template("twitter_user_account.html", choices=unique_symbols, table=filtered_df.to_html(), chart=hf.token_tweets_mentions_graph(selected_coin, hf.find_all_tweets_with_symbol(tweets_df, '$')).to_html(), twitter_username=selected_twitter_account, xxx = selected_coin)
        else:
            print('Coin NOT selected: ', selected_coin, 'for given user: ', selected_twitter_account)
            return render_template('twitter_user_account.html', choices=unique_symbols, table=tweets_df.to_html(), twitter_username=selected_twitter_account, xxx = selected_coin)
    
    return render_template("twitter_user_account.html", choices=unique_symbols, table=tweets_df.to_html(), twitter_username=selected_twitter_account, xxx = selected_coin)


if __name__ == "__main__":
    app.run(debug=True)