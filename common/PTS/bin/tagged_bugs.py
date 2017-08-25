#!/usr/bin/python

# Copyright 2008 Stefano Zacchiroli <zack@debian.org>
# This file is distributed under the terms of the General Public License
# version 2 or (at your option) any later version.

# Script to collect bug summaries from the Debian BTS via SOAP.
# Lookup can be performed via official tags or via usertags.

import SOAPpy
import string
import sys
import os

ca_path = '/etc/ssl/ca-debian'
if os.path.isdir(ca_path):
    os.environ['SSL_CERT_DIR'] = ca_path

url = 'https://bugs.debian.org/cgi-bin/soap.cgi'
namespace = 'Debbugs/SOAP'
server = SOAPpy.SOAPProxy(url, namespace)

def get_usertag(email, *tags):
    result = server.get_usertag(email, *tags)
    return result

def get_status(*args):
    result = []
    for arg in args:
        if isinstance(arg, list):
            for i in range(0, len(arg), 500):
                status = server.get_status(arg[i:i+500])
                result.extend(status[0])
        else:
            status = server.get_status(arg)
            result.extend(status[0])
    return [result]

def get_bugs(*args):
    result = server.get_bugs(*args)
    return result

def mk_summary(bugs):
    pkgs = {}   # map package names to list of newcomer bug numbers
    statuses = get_status(bugs)
    i = 0
    for status in statuses[0]:
        if status['value']['done'] or status['value']['fixed'] or \
            status['value']['pending'] == 'fixed':
                # roughly equivalent to filtering via Debbugs URL snippet
                # pend-exc=pending-fixed&pend-exc=fixed&pend-exc=done
                continue
        pkg = status['value']['package']
        if not pkgs.has_key(pkg):
            pkgs[pkg] = []
        pkgs[pkg].append(str(bugs[i]))
        i += 1
    return pkgs

def find_usertagged(user, tag):
    bugs = get_usertag(user, tag)
    return mk_summary(bugs[0])

def find_tagged(tag):
    bugs = get_bugs('tag', tag)
    return mk_summary(bugs)

if __name__ == '__main__':

    def print_bug_summary(dict):
        for (pkg, bugs) in dict.iteritems():
            pkg = string.replace(pkg, ' ', '')  # ensure spaces do not occur
                                                # between packages
            print "%s\t%d" % (pkg, len(bugs))

    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print 'Usage: tagged_bugs.py TAG [USER]'
        sys.exit(2)
    elif len(sys.argv) == 2:
        print_bug_summary(find_tagged(sys.argv[1]))
    elif len(sys.argv) == 3:
        print_bug_summary(find_usertagged(sys.argv[2], sys.argv[1]))

