import plotly.graph_objects as go

GRAPH_SIZE = 2000
RANGE_DELTA = 200


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
        newshape=dict({"line": {"color": "rgba(0, 0, 0, 0.5)"}}),
        xaxis_range=[
            int(centerCoord_x - RANGE_DELTA),
            int(centerCoord_x + RANGE_DELTA),
        ],
        yaxis_range=[
            int(centerCoord_y - RANGE_DELTA),
            int(centerCoord_y + RANGE_DELTA),
        ],
    )
