from .domain.eld import build_days
from .domain.hos_rules import START_HOUR, MAX_CYCLE_HOURS
from .domain.scheduler import schedule_trip


def plan_trip(route, cycle_used,rules):

    schedule_result = schedule_trip(
        route,
        cycle_used
        ,rules
    )

    events = schedule_result["events"]
    stops = schedule_result["stops"]
    steps = schedule_result["steps"]
    cycle_end = schedule_result["cycleEnd"]

    days = build_days(events)

    return {
        "route": route,

        "stops": stops,

        "events": events,

        "days": days,

        "steps": steps,

        "summary": {
            "distanceMiles": route["distanceMiles"],
            "drivingHours": route["drivingHours"],

            "durationHours": (
                events[-1]["end"] - START_HOUR
            ),

            "days": len(days),

            "cycleStart": cycle_used,

            "cycleEnd": cycle_end,
        },
    }