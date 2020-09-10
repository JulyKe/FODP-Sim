from disk import Disk
import operator as op
from heapq import *

class Estimate:
    def __init__(self, sys, events_queue, rebuild, disks):
        self.sys = sys
        self.disks = disks
        self.rebuild = rebuild
        self.events_queue = events_queue 


    def estimate_RAID_time(self, diskId, curr_time):
        self.rebuild.estimate_RAID_time(diskId)
        self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)



    def estimate_decluster_time(self, diskId, serverId, curr_time):
        failures_per_server = len(self.get_failed_disks_per_server(serverId))
        normals_per_server = self.sys.num_disks_per_server - failures_per_server
        self.rebuild.estimate_decluster_time(diskId, normals_per_server)
        self.rebuild.generate_repair_event(diskId, curr_time, self.events_queue)


    def estimate_FODP_time(self, diskId, curr_time):
    	self.rebuild.estimate_FODP_time(diskId)
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
