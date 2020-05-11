from datetime import datetime

from django.core.management import BaseCommand
import luigi

from ...models import FactDeliveryTime, DimQueryTime
from grocer.instacart.tasks import GetDeliveryTimes


def parse_date(date):
    """
    >>> parse_date("Monday, May 11")
    datetime(2020, 5, 11, 0, 0)
    """
    return datetime.strptime(
        date.split(", ")[1] + " " + str(datetime.now().year), "%B %d %Y"
    )


def parse_time_str(time):
    """
    >>> parse_time_str('4pm')
    16
    >>> parse_time_str('Noon')
    12
    >>> parse_time_str('9am')
    9
    """
    if time == "Noon" or time == "12pm":
        time = "0pm"
    elif time == "Midnight" or time == "12am":
        time = "0am"
    if "am" in time:
        return int(time.strip("am"))
    return int(time.strip("pm")) + 12


def parse_times(times):
    split_times = times.split(" - ")
    return {
        "start": parse_time_str(split_times[0]),
        "end": parse_time_str(split_times[1]),
    }


def parse_price(price):
    return price.strip("$")[1]


def parse_delivery_time(delivery_time):
    date = parse_date(delivery_time["date"])
    times = parse_times(delivery_time["time"])
    price = parse_price(delivery_time["price"])
    return {
        "start": date.replace(hour=times["start"]),
        "end": date.replace(hour=times["end"]),
        "price": price,
    }


def get_delivery_times(**options):
    delivery_times_task = GetDeliveryTimes()
    luigi.build([delivery_times_task], local_scheduler=True)
    return [
        parse_delivery_time(delivery_time)
        for index, delivery_time in delivery_times_task.get_results().iterrows()
    ]


class Command(BaseCommand):
    help = "Load delivery times"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--full", action="store_true")

    def handle(self, *args, **options):
        query_time = datetime.now()
        delivery_times = get_delivery_times(**options)
        if len(delivery_times) > 0:
            FactDeliveryTime.objects.get_or_create(
                timestamp=DimQueryTime.objects.get_or_create(timestamp=query_time)[0],
                slot_start=None,
                slot_end=None,
                price=None,
            )
        else:
            for delivery_time in delivery_times:
                created_delivery_times.append(
                    FactDeliveryTime.objects.get_or_create(
                        timestamp=DimQueryTime.objects.get_or_create(
                            timestamp=query_time
                        )[0],
                        slot_start=delivery_time["start"],
                        slot_end=delivery_time["end"],
                        price=delivery_time["price"],
                    )
                )
