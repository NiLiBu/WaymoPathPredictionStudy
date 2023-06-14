import src.sharedFunctionsPlotly as sharedFunctionsPlotly
import plotly.graph_objects as go


def getDragAndDropFigure(mapCenter_x: float, mapCenter_y: float, zoomLevel):
    layout = sharedFunctionsPlotly.getDragAndDropLayout(
        centerCoord_x=mapCenter_x, centerCoord_y=mapCenter_y, zoomLevel=zoomLevel
    )

    return go.Figure(
        data=[],
        layout=layout,
    )


def getPredictionFigure(
    xPredict: float,
    yPredict: float,
    xStart: float,
    yStart: float,
    width: float,
    lenght: float,
    rotation: float,
    mapCenter_x: float,
    mapCenter_y: float,
    zoomLevel,
):
    x, y = sharedFunctionsPlotly.getPolygonCoordsFromCenterCoords(
        center_x=xStart, center_y=yStart, degrees=rotation, width=width, length=lenght
    )

    plotStart = go.Scattergl(
        x=x,
        y=y,
        hoverinfo="skip",
        mode="lines",
        fill="none",
        fillcolor="rgba(0,0,0, 0)",
        line={
            "color": "rgba(255,0,0, 1)",
        },
    )

    layout = sharedFunctionsPlotly.getPlotLayout(
        centerCoord_x=mapCenter_x, centerCoord_y=mapCenter_y, zoomLevel=zoomLevel
    )
    plotPredict = go.Scattergl(
        x=[xPredict],
        y=[yPredict],
        hoverinfo="skip",
        mode="markers",
        marker={
            "color": "white",
            "line": {
                "color": "red",
                "width": 2,
            },
            "size": 8,
            "symbol": "octagon",
        },
    )

    return go.Figure(
        data=[plotStart, plotPredict],
        layout=layout,
    )
