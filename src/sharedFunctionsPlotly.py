import plotly.graph_objects as go
import math

GRAPH_SIZE = 1000
RANGE_DELTA = 100


def getPlotLayout(centerCoord_x: int, centerCoord_y: int) -> go.Layout:
    """
    Generate a Layout that can be used for all Plots

    Args:
        centerCoord_x (int): The start of the track to predict in x-Direction
        centerCoord_y (int): The start of the track to predict in y-Direction

    Returns:
        go.Layout: Layout to use in all Plots
    """
    return go.Layout(
        xaxis={"fixedrange": True, "visible": False},
        yaxis={"fixedrange": True, "visible": False},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=False,
        height=GRAPH_SIZE,
        width=GRAPH_SIZE,
        template="simple_white",
        showlegend=False,
        xaxis_range=[
            int(centerCoord_x - RANGE_DELTA),
            int(centerCoord_x + RANGE_DELTA),
        ],
        yaxis_range=[
            int(centerCoord_y - RANGE_DELTA),
            int(centerCoord_y + RANGE_DELTA),
        ],
    )


def getDragAndDropLayout(centerCoord_x: int, centerCoord_y: int) -> go.Layout:
    """
    Generate a Layout that can be used for all Plots

    Args:
        centerCoord_x (int): The start of the track to predict in x-Direction
        centerCoord_y (int): The start of the track to predict in y-Direction

    Returns:
        go.Layout: Layout to use in all Plots
    """
    return go.Layout(
        xaxis={"fixedrange": True, "visible": False},
        yaxis={"fixedrange": True, "visible": False},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=False,
        height=GRAPH_SIZE,
        width=GRAPH_SIZE,
        template="simple_white",
        showlegend=False,
        dragmode="drawline",
        # newshape={"line": {"color": "cyan"}},
        xaxis_range=[
            int(centerCoord_x - RANGE_DELTA),
            int(centerCoord_x + RANGE_DELTA),
        ],
        yaxis_range=[
            int(centerCoord_y - RANGE_DELTA),
            int(centerCoord_y + RANGE_DELTA),
        ],
    )


def getPolygonCoordsFromCenterCoords(
    center_x: float, center_y: float, degrees: int, width: float, length: float
) -> list[list[int]]:
    """
    Return the polygon coordinates of a rectangle with given center coordinated

    Args:
        center_x (_type_): _description_
        list (_type_): _description_

    Returns:
        _type_: _description_
    """
    rad = (360 - degrees) / 180 * math.pi  # the angle in rad instead of degrees

    Rx1 = center_x - (width / 2 * math.cos(rad)) - (length / 2 * math.sin(rad))
    Ry1 = center_y + (width / 2 * math.sin(rad)) - (length / 2 * math.cos(rad))

    Rx2 = center_x + (width / 2 * math.cos(rad)) - (length / 2 * math.sin(rad))
    Ry2 = center_y - (width / 2 * math.sin(rad)) - (length / 2 * math.cos(rad))

    Rx3 = center_x + (width / 2 * math.cos(rad)) + (length / 2 * math.sin(rad))
    Ry3 = center_y - (width / 2 * math.sin(rad)) + (length / 2 * math.cos(rad))

    Rx4 = center_x - (width / 2 * math.cos(rad)) + (length / 2 * math.sin(rad))
    Ry4 = center_y + (width / 2 * math.sin(rad)) + (length / 2 * math.cos(rad))

    return [Rx1, Rx2, Rx3, Rx4, Rx1], [Ry1, Ry2, Ry3, Ry4, Ry1]


def getPolygonCoordsFromCenterCoordsForMultipleInstances(
    center_x: float, center_y: float, degrees: int, width: float, length: float
) -> list[list[int]]:
    """
    Return the polygon coordinates of a rectangle with given center coordinated

    Args:
        center_x (_type_): _description_
        list (_type_): _description_

    Returns:
        _type_: _description_
    """
    rad = (360 - degrees) / 180 * math.pi  # the angle in rad instead of degrees

    Rx1 = center_x - (width / 2 * math.cos(rad)) - (length / 2 * math.sin(rad))
    Ry1 = center_y + (width / 2 * math.sin(rad)) - (length / 2 * math.cos(rad))

    Rx2 = center_x + (width / 2 * math.cos(rad)) - (length / 2 * math.sin(rad))
    Ry2 = center_y - (width / 2 * math.sin(rad)) - (length / 2 * math.cos(rad))

    Rx3 = center_x + (width / 2 * math.cos(rad)) + (length / 2 * math.sin(rad))
    Ry3 = center_y - (width / 2 * math.sin(rad)) + (length / 2 * math.cos(rad))

    Rx4 = center_x - (width / 2 * math.cos(rad)) + (length / 2 * math.sin(rad))
    Ry4 = center_y + (width / 2 * math.sin(rad)) + (length / 2 * math.cos(rad))

    return [Rx1, Rx2, Rx3, Rx4, None], [Ry1, Ry2, Ry3, Ry4, None]
