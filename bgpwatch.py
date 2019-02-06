#!/usr/bin/env python

import argparse
import time
import textwrap
import pytricia
from _pybgpstream import BGPStream, BGPRecord, BGPElem
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description = textwrap.dedent('''\
        a proof-of-concept utility for watching updates from BGPstream
        and then printing out if an unexpected update is heard
        ''')
    parser.epilog = textwrap.dedent('''\
        Example: watch these route announcements
            %(prog)s -f routes.yaml ''')
    required = parser.add_argument_group('required arguments')
    required.add_argument("-f", "--file", required=True, help="yaml file of prefixes to origin asn")
    parser.add_argument("-d", "--debug", action='store_true', help="print out all updates containing these prefixes")
    args = parser.parse_args()

    routes = pytricia.PyTricia(48) # longest reasonable pfx in dfz
    
    with open(args.file, 'r') as f:
        routesfile = yaml.safe_load(f)
    for pfx in routesfile:
        routes[pfx] = routesfile[pfx]
    
    stream = BGPStream()
    rec = BGPRecord()
    stream.add_filter('record-type', 'updates')
    stream.add_interval_filter(int(time.time()),0)
    stream.set_live_mode()
    stream.start()
    
    while(stream.get_next_record(rec)):
        if rec.status == 'valid':
            elem = rec.get_next_elem()
            while(elem):
                if 'as-path' in elem.fields:
                    path = elem.fields['as-path'].split()
                    prefix = elem.fields['prefix']
                    if prefix in routes and (routes[prefix] != path[-1] or args.debug):
                        print('Heard prefix:', elem.fields['prefix'], 'AS-PATH:', elem.fields['as-path'], '  Found by project:', rec.project, 'collector:', rec.collector, 'type:', rec.type, 'at time:', rec.time, 'Type:', elem.type, 'Peer:', elem.peer_address, 'AS', elem.peer_asn)
    
                elem = rec.get_next_elem()


if __name__ == "__main__":
    main()
