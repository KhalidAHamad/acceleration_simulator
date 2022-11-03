import csv
import pytest
from vehicle import Vehicle
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger_formatter =
logger_file_handler = logging.FileHandler("logs/test_vehicle.log")
# logger_file_handler.setFormatter(logger_formatter)

logger.addHandler(logger_file_handler)


TEST_DATA_FILE = "data/standard_parameters.csv"


@pytest.fixture
def ElectFSAE():
    # main_file_path = Path(__file__).parents[1]
    # csv_files = sorted(main_file_path.glob("*.csv"))
    # parameters_file = csv_files[0]
    return Vehicle.from_file(TEST_DATA_FILE)


def test_init_from_file(ElectFSAE):
    with open(TEST_DATA_FILE) as file:
        p = {}
        reader = csv.reader(file)
        for row in reader:
            p[row[0]] = float(row[1])

    g = ElectFSAE.G
    assert g == 9.807, "Gravitational acceleration is not the expected value"
    acc = p["mue"] * g

    # v = 0, thus, F_drag and F_lift = 0
    assert ElectFSAE.get_acceleration() == pytest.approx(acc)

    # setting velocity equal to 1 and checking the calculations
    v_test = 1
    ElectFSAE.velocity = v_test
    C_df = -p["lift_coefficient"]
    C_d = p["drag_coefficient"]
    A = p["frontal_area"]
    M = p["mass"]
    acc_w_velocity = p["mue"] * g + \
    ((0.5 * 1.2 * A * (p["mue"] * C_df - C_d) * (v_test**2)) / M)
    logger.debug(f"Value from Vehicle module = {ElectFSAE.get_acceleration()}"
    f" Value from our calculations = {acc_w_velocity}")
    logger.debug(f"{ElectFSAE.get_acceleration() is acc_w_velocity=}")

    assert ElectFSAE.get_acceleration() == pytest.approx(
        acc_w_velocity
    ), "Acceleration is wrong when velocity is set"
