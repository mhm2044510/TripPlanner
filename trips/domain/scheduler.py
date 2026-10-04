from . import hos_rules as H


EPS = 1e-6


def format_hours(number):
    return f"{number:.1f}"


def get_rule_text(limit, rules):
    text_map = {
       H.Limit.BREAK: f"{rules['breakAfterDrivingHours']:.0f} cumulative driving hours reached",
       H.Limit.DRIVING_LIMIT: f"{rules['maxDrivingHours']:.0f}-hour driving limit reached",
       H.Limit.WINDOW: f"{rules['maxDutyWindowHours']:.0f}-hour duty window exhausted",
       H.Limit.CYCLE: f"{rules['maxCycleHours']:.0f}-hour cycle exhausted",
    }
    return text_map[limit]


def schedule_trip(route, cycle_used, rules):

    clock =H. DutyClock(cycle_used, rules)

    events = []
    stops = []
    steps = []

    now = rules["startHour"]
    miles = 0.0
    since_fuel = 0.0
    shift = 0

    def log(title, detail=""):
        steps.append({"title": title, "detail": detail})

    def add(status, hours, label, reason):
        nonlocal now
        events.append(
            {
                "status": status,
                "start": now,
                "end": now + hours,
                "label": label,
                "reason": reason,
            }
        )
        now += hours

    def add_stop(stop_type, status, hours, reason):
        stops.append(
            {
                "type": stop_type,
                "mile": miles,
                "start": now,
                "durationHours": hours,
                "reason": reason,
            }
        )
        add(status, hours, stop_type, reason)

    def ensure_shift():
        nonlocal shift
        if clock.window_open:
            return

        shift += 1
        log(
            f"Driver starts shift {shift}",
            (
                f"Available driving: {rules['maxDrivingHours']} h · "
                f"duty window: {rules['maxDutyWindowHours']} h · "
                f"cycle remaining: "
                f"{format_hours(rules['maxCycleHours'] - clock.cycle_used)} h"
            ),
        )

    def time_off(limit):
        why = get_rule_text(limit, rules)

        if limit ==H.Limit.BREAK:
            break_mins = int(rules["requiredBreakHours"] * 60)
            log(
                why,
                f"→ {break_mins}-minute break inserted "
                f"(resets the {rules['breakAfterDrivingHours']:.0f} h meter, NOT the {rules['maxDutyWindowHours']:.0f} h window)",
            )
            add_stop(
                "BREAK",
                "OFF_DUTY",
                rules["requiredBreakHours"],
                why,
            )
            clock.take_break(rules["requiredBreakHours"])

        elif limit == H.Limit.CYCLE:
            log(
                why,
                f"→ {rules['restartHours']:.0f}-hour restart inserted "
                f"(resets the {rules['maxCycleHours']:.0f} h cycle)",
            )
            add_stop(
                "RESTART",
                "OFF_DUTY",
                rules["restartHours"],
                f"{why} → {rules['restartHours']:.0f}h restart",
            )
            clock.take_restart()

        else:
            log(
                why,
                f"→ driving stopped, {rules['requiredRestHours']:.0f}-hour rest inserted "
                "(new shift afterwards)",
            )
            add_stop(
                "REST",
                "SLEEPER",
                rules["requiredRestHours"],
                why,
            )
            clock.take_rest()

    def on_duty_stop(stop_type, hours, reason):
        while True:
            if clock.cycle_used + hours > rules["maxCycleHours"] + EPS:
                time_off(Limit.CYCLE)
            elif (
                clock.window_open
                and clock.window_used + hours
                > rules["maxDutyWindowHours"] + EPS
            ):
                time_off(Limit.WINDOW)
            else:
                break

        ensure_shift()
        log(
            f"{stop_type} inserted",
            f"Duration: {hours} h (ON_DUTY) · {reason}",
        )
        add_stop(stop_type, "ON_DUTY", hours, reason)
        clock.on_duty(hours)

    log(
        "Route calculated",
        (
            f"Distance: {round(route['distanceMiles'])} mi · "
            f"Driving time: {format_hours(route['drivingHours'])} h"
        ),
    )

    log(
        "Initial cycle",
        (
            f"{cycle_used} / {rules['maxCycleHours']} h used · "
            f"remaining: {format_hours(rules['maxCycleHours'] - cycle_used)} h"
        ),
    )

    for leg in route["legs"]:
        leg_hours = leg["hours"]
        leg_miles = leg["miles"]
        speed = leg_miles / leg_hours if leg_hours > EPS else 0
        left = leg_miles

        if left > EPS and speed > 0:
            log(
                f"Start leg: {leg['name']}",
                f"{round(leg_miles)} mi · {format_hours(leg_hours)} h",
            )

        while left > EPS and speed > 0:
            if since_fuel >= rules["fuelIntervalMiles"] - EPS:
                on_duty_stop(
                    "FUEL",
                    rules["fuelStopHours"],
                    f"{rules['fuelIntervalMiles']:,}-mile fueling interval",
                )
                since_fuel = 0
                continue

            allowed, limit = clock.max_drive_now()
            if allowed < EPS:
                time_off(limit)
                continue

            to_fuel = (rules["fuelIntervalMiles"] - since_fuel) / speed
            to_end = left / speed
            chunk = min(allowed, to_fuel, to_end)

            ensure_shift()

            if to_end <= min(allowed, to_fuel) + EPS:
                why = "reached the waypoint"
            elif to_fuel <= allowed + EPS:
                why = f"next: {rules['fuelIntervalMiles']:,}-mile fuel stop"
            else:
                why = f"next: {get_rule_text(limit, rules)}"

            log(
                f"Drive {format_hours(chunk)} h ({round(chunk * speed)} mi)",
                f"Limited by: {why}",
            )
            add("DRIVING", chunk, "DRIVING", f"Route: {leg['name']}")
            clock.drive(chunk)

            distance_driven = chunk * speed
            left -= distance_driven
            miles += distance_driven
            since_fuel += distance_driven

        if leg["endsWith"] == "PICKUP":
            on_duty_stop("PICKUP", rules["pickupHours"], "Loading at pickup")
            log("Continue to dropoff")
        else:
            on_duty_stop("DROPOFF", rules["dropoffHours"], "Unloading at dropoff")

    log(
        "Trip complete",
        (
            f"Cycle used at end: {format_hours(clock.cycle_used)} / "
            f"{rules['maxCycleHours']} h"
        ),
    )

    return {
        "events": events,
        "stops": stops,
        "steps": steps,
        "cycleEnd": clock.cycle_used,
    }