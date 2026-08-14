"""
CSP221A - Fleet Management System
"""

import abc
import functools
import logging

# Configure basic logging to terminal
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- 1.3 Decorators ---
def log_action(func):
    """Decorator that logs method execution and handles errors."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {self.name} starting action: '{func.__name__}'")
        try:
            result = func(self, *args, **kwargs)
            print(f"[LOG] {self.name} completed action successfully.")
            return result
        except Exception as e:
            print(f"[LOG] {self.name} failed action with error: {e}")
            raise
    return wrapper
    
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
            # --- 1.2 Concrete Subclasses ---
class DroneRobot(Robot):
    """A flying robot subclass with altitude limits."""

    def __init__(self, name: str, battery: int = 100, max_altitude: int = 500):
        super().__init__(name, battery)
        self.max_altitude = max_altitude
    @log_action
    def perform_task(self, altitude: int = 100, **kwargs) -> str:
        # Task costs 15% battery
        battery_cost = 15
        self.use_battery(battery_cost)
        
        target_alt = min(altitude, self.max_altitude)
        return f"{self.name} flew to {target_alt}m altitude!"


class CleaningRobot(Robot):
    """A ground-based cleaning robot."""

    def __init__(self, name: str, battery: int = 100, cleaning_mode: str = "vacuum"):
        super().__init__(name, battery)
        self.cleaning_mode = cleaning_mode
    @log_action
    def perform_task(self, area_sqm: int = 20, **kwargs) -> str:
        # Cleaning consumes 1% battery per square meter
        battery_cost = area_sqm * 1
        self.use_battery(battery_cost)
        
        return f"{self.name} cleaned {area_sqm}m² using {self.cleaning_mode} mode!"

# --- Test Code at the Bottom ---
if __name__ == "__main__":
    # Test DroneRobot
    drone = DroneRobot(name="Aqua-Drone", battery=50, max_altitude=300)
    print(drone.perform_task(altitude=150))

    # Test CleaningRobot
    cleaner = CleaningRobot(name="Dust-E", battery=80, cleaning_mode="mop")
    print(str(cleaner))
    print(cleaner.perform_task(area_sqm=30))
    print(str(cleaner))
