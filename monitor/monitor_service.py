import psutil as p

# since boot

p.cpu_stats()
p.disk_io_counters()
p.virtual_memory()

p.cpu_times_percent()

p.disk_usage("/")
# average load in 5, 10, 15 minutes load
p.get_loadavg()
# network i/o counters
psutil.net_io_counters()