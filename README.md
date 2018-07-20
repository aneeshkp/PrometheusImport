# PrometheusImport

#use full aggregators 
 100 * (1 - avg by(instance)(irate(collectd_cpu_percent[1h])))

How many same metric name 
sort_desc(count by(__name__)({__name__=~".+"}))
sort_desc(count by(__name__,instance)({__name__=~".+"}))


How many cpu per node 
count without(cpu)(count without (job,service)(collectd_cpu_percent))
count without(cpu)(count without (service)(collectd_cpu_percent))


#Counts values 
count_values without(instance)("value", collectd_cpu_percent)
