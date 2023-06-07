from waymo_open_dataset.protos import scenario_pb2
import plotly.graph_objects as go
import random
import math
import sharedFunctionsPlotly


def getRandomAgent(scenario: scenario_pb2.Scenario):
    # Find Track that should be predicted
    trackIsToPredict = []

    for track in scenario.tracks_to_predict:
        trackIsToPredict.append(track.track_index)

    trackForPrediction = random.choice(trackIsToPredict)

    trackIdList = []

    for trackIndex, track in enumerate(scenario.tracks):
        trackIdList.append([trackIndex, track.id])

    trackType = {
        0: "Undefined",
        1: "Vehicle",
        2: "Pedestrian",
        3: "Cyclist",
        4: "Other",
    }

    tracks = []

    centerValue = []
    trackToPredictSize = []
    direction = 0

    for trackIndex, trackId in trackIdList:
        x = []
        y = []

        length = 0
        width = 0

        trackToPredict = trackIndex == trackForPrediction

        for stateIndex, state in enumerate(scenario.tracks[trackIndex].states):
            if state.valid and stateIndex <= 10:
                length = state.length
                width = state.width

                x.append(state.center_x)
                y.append(state.center_y)

                if trackToPredict:
                    centerValue = [
                        state.center_x,
                        state.center_y,
                    ]

                    trackToPredictSize = [state.length, state.width]

                    direction = state.heading * 180 / math.pi

        if x.__len__() > 0:
            tracks.append(
                {
                    "type": trackType.get(
                        scenario.tracks[trackIndex].object_type, "Undefined"
                    ),
                    "x": x,
                    "y": y,
                    "direction": state.heading * 180 / math.pi,
                    "length": length,
                    "width": width,
                    "toPredict": trackToPredict,
                }
            )

    return centerValue, trackToPredictSize, direction, tracks


def getAllAgentsScatterPlot(
    centerCoord_x: int, centerCoord_y: int, scenario: scenario_pb2.Scenario
):
    layout = sharedFunctionsPlotly.getPlotLayout(
        centerCoord_x=centerCoord_x, centerCoord_y=centerCoord_y
    )

    # trackType = {
    #     0: "Undefined",
    #     1: "Vehicle",
    #     2: "Pedestrian",
    #     3: "Cyclist",
    #     4: "Other",
    # }

    x = []
    y = []

    for trackIndex in range(10):
        for stateIndex, state in enumerate(scenario.tracks[trackIndex].states):
            if state.valid and stateIndex <= 10:
                (
                    x_addition,
                    y_addition,
                ) = sharedFunctionsPlotly.getPolygonCoordsFromCenterCoordsForMultipleInstances(
                    center_x=state.center_x,
                    center_y=state.center_y,
                    degrees=state.heading * 180 / math.pi,
                    length=state.width,
                    width=state.length,
                )

                x.extend(x_addition)
                y.extend(y_addition)

    plot = go.Scattergl(
        x=x,
        y=y,
        hoverinfo="skip",
        mode="markers",
        fill="toself",
        marker={
            "size": 1,
            "opacity": 1,
            "line": {"width": 2, "color": "lime"},
            "color": "blue",
        },
    )

    return go.Figure(
        data=[plot],
        layout=layout,
    )
