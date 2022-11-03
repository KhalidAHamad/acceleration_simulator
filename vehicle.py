import csv


class Vehicle:
    G = 9.807
    # rolling_coef = 0.98             # used to estimate tire's rolling radius

    def __init__(self, **kwargs):
                # (self, mass, fric_coef, roll_radius, torque, gear_ratio, trans_eff,
                # frontal_area, cd, cl, cg_height, wb_length, weight_dist, cp_location):
        ## Parsing args from user
        
        # Chassis and Tire Parameters
        self.mass = kwargs["mass"]
        self.mue = kwargs["mue"]
        self.weight = self.G * self.mass
        # self._rolling_radius = self._parameters["static_tire_radius"] * self.rolling_coef
        # Powertrain Parameters
        # self._torque = self._parameters["engine_torque"]
        # self._gear_ratio = self._parameters["gear_ratio"]
        # self._trans_eff = self._parameters["transmission_eff"]
        # aero
        
        ## calculating args
        self._acceleration = self.acceleration

    @classmethod
    def from_file(cls, file_name: str):
        parameters = {}
        with open(file_name, encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                value = row[1]
                parameters[row[0]] = int(value) if value.isdigit() else float(value)

        return cls(mass=parameters["mass"], mue=parameters["mue"])

    @property
    def acceleration(self):
        frictional_forces = self.mue * self.weight
        return frictional_forces / self.mass



# if __name__ == "__main__":
    # main()