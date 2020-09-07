from disk import Disk
import operator as op
from heapq import *
class Estimate:
    def __init__(self, sys, events_queue, rebuild, network, disks):
        self.sys = sys
        self.events_queue = events_queue 
        #--------------------------------
        self.rebuild = rebuild
        self.network = network
        #--------------------------------
        self.disks = disks


    def estimate_group_time(self, diskId, groupId, curr_time):
        self.disks[diskId].global_done = False
        self.network.estimate_group_time(diskId, groupId)
        self.network.generate_repair_event(diskId, curr_time, self.events_queue)

    def estimate_copyset_time(self, diskId, groupId, curr_time):
        self.disks[diskId].global_done = False
        self.network.estimate_copyset_time(diskId, groupId)
        self.network.generate_repair_event(diskId, curr_time, self.events_queue)


    def estimate_RAID_time(self, diskId, serverId, curr_time):
        intraset = self.sys.RAID_stripeset_per_disk[diskId]
        failures_per_set = self.get_failed_disks_per_stripeset(intraset)
        if self.sys.add_tier:
            if len(failures_per_set) > self.sys.mb:
                self.disks[diskId].global_done = False
                self.sys.global_repair += 1
                self.network.estimate_RAID_time(diskId, serverId)
                self.network.generate_repair_event(diskId, curr_time, self.events_queue)
            else:
                self.disks[diskId].local_done = False
                self.sys.local_repair += 1
                self.rebuild.estimate_RAID_time(diskId)
                self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)
        else:
            self.disks[diskId].local_done = False
            self.rebuild.estimate_RAID_time(diskId)
            self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)



    def estimate_decluster_time(self, diskId, serverId, curr_time):
        failures_per_server = len(self.get_failed_disks_per_server(serverId))
        normals_per_server = self.sys.num_disks_per_server - failures_per_server
        if self.sys.add_tier:
            #--------------------------------------------------------------------
            total_sets = self.ncr(self.sys.num_disks_per_server - 1, self.sys.kb + self.sys.mb - 1)
            if failures_per_server > self.sys.mb:
                global_sets = 0
                for num_failures  in range(self.sys.mb+1, min(failures_per_server+1, self.sys.kb+self.sys.mb+1)):
                    global_sets += self.ncr(normals_per_server, self.sys.kb+self.sys.mb-num_failures) * self.ncr(failures_per_server - 1, num_failures - 1)
                self.disks[diskId].DP_percent['global'] = float(global_sets) / total_sets
            #--------------------------------------------------------------------
            local_sets = 0 
            for num_failures  in range(1, min(failures_per_server+1, self.sys.mb+1)):
                local_sets += self.ncr(normals_per_server, self.sys.kb+self.sys.mb-num_failures) * self.ncr(failures_per_server - 1, num_failures - 1)
            self.disks[diskId].DP_percent['local'] = float(local_sets) / total_sets
            #--------------------------------------------------------------------
            print "  >> decluster percent >>  ", self.disks[diskId].DP_percent
            #--------------------------------------------------------------------
            if self.disks[diskId].DP_percent['local'] > 0:
                self.disks[diskId].local_done = False
                self.sys.local_repair += self.disks[diskId].DP_percent['local']
                self.rebuild.estimate_decluster_time(diskId, self.disks[diskId].DP_percent['local'], normals_per_server)
                self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)
            #--------------------------------------------------------------------
            if self.disks[diskId].DP_percent['global'] > 0:
                self.disks[diskId].global_done = False
                self.sys.global_repair += self.disks[diskId].DP_percent['global']
                self.network.estimate_decluster_time(diskId, serverId, self.disks[diskId].DP_percent['global'], failures_per_server)
                self.network.generate_repair_event(diskId, curr_time, self.events_queue)
        else:
            self.disks[diskId].local_done = False
            self.rebuild.estimate_decluster_time(diskId, 1.0, normals_per_server)
            self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)



    def estimate_FODP_time(self, diskId, serverId, curr_time):
        if self.sys.add_tier:
            for stripeset in self.sys.FODP_stripesets_per_disk[diskId]:
                if len(self.get_failed_disks_per_stripeset(stripeset)) > self.sys.mb:
                    self.disks[diskId].FODP_percent['global'].append(stripeset) 
                else:
                    self.disks[diskId].FODP_percent['local'] += 1
            print "\n ----- >>> FODP percent >>> -----", self.disks[diskId].FODP_percent,"\n"
            #--------------------------------------------------------------
            local_sets_per_disk = self.disks[diskId].FODP_percent['local']
            if local_sets_per_disk > 0:
                self.disks[diskId].local_done = False
                self.sys.local_repair += local_sets_per_disk/float(self.sys.fb)
                self.rebuild.estimate_FODP_time(diskId, local_sets_per_disk)
                self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)
            #--------------------------------------------------------------
            global_sets_per_disk = len(self.disks[diskId].FODP_percent['global'])
            if global_sets_per_disk > 0:
                self.disks[diskId].global_done = False
                self.sys.global_repair += global_sets_per_disk/float(self.sys.fb)
                self.network.estimate_FODP_time(diskId, serverId)
                self.network.generate_repair_event(diskId, curr_time, self.events_queue)
        else:
            self.disks[diskId].local_done = False
            self.rebuild.estimate_FODP_time(diskId, self.sys.fb)
            self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)



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


    def ncr(self, n, r):
        r = min(r, n-r)
        numer = reduce(op.mul, range(n, n-r, -1), 1)
        denom = reduce(op.mul, range(1, r+1), 1)
        return numer / denom
