from collections import defaultdict, deque
from datetime import timedelta
from ..models import City, Flight
from django.db import connection


def get_flight_paths(origin_id, destination_id):
    query = """
    WITH RECURSIVE flight_paths AS (
        SELECT 
            f.origin_id AS start_city,
            f.destination_id AS next_city,
            ARRAY[f.id] AS flight_ids,
            0 AS transfers,
            f.date_of_flight,
            f.arrival_date
        FROM flights f
        WHERE f.origin_id = %s

        UNION ALL

        SELECT 
            fp.start_city,
            f.destination_id,
            fp.flight_ids || f.id,
            fp.transfers + 1,
            f.date_of_flight,
            f.arrival_date
        FROM flight_paths fp
        JOIN flights f ON fp.next_city = f.origin_id
        WHERE fp.transfers < 3 AND f.date_of_flight >= fp.arrival_date + INTERVAL '30 minutes'
    )
    SELECT * 
    FROM flight_paths 
    WHERE next_city = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [origin_id, destination_id])
        rows = cursor.fetchall()
    return rows


from collections import defaultdict, deque
from datetime import timedelta


def get_undirected_path(origin: City, destination: City, date):
    seen = set()
    result = []
    flights = Flight.objects.select_related("origin", "destination").only(
        "id", "origin_id", "destination_id", "date_of_flight", "arriving_date"
    ).filter(date_of_flight__inrange=(date, date+timedelta(days=1)))

    graph = defaultdict(list)
    for flight in flights:
        graph[flight.origin.id].append(
            {"flight_id": flight.id, "destination": flight.destination.id,
             "arrival_date": flight.arriving_date, "date_of_flight": flight.date_of_flight}
        )

    que = deque([(origin.id, [], None)])
    layers = 3
    while que and layers > 0:
        current_level_size = len(que)
        for _ in range(current_level_size):
            cur_city, path, arriving_date = que.popleft()

            for flight in graph[cur_city]:
                if (arriving_date and
                    flight["date_of_flight"] - arriving_date < timedelta(days=30)) or flight["flight_id"] in seen:
                    continue

                seen.add(flight["flight_id"])
                new_path = path + [(flight["flight_id"], cur_city, flight["destination"], flight["arrival_date"])]

                if flight["destination"] == destination.id:
                    result.append(new_path)
                else:
                    que.append((flight["destination"], new_path, flight["arrival_date"]))
        layers -= 1

    return result
