from waymo_open_dataset.protos import scenario_pb2
import src.sharedFunctionsPlotly as sharedFunctionsPlotly
import plotly.graph_objects as go
import math


def getDynamicLaneStates(
    centerCoord_x: int, centerCoord_y: int, scenario: scenario_pb2.Scenario, zoomLevel
):
    """
        Get all lanes together with their lane state at the beginning

    Returns:
        list[list[float]]: [x[float] , y[float] , laneState[float]]
    """
    layout = sharedFunctionsPlotly.getPlotLayout(
        centerCoord_x=centerCoord_x, centerCoord_y=centerCoord_y, zoomLevel=zoomLevel
    )

    layout.updatemenus = [
        dict(
            type="buttons",
            direction="left",
            bgcolor="red",
            buttons=list(
                [
                    dict(
                        args=[
                            None,
                            {
                                "frame": {"duration": 100, "redraw": False},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                        label="Abspielen der aktuellen Verkehrssituation",
                        method="animate",
                    ),
                ]
            ),
            pad={"r": 0, "t": 0},
            showactive=True,
            x=0,
            xanchor="left",
            y=1.1,
            yanchor="top",
        )
    ]

    FRAMES_TO_PLOT = 10
    # FRAMES_TO_PLOT = 89

    dictionarys = []

    ###################################################################################################
    #                                       Lane States
    ###################################################################################################

    for item in range(0, FRAMES_TO_PLOT):
        laneStateDictionary = {}
        for lane_state in scenario.dynamic_map_states[item].lane_states:
            laneStateDictionary[lane_state.lane] = lane_state.state
        dictionarys.append(laneStateDictionary)

    plot = []
    frames = []
    xLines = []
    yLines = []
    colorLines = []
    dotSize = []

    for i in range(0, FRAMES_TO_PLOT):
        plot.append([])
        xLines.append([])
        yLines.append([])
        colorLines.append([])
        dotSize.append([])

    for timeStep in range(0, FRAMES_TO_PLOT):
        for feature in scenario.map_features:
            feature_id = feature.id
            for polyline in feature.lane.polyline:
                try:
                    if laneStateDictionary[feature_id] != 0:
                        xLines[timeStep].append(polyline.x)
                        yLines[timeStep].append(polyline.y)
                        colorDictionary = {
                            0: "lightgrey",  # no state
                            1: "yellow",  # arrow caution
                            2: "red",  # arrow stop
                            3: "green",  # arrow go
                            4: "red",  # stop
                            5: "yellow",  # caution
                            6: "green",  # go
                            7: "darkred",  # flashing stop
                            8: "gold",  # flashing caution
                        }

                        laneStateDictionary = dictionarys[timeStep]
                        dotSize[timeStep].append(1.5)
                        colorLines[timeStep].append(
                            colorDictionary[laneStateDictionary[feature_id]]
                        )
                except:
                    pass

    ###################################################################################################
    #                                       Agent Features
    ###################################################################################################
    xVehicle = []
    yVehicle = []

    xUndefined = []
    yUndefined = []

    xPedestrian = []
    yPedestrian = []

    xCyclist = []
    yCyclist = []

    frames = []

    for i in range(FRAMES_TO_PLOT):
        xVehicle.append([])
        yVehicle.append([])

        xUndefined.append([])
        yUndefined.append([])

        xPedestrian.append([])
        yPedestrian.append([])

        xCyclist.append([])
        yCyclist.append([])

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
                # trackType = {
                #     0: "Undefined",
                #     1: "Vehicle",
                #     2: "Pedestrian",
                #     3: "Cyclist",
                #     4: "Other",
                # }

                if track.object_type == 0:
                    xUndefined[stateIndex].extend(x_addition)
                    yUndefined[stateIndex].extend(y_addition)
                elif track.object_type == 1:
                    xVehicle[stateIndex].extend(x_addition)
                    yVehicle[stateIndex].extend(y_addition)
                elif track.object_type == 2:
                    xPedestrian[stateIndex].extend(x_addition)
                    yPedestrian[stateIndex].extend(y_addition)
                elif track.object_type == 3:
                    xCyclist[stateIndex].extend(x_addition)
                    yCyclist[stateIndex].extend(y_addition)
                else:
                    xUndefined[stateIndex].extend(x_addition)
                    yUndefined[stateIndex].extend(y_addition)

    ###################################################################################################
    #                                       Plot Both
    ###################################################################################################
    plot = [
        go.Scatter(
            x=xLines[FRAMES_TO_PLOT - 1],
            y=yLines[FRAMES_TO_PLOT - 1],
            hoverinfo="skip",
            mode="markers",
            marker={
                "size": dotSize[FRAMES_TO_PLOT - 1],
                "opacity": 1,
                "line": {"width": 1, "color": colorLines[0]},
            },
        ),
        # undefined Agent (grey)
        go.Scatter(
            x=xUndefined[FRAMES_TO_PLOT - 1],
            y=yUndefined[FRAMES_TO_PLOT - 1],
            hoverinfo="skip",
            mode="none",
            fill="toself",
            fillcolor="rgba(50,50,50, 0.7)",
        ),
        # Vehicle Agent (black)
        go.Scatter(
            x=xVehicle[FRAMES_TO_PLOT - 1],
            y=yVehicle[FRAMES_TO_PLOT - 1],
            hoverinfo="skip",
            mode="none",
            fill="toself",
            fillcolor="rgba(0,0,0, 0.7)",
        ),
        # Pedestrian Agent (green)
        go.Scatter(
            x=xPedestrian[FRAMES_TO_PLOT - 1],
            y=yPedestrian[FRAMES_TO_PLOT - 1],
            hoverinfo="skip",
            mode="none",
            fill="toself",
            fillcolor="rgba(0, 150,0, 0.7)",
        ),
        # Cyclist Agent (orange)
        go.Scatter(
            x=xCyclist[FRAMES_TO_PLOT - 1],
            y=yCyclist[FRAMES_TO_PLOT - 1],
            hoverinfo="skip",
            mode="none",
            fill="toself",
            fillcolor="rgba(255,255,255, 0.7)",
        ),
    ]

    for index, element in enumerate(xLines):
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=xLines[index],
                        y=yLines[index],
                        hoverinfo="skip",
                        mode="markers",
                        marker={
                            "size": dotSize[index],
                            "opacity": 1,
                            "line": {"width": 1, "color": colorLines[index]},
                        },
                    ),
                    # undefined Agent
                    go.Scatter(
                        x=xUndefined[index],
                        y=yUndefined[index],
                        hoverinfo="skip",
                        mode="none",
                        fill="toself",
                        fillcolor="rgba(50,50,50, 0.7)",
                    ),
                    # Vehicle Agent (Black)
                    go.Scatter(
                        x=xVehicle[index],
                        y=yVehicle[index],
                        hoverinfo="skip",
                        mode="none",
                        fill="toself",
                        fillcolor="rgba(0,0,0, 0.7)",
                    ),
                    # Pedestrian Agent (green)
                    go.Scatter(
                        x=xPedestrian[index],
                        y=yPedestrian[index],
                        hoverinfo="skip",
                        mode="none",
                        fill="toself",
                        fillcolor="rgba(0,150,0, 0.7)",
                    ),
                    # Cyclist Agent (orange)
                    go.Scatter(
                        x=xCyclist[index],
                        y=yCyclist[index],
                        hoverinfo="skip",
                        mode="none",
                        fill="toself",
                        fillcolor="rgba(200,100,0, 0.7)",
                    ),
                ]
            )
        )

    return go.Figure(
        data=plot,
        layout=layout,
        frames=frames,
    )
