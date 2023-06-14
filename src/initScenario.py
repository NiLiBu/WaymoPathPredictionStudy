import random
import src.waymoOpenDataset as waymoOpenDataset
import src.extractStaticFeatures as extractStaticFeatures
import src.extractAgentFeatures as extractAgentFeatures
import src.prediction as prediction
import src.extractDynamicMapFeatures as extractDynamicMapFeatures
import plotly.graph_objects as go


def getRandomScenario():
    scenarioID = random.randint(1, 1000)
    fileNumber = random.randint(0, 0)
    data = waymoOpenDataset.getWaymoScenario(fileNumber, scenarioID)

    (
        trackCenter,
        trackSpeed,
        finalCoords,
        trackSize,
        trackDirection,
        trackID,
    ) = extractAgentFeatures.getAgentParams(scenario=data, trackID=None)

    return (
        (extractAgentFeatures.getAgentParams(scenario=data, trackID=trackID)),
        scenarioID,
        fileNumber,
    )


def initScenario(scenarioData, trackID, zoomLevel, predictionX, predictionY):
    (
        trackCenter,
        trackSpeed,
        finalCoords,
        trackSize,
        trackDirection,
        trackID,
    ) = extractAgentFeatures.getAgentParams(scenario=scenarioData, trackID=trackID)

    figureStreet = extractStaticFeatures.getRoadFeaturesScatterPlot(
        trackCenter[0], trackCenter[1], scenarioData, zoomLevel
    )

    figurePolygons = extractStaticFeatures.getPolygonFeaturesScatterPlot(
        trackCenter[0], trackCenter[1], scenarioData, zoomLevel
    )

    figureStopSign = extractStaticFeatures.getStopSignScatterPlot(
        trackCenter[0], trackCenter[1], scenarioData, zoomLevel
    )

    figureDragAndDrop = prediction.getDragAndDropFigure(
        mapCenter_x=trackCenter[0], mapCenter_y=trackCenter[1], zoomLevel=zoomLevel
    )

    figurePrediction = prediction.getPredictionFigure(
        xPredict=predictionX,
        yPredict=predictionY,
        xStart=trackCenter[0],
        yStart=trackCenter[1],
        rotation=trackDirection,
        width=trackSize[0],
        lenght=trackSize[1],
        mapCenter_x=trackCenter[0],
        mapCenter_y=trackCenter[1],
        zoomLevel=zoomLevel,
    )

    figureAgentsAndLaneStates = extractDynamicMapFeatures.getDynamicLaneStates(
        trackCenter[0], trackCenter[1], scenarioData, zoomLevel
    )

    return (
        figureStreet,
        figurePolygons,
        figureStopSign,
        figureDragAndDrop,
        figurePrediction,
        figureAgentsAndLaneStates,
    )


def blank_figure():
    fig = go.Figure(go.Scattergl(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig
