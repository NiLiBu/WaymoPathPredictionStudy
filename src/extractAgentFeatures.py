from waymo_open_dataset.protos import scenario_pb2
import plotly.graph_objects as go
import random
import math
import src.sharedFunctionsPlotly as sharedFunctionsPlotly


def getRandomAgent(scenario: scenario_pb2.Scenario):
    """UNUSED FUNCTION IS NO LONGER MAINTAINED

    Args:
        scenario (scenario_pb2.Scenario): _description_

    Returns:
        _type_: _description_
    """
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
            if state.valid and stateIndex < 10:
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
    
    layout.updatemenus=[dict(
            type="buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=[
                        None, 
                        {
                            "frame": {
                                "duration": 100, 
                                "redraw": False
                            },
                            "fromcurrent": True, 
                            "transition": {
                                "duration": 0
                            }
                        }
                    ],
                    label="Abspielen der aktuellen Verkehrssituation",
                    method="animate"
                ),
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.1,
            yanchor="top"
            )
        ]

    # trackType = {
    #     0: "Undefined",
    #     1: "Vehicle",
    #     2: "Pedestrian",
    #     3: "Cyclist",
    #     4: "Other",
    # }
    
    
    FRAMES_TO_PLOT = 90
    
    x = []
    y = []
    plot = []
    frames = []
    
    for i in range(FRAMES_TO_PLOT):
        x.append([])
        y.append([])
        plot.append([])


    for track in scenario.tracks:
        for stateIndex, state in enumerate(track.states):
            if stateIndex < FRAMES_TO_PLOT:
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

                x[stateIndex].extend(x_addition)
                y[stateIndex].extend(y_addition)

    for index, element in enumerate(x):
        plot[index] = go.Scatter(
            x=x[index],
            y=y[index],
            hoverinfo="skip",
            mode="none",
            fill="toself",
            fillcolor='rgba(0,0,255, 1)',
        )
        
        frames.append(go.Frame(data=go.Scatter(
            x=x[index],
            y=y[index],
            hoverinfo="skip",
            mode="none",
            fill="toself",
            fillcolor='rgba(0,0,255, 1)',
        )))
        
    
    return go.Figure(
        data=[plot[0]],
        layout=layout,
        frames=frames,
    )
