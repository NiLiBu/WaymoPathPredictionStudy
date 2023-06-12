from waymo_open_dataset.protos import scenario_pb2
import src.sharedFunctionsPlotly as sharedFunctionsPlotly
import plotly.graph_objects as go
from PIL import Image


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
            "line": {"width": 1, "color": "black"},
            "color": "black",
        },
    )

    return go.Figure(
        data=[plot],
        layout=layout,
    )


def extractStaticPolynomials(
    scenario: scenario_pb2.Scenario,
) -> list[list[int]]:
    """
    Extract speedbumps, driveways and crosswalks

    Args:
        scenario (scenario_pb2.Scenario,): The sceanrio to extract it from
        list (list): Three lists of type x, y, dotSize
        list (float): x values, y values and dotSize values

    Returns:
        _type_: x values, y values, color
    """

    x_crosswalk = []
    x_speed_bump = []
    x_driveway = []
    y_crosswalk = []
    y_speed_bump = []
    y_driveway = []

    for feature in scenario.map_features:
        for polygon in feature.crosswalk.polygon:
            x_crosswalk.append(polygon.x)
            y_crosswalk.append(polygon.y)
        x_crosswalk.append(None)
        y_crosswalk.append(None)

        for polygon in feature.speed_bump.polygon:
            x_speed_bump.append(polygon.x)
            y_speed_bump.append(polygon.y)
        x_speed_bump.append(None)
        y_speed_bump.append(None)

        for polygon in feature.driveway.polygon:
            x_driveway.append(polygon.x)
            y_driveway.append(polygon.y)
        x_driveway.append(None)
        y_driveway.append(None)

    return x_speed_bump, y_speed_bump, x_crosswalk, y_crosswalk, x_driveway, y_driveway


def getPolygonFeaturesScatterPlot(
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
    (
        x_speed_bump,
        y_speed_bump,
        x_crosswalk,
        y_crosswalk,
        x_driveway,
        y_driveway,
    ) = extractStaticPolynomials(scenario=scenario)

    plot_crosswalk = go.Scattergl(
        x=x_crosswalk,
        y=y_crosswalk,
        hoverinfo="skip",
        mode="none",
        fill="toself",
        marker={
            "size": 1,
            "opacity": 1,
            "line": {"width": 2, "color": "yellow"},
            "color": "yellow",
        },
    )

    plot_speed_bump = go.Scattergl(
        x=x_speed_bump,
        y=y_speed_bump,
        hoverinfo="skip",
        mode="none",
        fill="toself",
        marker={
            "size": 1,
            "opacity": 1,
            "line": {"width": 2, "color": "orange"},
            "color": "orange",
        },
    )

    plot_driveway = go.Scattergl(
        x=x_driveway,
        y=y_driveway,
        hoverinfo="skip",
        mode="none",
        fill="toself",
        marker={
            "size": 1,
            "opacity": 1,
            "line": {"width": 2, "color": "lime"},
            "color": "lime",
        },
    )

    return go.Figure(
        data=[plot_crosswalk, plot_speed_bump, plot_driveway],
        layout=layout,
    )


def extractStopSigns(
    scenario: scenario_pb2.Scenario,
) -> list[list[int]]:
    """
    Gets all points of stop signs

    Args:
        scenario (scenario_pb2.Scenario,): The sceanrio to extract it from
        list (list): Three lists of type x, y, dotSize
        list (float): x values, y values and dotSize values

    Returns:
        list[list[float]]: [x[float] , y[float]]
    """

    x = []
    y = []

    for feature in scenario.map_features:
        if feature.stop_sign.position.x != 0.0:
            x.append(feature.stop_sign.position.x)
            y.append(feature.stop_sign.position.y)

    return x, y


def getStopSignScatterPlot(
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
    x, y = extractStopSigns(scenario=scenario)

    plot = go.Scattergl(
        x=[],
        y=[],
        hoverinfo="skip",
        mode="markers",
        fill="toself",
        marker={
            "size": 1,
            "opacity": 1,
            "line": {"width": 2, "color": "yellow"},
            "color": "yellow",
        },
    )

    figure = go.Figure(
        data=[plot],
        layout=layout,
    )

    for index in range(len(x)):
        figure.add_layout_image(
            dict(
                source=Image.open(
                    "assets/stopSign.png"
                ),
                xref="x",
                yref="y",
                x=x[index],
                y=y[index],
                xanchor="center",
                yanchor="middle",
                sizex=10,
                sizey=10,
                sizing="stretch",
                opacity=0.7,
                layer="above",
            )
        )

    return figure
