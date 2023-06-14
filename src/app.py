"""
 # @ Create Time: 2023-06-05 11:16:51.582403
"""

from dash import html, dcc, Input, Output, State
import dash
import src.initScenario as init
import src.waymoOpenDataset as waymoOpenDataset
import src.metrics as metrics
import src.prediction as prediction
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
from dash.exceptions import PreventUpdate

app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()])


# app = Dash(__name__, title="WaymoPathPredictionStudy")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

app.layout = html.Div(
    children=[
        dcc.Markdown(
            """
                     # Plotly Path Prediction
                     Auswählen der Endposition über Drag & Drop.
                     
                     Auswählen der Drehung ist nicht relevant für die Auswertung.
                     
                     Über erneutes Klicken des Abspielen knopfs kann der Datensatz erneut angesehen werden.
                     
                     Für eine korrekte Funktionsweise 100% Skallierung beibehalten.
                     
                     Es soll der Standort nach 8 Sekunden angegeben werden.
                     
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
        html.Button(
            "✅ Vorhersage abgeben",
            id="guessScenario",
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
            n_clicks=0,
        ),
        html.Button(
            "➖ Zoom Out",
            id="zoomOut",
            style={
                "margin-top": "2rem",
                "margin-left": "10px",
                "cursor": "pointer",
                "border-radius": "2px",
                "border": "2px solid #bec8d9",
                "background": "#f4faff",
                "padding": "6px",
                "color": "#393939",
            },
            n_clicks=0,
        ),
        html.Button(
            "➕ Zoom In",
            id="zoomIn",
            style={
                "margin-top": "2rem",
                "margin-left": "10px",
                "cursor": "pointer",
                "border-radius": "2px",
                "border": "2px solid #bec8d9",
                "background": "#f4faff",
                "padding": "6px",
                "color": "#393939",
            },
            n_clicks=0,
        ),
        html.Button(
            "▶️ Laden des Scenarios",
            id="loadScenario",
            style={
                "margin-top": "2rem",
                "margin-left": "10px",
                "cursor": "pointer",
                "border-radius": "2px",
                "border": "2px solid #bec8d9",
                "background": "#f4faff",
                "padding": "6px",
                "color": "#393939",
            },
            n_clicks=0,
        ),
        dcc.Store(id="ScenarioID"),
        dcc.Store(id="FileNumber"),
        dcc.Store(id="TrackData"),
        dcc.Store(id="ZoomLevel"),
        dcc.Store(id="PredictionX"),
        dcc.Store(id="PredictionY"),
        dcc.Graph(
            id="Street",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=init.blank_figure(),
        ),
        dcc.Graph(
            id="Polygon",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=init.blank_figure(),
        ),
        dcc.Graph(
            id="StopSign",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=init.blank_figure(),
        ),
        dcc.Graph(
            id="PredictionDot",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=init.blank_figure(),
        ),
        # Must be second lowset to allow Button "Abspielen der Verkehrssituation" to be pressed
        dcc.Graph(
            id="Lanes",
            style={"display": "block", "position": "absolute", "width": "100%"},
            figure=init.blank_figure(),
        ),
        # Predict has to be lowest for drag an drop functionallyty
        # Therefore it has spacing at the top that buttons underneath can be accessed
        dcc.Graph(
            id="Predict",
            style={
                "display": "block",
                "position": "absolute",
                "width": "100%",
                "top": "550px",
            },
            figure=init.blank_figure(),
        ),
    ]
)


@app.callback(
    Output("Street", "figure"),
    Output("Polygon", "figure"),
    Output("StopSign", "figure"),
    Output("Predict", "figure"),
    Output("PredictionDot", "figure"),
    Output("Lanes", "figure"),
    Output("TrackData", "data"),
    Output("ZoomLevel", "data"),
    Output("PredictionX", "data"),
    Output("PredictionY", "data"),
    Output("FileNumber", "data"),
    Output("ScenarioID", "data"),
    [
        Input("loadScenario", "n_clicks"),
    ],
)
def loadScenario(n_clicks):
    trackData, scenarioID, fileNumber = init.getRandomScenario()
    trackCenter, trackSpeed, finalCoords, trackSize, trackDirection, trackID = trackData
    ScenarioData = waymoOpenDataset.getWaymoScenario(fileNumber, scenarioID)
    (
        figureStreet,
        figurePolygons,
        figureStopSign,
        figureDragAndDrop,
        figurePrediction,
        figureAgentsAndLaneStates,
    ) = init.initScenario(ScenarioData, trackID, 100, trackCenter[0], trackCenter[1])

    return (
        figureStreet,
        figurePolygons,
        figureStopSign,
        figureDragAndDrop,
        figurePrediction,
        figureAgentsAndLaneStates,
        trackData,
        100,
        trackCenter[0],
        trackCenter[1],
        fileNumber,
        scenarioID,
    )


@app.callback(
    Output("PredictionDot", "figure"),
    Output("PredictionX", "data"),
    Output("PredictionY", "data"),
    [
        Input("Predict", "relayoutData"),
        State("ScenarioID", "data"),
        State("TrackData", "data"),
        State("ZoomLevel", "data"),
        State("PredictionX", "data"),
        State("PredictionY", "data"),
    ],
)
def dragAndDrop(graphData, ScenarioID, trackData, ZoomLevel, PredictionX, PredictionY):
    if (
        graphData is None
        or ZoomLevel is None
        or ScenarioID is None
        or trackData is None
    ):
        raise PreventUpdate
    else:
        data = graphData["shapes"][-1]
        dx = data["x1"] - data["x0"]
        dy = data["y1"] - data["y0"]

        predictionCoordinate_x = PredictionX + dx
        predictionCoordinate_y = PredictionY + dy

        (
            trackCenter,
            trackSpeed,
            finalCoords,
            trackSize,
            trackDirection,
            trackID,
        ) = trackData

        figurePrediction = prediction.getPredictionFigure(
            xPredict=predictionCoordinate_x,
            yPredict=predictionCoordinate_y,
            xStart=trackCenter[0],
            yStart=trackCenter[1],
            rotation=trackDirection,
            width=trackSize[0],
            lenght=trackSize[1],
            mapCenter_x=trackCenter[0],
            mapCenter_y=trackCenter[1],
            zoomLevel=ZoomLevel,
        )
        return figurePrediction, predictionCoordinate_x, predictionCoordinate_y


@app.callback(
    Output("Street", "figure"),
    Output("Polygon", "figure"),
    Output("StopSign", "figure"),
    Output("Predict", "figure"),
    Output("PredictionDot", "figure"),
    Output("Lanes", "figure"),
    Output("ZoomLevel", "data"),
    [
        Input("zoomOut", "n_clicks"),
        State("ZoomLevel", "data"),
        State("TrackData", "data"),
        State("FileNumber", "data"),
        State("ScenarioID", "data"),
        State("PredictionX", "data"),
        State("PredictionY", "data"),
    ],
)
def zoomOut(
    n_clicks, ZoomLevel, TrackData, FileNumber, ScenarioID, PredictionX, PredictionY
):
    if (
        n_clicks is None
        or ZoomLevel is None
        or TrackData is None
        or FileNumber is None
        or ScenarioID is None
    ):
        raise PreventUpdate
    else:
        (
            trackCenter,
            trackSpeed,
            finalCoords,
            trackSize,
            trackDirection,
            trackID,
        ) = TrackData
        ScenarioData = waymoOpenDataset.getWaymoScenario(FileNumber, ScenarioID)

        (
            figureStreet,
            figurePolygons,
            figureStopSign,
            figureDragAndDrop,
            figurePrediction,
            figureAgentsAndLaneStates,
        ) = init.initScenario(
            ScenarioData,
            trackID,
            zoomLevel=ZoomLevel * 1.3,
            predictionX=PredictionX,
            predictionY=PredictionY,
        )

        return (
            figureStreet,
            figurePolygons,
            figureStopSign,
            figureDragAndDrop,
            figurePrediction,
            figureAgentsAndLaneStates,
            ZoomLevel * 1.3,
        )


@app.callback(
    Output("Street", "figure"),
    Output("Polygon", "figure"),
    Output("StopSign", "figure"),
    Output("Predict", "figure"),
    Output("PredictionDot", "figure"),
    Output("Lanes", "figure"),
    Output("ZoomLevel", "data"),
    [
        Input("zoomIn", "n_clicks"),
        State("ZoomLevel", "data"),
        State("TrackData", "data"),
        State("FileNumber", "data"),
        State("ScenarioID", "data"),
        State("PredictionX", "data"),
        State("PredictionY", "data"),
    ],
)
def zoomIn(
    n_clicks, ZoomLevel, TrackData, FileNumber, ScenarioID, PredictionX, PredictionY
):
    if (
        n_clicks is None
        or ZoomLevel is None
        or TrackData is None
        or FileNumber is None
        or ScenarioID is None
    ):
        raise PreventUpdate
    else:
        (
            trackCenter,
            trackSpeed,
            finalCoords,
            trackSize,
            trackDirection,
            trackID,
        ) = TrackData
        ScenarioData = waymoOpenDataset.getWaymoScenario(FileNumber, ScenarioID)

        (
            figureStreet,
            figurePolygons,
            figureStopSign,
            figureDragAndDrop,
            figurePrediction,
            figureAgentsAndLaneStates,
        ) = init.initScenario(
            ScenarioData,
            trackID,
            zoomLevel=ZoomLevel * 0.7,
            predictionX=PredictionX,
            predictionY=PredictionY,
        )

        return (
            figureStreet,
            figurePolygons,
            figureStopSign,
            figureDragAndDrop,
            figurePrediction,
            figureAgentsAndLaneStates,
            ZoomLevel * 0.7,
        )


@app.callback(
    Output("Street", "figure"),
    Output("Polygon", "figure"),
    Output("StopSign", "figure"),
    Output("Predict", "figure"),
    Output("PredictionDot", "figure"),
    Output("Lanes", "figure"),
    Output("TrackData", "data"),
    Output("ZoomLevel", "data"),
    Output("PredictionX", "data"),
    Output("PredictionY", "data"),
    Output("FileNumber", "data"),
    Output("ScenarioID", "data"),
    [
        Input("guessScenario", "n_clicks"),
        State("TrackData", "data"),
        State("ZoomLevel", "data"),
        State("PredictionX", "data"),
        State("PredictionY", "data"),
        State("FileNumber", "data"),
        State("ScenarioID", "data"),
    ],
)
def predictionFinished(
    n_clicks,
    ScenarioDatei,
    TrackData,
    ZoomLevel,
    PredictionX,
    PredictionY,
    FileNumber,
    ScenarioID,
):
    if (
        n_clicks is None
        or ZoomLevel is None
        or ScenarioDatei is None
        or ScenarioID is None
        or TrackData is None
        or FileNumber is None
        or ScenarioID is None
    ):
        raise PreventUpdate
    else:
        (
            trackCenter,
            trackSpeed,
            finalCoords,
            trackSize,
            trackDirection,
            trackID,
        ) = TrackData

        displacement = metrics.calculateDisplacementError(
            PredictionX,
            PredictionY,
            trackSpeed[0],
            trackSpeed[1],
            finalCoords[0],
            finalCoords[1],
        )
        missRate = metrics.calculateMissBoolean8s(
            PredictionX,
            PredictionY,
            trackSpeed[0],
            trackSpeed[1],
            finalCoords[0],
            finalCoords[1],
        )

        with open("src/results.csv", "a") as file:
            file.write(
                "%s, %s, %s, %s, %s, %s \n"
                % (
                    str(FileNumber),
                    str(PreventUpdate),
                    str(trackID),
                    str(missRate),
                    str(displacement[0]),
                    str(displacement[1]),
                )
            )

        trackData, ScenarioID, fileNumber = init.getRandomScenario()
        ScenarioData = waymoOpenDataset.getWaymoScenario(FileNumber, ScenarioID)
        (
            trackCenter,
            trackSpeed,
            finalCoords,
            trackSize,
            trackDirection,
            trackID,
        ) = trackData
        (
            figureStreet,
            figurePolygons,
            figureStopSign,
            figureDragAndDrop,
            figurePrediction,
            figureAgentsAndLaneStates,
        ) = init.initScenario(
            ScenarioData, trackID, 100, trackCenter[0], trackCenter[1]
        )

        return (
            figureStreet,
            figurePolygons,
            figureStopSign,
            figureDragAndDrop,
            figurePrediction,
            figureAgentsAndLaneStates,
            trackData,
            100,
            trackCenter[0],
            trackCenter[1],
            fileNumber,
            ScenarioID,
        )


if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
