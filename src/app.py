"""
 # @ Create Time: 2023-06-05 11:16:51.582403
"""

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import waymoOpenDataset
import extractStaticFeatures

app = Dash(__name__, title="WaymoPathPredictionStudy")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

data = waymoOpenDataset.getWaymoScenario(0, 1)


figure = extractStaticFeatures.getRoadFeaturesScatterPlot(3400, 1500, data)

app.layout = html.Div(
    children=[
        dcc.Markdown(
            """
                     # Plotly Path Prediction
                     Auswählen der Endposition über die Spinner unter diesem Text.
                     Bestätigen über den Bestätigungsknopf.
                     """
        ),
        dcc.Graph(id="example-graph", figure=figure),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
