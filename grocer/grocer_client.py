import os

import luigi

from .wegmans.tasks import GetDeliveryTimes


class GrocerClient:
    def __init__(self, merchant, email, password):
        # TODO: use email and password and merchant as params to task
        self.merchant = merchant
        self.email = email
        self.password = password

    def get_delivery_times(self):
        delivery_times = GetDeliveryTimes()
        luigi.build([delivery_times], local_scheduler=True)
        return delivery_times.get_results()
