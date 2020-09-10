from handler import Handler
from server import Server
from disk import Disk
from heapq import *

class State:
    def __init__(self, sys, rebuild, copyback, events_queue):
        #----------------------------------
        self.sys = sys
        #----------------------------------
        self.disks = {}
        for diskId in range(sys.num_disks):
            self.disks[diskId] = Disk(diskId, sys.repair_data)
        #----------------------------------
        self.servers = {}
        for serverId in range(sys.num_servers):
            self.servers[serverId] = Server(serverId, sys.num_spares_per_server)
        #----------------------------------
        self.handler = Handler(sys, events_queue, rebuild, copyback, self.servers, self.disks)
        #----------------------------------
        rebuild.disks = self.disks
        rebuild.servers = self.servers
        copyback.disks = self.disks
        #----------------------------------
        self.MTTDL = dict()



    def update_clock(self, event_type, curr_time):
        self.curr_time = curr_time



    def update_state(self, event_type, deviceset):
        #----------------------------------------------
        if event_type == Disk.EVENT_FAIL:
        #----------------------------------------------
            for diskId in deviceset:
                self.disks[diskId].state = Disk.STATE_FAILED
        #----------------------------------------------
        if event_type == Disk.EVENT_DEGRADEDREBUILD:
        #----------------------------------------------
            for diskId in deviceset:
		if diskId in self.MTTDL:
		    if self.sys.dp_type == 1:
			unrecoverables = self.MTTDL[diskId]['failures']
			for failId in unrecoverables:
			    self.disks[failId].state = Disk.STATE_FAILED
	    	else:
		    self.disks[diskId].state = Disk.STATE_NORMAL




    def update_event(self, event_type, deviceset):
        if event_type == Disk.EVENT_FAIL:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Disk Failure Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_disk_failure_event(deviceset, self.curr_time)

        if event_type == Disk.EVENT_DEGRADEDREBUILD:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Degraded Rebuild Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_disk_degraded_rebuild_event(deviceset, self.curr_time)

        if event_type == Disk.EVENT_COPYBACK:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Disk Copyback Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_disk_copyback_event(deviceset)

