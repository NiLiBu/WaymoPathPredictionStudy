# Dash Default Template: WaymoPathPredictionStudy

Created on 2023-06-05 11:16:51.582158

Welcome to your [Plotly Dash](https://plotly.com/dash/) App! This is a template for your WaymoPathPredictionStudy app.

See the [Dash Documentation](https://dash.plotly.com/introduction) for more information on how to get your app up and running.

## Running the App

Run `src/app.py` and navigate to http://127.0.0.1:8050/ in your browser.

Die Gunicorn App kann gestartet werden mit 

    gunicorn gunicorn src.app:server

Dazu muss das venv installiert und aktiviert werden

    python3.10 -m venv PlotlyDash/
    source PlotlyDash/bin/activate
    pip install -r requirements.txt
    docker build -t study .
    docker run -p 8080:80 study
