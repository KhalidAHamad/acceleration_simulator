import csv
import logging

import pytest

from vehicle import Vehicle

# Setting up a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.FileHandler("logs/test_vehicle.log", mode="w")
logger_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger_file_handler.setFormatter(logger_formatter)
logger.addHandler(logger_file_handler)

# Config parameters
TEST_DATA_FILE = "data/standard_parameters.csv"


@pytest.fixture
def electFSAE():
    # main_file_path = Path(__file__).parents[1]
    # csv_files = sorted(main_file_path.glob("*.csv"))
    # parameters_file = csv_files[0]
    return Vehicle.from_file(TEST_DATA_FILE)


def test_init_from_file(electFSAE):
    with open(TEST_DATA_FILE) as file:
        p = {}
        reader = csv.reader(file)
        for row in reader:
            p[row[0]] = float(row[1])

    g = electFSAE.G
    assert g == 9.807, "Gravitational acceleration is not the expected value"
    acc = p["mue"] * g

    # v = 0, thus, F_drag and F_lift = 0
    assert electFSAE.get_acceleration() == pytest.approx(acc)

    # setting velocity equal to 1 and checking the calculations
    v_test = 1
    electFSAE.velocity = v_test
    C_df = -p["lift_coefficient"]
    C_d = p["drag_coefficient"]
    A = p["frontal_area"]
    M = p["mass"]
    acc_w_velocity = p["mue"] * g + (
        (0.5 * 1.2 * A * (p["mue"] * C_df - C_d) * (v_test**2)) / M
    )
    logger.debug(
        f"Value from Vehicle module = {electFSAE.get_acceleration()}"
        f" Value from our calculations = {acc_w_velocity}"
    )
    logger.debug(f"{electFSAE.get_acceleration() is acc_w_velocity=}")

    assert electFSAE.get_acceleration() == pytest.approx(
        acc_w_velocity
    ), "Acceleration is wrong when velocity is set"
