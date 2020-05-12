import os

import luigi

from .wegmans.tasks import GetDeliveryTimes


class GrocerClient:
    def __init__(self):
        # TODO: email and password and merchant as inputs and remove hard-coding
        self.merchant = "wegmans"
        self.email = os.environ["EMAIL"]
        self.password = os.environ["PASSWORD"]

    def get_delivery_times(self):
        delivery_times = GetDeliveryTimes()
        luigi.build([delivery_times], local_scheduler=True)
        return delivery_times.get_results()
