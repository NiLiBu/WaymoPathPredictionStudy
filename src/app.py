"""
 # @ Create Time: 2023-06-05 11:16:51.582403
"""

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import src.waymoOpenDataset as waymoOpenDataset
import src.extractStaticFeatures as extractStaticFeatures
import src.extractAgentFeatures as extractAgentFeatures
import src.prediction as prediction
import src.extractDynamicMapFeatures as extractDynamicMapFeatures
 

app = Dash(__name__, title="WaymoPathPredictionStudy")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


data = waymoOpenDataset.getWaymoScenario(0, 5)
trackCenter, trackSize, trackDirection, tracks = extractAgentFeatures.getRandomAgent(
    scenario=data
)

figureStreet = extractStaticFeatures.getRoadFeaturesScatterPlot(
    trackCenter[0], trackCenter[1], data
)
figurePolygons = extractStaticFeatures.getPolygonFeaturesScatterPlot(
    trackCenter[0], trackCenter[1], data
)
figureStopSign = extractStaticFeatures.getStopSignScatterPlot(
    trackCenter[0], trackCenter[1], data
)

figurePredict = prediction.getPredictionFigure(
    x=trackCenter[0],
    y=trackCenter[1],
    rotation=trackDirection,
    width=trackSize[0],
    lenght=trackSize[1],
    mapCenter_x=trackCenter[0],
    mapCenter_y=trackCenter[1],
)

figureAgentsAndLaneStates = extractDynamicMapFeatures.getDynamicLaneStates(
    trackCenter[0], trackCenter[1], data
)

predictionCoordinate_x = trackCenter[0]
predictionCoordinate_y = trackCenter[1]


app.layout = html.Div(
    children=[
        dcc.Markdown(
            """
                     # Plotly Path Prediction
                     Auswählen der Endposition über Drag & Drop 
                     
                     Auswählen der Drehung ist nicht relevant für die Auswertung
                     
                     Über erneutes Klicken des Abspielen knopfs kann der Datensatz erneut angesehen werden.
                     
                     
                     ### Legende
                     
                     Statische Legende | Dynamische Legende 
                     ----------------- | -------------------
                     🔴 Stop Schilder | ⬛ Kraftfahrzeug
                     🟧 Bodenschwellen | 🟧 Radfahrer
                     🟦 Fußgängerüberwege | 🟩 Fußgänger
                     🟩 Ein-/ Ausfahrten | 🔲 Nicht definierter Verkehrsteilnehmer
                     🞉 Straßenamarkierungen | ⭕ Endposition des Fahrzeugs, welches vorhergesagt werden soll
                     🞅 Fahrstreifenmarkierung |
                        
                     """
        ),
        
        dcc.Graph(
            id="Street",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figureStreet,
        ),
        dcc.Graph(
            id="Polygon",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figurePolygons,
        ),
        dcc.Graph(
            id="StopSign",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figureStopSign,
        ),
        dcc.Graph(
            id="Predict",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figurePredict,
        ),
        dcc.Graph(
            id="Lanes",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figureAgentsAndLaneStates,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8052)

