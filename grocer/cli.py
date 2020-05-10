import argparse

import luigi

from .instacart.tasks import GetDeliveryTimes


def main():
    parser = argparse.ArgumentParser(description="Grocer CLI")
    args = parser.parse_args()
    delivery_times = GetDeliveryTimes()
    luigi.build([delivery_times], local_scheduler=True)
    delivery_times.print_results()
