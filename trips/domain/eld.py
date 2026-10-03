import math


EPS = 1e-9


def build_days(events):

    # Number of days needed to contain all events
    last_event_end = events[-1]["end"]

    n = math.ceil(
        last_event_end / 24 - EPS
    )

    days = []

    for i in range(n):

        day_start = i * 24
        day_end = day_start + 24

        output_events = []

        cursor = day_start

        # -------------------------------------------------
        # Create OFF_DUTY filler event
        # -------------------------------------------------

        def filler(start, end):
            return {
                "status": "OFF_DUTY",
                "start": start,
                "end": end,
                "label": "OFF DUTY",
                "reason": "No trip activity",
                "filler": True,
            }

        # -------------------------------------------------
        # Go through all trip events
        # -------------------------------------------------

        for event in events:

            start = max(
                event["start"],
                day_start
            )

            end = min(
                event["end"],
                day_end
            )

            # Event does not overlap this day
            if end - start < EPS:
                continue

            # There is a gap before this event
            if start > cursor + EPS:
                output_events.append(
                    filler(cursor, start)
                )

            # Add the portion of the event
            # that belongs to this day
            split_event = {
                **event,
                "start": start,
                "end": end,
            }

            output_events.append(split_event)

            cursor = end

        # -------------------------------------------------
        # Fill remaining time until midnight
        # -------------------------------------------------

        if cursor < day_end - EPS:
            output_events.append(
                filler(cursor, day_end)
            )

        # -------------------------------------------------
        # Calculate totals for this day
        # -------------------------------------------------

        totals = {
            "OFF_DUTY": 0,
            "SLEEPER": 0,
            "DRIVING": 0,
            "ON_DUTY": 0,
        }

        for event in output_events:

            status = event["status"]

            duration = (
                event["end"]
                - event["start"]
            )

            totals[status] += duration

        # -------------------------------------------------
        # Add day
        # -------------------------------------------------

        days.append({
            "day": i + 1,
            "events": output_events,
            "totals": totals,
        })

    return days