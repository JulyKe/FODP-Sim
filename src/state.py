from handler import Handler
from server import Server
from group import Group
from disk import Disk
from heapq import *

class State:
    def __init__(self, sys, rebuild, copyback, network, events_queue):
        self.sys = sys
        #----------------------------------
        self.disks = {}
        for diskId in range(sys.num_disks):
            self.disks[diskId] = Disk(diskId, sys.repair_data)
        #----------------------------------
        self.servers = {}
        for serverId in range(sys.num_servers):
            self.servers[serverId] = Server(serverId, sys.num_spares_per_server, network.networkBW)
        #----------------------------------
        self.groups = {}
        if self.sys.bottom_type == 4:
            for groupId in range(sys.num_groups):
                self.groups[groupId] = Group(groupId, self.sys.flat_group_layout[groupId], sys.num_spares_per_group, network.networkBW)
        if self.sys.bottom_type == 3:
            for groupId in range(sys.num_groups):
                self.groups[groupId] = Group(groupId, self.sys.disks_per_server[groupId], sys.num_spares_per_group, network.networkBW)
        #----------------------------------
        self.sys.local_repair = 0.0
        self.sys.global_repair = 0.0
        self.handler = Handler(sys, events_queue, rebuild, copyback, network, self.servers, self.groups, self.disks)
        #----------------------------------
        rebuild.disks = self.disks
        rebuild.servers = self.servers
        #----------------------------------
        copyback.disks = self.disks
        #----------------------------------
        network.disks = self.disks
        network.servers = self.servers
        #----------------------------------
        self.MTTDL = dict()



    def update_clock(self, event_type, curr_time):
        self.curr_time = curr_time



    def update_state(self, event_type, deviceset):
        #----------------------------------------------
        if event_type == Server.EVENT_FAIL:
        #----------------------------------------------
            for serverId in deviceset:
                for diskId in self.sys.disks_per_server[serverId]:
                    self.disks[diskId].state = Disk.STATE_FAILED
        #----------------------------------------------
        if event_type == Server.EVENT_REPAIR:
        #----------------------------------------------
            for (interId, intraId, diskId) in deviceset:
                del self.disks[diskId].inter_intra_per_disk[(interId, intraId)] 
                if len(self.disks[diskId].inter_intra_per_disk) == 0:
                    self.disks[diskId].global_done = True
                if self.disks[diskId].local_done and self.disks[diskId].global_done:
                    self.disks[diskId].state = Disk.STATE_NORMAL
        #----------------------------------------------
        if event_type == Disk.EVENT_FAIL:
        #----------------------------------------------
            for diskId in deviceset:
                self.disks[diskId].state = Disk.STATE_FAILED
        #----------------------------------------------
        if event_type == Disk.EVENT_DEGRADEDREBUILD:
        #----------------------------------------------
            for diskId in deviceset:
                self.disks[diskId].local_done = True
                if self.disks[diskId].local_done and self.disks[diskId].global_done:
		    if diskId in self.MTTDL:
        		if self.sys.top_type == 1 and self.sys.bottom_type == 1:
			    unrecoverables = self.MTTDL[diskId]['failures']
			    for failId in unrecoverables:
			        self.disks[failId].state = Disk.STATE_FAILED
		    else:
                    	self.disks[diskId].state = Disk.STATE_NORMAL
        #----------------------------------------------
        if event_type == Disk.EVENT_CRITICALREBUILD:
        #----------------------------------------------
            print "critical rebuild"




    def update_event(self, event_type, deviceset):
        if event_type == Server.EVENT_FAIL:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Network Failure Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_network_failure_event(deviceset, self.curr_time)

        if event_type == Server.EVENT_REPAIR:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Network Repair Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_network_repair_event(deviceset, self.curr_time)

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

        if event_type == Disk.EVENT_CRITICALREBUILD:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Critical Rebuild Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_disk_critical_rebuild_event(deviceset, self.curr_time)
            
        if event_type == Disk.EVENT_COPYBACK:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            print " Handle Disk Copyback Event ", deviceset
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            self.handler.handle_disk_copyback_event(deviceset)

