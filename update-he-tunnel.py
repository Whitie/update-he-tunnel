#!/usr/bin/env python

import os
import sys

import requests

from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path

from requests.exceptions import RequestException


DEFAULT_CONFIG_FILE = '/etc/update-he-tunnel.conf'
EXTERNAL_IP_SERVICE = 'https://ipv4.icanhazip.com'
CACHE_FILE = '/tmp/update-he-tunnel.ip'


def get_external_ip(service):
    req = requests.get(service)
    req.raise_for_status()
    return req.text.strip()


def get_cached_ip(cache_file):
    if cache_file.is_file():
        return cache_file.open().read().strip()
    return ''


def write_new_cache(cache_file, external_ip):
    new_cache = cache_file.parent / 'new_ip.ip'
    with new_cache.open('w') as fp:
        fp.write(external_ip)
    cache_file.unlink()
    new_cache.rename(cache_file)


def update_he(update_url, external_ip):
    req = requests.get(update_url)
    req.raise_for_status()
    return ('good' in req.text and external_ip in req.text)


def get_config():
    parser = ArgumentParser(description='Check external IP and update '
                            'HE tunnel endpoint.')
    parser.add_argument('-c', '--config', default=DEFAULT_CONFIG_FILE,
                        help='Provide config file, default: %(default)s')
    args = parser.parse_args()
    config = dict(own_config=Path(args.config))
    cparser = ConfigParser()
    with config['own_config'].open() as fp:
        cparser.read_file(fp)
    config['external_ip_service'] = cparser.get(
        'global', 'external_ip_service', fallback=EXTERNAL_IP_SERVICE
    )
    config['cache_file'] = Path(
        cparser.get('global', 'cache_file', fallback=CACHE_FILE)
    )
    config['update_url'] = cparser.get('global', 'update_url')
    return config


def main():
    config = get_config()
    cached_ip = get_cached_ip(config['cache_file'])
    try:
        external_ip = get_external_ip(config['external_ip_service'])
    except RequestException as error:
        print('Error while getting external IP')
        print(error)
        sys.exit(1)
    if cached_ip == external_ip:
        print(f'IP not changed: {cached_ip}')
        return
    write_new_cache(config['cache_file'], config['external_ip'])
    try:
        updated = update_he(config['update_url'], external_ip)
    except RequestException as error:
        print('Error while updating HE')
        print(error)
        sys.exit(1)
    if updated:
        print(f'IP updated at HE with {external_ip}')
    else:
        print('Unknown error while updating at HE')
        sys.exit(1)


if __name__ == '__main__':
    main()
