
"""
aputtur@redhat.com
Prometheus report for T-Mobile
"""

import csv
import sys
import time
from collections import defaultdict
from optparse import OptionParser
import requests



## Get Metric Names
def get_meterics_names(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    results = response.json()['data']
    #Return metrix
    return results

## Get Instance Names
def get_instance_names(url):
    try:
        response = requests.get('{0}/api/v1/series?match[]=collectd_uptime'.format(url))
        results = response.json()['data']
        node_instances = set()
        for result in results:
            node_instances.add(result.get("instance", ''))
        return node_instances
    except:
        print("Unexpected error Check prometheus server address is correct:", sys.exc_info()[0])
        sys.exit(1)
## Get Report Header
def get_report_header(mname, per, pervalue):
    if per is None:
        return mname
    else:
        return "{0}:{1}:{2}".format(mname, per, pervalue)

#global list
labelList = {}

labelList["CPU System Utilization Summary (percentage)"] = {"metrics":
                                                            [{"name":"perf_cpu_system_util:max1h", "header":"Max", "per":"cpu"},
                                                             {"name":"perf_cpu_system_util:min1h", "header":"Min", "per":"cpu"},
                                                             {"name":"perf_cpu_system_util:avg1h", "header":"Avg", "per":"cpu"}],
                                                            "labels":("__name__", "instance", "cpu")}

labelList["CPU User Utilization Summary (percentage)"] = {"metrics":
                                                          [{"name":"perf_cpu_user_util:max1h", "header":"Max", "per":"cpu"},
                                                           {"name":"perf_cpu_user_util:min1h", "header":"Min", "per":"cpu"},
                                                           {"name":"perf_cpu_user_util:avg1h", "header":"Avg", "per":"cpu"}],
                                                          "labels":("__name__", "instance", "cpu")}

labelList["Disk Utilization Summary (percentage)"] = {"metrics":
                                                      [{"name":"perf_cpu_user_util:max1h", "header":"Max", "per":"cpu"},
                                                       {"name":"perf_cpu_user_util:min1h", "header":"Min", "per":"cpu"},
                                                       {"name":"perf_cpu_user_util:avg1h", "header":"Avg", "per":"cpu"}],
                                                      "labels":("__name__", "instance", "cpu")}

labelList["Disk Utilization Summary (percentage)"] = {"metrics":
                                                      [{"name":"perf_disk_util:max1h", "header":"Max", "per":"df"},
                                                       {"name":"perf_disk_util:min1h", "header":"Min", "per":"df"},
                                                       {"name":"perf_disk_util:avg1h", "header":"Avg", "per":"df"}],
                                                      "labels":("__name__", "instance", "df")}

labelList["Disk Write Time (milliseconds)"] = {"metrics":
                                               [{"name":"perf_disk_write:max1h", "header":"Max", "per":"disk"},
                                                {"name":"perf_disk_write:min1h", "header":"Min", "per":"disk"},
                                                {"name":"perf_disk_write:avg1h", "header":"Avg", "per":"disk"}],
                                               "labels":("__name__", "instance", "disk")}

labelList["Disk Read Time (milliseconds)"] = {"metrics":
                                              [{"name":"perf_disk_read:max1h", "header":"Max", "per":"disk"},
                                               {"name":"perf_disk_read:min1h", "header":"Min", "per":"disk"},
                                               {"name":"perf_disk_read:avg1h", "header":"Avg", "per":"disk"}],
                                              "labels":("__name__", "instance", "disk")}

labelList["Memory Utlization Summary (percentage)"] = {"metrics":
                                                       [{"name":"perf_memory_util:max1h", "header":"Max", "per":"memory"},
                                                        {"name":"perf_memory_util:min1h", "header":"Min", "per":"memory"},
                                                        {"name":"perf_memory_util:avg1h", "header":"Avg", "per":"memory"}],
                                                       "labels":("__name__", "instance")}

labelList["Interface Drops (In)"] = {"metrics":
                                     [{"name":"perf_packet_drops_in:max1h", "header":"Max", "per":"interface"},
                                      {"name":"perf_packet_drops_in:min1h", "header":"Min", "per":"interface"},
                                      {"name":"perf_packet_drops_in:avg1h", "header":"Avg", "per":"interface"}],
                                     "labels":("__name__", "instance", "interface")}

labelList["Interface Drops (Out)"] = {"metrics":
                                      [{"name":"perf_packet_drops_out:max1h", "header":"Max", "per":"interface"},
                                       {"name":"perf_packet_drops_out:min1h", "header":"Min", "per":"interface"},
                                       {"name":"perf_packet_drops_out:avg1h", "header":"Avg", "per":"interface"}],
                                      "labels":("__name__", "instance", "interface")}

labelList["Interface Errors (In)"] = {"metrics":
                                      [{"name":"perf_packet_errs_in:max1h", "header":"Max", "per":"interface"},
                                       {"name":"perf_packet_errs_in:min1h", "header":"Min", "per":"interface"},
                                       {"name":"perf_packet_errs_in:avg1h", "header":"Avg", "per":"interface"}],
                                      "labels":("__name__", "instance", "interface")}

labelList["Interface Errors (Out)"] = {"metrics":
                                       [{"name":"perf_packet_errs_out:max1h", "header":"Max", "per":"interface"},
                                        {"name":"perf_packet_errs_out:min1h", "header":"Min", "per":"interface"},
                                        {"name":"perf_packet_errs_out:avg1h", "header":"Avg", "per":"interface"}],
                                       "labels":("__name__", "instance", "interface")}

labelList["Interface Packets (In)"] = {"metrics":
                                       [{"name":"perf_packets_in:max1h", "header":"Max", "per":"interface"},
                                        {"name":"perf_packets_in:min1h", "header":"Min", "per":"interface"},
                                        {"name":"perf_packets_in:avg1h", "header":"Avg", "per":"interface"}],
                                       "labels":("__name__", "instance", "interface")}

labelList["Interface Packets (Out)"] = {"metrics":
                                        [{"name":"perf_packets_out:max1h", "header":"Max", "per":"interface"},
                                         {"name":"perf_packets_out:min1h", "header":"Min", "per":"interface"},
                                         {"name":"perf_packets_out:avg1h", "header":"Avg", "per":"interface"}],
                                        "labels":("__name__", "instance", "interface")}

labelList["System Load"] = {"metrics":
                            [{"name":"perf_system_load:max1h", "header":"Max", "per":None},
                             {"name":"perf_system_load:min1h", "header":"Min", "per":None},
                             {"name":"perf_system_load:avg1h", "header":"Avg", "per":None}],
                            "labels":("__name__", "instance")}

labelList["System Uptime"] = {"metrics":
                              [{"name":"perf_system_uptime:max1h", "header":"Max", "per":None},
                               {"name":"perf_system_uptime:min1h", "header":"Min", "per":None},
                               {"name":"perf_system_uptime:avg1h", "header":"Avg", "per":None}],
                              "labels":("__name__", "instance")}



def generate_report(url,node,metric):
    ##Set up  writer
    writer = csv.writer(sys.stdout)
    filtered_metric={}
    if metric is None:
        filtered_metric=labelList
    else:
        filtered_metric[metric]=labelList[metric]

    for instance in instances:
        #write all header first
        header_row1 = [""]
        header_row1.append("")
        header_row1.append("")
        header_row2 = ["Node"]
        header_row2.append("Start Time")
        header_row2.append("End time")
        SanitizedResult = defaultdict(list)
        SanitizedResult = {"node":instance, "starttime":"", "endtime":"", "results":{}}
        writeNewRow = True

        for mname, mvalue in filtered_metric.iteritems():
            if mname not in SanitizedResult["results"]:
                SanitizedResult["results"][mname] = {"Max":[], "Min":[],
                                                     "Avg":[], "Per":mvalue["metrics"][0]["per"]}
            for data in mvalue["metrics"]:
                response = requests.get(options.prom_host+'/api/v1/query?query='+data["name"]+'{instance="'+instance+'"}')
                results = response.json()['data']["result"]
                for result in results:
                    #if result['metric'].get(data["per"],'')=="":
                    #    print result['metric']
                    SanitizedResult["starttime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0]-3600))
                    SanitizedResult["endtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0]))
                    SanitizedResult["results"][mname].get(data["header"], '').append({"value":result['value'][1],
                                                                                  "per":data["per"], "per_value":result['metric'].get(data["per"], '')})
            if writeNewRow is True:
                data_row = [SanitizedResult["node"]]
                data_row.append(SanitizedResult["starttime"])
                data_row.append(SanitizedResult["endtime"])
                writeNewRow = False
        #Print before goign to next instance
        for key, value in SanitizedResult["results"].iteritems():
            for index, item in enumerate(value["Max"]):
                header_row2.append("Max")
                header_row2.append("Avg")
                header_row2.append("Min")
                try:
                    data_row.append(value["Max"][index]["value"])
                    header_row1.append(get_report_header(key, value["Max"][0]["per"], value["Max"][index]["per_value"]))
                except IndexError:
                    data_row.append(-1)
                    header_row1.append(key + "_for_ error")
                try:
                    data_row.append(value["Avg"][index]["value"])
                    header_row1.append(get_report_header(key, value["Avg"][0]["per"], value["Avg"][index]["per_value"]))
                except IndexError:
                    data_row.append(-1)
                    header_row1.append(key + "_for_ error")
                try:
                    data_row.append(value["Min"][index]["value"])
                    header_row1.append(get_report_header(key, value["Min"][0]["per"], value["Min"][index]["per_value"]))
                except IndexError:
                    data_row.append(-1)
                    header_row1.append(key + "_for_ error")
        writer.writerow(header_row1)
        writer.writerow(header_row2)
        writer.writerow(data_row)

if __name__ == '__main__':
    #Main Header
    parser = OptionParser()
    instances = set()
    parser.add_option("-n", "--nodes", action='store_true', help="list all nodes used for the report.")
    parser.add_option("-l", "--list", action='store_true', help="list all metrics name.")
    parser.add_option("-m", "--mfilter", dest="mfilter", help="Filter metrics by name.")
    parser.add_option("-s", "--nfilter", dest="nfilter", help="Filter metrics by node.")
    parser.add_option("-p", "--prometheus", dest="prom_host", help="http://promethues:9090")

    (options, args) = parser.parse_args()

    #Check if list was selected
    if options.list is not None:
        print("**********************************************")
        print("*  List of recording rules metrics            *")
        print("**********************************************")
        for mname, mvalue in labelList.iteritems():
            print(mname)
        sys.exit(1)

    if options.nodes is not None:
        if options.prom_host is None:
            options.prom_host = raw_input('Enter Prometheus servet (http://promserver:9090):')
        instances = get_instance_names(options.prom_host)
        print("**********************************************")
        print("*  List of nodes                             *")
        print("**********************************************")
        for instance in instances:
            print(instance)
        sys.exit(1)

    #Check if filter was passed

    if options.mfilter is not None:
        if options.mfilter not in labelList:
            print("Error: Cannot filter Metrics[ {0} ]not found in the list".format(options.mfilter))
            sys.exit(1)


    if options.prom_host is None:
        options.prom_host = raw_input('Enter Prometheus serve (http://promserver:9090):')

    instances = get_instance_names(options.prom_host)
    #Check if filter was passed
    if options.nfilter is not None:
        if options.nfilter not in instances:
            print("Error: Cannot filter Nodes [ {0} ]not found in the list".format(options.nfilter))
            sys.exit(1)
        else:
            instances = [options.nfilter]

    generate_report(options.prom_host,instances,options.mfilter)
