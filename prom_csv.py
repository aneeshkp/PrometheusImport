import csv
import requests
import sys
def GetMetrixNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    results = response.json()['data']

    #Return metrix
    return results


"""
A simple program to print the result of a Prometheus query as CSV.
"""
writer = csv.writer(sys.stdout)
# Write the header,

if len(sys.argv) != 2:
    print('Usage: {0} http://prometheus:9090'.format(sys.argv[0]))
    sys.exit(1)
metrixResults=GetMetrixNames(sys.argv[1])

writeHeader=True
for metrixResult in metrixResults:
    if metrixResult.startswith("collectd"):
        response = requests.get('{0}/api/v1/query'.format(sys.argv[1]),
        params={'query': metrixResult+'[1h]'})
        results = response.json()['data']['result']
        # Build a list of all labelnames used.
        #gets all keys and discard __name__
        labelnames = set()
        for result in results:
            labelnames.update(result['metric'].keys())
        # Canonicalize
        labelnames.discard('__name__')
        labelnames = sorted(labelnames)
        # Write the samples.
        if writeHeader:
            writer.writerow(['name', 'timestamp', 'value'] + labelnames)
            writeHeader=False
        for result in results:
            l = [result['metric'].get('__name__', '')] + result['values']
            for label in labelnames:
                l.append(result['metric'].get(label, ''))
            writer.writerow(l)
