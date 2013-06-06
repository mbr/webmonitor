import argparse
import logbook
import requests
from requests.exceptions import RequestException
import time

log = logbook.Logger('webmonitor')

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('-d', '--debug', action='store_const',
                    cosnt=logbook.DEBUG,
                    help='Show detailed output')
parser.add_argument('-i', '--interval', default=30, type=float,
                    help='How many seconds to wait between checks.')
parser.add_argument('-V', '--no-verify', default=True, dest='verify',
                    action='store_false',
                    help='Disable certificate verification on HTTPS'
                         'requests.')
parser.set_defauts(loglevel=logbook.ERROR)
args = parser.parse_args()

last_known_good = None
log.info('Starting monitor on %s' % args.url)

while True:
    log.debug('Retrieving %r' % args.url)

    try:
        r = requests.get(args.url, verify=args.verify)
        r.raise_for_status()
    except RequestException as e:
        if not last_known_good:
            last = 'Website was never up before.'
        else:
            last = 'Last recorded good response was %.2f seconds ago.' % (
                time.time() - last_known_good
            )
        log.error('Failed to retrieve %r: %r. %s' % (args.url, e, last))
    else:
        log.info('%r is up' % args.url)
        last_known_good = time.time()

    log.debug('Sleeping for %s seconds.' % args.interval)
    time.sleep(args.interval)