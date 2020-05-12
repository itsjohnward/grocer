<h1 style="text-align: center">Grocer: A Programmable Grocery Delivery Interface</h1>
<p align="center">
<a href="https://travis-ci.com/itsjohnward/grocer"><img alt="Build Status" src="https://travis-ci.com/itsjohnward/grocer.svg?branch=master"></a>
<a href="https://codeclimate.com/github/itsjohnward/grocer/maintainability"><img src="https://api.codeclimate.com/v1/badges/44e9c2a633eb3c569c49/maintainability" /></a>
<a href="https://codeclimate.com/github/itsjohnward/grocer/test_coverage"><img src="https://api.codeclimate.com/v1/badges/44e9c2a633eb3c569c49/test_coverage" /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/itsjohnward/grocer/releases"><img alt="Code style: black" src="https://img.shields.io/github/v/release/itsjohnward/grocer"></a>
</p>

## Install

```py
pip install git+https://github.com/itsjohnward/grocer.git
```

## Use from the command line

```sh
$ grocer <store> <action>
```

For example:

```sh
$ grocer wegmans times
                  date         time  price
index                                     
0       Monday, May 11    4pm - 6pm  $5.99
1       Monday, May 11    5pm - 7pm  $5.99
2      Tuesday, May 12  10am - Noon  $5.99
3      Tuesday, May 12   11am - 1pm  $5.99
4      Tuesday, May 12   Noon - 2pm  $5.99
5      Tuesday, May 12    1pm - 3pm  $5.99
```

## Import to create your own python programs

For example:

```py
from grocer import GrocerClient

# Create a client instance
client = GrocerClient(merchant="wegmans", email="example@example.com", password="password")

# Call client methods
print(client.get_delivery_times())
```

## Example project

See <https://github.com/itsjohnward/grocer-notifier> as an example of a project written using Grocer.

## Feature Roadmap / Further Work

### Merchants

- [x] Wegmans (Instacart)
- [ ] Fairway (Instacart)
- [ ] FreshDirect
- [ ] Amazon Fresh

### Actions

- [x] times: get available delivery times
- [ ] search: search for products
- [ ] add: add product to cart
- [ ] remove: remove product from cart
- [ ] cart: get the status of the current cart
- [ ] checkout: purchase the items currently in the cart

