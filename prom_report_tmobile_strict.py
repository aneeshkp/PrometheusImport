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
labelList={}



labelList["perf_cpu_util:max1h"]        =   {"labels":("__name__","instance","cpu"),"sub_header":"max","filter":{"system":"CPU System Utilization Summary (percentage)","user":"CPU User Utilization Summary (percentage)"}}
labelList["perf_cpu_util:min1h"]        =   {"labels":("__name__","instance","cpu"),"sub_header":"min","filter":{"system":"CPU System Utilization Summary (percentage)","user":"CPU User Utilization Summary (percentage)"}}
labelList["perf_cpu_util:avg1h"]        =   {"labels":("__name__","instance","cpu"),"sub_header":"avg","filter":{"system":"CPU System Utilization Summary (percentage)","user":"CPU User Utilization Summary (percentage)"}}

labelList["perf_disk_util:avg1h"]       =   {"labels":("__name__","instance","df")}
labelList["perf_disk_util:max1h"]       =   {"labels":("__name__","instance","df")}
labelList["perf_disk_util:min1h"]       =   {"labels":("__name__","instance","df")}

labelList["perf_disk_write:max1h"]       =   {"labels":("__name__","instance","disk")}
labelList["perf_disk_write:min1h"]       =   {"labels":("__name__","instance","disk")}
labelList["perf_disk_write:avg1h"]       =   {"labels":("__name__","instance","disk")}

labelList["perf_disk_read:max1h"]       =   {"labels":("__name__","instance","disk")}
labelList["perf_disk_read:min1h"]       =   {"labels":("__name__","instance","disk")}
labelList["perf_disk_read:avg1h"]       =   {"labels":("__name__","instance","disk")}

labelList["perf_memory_util:max1h"]     =   {"labels":("__name__","instance","memory")}
labelList["perf_memory_util:min1h"]     =   {"labels":("__name__","instance","memory")}
labelList["perf_memory_util:avg1h"]     =   {"labels":("__name__","instance","memory")}

labelList["perf_packet_drops_in:max1h"] =   {"labels":("__name__","instance","interface")}
labelList["perf_packet_drops_in:min1h"] =   {"labels":("__name__","instance","interface")}
labelList["perf_packet_drops_in:avg1h"] =   {"labels":("__name__","instance","interface")}

labelList["perf_packet_drops_out:max1h"]=   {"labels":("__name__","instance","interface")}
labelList["perf_packet_drops_out:min1h"]=   {"labels":("__name__","instance","interface")}
labelList["perf_packet_drops_out:avg1h"]=   {"labels":("__name__","instance","interface")}

labelList["perf_packet_errs_in:max1h"]  =   {"labels":("__name__","instance","interface")}
labelList["perf_packet_errs_in:min1h"]  =   {"labels":("__name__","instance","interface")}
labelList["perf_packet_errs_in:avg1h"]  =   {"labels":("__name__","instance","interface")}

labelList["perf_packet_errs_out:max1h"] =   {"labels":("__name__","instance","interface")}
labelList["perf_packet_errs_out:min1h"] =   {"labels":("__name__","instance","interface")}
labelList["perf_packet_errs_out:avg1h"] =   {"labels":("__name__","instance","interface")}

labelList["perf_packets_in:max1h"]      =   {"labels":("__name__","instance","interface")}
labelList["perf_packets_in:min1h"]      =   {"labels":("__name__","instance","interface")}
labelList["perf_packets_in:avg1h"]      =   {"labels":("__name__","instance","interface")}

labelList["perf_packets_out:max1h"]     =   {"labels":("__name__","instance","interface")}
labelList["perf_packets_out:min1h"]     =   {"labels":("__name__","instance","interface")}
labelList["perf_packets_out:avg1h"]     =   {"labels":("__name__","instance","interface")}

labelList["perf_system_load:avg1h"]     =   {"labels":("__name__","instance")}
labelList["perf_system_load:max1h"]     =   {"labels":("__name__","instance")}
labelList["perf_system_load:min1h"]     =   {"labels":("__name__","instance")}

labelList["perf_system_uptime:avg1h"]   =   {"labels":("__name__","instance")}
labelList["perf_system_uptime:max1h"]   =   {"labels":("__name__","instance")}
labelList["perf_system_uptime:min1h"]   =   {"labels":("__name__","instance")}

for k, v in labelList.iteritems():
 print "{0} : {1}".format(k,v)
 print "Labels: {0} ".format(v["labels"])
 try:
     print "Filters: {0} ".format(v["filter"])
    # Do something
 except KeyError:
    pass

sys.exit(1)


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
