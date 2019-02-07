# bgpwatch: watching prefixes via BGPStream

## What it does
bgpwatch is a python script that uses the pybgpstream library to subscribe to CAIDA's [BGPStream](https://bgpstream.caida.org/) [Broker Service](https://bgpstream.caida.org/docs/api/broker) and processes bgp updates collected by the [public bgp monitoring ecosystem](https://bgpstream.caida.org/data).
Upon connecting to the service, bgpwatch inspects the updates received to see if they contain an unexpected origin asn for the prefixes you want to watch.

This code is largely just a proof-of-concept.

## Installation

### 1) Install BGPStream
First, follow the instructions to install BGPStream on your system
https://bgpstream.caida.org/docs/install/bgpstream

### 2) Install bgpwatch into a virtual environment thing
note: bgpwatch requires python 3 because it's no longer the year 2010

    git clone https://github.com/dwcarder/bgpwatch
    cd bgpwatch/
    python3 -m venv bgpwatch-venv
    source bgpwatch-venv/bin/activate
    python setup.py install

## Config
Create a yaml file containing the routes you want to watch, and the origin ASN's they should have in the following format (prefix: asn):

    192.0.2.0/24: '64512'
    198.51.100.0/24: '64512'
    2001:DB8::/32: '64512'

## Use

invoke bgpwatch with the yaml file containing the routes to watch:

    source bgpwatch-venv/bin/activate
    bgpwatch -f routes.yaml

## debug

Use the `-d` option for showing all updates received matching your prefix list.
This is quite verbose.

## Devel

This was written as a proof-of-concept code, contributions greatly accepted to help make it better or to turn it into something real.

Things that would be not hard to do:
 - send out some sort of notification (email, trap, or use some sort of hipster web api thing)
 - watch components of an expected path asn rather than just origin asn
 - watch for more-specific announcements, even if the origin matches

## Docker

You can use the Dockerfile to build locally or pull from dwcarder/bgpwatch.
You need to bind mount the yaml file containing your prefixes:OriginASNs to be monitored.
Example:

    docker run -it --rm -v $PWD/routes.yaml:/routes.yaml dwcarder/bgpwatch -d -f routes.yaml

## Acknowledgements:

- Dale W. Carder - ESnet
- Karl Newell - Internet2
