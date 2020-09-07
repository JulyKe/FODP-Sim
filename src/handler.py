from estimate import Estimate
from disk import Disk
import operator as op
from heapq import *
#-----------------------------------------
# Handler is to process different events
#------------------------------------------
class Handler:
    def __init__(self, sys, events_queue, rebuild, copyback, network, servers, groups, disks):
        self.sys = sys
        #------------------------
        self.servers = servers
        self.groups = groups
        self.disks = disks
        #------------------------
        self.events_queue = events_queue 
        self.copyback = copyback
        self.network = network
        #------------------------
        self.estimate = Estimate(sys, events_queue, rebuild, network, disks)
        #------------------------




    def handle_disk_failure_event(self, deviceset, curr_time):
        for diskId in deviceset:
            #--------------------------------------------------------------------------------------
            if self.sys.bottom_type == 0:
            #--------------------------------------------------------------------------------------
                if diskId not in self.sys.RAID_stripeset_per_disk:
                    print "  -> RAID spare drive failure <-  ", diskId
                    self.copyback.start_replace(diskId, self.events_queue, curr_time)
                    continue
            #--------------------------------------------------------------------------------------
            if self.sys.bottom_type == 0 or self.sys.bottom_type == 1 or self.sys.bottom_type == 2:
            #--------------------------------------------------------------------------------------
                serverId = diskId / self.sys.num_disks_per_server
                if self.servers[serverId].avail_spares > 0:
                    self.servers[serverId].avail_spares -= 1
                    if self.sys.bottom_type == 0:
                        self.estimate.estimate_RAID_time(diskId, serverId, curr_time)
                    if self.sys.bottom_type == 1:
                        self.estimate.estimate_decluster_time(diskId, serverId, curr_time)
                    if self.sys.bottom_type == 2:
                        self.estimate.estimate_FODP_time(diskId, serverId, curr_time)
                else:
                    heappush(self.servers[serverId].wait_queue, (curr_time, Disk.EVENT_FAIL, diskId))
                    print "   >>> it's not enough, add", diskId, "to the server", serverId," wait repair queue"
            #--------------------------------------------------------------------------------------
            if self.sys.bottom_type == 3 or self.sys.bottom_type == 4:
            #--------------------------------------------------------------------------------------
                groupId = self.sys.group_per_disk[diskId]
                if self.groups[groupId].avail_spares > 0:
                    self.groups[groupId].avail_spares -= 1
                    if self.sys.bottom_type == 3:
                        self.estimate.estimate_copyset_time(diskId, groupId, curr_time)
                    if self.sys.bottom_type == 4:
                        self.estimate.estimate_group_time(diskId, groupId, curr_time)
                else:
                    heappush(self.groups[groupId].wait_queue, (curr_time, Disk.EVENT_FAIL, diskId))
                    print "   >>> it's not enough, add", diskId, "to the group", groupId," wait repair queue"



    def handle_disk_critical_rebuild_event(self, deviceset, curr_time):
        print "-"



    def handle_disk_degraded_rebuild_event(self, deviceset, curr_time):
        for diskId in deviceset:
            if self.sys.bottom_type == 0:
                self.copyback.start_replace(diskId, self.events_queue, curr_time)
            if self.sys.bottom_type == 1 or self.sys.bottom_type == 2 or self.sys.bottom_type == 3 or self.sys.bottom_type == 4:
                self.copyback.start_copyback(diskId, self.events_queue, curr_time)


    def handle_disk_copyback_event(self, deviceset):
        for diskId in deviceset:
            #--------------------------------------------------------------------------------------
            if self.sys.bottom_type == 0 or self.sys.bottom_type == 1 or self.sys.bottom_type == 2:
            #--------------------------------------------------------------------------------------
                serverId = diskId / self.sys.num_disks_per_server
                self.servers[serverId].avail_spares += 1
                print "   @server", serverId, " - current spare spaces - ", self.servers[serverId].avail_spares
            #-----------------------------------------------------------
            if self.sys.bottom_type == 3 or self.sys.bottom_type == 4:
            #-----------------------------------------------------------
                groupId = self.sys.group_per_disk[diskId]
                self.groups[groupId].avail_spares += 1
                print "   @group", groupId, " - current spare spaces - ", self.groups[groupId].avail_spares


    def handle_network_failure_event(self, deviceset, curr_time):
        print ""



    def handle_network_repair_event(self, deviceset, curr_time):
        #--------------------------------------------------------------------------------------
        if self.sys.bottom_type == 0 or  self.sys.bottom_type == 1 or self.sys.bottom_type == 2:
        #--------------------------------------------------------------------------------------
            for (interId, intraId, diskId) in deviceset:
                print "update avail bw & network repairs(", interId, intraId, diskId, ")", self.network.repairs[(interId, intraId, diskId)]
                if self.sys.top_type == 0 or self.sys.top_type == 2:
                    serverId = diskId / self.sys.num_disks_per_server
                    if self.sys.bw_share[(interId, intraId, serverId)] > 1:
                        self.sys.bw_share[(interId, intraId, serverId)] -= 1
                    else:
                        del self.sys.bw_share[(interId, intraId, serverId)]
                        #------------------------------------------------------------------------------
                        for helpId in self.network.repairs[(interId, intraId, diskId)]['helps']:
                            self.servers[helpId].share -= 1
                            print "   ++++  ", helpId, " - share - ", self.servers[helpId].share
                    print " delete network repair - ", interId, intraId, diskId
                    del self.network.repairs[(interId, intraId, diskId)]
        #--------------------------------------------------------------------------------------
        if self.sys.bottom_type == 3 or self.sys.bottom_type == 4:
        #--------------------------------------------------------------------------------------
            for (groupId, intraId, diskId) in deviceset:
                print "update avail bw & network repairs(", groupId, intraId, diskId, ")", self.network.repairs[(groupId, intraId, diskId)]
                serverId = diskId / self.sys.num_disks_per_server
                if self.sys.bw_share[(groupId, intraId, serverId)] > 1:
                    self.sys.bw_share[(groupId, intraId, serverId)] -= 1
                else:
                    del self.sys.bw_share[(groupId, intraId, serverId)]
                    #------------------------------------------------------------------------------
                    for helpId in self.network.repairs[(groupId, intraId, diskId)]['helps']:
                        self.servers[helpId].share -= 1
                        print "   ++++  ", helpId, " - share - ", self.servers[helpId].share
                print " delete network repair - ", groupId, intraId , diskId
                del self.network.repairs[(groupId, intraId,  diskId)]
                #------------------------------------------------------------------------------
                if self.disks[diskId].global_done is True and self.disks[diskId].state == Disk.STATE_NORMAL:
                    self.copyback.start_copyback(diskId, self.events_queue, curr_time)




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

    def get_failed_disks_per_group(self, groupId):
        fail_per_group = []
        for diskId in self.sys.flat_group_layout[groupId]:
            if self.disks[diskId].state == Disk.STATE_FAILED:
                fail_per_group.append(diskId)
        return fail_per_group
