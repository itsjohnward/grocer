import argparse

import luigi

from .wegmans.tasks import GetDeliveryTimes


def main():
    parser = argparse.ArgumentParser(description="Grocer CLI")
    # TODO: take merchant and username and password as inputs and pass to task
    args = parser.parse_args()
    delivery_times = GetDeliveryTimes()
    luigi.build([delivery_times], local_scheduler=True)
    delivery_times.print_results()
