import csv
import pytest

from pathlib import Path

from vehicle import Vehicle

@pytest.fixture
def ElectFSAE():
    # main_file_path = Path(__file__).parents[1]
    # csv_files = sorted(main_file_path.glob("*.csv"))
    # parameters_file = csv_files[0]
    return Vehicle.from_file("parameters.csv")


def test_init_from_files(ElectFSAE):
    with open("parameters.csv") as file:
        p = {}
        reader = csv.reader(file)
        for row in reader:
                p[row[0]] = row[1]
        
    acc = float(p["mue"]) * 9.807 

    assert ElectFSAE.get_acceleration() == pytest.approx(acc)


