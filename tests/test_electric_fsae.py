import csv
import pytest


from vehicle import Vehicle

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
            p[row[0]] = row[1]

    acc = float(p["mue"]) * 9.807

    assert ElectFSAE.acceleration == pytest.approx(acc)
