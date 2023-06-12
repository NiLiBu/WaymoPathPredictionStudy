import src.sharedFunctionsPlotly as sharedFunctionsPlotly
import plotly.graph_objects as go


def getPredictionFigure(
    x: float,
    y: float,
    width: float,
    lenght: float,
    rotation: float,
    mapCenter_x: float,
    mapCenter_y: float,
):
    layout = sharedFunctionsPlotly.getDragAndDropLayout(
        centerCoord_x=mapCenter_x, centerCoord_y=mapCenter_y
    )
    
  

    x, y = sharedFunctionsPlotly.getPolygonCoordsFromCenterCoords(
        center_x=x, center_y=y, degrees=rotation, width=width, length=lenght
    )

    plot = go.Scattergl(
        x=x,
        y=y,
        hoverinfo="skip",
        mode="lines",
        fill="none",
        fillcolor='rgba(0,0,0, 1)',
        line= {
            "color": "red",
        }
    )

    return go.Figure(
        data=[plot],
        layout=layout,
    )
