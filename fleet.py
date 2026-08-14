"""
CSP221A - Fleet Management System
"""

import abc
import functools
import logging

# Configure basic logging to terminal
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# --- 1.4 Custom Exception ---
class InsufficientBatteryError(Exception):
    """Raised when a robot attempts a task without enough battery."""

    def __init__(self, robot_name: str, required: int, available: int):
        self.robot_name = robot_name
        self.required = required
        self.available = available
        message = f"{robot_name} needs {required}% battery for this task but only has {available}%."
        super().__init__(message)


# --- 1.1 Robot Base Class ---
class Robot(abc.ABC):
    manufacturer = "RoboCorp"  # Class attribute shared across all instances
    population = 0  # Class attribute counter

    def __init__(self, name: str, battery: int = 100):
        self.name = name
        self.battery = battery  # Uses the property setter below
        Robot.population += 1

    # --- Property Getter & Clamped Setter ---
    @property
    def battery(self) -> int:
        return self._battery

    @battery.setter
    def battery(self, value: int):
        # Clamps battery value between 0 and 100
        self._battery = max(0, min(100, value))

    # --- Shared Battery Drain Method ---
    def use_battery(self, amount: int):
        if self.battery < amount:
            raise InsufficientBatteryError(
                robot_name=self.name,
                required=amount,
                available=self.battery,
            )
        self.battery -= amount

    # --- Representations ---
    def __str__(self) -> str:
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', battery={self.battery})"

    # --- 1.7 Alternative Constructor ---
    @classmethod
    def from_config(cls, config: dict):
        return cls(name=config["name"], battery=config.get("battery", 100))

    # --- Abstract Method ---
    @abc.abstractmethod
    def perform_task(self, **kwargs):
        pass

        if __name__ == "__main__":
            print(f"Base Robot manufacturer: {Robot.manufacturer}")

            # --- 1.2 Concrete Subclasses ---
class DroneRobot(Robot):
    """A flying robot subclass with altitude limits."""

    def __init__(self, name: str, battery: int = 100, max_altitude: int = 500):
        super().__init__(name, battery)
        self.max_altitude = max_altitude  # Subclass-specific attribute

    def perform_task(self, altitude: int = 100, **kwargs) -> str:
        # Task costs 15% battery
        battery_cost = 15
        self.use_battery(battery_cost)
        
        target_alt = min(altitude, self.max_altitude)
        return f"{self.name} flew to {target_alt}m altitude!"


# --- Test Code at the Bottom ---
if __name__ == "__main__":
    drone = DroneRobot(name="Aqua-Drone", battery=50, max_altitude=300)
    print(str(drone))  # Output: Aqua-Drone (50% battery)
    result = drone.perform_task(altitude=150)
    print(result)      # Output: Aqua-Drone flew to 150m altitude!
    print(str(drone))  # Output: Aqua-Drone (35% battery)