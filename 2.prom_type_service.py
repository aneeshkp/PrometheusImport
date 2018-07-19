import csv
import requests
import sys

def GetInstanceNames(url):
    response = requests.get('{0}/api/v1/series?match[]=collectd_uptime'.format(sys.argv[1]))
    results = response.json()['data']
    instances=set()
    for result in results:
      instances.add(result.get("instance",''))


    #Return metrix
    return instances

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
instances=set()
instances=GetInstanceNames(sys.argv[1])
metricNames=GetMetrixNames(sys.argv[1])
for instance in instances:
        print("***********************************"+ instance +"******************************\n")
	for metricName in metricNames:
              if metricName.startswith("collectd_cpu_percent"):
                        response = requests.get(sys.argv[1]+'/api/v1/series?match[]='+metricName+'{instance="'+instance+'"}')
			results = response.json()['data']
                        # Build a list of all labelnames used.
		        #gets all keys and discard __name__
		        labelnames = set()
		        for result in results:
	          	       labelnames.update(result.keys())
		        # Canonicalize
		        labelnames.discard('job')
                        labelnames.discard("__name__")
                        labelnames.discard("instance")
		        labelnames = sorted(labelnames)
                        for result in results:
                            l = [result.get('__name__', '')] 
                            l.append(result.get("instance",''))
		            for label in labelnames:
		                l.append(label+'='+result.get(label, ''))
		            writer.writerow(l)
