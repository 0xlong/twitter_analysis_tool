# Adding path to libraries directories to import them
#import sys
#sys.path.append('c:/Users/Longin/Desktop/Projects/twitter_analysis_tool/twitter_analysis_tool/twitter_analysis_tool/src/data')


from flask import Flask, render_template, request
import pandas as pd
import json
import helper_functions as hf
from flask import Flask
import plotly
import plotly.express as px

app = Flask(__name__)
app.debug = True




@app.route('/', methods=['GET', 'POST'])

def index():
    
    tweets_from_json = pd.read_json(f'../data/processed/CryptoTubylec-tweets.json')
    
    tweets_df = tweets_from_json[['created_at','id','text','entities','retweet_count','favorite_count']]
    
    alltweets = hf.find_all_tweets_with_symbol(tweets_df, '$')
    
    unique_symbols = list(dict.fromkeys([x.upper() for x in sum(list([d[2] for d in alltweets]), [])]))
    
    
    chart = hf.token_tweets_mentions_graph('CAW', 150, hf.find_all_tweets_with_symbol(tweets_df, '$'))
    
    print(chart.to_html())
    
    
    
    if request.method == 'POST':
        
        
        # Get token from dropdown list based on user front-end choice
        selected_coin = request.form['dropdown_choice']

        # Filter df based on the user choice
        filtered_df = tweets_df[tweets_df['text'].str.lower().str.contains(selected_coin.lower(), na=False)]
    
        # Return rendered page with filtere df, pass options list to dropdown menu and filtered df to table variable
        return render_template("index.html", choices = unique_symbols, table=filtered_df.to_html(), chart = chart.to_html())

    # If no choice return full dataframe
    return render_template('index.html', choices = unique_symbols, table=tweets_df.to_html(), chart=chart.to_html())
    

if __name__ == "__main__":
    app.run(debug=True)