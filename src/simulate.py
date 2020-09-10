from placement import Placement
from campaign import Campaign
from copyback import Copyback
from rebuild import Rebuild
from batch import Batch
from poisson import Poisson
from exponential import Exponential
from server import Server
from state import State
from disk import Disk
from heapq import *
#------------------------------------
# Simulations
#------------------------------------
class Simulate:
    def __init__(self,mission_time, plus_one, num_servers, num_disks_per_server, num_spares_per_server, k, m, fb, dp_type, failure_type, mtbf, failure_percent, rebuildIO, slaTime, copybackIO, diskCap, useRatio):
        #---------------------------
	# compressed time window
        #---------------------------
        self.mission_time = mission_time
        #---------------------------
        # system and placement
        #---------------------------
        self.sys = Campaign(plus_one, num_servers, num_disks_per_server, num_spares_per_server, k, m, fb, dp_type, diskCap, useRatio)
        self.place = Placement(self.sys)
        #--------------------------------------
	# fast rebuild + copyback phases
        #--------------------------------------
        self.rebuild = Rebuild(self.sys, rebuildIO)
        self.copyback = Copyback(copybackIO, slaTime)
        #--------------------------------------
	# failures distribution and mtbf
        #--------------------------------------
	self.mtbf = mtbf
	self.failure_type = failure_type
        self.failure_percent = failure_percent


    def reset(self):
        #----------------------------------------------
        # failures arrive by using poisson distribution
        #----------------------------------------------
	if self.failure_type == 0:
            trace = Poisson(self.sys.num_disks, self.failure_percent, self.mtbf)
	if self.failure_type == 1:
            trace = Exponential(self.sys.num_disks, self.failure_percent, self.mtbf)
	if self.failure_type == 2:
           trace = Batch(self.sys.num_disks, self.failure_percent, self.mtbf, cascade_factor=10.0)
        self.trace_entry = trace.generate_failures()
        #------------------------------------------
        # put the disk failures in the event queue
        #------------------------------------------
        self.events_queue = []
        for disk_fail_time, diskId in self.trace_entry:
            heappush(self.events_queue, (disk_fail_time, Disk.EVENT_FAIL, diskId))
            print ">>>>> reset disk", diskId, Disk.EVENT_FAIL, "@",disk_fail_time
            self.mission_time = disk_fail_time
        print " - system mission time - ", self.mission_time
        #------------------------------
        # initialize the system state
        #------------------------------
        self.state = State(self.sys, self.rebuild, self.copyback, self.events_queue)



    def get_next_wait_events(self):
        events = []
        #---------------------------------------------------------------------------------------
        if self.sys.dp_type == 0 or self.sys.dp_type == 1 or self.sys.dp_type == 2:
        #---------------------------------------------------------------------------------------
            for serverId in self.sys.servers:
                if self.state.servers[serverId].wait_queue:
                    avail_spares = self.state.servers[serverId].avail_spares
                    while avail_spares and self.state.servers[serverId].wait_queue:
                        print "\n@wait_queue in server [", serverId , "] avail spares:",self.state.servers[serverId].avail_spares
                        deviceset = []
                        next_event = heappop(self.state.servers[serverId].wait_queue)
                        #------------------------------------------
                        next_event_time = next_event[0]
                        next_event_type = next_event[1]
                        deviceset.append(next_event[2])
                        avail_spares -= 1
                        while self.state.servers[serverId].wait_queue and self.state.servers[serverId].wait_queue[0][0] == next_event_time and self.state.servers[serverId].wait_queue[0][1] == next_event_type and avail_spares > 0:
                            simultaneous_event = heappop(self.state.servers[serverId].wait_queue)
                            deviceset.append(simultaneous_event[2])
                            avail_spares -= 1
                        print ">>>>> pop server wait disk", deviceset, next_event_type, " - time - ", next_event_time
                        events.append((next_event_time, next_event_type, deviceset))
            return events




    def get_next_events(self):
        #--------------------------------------------------------------
        wait_events = self.get_next_wait_events()
        if len(wait_events) > 0:
            return wait_events
        #--------------------------------------------------------------
        if self.events_queue:
            deviceset = []
            next_event = heappop(self.events_queue)
            #------------------------------------------
            next_event_time = next_event[0]
            next_event_type = next_event[1]
            deviceset.append(next_event[2])
            #----------------------------------------------
            # gather the simultaneous failure/repair events
            #----------------------------------------------
            while self.events_queue and self.events_queue[0][0]==next_event_time and self.events_queue[0][1]==next_event_type:
                simultaneous_event = heappop(self.events_queue)
                deviceset.append(simultaneous_event[2])
            print "\n\n>>>>> pop next event -", deviceset, next_event_type, next_event_time
            return [(next_event_time, next_event_type, deviceset)]
        else:
            return [(None, None, None)]




    def run_simulation(self, iterations_per_worker, traces_per_worker):
        results = []
        for one_iter in range(iterations_per_worker):
            results.append(self.run_iteration(one_iter))
        return results
    



    def run_iteration(self, num_iter):
        self.reset()
        curr_time = 0
        loss = 0
        loopflag = True
        eventDL = 0
        while loopflag:
            for each_event in self.get_next_events():
                (event_time, event_type, deviceset) = each_event
                #-----------------------------
                # if invalid event, then exit
                #-----------------------------
                if event_time == None:
                    loopflag = False
                    break
                #----------------------------------
                # update the system time and state
                #----------------------------------
                if curr_time < event_time:
                    curr_time = event_time
                #---------------------------
                # exceed mission-time, exit
                #---------------------------
                if curr_time > self.mission_time:
                    loopflag = False
                    loss = self.place.calculate_dataloss(self.state)
                    break
                #----------------------------------
                self.state.update_clock(event_type, curr_time)
                self.state.update_state(event_type, deviceset)
                self.state.update_event(event_type, deviceset)
                #-------------------------------------------------------
                # degraded rebuild or copyback event, continue
                #-------------------------------------------------------
                if event_type == Disk.EVENT_DEGRADEDREBUILD or event_type == Disk.EVENT_COPYBACK:
                    continue
                #------------------------------------------
                # check the PDL according to failure events
                #------------------------------------------
                if event_type == Disk.EVENT_FAIL:
                    eventDL = eventDL + 1
                    if self.place.check_global_dataloss(self.state, deviceset):
                        print "############### data loss ##############", eventDL, "deviceset", deviceset, curr_time, ">>> unrecoverables - ", self.state.MTTDL, "\n"
        return (self.state.MTTDL, loss)

