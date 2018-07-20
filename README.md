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


FOR REPOTS
CPU usage 

avg_over_time(collectd_cpu_percent{service="user",instance="pod3-server5.practice.redhat.com"}[1h])
avg without(cpu,job)(avg_over_time(collectd_cpu_percent{service="user"}[1h]))  


avg without(cpu,job)(avg_over_time(collectd_cpu_percent{service="system"}[1h]))  

max without(cpu,job)(max_over_time(collectd_cpu_percent{service="system"}[1h]))  
min without(cpu,job)(min_over_time(collectd_cpu_percent{service="system"}[1h]))  

