from waymo_open_dataset.protos import scenario_pb2
import sharedFunctionsPlotly
import plotly.graph_objects as go


def extractRoadFeatures(
    scenario: scenario_pb2.Scenario,
) -> list[list[int]]:
    """
    Extract road lines, road lanes and road edges from the dataset

    Args:
        scenario (scenario_pb2.Scenario,): The sceanrio to extract it from
        list (list): Three lists of type x, y, dotSize
        list (float): x values, y values and dotSize values

    Returns:
        _type_: _description_
    """
    x = []
    y = []
    size = []

    for feature in scenario.map_features:
        for polyline in feature.road_edge.polyline:
            x.append(polyline.x)
            y.append(polyline.y)
            size.append(1)
        for polyline in feature.road_line.polyline:
            x.append(polyline.x)
            y.append(polyline.y)
            size.append(0.1)
        for polyline in feature.lane.polyline:
            x.append(polyline.x)
            y.append(polyline.y)
            size.append(0.02)

    return [x, y, size]


def getRoadFeaturesScatterPlot(
    centerCoord_x: int,
    centerCoord_y: int,
    scenario: scenario_pb2.Scenario,
) -> go.Figure:
    """
    Generate a scatter plot which shows the roadFeatures

    Args:
        centerCoord_x (int): The start of the track to predict in x-Direction
        centerCoord_y (int): The start of the track to predict in y-Direction

    Returns:
        go.Figure: A scatter plot which shows the roadFeatures
    """
    layout = sharedFunctionsPlotly.getPlotLayout(
        centerCoord_x=centerCoord_x, centerCoord_y=centerCoord_y
    )
    x, y, dotSize = extractRoadFeatures(scenario=scenario)

    plot = go.Scattergl(
        x=x,
        y=y,
        hoverinfo="skip",
        mode="markers",
        marker={
            "size": dotSize,
            "opacity": 1,
            "line": {"width": 2, "color": "black"},
            "color": "black",
        },
    )

    return go.Figure(
        data=[plot],
        layout=layout,
    )
