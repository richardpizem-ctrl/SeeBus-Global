import csv
from dataclasses import dataclass
from datetime import date

@dataclass
class Service:
    service_id: str
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int
    sunday: int
    start_date: date
    end_date: date

def load_calendar(path: str) -> dict[str, Service]:
    services = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service = Service(
                service_id=row["service_id"],
                monday=int(row["monday"]),
                tuesday=int(row["tuesday"]),
                wednesday=int(row["wednesday"]),
                thursday=int(row["thursday"]),
                friday=int(row["friday"]),
                saturday=int(row["saturday"]),
                sunday=int(row["sunday"]),
                start_date=date.fromisoformat(row["start_date"]),
                end_date=date.fromisoformat(row["end_date"])
            )
            services[service.service_id] = service

    return services

def is_service_active(service: Service, today: date) -> bool:
    if not (service.start_date <= today <= service.end_date):
        return False

    weekday = today.weekday()  # 0 = pondelok, 6 = nedeľa
    flags = [
        service.monday,
        service.tuesday,
        service.wednesday,
        service.thursday,
        service.friday,
        service.saturday,
        service.sunday
    ]

    return flags[weekday] == 1
