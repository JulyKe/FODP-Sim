from heapq import *
from disk import Disk
#---------------------------------------------
# Service Level Agreements (SLA) + Copyback  
#---------------------------------------------
class Copyback:
    def __init__(self, copybackIO, slaTime):
        self.copybackIO = copybackIO
        self.slaTime = slaTime


    def start_replace(self, diskId, events_queue, curr_time):
        estimate_time = curr_time + self.slaTime
        heappush(events_queue, (estimate_time, Disk.EVENT_COPYBACK, diskId))
        print "--------> push ", diskId, Disk.EVENT_COPYBACK, self.slaTime, " Until", estimate_time


    def start_copyback(self, diskId, events_queue, curr_time):
        copyback_time = self.calculate_copyback_time(diskId)
        estimate_time = curr_time + self.slaTime + copyback_time
        heappush(events_queue, (estimate_time, Disk.EVENT_COPYBACK, diskId))
        print "--------> push ", diskId, Disk.EVENT_COPYBACK, copyback_time, " Until", estimate_time


    def calculate_copyback_time(self, diskId):
        repair_data = self.disks[diskId].repair_data
        copyback_time = repair_data / self.copybackIO
        print "    >>> estimate copyback disk >>>[", diskId, "]", " copyback time->",copyback_time/3600
        return float(copyback_time)/3600
        # dual acurator
