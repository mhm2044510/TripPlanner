from enum import Enum


# =========================================================
# HOS RULES
# =========================================================
MAX_DRIVING_HOURS = 11
MAX_DUTY_WINDOW_HOURS = 14
REQUIRED_REST_HOURS = 10
BREAK_AFTER_DRIVING_HOURS = 8
REQUIRED_BREAK_HOURS = 0.5
MAX_CYCLE_HOURS = 70
RESTART_HOURS = 34
FUEL_INTERVAL_MILES = 1000
FUEL_STOP_HOURS = 0.5
PICKUP_HOURS = 1
DROPOFF_HOURS = 1
START_HOUR = 6
# =========================================================
# LIMIT TYPES
# =========================================================
class Limit(Enum):
    BREAK = "BREAK"
    DRIVING_LIMIT = "DRIVING_LIMIT"
    WINDOW = "WINDOW"
    CYCLE = "CYCLE"


# =========================================================
# DUTY CLOCK
# =========================================================
# Tracks the four meters the driver consumes.
# =========================================================

class DutyClock:

    def __init__(self, cycle_used, rules):
        self.driving_this_shift = 0
        self.driving_since_break = 0
        self.window_used = 0
        self.window_open = False
        self.cycle_used = cycle_used

        self.rules = rules

    def max_drive_now(self):

        room = {
            Limit.BREAK:
                self.rules["breakAfterDrivingHours"]
                - self.driving_since_break,

            Limit.DRIVING_LIMIT:
                self.rules["maxDrivingHours"]
                - self.driving_this_shift,

            Limit.WINDOW:
                self.rules["maxDutyWindowHours"]
                - self.window_used,

            Limit.CYCLE:
                self.rules["maxCycleHours"]
                - self.cycle_used,
        }

        limit = min(room, key=room.get)

        return max(0, room[limit]), limit

    def drive(self, hours):

        self.window_open = True

        self.driving_this_shift += hours
        self.driving_since_break += hours
        self.window_used += hours
        self.cycle_used += hours

    def on_duty(self, hours):

        self.window_open = True

        self.window_used += hours
        self.cycle_used += hours

    def take_break(self, hours):

        if self.window_open:
            self.window_used += hours

        self.driving_since_break = 0

    def take_rest(self):

        self.driving_this_shift = 0
        self.driving_since_break = 0
        self.window_used = 0
        self.window_open = False

    def take_restart(self):

        self.take_rest()
        self.cycle_used = 0