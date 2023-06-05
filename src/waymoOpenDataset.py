import waymo_open_dataset
from waymo_open_dataset.protos import scenario_pb2

# disable warnings of tensorflow
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# after disabled warnings import tf
import tensorflow


def getWaymoScenario(fileNumber: int, scenarioNumber: int) -> scenario_pb2.Scenario:
    """
    Get an Waymo Open Dataset Scenario

    Args:
        fileNumber (int): The number of the file (0 - 1000 is possible if all data exists)
        scenarioNumber (int): the number of the scenario. If there is an overflow it will begin counting at the beginning. There should be arround 500 Scenarios in one file

    Returns:
        waymo_open_dataset.protos.scenario_pb2.Scenario: The Scenario which was selected
    """

    FILE_NAME = "StudyWaymoPathPrediction/WaymoPathPredictionStudy/waymoDatasetFiles/motion_1_2_0.tfrecord-0%s-of-01000" % str(
        fileNumber
    ).rjust(
        4, "0"
    )

    document = tensorflow.data.TFRecordDataset(FILE_NAME, compression_type="")

    scenario = waymo_open_dataset.protos.scenario_pb2.Scenario()

    counter = 0
    for unparsedScenario in document:
        counter += 1
        if counter == scenarioNumber:
            scenario.ParseFromString(bytearray(unparsedScenario.numpy()))
            return scenario

    # if overflow then modulo with max counter
    scenarioNumber = scenarioNumber % counter
    # parse again
    counter = 0
    for unparsedScenario in document:
        counter += 1
        if counter == scenarioNumber:
            scenario.ParseFromString(bytearray(unparsedScenario.numpy()))
            return scenario

    # This should never be reached
    raise ValueError(
        "Scenario Number could not be found",
        "This error should never occur! Check Function for programming error",
    )
