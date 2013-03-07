import urllib3
import xml.etree.ElementTree as xml
import throttle

HTTP = urllib3.PoolManager()
CENSUS = dict(map(lambda z:(z[1], int(z[0])), (s.split("\t") for s in open('censusscore.txt').read().strip().split("\n"))))
THROTTLE = throttle.Throttler(30, 48)

def ns_api(fields):
    THROTTLE.wait()
    url = 'http://www.nationstates.net/cgi-bin/api.cgi?' + '&'.join(
            '{0}={1}'.format(a, b) for a,b in fields.items()
            )
    r = HTTP.request('GET', url)
    if r.status == 421:
        raise ValueError("Scraper is currently blocked.")
    elif r.status != 200:
        raise ValueError("Unknown error. Please visit {0} for details.".format(url))
    THROTTLE.register()
    return xml.fromstring(r.data)

def nation_shard(nation, shard):
    return ns_api({'nation' : nation, 'q' : shard})

def nation_census(nation, census_name):
    return nation_shard(nation, 'censusscore-{0}'.format(CENSUS[census_name])).find('CENSUSSCORE').text

def region_shard(region, shard):
    return ns_api({'region' : region, 'q' : shard})

