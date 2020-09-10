from estimate import Estimate
from disk import Disk
import operator as op
from heapq import *
#-----------------------------------------
# Handler is to process different events
#------------------------------------------
class Handler:
    def __init__(self, sys, events_queue, rebuild, copyback, servers, disks):
        self.sys = sys
        #------------------------
        self.servers = servers
        self.disks = disks
        #------------------------
        self.events_queue = events_queue 
        self.copyback = copyback
        #------------------------
        self.estimate = Estimate(sys, events_queue, rebuild, disks)
        #------------------------




    def handle_disk_failure_event(self, deviceset, curr_time):
        for diskId in deviceset:
            #--------------------------------------------------------------------------------------
            if self.sys.dp_type == 0:
            #--------------------------------------------------------------------------------------
                if diskId not in self.sys.RAID_stripeset_per_disk:
                    print "  -> RAID spare drive failure <-  ", diskId
                    self.copyback.start_replace(diskId, self.events_queue, curr_time)
                    continue
            #--------------------------------------------------------------------------------------
	    serverId = diskId / self.sys.num_disks_per_server
            #--------------------------------------------------------------------------------------
	    if self.servers[serverId].avail_spares > 0:
	    	self.servers[serverId].avail_spares -= 1
	    	if self.sys.dp_type == 0:
		    self.estimate.estimate_RAID_time(diskId, curr_time)
	    	if self.sys.dp_type == 1:
		    self.estimate.estimate_decluster_time(diskId, serverId, curr_time)
	    	if self.sys.dp_type == 2:
		    self.estimate.estimate_FODP_time(diskId, curr_time)
	    else:
	        heappush(self.servers[serverId].wait_queue, (curr_time, Disk.EVENT_FAIL, diskId))
	        print "   >>> it's not enough, add", diskId, "to the server", serverId," wait repair queue"



    def handle_disk_degraded_rebuild_event(self, deviceset, curr_time):
        for diskId in deviceset:
	    if self.sys.dp_type == 0:
                self.copyback.start_replace(diskId, self.events_queue, curr_time)
	    if self.sys.dp_type == 1 or self.sys.dp_type == 2:
                self.copyback.start_copyback(diskId, self.events_queue, curr_time)




    def handle_disk_copyback_event(self, deviceset):
        for diskId in deviceset:
	    serverId = diskId / self.sys.num_disks_per_server
            self.servers[serverId].avail_spares += 1
	    print "   @server", serverId, " - current spare spaces - ", self.servers[serverId].avail_spares




    def get_failed_disks_per_stripeset(self, stripeset):
        fail_per_stripeset = []
        for diskId in stripeset:
            if self.disks[diskId].state == Disk.STATE_FAILED:
                fail_per_stripeset.append(diskId)
        return fail_per_stripeset




    def get_failed_disks_per_server(self, serverId):
        fail_per_server = []
        for diskId in self.sys.disks_per_server[serverId]:
            if self.disks[diskId].state == Disk.STATE_FAILED:
                fail_per_server.append(diskId)
        return fail_per_server
