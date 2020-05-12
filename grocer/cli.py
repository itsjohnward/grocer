import argparse

import luigi

from .wegmans.tasks import GetDeliveryTimes


def main():
    parser = argparse.ArgumentParser(description="Grocer CLI")
    parser.add_argument("merchant", action="store", type=str, choices=["wegmans"])
    parser.add_argument("action", action="store", type=str, choices=["times"])
    # TODO: take merchant and username and password as inputs and pass to task
    parser.add_argument("-e", "--email", action="store", type=str)
    parser.add_argument("-p", "--password", action="store", type=str)
    args = parser.parse_args()

    if args.action == "times":
        delivery_times = GetDeliveryTimes()
        luigi.build([delivery_times], local_scheduler=True)
        delivery_times.print_results()
