import csv
import requests
import sys
import time
from collections import defaultdict
def GetMetricNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    results = response.json()['data']

    #Return metrix
    return results

def GetInstanceNames(url):
    response = requests.get('{0}/api/v1/series?match[]=collectd_uptime'.format(sys.argv[1]))
    results = response.json()['data']
    instances = set()
    for result in results:
        instances.add(result.get("instance",''))
    return instances

"""
A simple program to print the result of a Prometheus query as CSV.
"""
writer = csv.writer(sys.stdout)



# Write the header,

if len(sys.argv) != 2:
    print('Usage: {0} http://prometheus:9090'.format(sys.argv[0]))
    sys.exit(1)
metricNames=GetMetricNames(sys.argv[1])
instances=set()
instances=GetInstanceNames(sys.argv[1])

writeHeader=True
for instance in instances:
    for metricName in metricNames:
        if metricName.startswith("perf_"):
            response = requests.get(sys.argv[1]+'/api/v1/query?query='+metricName+'{instance="'+instance+'"}')
            #print(response.json())
            results = response.json()['data']["result"]
            # Build a list of all labelnames used.
            #gets all keys and discard __name__
            labelnames = set()
            for result in results:
                labelnames.update(result["metric"].keys())
            # Canonicalize
            labelnames.discard('__name__')
            labelnames.discard('instance')
            labelnames = sorted(labelnames)
            # Write the samples.
            if writeHeader:
                writer.writerow(['name', 'timestamp', 'value'] + labelnames)
                writeHeader=False
            for result in results:
                l =  [instance]
                l.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0])) )
                l.append(result['metric'].get('__name__', ''))
                for label in labelnames:
                    l.append(result['metric'].get(label, ''))
                l.append(result['value'][1])
                writer.writerow(l)
