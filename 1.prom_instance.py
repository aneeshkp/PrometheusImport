import csv
import requests
import sys


"""
A simple program to print the result of a Prometheus query as CSV.
"""
writer = csv.writer(sys.stdout)
# Write the header,

if len(sys.argv) != 2:
    print('Usage: {0} http://prometheus:9090'.format(sys.argv[0]))
    sys.exit(1)
response = requests.get('{0}/api/v1/series?match[]=collectd_uptime'.format(sys.argv[1]))
results = response.json()['data']
for result in results:
    print(result.get("instance",''))


