#! /usr/bin/env python
"""
aputtur@redhat.com
Prometheus report
"""
from __future__ import print_function
import argparse
import csv
import sys
import time
from collections import defaultdict
import requests


"""
Get Metrics Name.
"""
def get_meterics_names(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    results = response.json()['data']
    #Return metrix
    return results

"""
Get Instance Names.
"""
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
"""
Get Report Header.
"""
def get_report_header(mname, per, pervalue):
    if per is None:
        return mname
    else:
        return "{0}:{1}:{2}".format(mname, per, pervalue)

#global list
PROM_METRICS_LIST = {}

PROM_METRICS_LIST["CPU System Utilization Summary (percentage)"] = {"metrics":
                                                                    [{"name":"perf_cpu_system_util:max1h", "header":"Max", "per":"cpu"},
                                                                     {"name":"perf_cpu_system_util:min1h", "header":"Min", "per":"cpu"},
                                                                     {"name":"perf_cpu_system_util:avg1h", "header":"Avg", "per":"cpu"}],
                                                                    "labels":("__name__", "instance", "cpu")}

PROM_METRICS_LIST["CPU User Utilization Summary (percentage)"] = {"metrics":
                                                                  [{"name":"perf_cpu_user_util:max1h", "header":"Max", "per":"cpu"},
                                                                   {"name":"perf_cpu_user_util:min1h", "header":"Min", "per":"cpu"},
                                                                   {"name":"perf_cpu_user_util:avg1h", "header":"Avg", "per":"cpu"}],
                                                                  "labels":("__name__", "instance", "cpu")}

PROM_METRICS_LIST["Disk Utilization Summary (percentage)"] = {"metrics":
                                                              [{"name":"perf_disk_util:max1h", "header":"Max", "per":"df"},
                                                               {"name":"perf_disk_util:min1h", "header":"Min", "per":"df"},
                                                               {"name":"perf_disk_util:avg1h", "header":"Avg", "per":"df"}],
                                                              "labels":("__name__", "instance", "df")}

PROM_METRICS_LIST["Disk Write Time (milliseconds)"] = {"metrics":
                                                       [{"name":"perf_disk_write:max1h", "header":"Max", "per":"disk"},
                                                        {"name":"perf_disk_write:min1h", "header":"Min", "per":"disk"},
                                                        {"name":"perf_disk_write:avg1h", "header":"Avg", "per":"disk"}],
                                                       "labels":("__name__", "instance", "disk")}

PROM_METRICS_LIST["Disk Read Time (milliseconds)"] = {"metrics":
                                                      [{"name":"perf_disk_read:max1h", "header":"Max", "per":"disk"},
                                                       {"name":"perf_disk_read:min1h", "header":"Min", "per":"disk"},
                                                       {"name":"perf_disk_read:avg1h", "header":"Avg", "per":"disk"}],
                                                      "labels":("__name__", "instance", "disk")}

PROM_METRICS_LIST["Memory Utlization Summary (percentage)"] = {"metrics":
                                                               [{"name":"perf_memory_util:max1h", "header":"Max", "per":"memory"},
                                                                {"name":"perf_memory_util:min1h", "header":"Min", "per":"memory"},
                                                                {"name":"perf_memory_util:avg1h", "header":"Avg", "per":"memory"}],
                                                               "labels":("__name__", "instance")}

PROM_METRICS_LIST["Interface Drops (In)"] = {"metrics":
                                             [{"name":"perf_packet_drops_in:max1h", "header":"Max", "per":"interface"},
                                              {"name":"perf_packet_drops_in:min1h", "header":"Min", "per":"interface"},
                                              {"name":"perf_packet_drops_in:avg1h", "header":"Avg", "per":"interface"}],
                                             "labels":("__name__", "instance", "interface")}

PROM_METRICS_LIST["Interface Drops (Out)"] = {"metrics":
                                              [{"name":"perf_packet_drops_out:max1h", "header":"Max", "per":"interface"},
                                               {"name":"perf_packet_drops_out:min1h", "header":"Min", "per":"interface"},
                                               {"name":"perf_packet_drops_out:avg1h", "header":"Avg", "per":"interface"}],
                                              "labels":("__name__", "instance", "interface")}

PROM_METRICS_LIST["Interface Errors (In)"] = {"metrics":
                                              [{"name":"perf_packet_errs_in:max1h", "header":"Max", "per":"interface"},
                                               {"name":"perf_packet_errs_in:min1h", "header":"Min", "per":"interface"},
                                               {"name":"perf_packet_errs_in:avg1h", "header":"Avg", "per":"interface"}],
                                              "labels":("__name__", "instance", "interface")}

PROM_METRICS_LIST["Interface Errors (Out)"] = {"metrics":
                                               [{"name":"perf_packet_errs_out:max1h", "header":"Max", "per":"interface"},
                                                {"name":"perf_packet_errs_out:min1h", "header":"Min", "per":"interface"},
                                                {"name":"perf_packet_errs_out:avg1h", "header":"Avg", "per":"interface"}],
                                               "labels":("__name__", "instance", "interface")}

PROM_METRICS_LIST["Interface Packets (In)"] = {"metrics":
                                               [{"name":"perf_packets_in:max1h", "header":"Max", "per":"interface"},
                                                {"name":"perf_packets_in:min1h", "header":"Min", "per":"interface"},
                                                {"name":"perf_packets_in:avg1h", "header":"Avg", "per":"interface"}],
                                               "labels":("__name__", "instance", "interface")}

PROM_METRICS_LIST["Interface Packets (Out)"] = {"metrics":
                                                [{"name":"perf_packets_out:max1h", "header":"Max", "per":"interface"},
                                                 {"name":"perf_packets_out:min1h", "header":"Min", "per":"interface"},
                                                 {"name":"perf_packets_out:avg1h", "header":"Avg", "per":"interface"}],
                                                "labels":("__name__", "instance", "interface")}

PROM_METRICS_LIST["System Load"] = {"metrics":
                                    [{"name":"perf_system_load:max1h", "header":"Max", "per":None},
                                     {"name":"perf_system_load:min1h", "header":"Min", "per":None},
                                     {"name":"perf_system_load:avg1h", "header":"Avg", "per":None}],
                                    "labels":("__name__", "instance")}

PROM_METRICS_LIST["System Uptime"] = {"metrics":
                                      [{"name":"perf_system_uptime:max1h", "header":"Max", "per":None},
                                       {"name":"perf_system_uptime:min1h", "header":"Min", "per":None},
                                       {"name":"perf_system_uptime:avg1h", "header":"Avg", "per":None}],
                                      "labels":("__name__", "instance")}

"""
Generate Report.
"""
def generate_report(url, nodes, metric):
    ##Set up  writer
    writer = csv.writer(sys.stdout)
    filtered_metric = {}
    if metric is None:
        filtered_metric = PROM_METRICS_LIST
    else:
        filtered_metric[metric] = PROM_METRICS_LIST[metric]

    for node in nodes:
        #write all header first
        header_row1 = [""]
        header_row1.append("")
        header_row1.append("")
        header_row2 = ["Node"]
        header_row2.append("Start Time")
        header_row2.append("End time")
        prom_perf_report = defaultdict(list)
        prom_perf_report = {"node":node, "starttime":"", "endtime":"", "results":{}}
        write_new_row = True
        for mname, mvalue in filtered_metric.items():
            if mname not in prom_perf_report["results"]:
                prom_perf_report["results"][mname] = {"Max":[], "Min":[],
                                                      "Avg":[], "Per":mvalue["metrics"][0]["per"]}
            for data in mvalue["metrics"]:
                response = requests.get(url+'/api/v1/query?query='+data["name"]+'{instance="'+node+'"}')
                results = response.json()['data']["result"]
                for result in results:
                    #if result['metric'].get(data["per"],'')=="":
                    #    print result['metric']
                    prom_perf_report["starttime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0]-3600))
                    prom_perf_report["endtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['value'][0]))
                    prom_perf_report["results"][mname].get(data["header"], '').append({"value":result['value'][1], "per":data["per"],
                                                                                       "per_value":result['metric'].get(data["per"], '')})
            if write_new_row is True:
                data_row = [prom_perf_report["node"]]
                data_row.append(prom_perf_report["starttime"])
                data_row.append(prom_perf_report["endtime"])
                write_new_row = False
        #Print before goign to next node
        for key, value in prom_perf_report["results"].items():
            for max_value, min_value, avg_value in zip(value["Max"], value["Min"], value["Avg"]):
                #print('Max: {}, Min: {}, Avg: {}'.format(max, min, avg))
                header_row2.append("Max")
                data_row.append(max_value["value"])
                header_row1.append(get_report_header(key, max_value["per"], max_value["per_value"]))

                header_row2.append("Min")
                data_row.append(min_value["value"])
                header_row1.append(get_report_header(key, min_value["per"], min_value["per_value"]))

                header_row2.append("Avg")
                data_row.append(avg_value["value"])
                header_row1.append(get_report_header(key, avg_value["per"], avg_value["per_value"]))

        writer.writerow(header_row1)
        writer.writerow(header_row2)
        writer.writerow(data_row)
"""
Parse Command Line arguments and process reports.
"""
def parser_commandline():
    instances = set()
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nodes', action="store_true", help="List nodes available")
    parser.add_argument('-l', '--list', action="store_true", help="List metrics available")
    parser.add_argument('-m', '--mfilter', help="Filter metrics by name", default=None)
    parser.add_argument('-s', '--nfilter', help="Filter metrics by server", default=None)
    parser.add_argument("-p", "--prometheus", dest="prom_host", help="http://promethues:9090")
    #parser.print_help()
    args = parser.parse_args()

    #Check if list was selected
    if args.list:
        print("**********************************************")
        print("*  List of recording rules metrics            *")
        print("**********************************************")
        for metric_name, _ in PROM_METRICS_LIST.items():
            print(metric_name)
        sys.exit(1)

    if args.nodes:
        if args.prom_host is None:
            args.prom_host = raw_input('Enter Prometheus server (http://promserver:9090):')
        instances = get_instance_names(args.prom_host)
        print("**********************************************")
        print("*  List of nodes                             *")
        print("**********************************************")
        for instance in instances:
            print(instance)
        sys.exit(1)

    #Check if filter was passed
    if args.mfilter is not None:
        if args.mfilter not in PROM_METRICS_LIST:
            print("Error: Cannot filter Metrics[ {0} ]not found in the list".format(args.mfilter))
            sys.exit(1)


    if args.prom_host is None:
        args.prom_host = raw_input('Enter Prometheus serve (http://promserver:9090):')

    instances = get_instance_names(args.prom_host)
    #Check if filter was passed
    if args.nfilter is not None:
        if args.nfilter not in instances:
            print("Error: Cannot filter Nodes [ {0} ]not found in the list".format(args.nfilter))
            sys.exit(1)
        else:
            instances = [args.nfilter]

    generate_report(args.prom_host, instances, args.mfilter)

"""
Entry point.
"""
if __name__ == '__main__':
    #Main Header
    parser_commandline()
