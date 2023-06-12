"""
 # @ Create Time: 2023-06-05 11:16:51.582403
"""

from dash import Dash, html, dcc, Input, Output
import dash
import random
import plotly.express as px
import pandas as pd
import src.waymoOpenDataset as waymoOpenDataset
import src.extractStaticFeatures as extractStaticFeatures
import src.extractAgentFeatures as extractAgentFeatures
import src.prediction as prediction
import src.extractDynamicMapFeatures as extractDynamicMapFeatures
import src.metrics as metrics
 

app = Dash(__name__, title="WaymoPathPredictionStudy")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


def initApp():
    
    scenarioID = random.randint(1, 10)
    
    data = waymoOpenDataset.getWaymoScenario(0, scenarioID)
    global trackCenter
    global trackSpeed
    global finalCoords
    global trackSize
    global trackDirection
    trackCenter, trackSpeed, finalCoords, trackSize, trackDirection = extractAgentFeatures.getRandomAgent(
        scenario=data
    )

    global figureStreet
    figureStreet = extractStaticFeatures.getRoadFeaturesScatterPlot(
        trackCenter[0], trackCenter[1], data
    )
    
    global figurePolygons
    figurePolygons = extractStaticFeatures.getPolygonFeaturesScatterPlot(
        trackCenter[0], trackCenter[1], data
    )
    
    global figureStopSign
    figureStopSign = extractStaticFeatures.getStopSignScatterPlot(
        trackCenter[0], trackCenter[1], data
    )

    global figurePredict
    figurePredict = prediction.getPredictionFigure(
        x=trackCenter[0],
        y=trackCenter[1],
        rotation=trackDirection,
        width=trackSize[0],
        lenght=trackSize[1],
        mapCenter_x=trackCenter[0],
        mapCenter_y=trackCenter[1],
    )
    
    global figurePredictionDot
    figurePredictionDot =  prediction.getPredictionDot(
        x=trackCenter[0],
        y=trackCenter[1],
        mapCenter_x=trackCenter[0],
        mapCenter_y=trackCenter[1],
    )

    global figureAgentsAndLaneStates
    figureAgentsAndLaneStates = extractDynamicMapFeatures.getDynamicLaneStates(
        trackCenter[0], trackCenter[1], data
    )

    global predictionCoordinate_x
    predictionCoordinate_x = trackCenter[0]
    global predictionCoordinate_y
    predictionCoordinate_y = trackCenter[1]

initApp()

app.layout = html.Div(
    children=[
        dcc.Markdown(
            """
                     # Plotly Path Prediction
                     Auswählen der Endposition über Drag & Drop 
                     
                     Auswählen der Drehung ist nicht relevant für die Auswertung
                     
                     Über erneutes Klicken des Abspielen knopfs kann der Datensatz erneut angesehen werden.
                     
                     Für eine korrekte Funktionsweise 100% Skallierung beibehalten
                     
                     ### Legende
                     
                     Statische Farben | Fahrzeug Farben   | Fahrspurmarkierungen 
                     ----------------- | ---------------- | --------------------
                     🔴 Stop Schilder | ⬛ Kraftfahrzeug | 🞅 Kein Status
                     🟧 Bodenschwellen | 🟧 Radfahrer    | 🟥 Status STOPP
                     🟦 Fußgängerüberwege | 🟩 Fußgänger | 🟨 Status ACHTUNG
                     🟩 Ein-/ Ausfahrten | 🔲 Nicht definierter Verkehrsteilnehmer | 🟩 Status FAHREN
                     🞉 Straßenamarkierungen | ⭕ Endposition des Fahrzeugs, welches vorhergesagt werden soll
                        
                     """
        ),
        html.Button("Vorhersage abgeben", 
                    id="newScenario", 
                    style={
                        "margin-top": "2rem",
                        "margin-left": "80px",
                        "cursor": "pointer",
                        "border-radius": "2px",
                        "border": "2px solid red",
                        "background": "#f4faff",
                        "padding": "6px",
                        "color": "#393939",
                    },
                    n_clicks=0),
        
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
            id="PredictionDot",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figurePredictionDot,
        ),
        dcc.Graph(
            id="Lanes",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=figureAgentsAndLaneStates,
        ),
        dcc.Graph(
            id="Predict",
            style={"display": "block", "position": "absolute", "width": "100%", "top": "550px"},
            figure=figurePredict,
        ),
    ]
)

clicks = 0

@app.callback(
    Output("Street", "figure"),
    Output("Polygon", "figure"),
    Output("StopSign", "figure"),
    Output("Predict", "figure"),
    Output("PredictionDot", "figure"),
    Output("Lanes", "figure"),
    [Input("newScenario", "n_clicks"), Input("Predict", "relayoutData")],
)
def guessScenarioSelected(n_clicks, graphData):
    
    global clicks
    global predictionCoordinate_x
    global predictionCoordinate_y
    global figurePredictionDot
    
    if clicks != n_clicks:
        clicks = n_clicks
        print(metrics.calculateMissBoolean8s(
                predictionCoordinate_x, 
                predictionCoordinate_y, 
                trackSpeed[0], 
                trackSpeed[1], 
                finalCoords[0], 
                finalCoords[1]
            )
        )
        initApp()
        return figureStreet, figurePolygons, figureStopSign, figurePredict, figurePredictionDot, figureAgentsAndLaneStates
    
    if graphData is not None:
        data = graphData["shapes"][-1]
        dx = data["x1"] - data["x0"]
        dy = data["y1"] - data["y0"]
        
        
        predictionCoordinate_x += dx
        predictionCoordinate_y += dy
        
        figurePredictionDot = prediction.getPredictionDot(
        x=predictionCoordinate_x,
        y=predictionCoordinate_y,
        mapCenter_x=trackCenter[0],
        mapCenter_y=trackCenter[1],
        )
        
        graphData = None
        return figureStreet, figurePolygons, figureStopSign, figurePredict, figurePredictionDot, figureAgentsAndLaneStates
    else:
        return dash.no_update
    
        


def dragAndDrop(graphData):
    if graphData is None:
        return dash.no_update
    print(graphData)
    
    return figurePredict

if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
