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


##

#labelList["CPU System Utilization Summary (percentage)"]        =  {"metrics":[{"name":"perf_cpu_system_util:max1h","header":"Max","per":"cpu"},
#                                                                          {"name":"perf_cpu_system_util:min1h","header":"Min","per":"cpu"},
#                                                                          {"name":"perf_cpu_system_util:avg1h","header":"Avg","per":"cpu"}],
#                                                                    "labels":("__name__","instance","cpu")}

#labelList["CPU User Utilization Summary (percentage)"]        =   {"metrics":[{"name":"perf_cpu_user_util:max1h","header":"Max","per":"cpu"},
#                                                                          {"name":"perf_cpu_user_util:min1h","header":"Min","per":"cpu"},
#                                                                          {"name":"perf_cpu_user_util:avg1h","header":"Avg","per":"cpu"}],
#                                                                    "labels":("__name__","instance","cpu")}

#labelList["Disk Utilization Summary (percentage)"]        =   {"metrics":[{"name":"perf_cpu_user_util:max1h","header":"Max","per":"cpu"},
#                                                                          {"name":"perf_cpu_user_util:min1h","header":"Min","per":"cpu"},
#                                                                          {"name":"perf_cpu_user_util:avg1h","header":"Avg","per":"cpu"}],
#                                                                    "labels":("__name__","instance","cpu")}


#labelList["Disk Utilization Summary (percentage)"]       =    {"metrics":[{"name":"perf_disk_util:max1h","header":"Max","per":"df"},
#                                                                          {"name":"perf_disk_util:min1h","header":"Min","per":"df"},
#                                                                          {"name":"perf_disk_util:avg1h","header":"Avg","per":"df"}],
#                                                                    "labels":("__name__","instance","df")}


#labelList["Disk Write Time (milliseconds)"]       =    {"metrics":[{"name":"perf_disk_write:max1h","header":"Max","per":"df"},
#                                                                          {"name":"perf_disk_write:min1h","header":"Min","per":"df"},
#                                                                          {"name":"perf_disk_write:avg1h","header":"Avg","per":"df"}],
#                                                                    "labels":("__name__","instance","df")}


#labelList["Disk Read Time (milliseconds)"]       =    {"metrics":[{"name":"perf_disk_read:max1h","header":"Max","per":"df"},
#                                                                          {"name":"perf_disk_read:min1h","header":"Min","per":"df"},
#                                                                          {"name":"perf_disk_read:avg1h","header":"Avg","per":"df"}],
#                                                                    "labels":("__name__","instance","df")}

#labelList["Memory Utlization Summary (percentage)"]       =    {"metrics":[{"name":"perf_memory_util:max1h","header":"Max","per":"None"},
#                                                                          {"name":"perf_memory_util:min1h","header":"Min","per":"None"},
#                                                                          {"name":"perf_memory_util:avg1h","header":"Avg","per":"None"}],
#                                                                    "labels":("__name__","instance")}

##


labelList["Interface Drops (In)"]       =    {"metrics":[{"name":"perf_packet_drops_in:max1h","header":"Max","per":"interface"},
                                                                          {"name":"perf_packet_drops_in:min1h","header":"Min","per":"interface"},
                                                                          {"name":"perf_packet_drops_in:avg1h","header":"Avg","per":"interface"}],
                                                                    "labels":("__name__","instance","interface")}



labelList["Interface Drops (Out)"]       =    {"metrics":[{"name":"perf_packet_drops_out:max1h","header":"Max","per":"interface"},
                                                                          {"name":"perf_packet_drops_out:min1h","header":"Min","per":"interface"},
                                                                          {"name":"perf_packet_drops_out:avg1h","header":"Avg","per":"interface"}],
                                                                    "labels":("__name__","instance","interface")}



labelList["Interface Errors (In)"]       =    {"metrics":[{"name":"perf_packet_errs_in:max1h","header":"Max","per":"interface"},
                                                                          {"name":"perf_packet_errs_in:min1h","header":"Min","per":"interface"},
                                                                          {"name":"perf_packet_errs_in:avg1h","header":"Avg","per":"interface"}],
                                                                    "labels":("__name__","instance","interface")}



labelList["Interface Errors (Out)"]       =    {"metrics":[{"name":"perf_packet_errs_out:max1h","header":"Max","per":"interface"},
                                                                          {"name":"perf_packet_errs_out:min1h","header":"Min","per":"interface"},
                                                                          {"name":"perf_packet_errs_out:avg1h","header":"Avg","per":"interface"}],
                                                                    "labels":("__name__","instance","interface")}



labelList["Interface Packets (In)"]       =    {"metrics":[{"name":"perf_packets_in:max1h","header":"Max","per":"interface"},
                                                                          {"name":"perf_packets_in:min1h","header":"Min","per":"interface"},
                                                                          {"name":"perf_packets_in:avg1h","header":"Avg","per":"interface"}],
                                                                    "labels":("__name__","instance","interface")}




labelList["Interface Packets (Out)"]       =    {"metrics":[{"name":"perf_packets_out:max1h","header":"Max","per":"interface"},
                                                                          {"name":"perf_packets_out:min1h","header":"Min","per":"interface"},
                                                                          {"name":"perf_packets_out:avg1h","header":"Avg","per":"interface"}],
                                                                    "labels":("__name__","instance","interface")}



labelList["System Load"]       =    {"metrics":[{"name":"perf_system_load:max1h","header":"Max","per":"None"},
                                                                          {"name":"perf_system_load:min1h","header":"Min","per":"None"},
                                                                          {"name":"perf_system_load:avg1h","header":"Avg","per":"None"}],
                                                                    "labels":("__name__","instance")}



labelList["System Uptime"]       =    {"metrics":[{"name":"perf_system_uptime:max1h","header":"Max","per":"None"},
                                                                          {"name":"perf_system_uptime:min1h","header":"Min","per":"None"},
                                                                          {"name":"perf_system_uptime:avg1h","header":"Avg","per":"None"}],
                                                                    "labels":("__name__","instance")}

#Main Header

if len(sys.argv) != 2:
    print('Usage: {0} http://prometheus:9090'.format(sys.argv[0]))
    sys.exit(1)
instances=set()
instances=GetInstanceNames(sys.argv[1])
writeHeader=True


for instance in instances:

    #write all header first

    header_row1 =  [""]
    header_row1.append("")
    header_row1.append("")
    header_row2 =  ["Node"]
    header_row2.append("Start Time")
    header_row2.append("End time")
    SanitizedResult = defaultdict(list)
    SanitizedResult={"node":instance,"starttime":"","results":{}}
    writeNewRow=True
     #names= defaultdict(list)
    for k, v in labelList.iteritems():
        if k not in SanitizedResult["results"]:
            #SanitizedResult["results"][k]={"Max":[],"Min":[],"Avg":[],"Per":v["metrics"][0]["per"],"Per_Value":[]}
            SanitizedResult["results"][k]={"Max":[],"Min":[],"Avg":[],"Per":v["metrics"][0]["per"]}


    #SanitizedResult={"node":instance,"starttime":"","name":"","results":{"matrix_name":["max":{},"min":{},"avg":{},"per_name":"","per_value":""]}}
    #SanitizedResult={"node":instance,"starttime":"","name":"","results":{}}
    #result={"matrix_name":["max":{},"min":{},"avg":{},"per_name":"","per_value":""]}
    #result={"matrix_name":["max":{},"min":{},"avg":{},"per_name":"","per_value":""]}

    for k, v in labelList.iteritems():
        for data in v["metrics"]:
            response = requests.get(sys.argv[1]+'/api/v1/query?query='+data["name"]+'{instance="'+instance+'"}')
            results = response.json()['data']["result"]
            for result in results:

                SanitizedResult["starttime"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0]-3600))
                SanitizedResult["endtime"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0]))
                SanitizedResult["results"][k].get(data["header"], '').append({"value":result['value'][1],"per":data["per"],"per_value":result['metric'].get(data["per"], '')})

        #write first row
        #writer.writerow([' ', ' ', ' '] + labelnames)
        if writeNewRow==True:
            data_row=[SanitizedResult["node"]]
            data_row.append(SanitizedResult["starttime"])
            data_row.append(SanitizedResult["endtime"])
            writeNewRow=False

    for key,value in SanitizedResult["results"].iteritems():

        #for index,item in enumerate(value["Max"]):
            #print item["per_value"]
            #value["Max"][index]["per_value"]

        for index,item in enumerate(value["Max"]):
            header_row2.append("Max")
            header_row2.append("Avg")
            header_row2.append("Min")
            try:
                data_row.append(value["Max"][index]["value"])
                header_row1.append(key+ " : " + value["Max"][0]["per"] + " : " + value["Max"][index]["per_value"])
            except IndexError:
                data_row.append(-1)
                header_row1.append(key + "_for_ error")
            try:
                data_row.append(value["Avg"][index]["value"])
                header_row1.append(key+ " : " + value["Max"][0]["per"] + " : " + value["Max"][index]["per_value"])
            except IndexError:
                data_row.append(-1)
                header_row1.append(key + "_for_ error")
            try:
                data_row.append(value["Min"][index]["value"])
                header_row1.append(key+ " : " + value["Max"][0]["per"] + " : " + value["Max"][index]["per_value"])
            except IndexError:
                data_row.append(-1)
                header_row1.append(key + "_for_ error")


    writer.writerow(header_row1)
    writer.writerow(header_row2)
    writer.writerow(data_row)
