import argparse

import luigi

from . import GrocerClient


def main():
    parser = argparse.ArgumentParser(description="Grocer CLI")
    parser.add_argument("merchant", action="store", type=str, choices=["wegmans"])
    parser.add_argument("action", action="store", type=str, choices=["times"])
    # TODO: take merchant and username and password as inputs and pass to task
    parser.add_argument("-e", "--email", action="store", type=str)
    parser.add_argument("-p", "--password", action="store", type=str)
    args = parser.parse_args()

    client = GrocerClient(args.merchant, args.email, args.password)

    if args.action == "times":
        print(client.get_delivery_times())
