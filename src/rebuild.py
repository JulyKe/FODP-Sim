from state import State
from disk import Disk
from heapq import *

class Rebuild:
    def __init__(self, sys, rebuildIO):
        self.sys = sys
        self.rebuildIO = rebuildIO
        self.disks = {}
        self.servers = {}


    def estimate_RAID_time(self, diskId):
        self.disks[diskId].repair_time = self.disks[diskId].repair_data / (self.rebuildIO * 3600)
        print "    >>> estimate RAID local wo/P >>>[", diskId, "]", " repair time->",self.disks[diskId].repair_time


    def estimate_decluster_time(self, diskId, local_percent, normals_per_server):
        repair_IO = self.rebuildIO * normals_per_server
        repair_data = self.disks[diskId].repair_data * local_percent * (self.sys.kb + 1)
        repair_time = repair_data / repair_IO
        self.disks[diskId].repair_time = repair_time/3600
        print "    >>> estimate decluster wo/P >>>[", diskId, "]", " repair time->",self.disks[diskId].repair_time


    def estimate_FODP_time(self, diskId, local_sets_per_disk):
        repair_data = self.disks[diskId].repair_data * (local_sets_per_disk / float(self.sys.fb))
        repair_IO = self.rebuildIO * (self.sys.kb + self.sys.mb - 1) * local_sets_per_disk
        self.disks[diskId].repair_time = repair_data * (self.sys.kb + 1) / (repair_IO * 3600)
        print "    >>> estimate local FODP wo/P >>>[", diskId, "]", " repair time->",self.disks[diskId].repair_time


    def generate_repair_event(self, diskId, curr_time, events_queue):
        if self.disks[diskId].repair_time == 0:
            return
        estimate_time = curr_time + self.disks[diskId].repair_time
        heappush(events_queue, (estimate_time, Disk.EVENT_DEGRADEDREBUILD, diskId))
        print "--------> wo/P> push ", diskId, Disk.EVENT_DEGRADEDREBUILD, self.disks[diskId].repair_time, "  Until", estimate_time


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

