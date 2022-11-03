import csv
import logging
import numpy as np
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger_formatter =
logger_file_handler = logging.FileHandler("logs/vehicle.log", mode="w")
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_file_handler.setFormatter(formatter)
# logger_file_handler.setFormatter(logger_formatter)

logger.addHandler(logger_file_handler)


class Vehicle:
    G = 9.807  # Gravitational acceleration
    RHO = 1.2  # Air density
    # rolling_coef = 0.98             # used to estimate tire's rolling radius

    def __init__(self, **kwargs):
        # Chassis and Tire Parameters
        self.mass = kwargs["mass"]
        self.mue = kwargs["mue"]  # coefficient of friction
        # aero
        self.f_area = kwargs["frontal_area"]
        self.drag_cof = kwargs["drag_coefficient"]
        self.lift_cof = kwargs["lift_coefficient"]

        ## calculating args
        self.weight = self.G * self.mass
        self.velocity = 0
        self.velocity_vec = [self.velocity]
        self.acceleration_vec = []
        self.position = 0
        self.position_vec = [self.position]
        self.time_vec = None

    @classmethod
    def from_file(cls, file_name: str = "data/standard_parameters.csv"):
        parameters = {}
        with open(file_name, encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                value = row[1]
                parameters[row[0]] = int(value) if value.isdigit() else float(value)

        return cls(**parameters)

    def get_acceleration(self) -> float:
        # F_normal = W + F_downforce
        normal_force = self.weight - self.get_lift_force()
        # F_friction = mue * F_normal
        friction_force = self.mue * normal_force  # tractive frictional forces
        # acceleration = sum_of_forces(F_friction - F_drag) / self.mass
        acceleration = (friction_force - self.get_drag_force()) / self.mass
        assert acceleration >= 0, "Acceleration should be either 0 or a positive number"
        logger.info(f"{normal_force=} {friction_force=} {acceleration=}")
        return acceleration

    def get_lift_force(self) -> float:
        lift = 0.5 * self.RHO * self.f_area * self.lift_cof * (self.velocity ** 2)
        logger.debug(
            "Lift force = "
            f"{0.5} * {self.RHO=} * {self.f_area=} * {self.lift_cof=} * {self.velocity=} = {lift}"
        )
        assert lift <= 0, "Lift force is expected to be a negative number"
        return lift

    def get_drag_force(self) -> float:
        drag = 0.5 * self.RHO * self.f_area * self.drag_cof * (self.velocity ** 2)
        logger.debug(
            "Drag force = "
            f"{0.5} * {self.RHO=} * {self.f_area=} * {self.drag_cof=} * {self.velocity=} = {drag}"
        )
        assert drag >= 0, "Drag force is a negative number"
        if drag == 0:
            logger.warning(
                "Drag force is equal to zero, "
                f"{0.5=} * {self.RHO=} * {self.f_area=} * {self.drag_cof=} * {self.velocity=}"
            )
        return drag

    def simulate_acceleration(self, ti=0, tf=5, h=0.001):
        # range doesn't include tf=5, because we at each iteration, we calculate
        # velocity and position at the next step
        self.time_vec = np.arange(ti, tf + h, h)
        assert self.time_vec[-1] == tf

        for _ in range(len(self.time_vec) - 1):
            acc = self.get_acceleration()
            self.acceleration_vec.append(acc)
            self.velocity = self.velocity + acc * h
            self.velocity_vec.append(self.velocity * 3.6)
            self.position = self.position + self.velocity * h
            self.position_vec.append(self.position)
        
        self.acceleration_vec.append(self.get_acceleration())

        # assert len(self.time_vec) == len(self.velocity_vec)
        assert len(self.velocity_vec) == len(self.position_vec)
        assert len(self.velocity_vec) == len(self.acceleration_vec)

    def generate_plots(self, distance=None):
        plt.style.use("seaborn")
        fig, ax = plt.subplots()
        ax.plot(self.time_vec, self.position_vec, label="Position")#color="b", linewidth=2, )
        ax.plot(self.time_vec, self.velocity_vec, label="Velocity")#color="g", linewidth=2
        ax.plot(self.time_vec, self.acceleration_vec, label="Acceleration")#color="k", linewidth=2,
         
        if distance:
            x, y = None, None
            for t, p in zip(self.time_vec, self.position_vec):
                print(t, p)
                if p >= distance:
                    x = t
                    y = p
                    break
            ax.scatter(x, y, marker='X', s=100, color="r")
            title_ = f"Vehicle finishes a distance of {y:.2f}m in {x:.2f}s"
        else:
            title_ = "Vehicle Position vs Time"

        ax.set_title(title_)
        ax.set_xlabel("Time, [s]")
        ax.set_ylabel("Position, [m]")
        ax.legend()
        ax.grid(True)

        plt.show()



def main():
    car = Vehicle.from_file()
    car.simulate_acceleration(ti=0, tf=5, h=0.001)
    car.generate_plots(75)


if __name__ == "__main__":
    main()
