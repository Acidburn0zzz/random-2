#!/usr/bin/env python

import json, urllib
from optparse import OptionParser
target_url = "http://aur.archlinux.org/rpc.php"

class AppURLopener(urllib.FancyURLopener):
    version = 'AURJSON-Example/1.0 python'

urllib._urlopener = AppURLopener()

def search(args):
    params = urllib.urlencode({'type':'search', 'arg':args})
    response = urllib.urlopen("%s?%s" % (target_url,params)).read()
    print_results(json.loads(response))

def info(args):
    params = urllib.urlencode({'type':'info', 'arg':args})
    response = urllib.urlopen("%s?%s" % (target_url,params)).read()
    print_results(json.loads(response))

def print_results(data):
    if data['type'] == 'error':
        print 'Error: %s' % data['results']
        return
    if not isinstance(data['results'], list):
        data['results'] = [data['results'],]
    print 'Packages:'
    for pkg in data['results']:
        for name in pkg:
            print '  %s: %s' % (name, pkg[name])
        print ''

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage=usage)
    parser.set_defaults(search_mode=0)
    parser.add_option("-s",
            "--search",
            action="store_const",
            const=0,
            dest="search_mode",
            help="Operate in search mode")
    parser.add_option("-i",
            "--info",
            action="store_const",
            const=1,
            dest="search_mode",
            help="Operate in detail mode")

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("Incorrect number of arguments")
    if options.search_mode == 1:
        info(args[0])
    else:
        search(args[0])

if __name__ == "__main__":
    main()

