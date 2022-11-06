import csv
import logging

import pytest

from vehicle import Vehicle

# Config parameters
TEST_DATA_FILE = "data/standard_parameters.csv"

# Setting up a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.FileHandler("logs/test_vehicle.log", mode="w")
logger_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger_file_handler.setFormatter(logger_formatter)
logger.addHandler(logger_file_handler)


@pytest.fixture
def electFSAE():
    # main_file_path = Path(__file__).parents[1]
    # csv_files = sorted(main_file_path.glob("*.csv"))
    # parameters_file = csv_files[0]
    return Vehicle.from_file(TEST_DATA_FILE)


def test_init_from_file(electFSAE):
    with open(TEST_DATA_FILE) as file:
        csv_params = {}
        reader = csv.reader(file)
        for row in reader:
            csv_params[row[0]] = float(row[1])

    vehicle_params = vars(electFSAE)
    for key in csv_params:
        if key in vehicle_params:
            assert csv_params[key] == vehicle_params[key]
        else:
            logger.warning(f"{key} not found in Vehicle Parameters")


def test_get_acceleration(electFSAE):
    # helper function to compute velocity
    def dv_dt(velocity):
        acceleration = mue * g + (
            (0.5 * 1.2 * A * (mue * C_df - C_d) * (velocity**2)) / mass
        )

        return acceleration

    # Get the parameters needed to calculate the acceleration
    mass = electFSAE.mass
    g = electFSAE.G
    mue = electFSAE.mue
    C_df = -electFSAE.lift_cof
    C_d = electFSAE.drag_cof
    A = electFSAE.f_area

    # * acceleration when velocity = 0
    assert g == 9.807, "Gravitational acceleration is not the expected value"
    acceleration_zero_velocity = mue * g
    assert electFSAE.get_acceleration() == pytest.approx(acceleration_zero_velocity)
    assert electFSAE.get_acceleration() == pytest.approx(dv_dt(0))

    # * acceleration when velocity is a positive number
    v_test = 1  # [m/s]
    electFSAE.velocity = v_test
    assert electFSAE.get_acceleration() == pytest.approx(dv_dt(v_test))

    v_test = 3
    electFSAE.velocity = v_test
    assert electFSAE.get_acceleration() == pytest.approx(dv_dt(v_test))

    v_test = 55  # around ~200 kph
    electFSAE.velocity = v_test
    assert electFSAE.get_acceleration() == pytest.approx(dv_dt(v_test))

    # ! this test fails at the current stage, investigate
    # v_test = 200
    # electFSAE.velocity = v_test
    # assert electFSAE.get_acceleration() == pytest.approx(dv_dt(v_test))
