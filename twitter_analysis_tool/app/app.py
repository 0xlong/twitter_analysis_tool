from flask import Flask, render_template, request
import pandas as pd
#from /src/data/helper_functions import get_tweets

from flask import Flask
app = Flask(__name__)
app.debug = True


#pd.read_csv()
charts = ['chart1', 'chart2', 'chart3']



@app.route('/', methods=['GET', 'POST'])
def index():
    input = None
    if request.method == 'POST':
        input = request.form["inpstring"]
    else:
        chart_name = None
    return render_template('index.html', inpstring=input, chart_name=charts)

if __name__ == "__main__":
    app.run(debug=True)