from flask import Flask, render_template, request
import pandas as pd
import json
#from /src/data/helper_functions import get_tweets

from flask import Flask
app = Flask(__name__)
app.debug = True




@app.route('/', methods=['GET', 'POST'])
def index():
    tweets_from_json = pd.read_json(f'../data/processed/CryptoTubylec-tweets.json')[['created_at','id','text','retweet_count','favorite_count']]

    if request.method == 'POST':
        #chart_type = request.form.get('chart')
        #input = request.form["inpstring"]
        
        string = request.form["inpstring"].lower()
        filtered_df = tweets_from_json[tweets_from_json['text'].str.lower().str.contains(string, na=False)]
        
        return render_template("index.html", inpstring=string, table=filtered_df.to_html())
    
    return render_template('index.html', inpstring=string, table=tweets_from_json.to_html())

if __name__ == "__main__":
    app.run(debug=True)