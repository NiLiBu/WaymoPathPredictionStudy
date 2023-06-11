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
 

app = Dash(__name__, title="WaymoPathPredictionStudy")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


data = waymoOpenDataset.getWaymoScenario(0, 1)
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

figureAgents = extractAgentFeatures.getAllAgentsScatterPlot(
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
                     Auswählen der Drehung über den Slider (Die Drehung ist nicht relevant für die Auswertung)
                     
                     
                     ### Legende
                        🔴 Stop Schilder
                        
                        🟧 Bodenschwellen
                        
                        🟨 Fußgängerüberwege
                        
                        🟩 Ein-/ Ausfahrten
                        
                        🞉 Straßenamarkierungen
                        
                        🞅 Fahrstreifenmarkierung
                        
                     """
        ),
        dcc.Graph(
            id="Predict",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figurePredict,
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
            id="Agents",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figureAgents,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
