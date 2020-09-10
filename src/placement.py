import numpy as np
import operator as op
import random

#-------------------------------------------
# check PDL according to the data placement
#-------------------------------------------
class Placement:
    def __init__(self, sys):
        self.sys = sys


    def check_global_dataloss(self, state, deviceset):
        switcher = {
                0: 'RAID',
                1: 'decluster_parity',
                2: 'FODP'}
        if self.sys.dp_type == 0:
            return self.tiered_RAID_simulate(state, deviceset)
        if self.sys.dp_type == 1:
            return self.tiered_decluster_simulate(state, deviceset)
        if self.sys.dp_type == 2:
            return self.tiered_FODP_simulate(state, deviceset)



    def calculate_dataloss(self, state):
	loss = 0
	#-------------------------------------------------------------------------
	if self.sys.dp_type == 2:
	    failures_per_server = {}
	    for diskId in state.MTTDL:
	    	serverId = state.MTTDL[diskId]['serverId']
	    	if serverId not in failures_per_server:
		    failures_per_server[serverId] = [diskId]
	    	else:
		    failures_per_server[serverId].append(diskId)
	    print "MTTDL failures per server",failures_per_server
	    #-------------------------------------------------------------
	    for serverId in failures_per_server:
	    	unrecoverables = []
	    	for diskId in failures_per_server[serverId]:
		    failures_per_stripeset = state.MTTDL[diskId]['failures']
		    for failId in failures_per_stripeset:
		        if failId not in unrecoverables:
			    unrecoverables.append(failId)
	    	print serverId, "MTTDL unrecoverables", unrecoverables
	    	#-----------------------------------------------------------
	    	for intraset in self.sys.tiered_FODP_intra_layout[serverId]:
		    #print "- serverId -", serverId, ">", intraset
		    failures_per_stripeset = []
		    for each in intraset:
		    	if each in unrecoverables:
			    failures_per_stripeset.append(each)
		    if len(failures_per_stripeset) > self.sys.m:
		        percent_stripeset =  len(failures_per_stripeset)/float(self.sys.k+self.sys.m)
		        print "  >>> unrecoverable stripesets", failures_per_stripeset, percent_stripeset
		    	if self.sys.plus_one:
			    percent_plus1 = len(unrecoverables) / float(self.sys.num_disks_per_server)
			    loss_per_stripeset = self.sys.data_per_FODP_stripeset * percent_stripeset * percent_plus1
			    loss += loss_per_stripeset
		        else:
			    loss_per_stripeset = self.sys.data_per_FODP_stripeset * percent_stripeset 
			    loss += loss_per_stripeset
		    print "      >>>loss", loss/1024
	    print " - FODP data loss - percent -", loss/self.sys.data_per_system
	#-------------------------------------------------------------------------
	if self.sys.dp_type == 0:
	    failures_per_server = {}
	    for diskId in state.MTTDL:
	        serverId = state.MTTDL[diskId]['serverId']
	        if serverId not in failures_per_server:
		    failures_per_server[serverId] = [diskId]
	    	else:
		    failures_per_server[serverId].append(diskId)
	    print "MTTDL failures per server",failures_per_server
	    #-------------------------------------------------------------
	    for serverId in failures_per_server:
	        unrecoverables = []
	    	for diskId in failures_per_server[serverId]:
		    failures_per_stripeset = state.MTTDL[diskId]['failures']
		    for failId in failures_per_stripeset:
		        if failId not in unrecoverables:
			    unrecoverables.append(failId)
	    	#-----------------------------------------------------------
	    	for intraset in self.sys.tiered_RAID_intra_layout[serverId]:
		    print "- serverId -", serverId, ">", intraset
		    failures_per_stripeset = []
		    for each in intraset:
		    	if each in unrecoverables:
			    failures_per_stripeset.append(each)
		    if len(failures_per_stripeset) > self.sys.m:
		        percent_stripeset =  len(failures_per_stripeset)/float(self.sys.k+self.sys.m)
		        print "  >>>", failures_per_stripeset
		        loss_per_stripeset = self.sys.data_per_RAID_stripeset * percent_stripeset 
		        loss += loss_per_stripeset
	    print " - RAID data loss - percent -", loss/self.sys.data_per_system
	#-------------------------------------------------------------------------
	if self.sys.dp_type == 1:
	    failures_per_server = {}
	    for diskId in state.MTTDL:
	    	serverId = state.MTTDL[diskId]['serverId']
	    	if serverId not in failures_per_server:
		    failures_per_server[serverId] = [diskId]
	    	else:
		    failures_per_server[serverId].append(diskId)
	    print "MTTDL failures per server",failures_per_server
	    #-------------------------------------------------------------
	    for serverId in failures_per_server:
	    	fails_per_server = len(failures_per_server[serverId]) + self.sys.m
	    	normals_per_server = self.sys.num_disks_per_server - fails_per_server
	    	total_sets = self.ncr(self.sys.num_disks_per_server, self.sys.k + self.sys.m)
	    	loss_sets = 0
	    	for num_failures  in range(self.sys.m+1, min(fails_per_server+1, self.sys.k+self.sys.m+1)):
		    loss_sets += self.ncr(normals_per_server, self.sys.k+self.sys.m-num_failures) * self.ncr(fails_per_server, num_failures)
	    	loss_percent = loss_sets / float(total_sets)
	    	loss += loss_percent * self.sys.data_per_server
	    print " - Declustered Parity data loss - percent -", loss/self.sys.data_per_system
	#-------------------------------------------------------------------------
	return loss/self.sys.data_per_system





    def tiered_RAID_simulate(self, state, deviceset):
        localProb = 0
	for diskId in deviceset:
	    if diskId not in self.sys.RAID_stripeset_per_disk:
	    	print "  -> RAID spare drive failure <-  ", diskId
	    	continue
	    intraset = self.sys.RAID_stripeset_per_disk[diskId]
	    failures_per_stripeset = state.handler.get_failed_disks_per_stripeset(intraset)
	    if len(failures_per_stripeset) > self.sys.m:
	    	state.MTTDL[diskId] = {'serverId': diskId/self.sys.num_disks_per_server, 'failures': failures_per_stripeset}
	    	localProb = 1
	    	return localProb
        return localProb



    def tiered_FODP_simulate(self, state, deviceset):
        localProb = 0
    	#----------------------------------------------------------------
	for diskId in deviceset:
	    intrasets = self.sys.FODP_stripesets_per_disk[diskId]
	    for intraset in intrasets: 
	    	failures_per_stripeset = state.handler.get_failed_disks_per_stripeset(intraset)
	    	if len(failures_per_stripeset) > self.sys.m:
	            state.MTTDL[diskId] = {'serverId': diskId/self.sys.num_disks_per_server, 'failures': failures_per_stripeset}
		    localProb = 1
		    return localProb
	return localProb



    def tiered_decluster_simulate(self, state, deviceset):
        localProb = 0
    	#----------------------------------------------------------------
    	for diskId in deviceset:
	    serverId = diskId / self.sys.num_disks_per_server
	    failures_per_server = state.handler.get_failed_disks_per_server(serverId)
	    if len(failures_per_server) > self.sys.m:
	        state.MTTDL[diskId] = {'serverId': serverId, 'failures': failures_per_server}
	        localProb = 1
	        return localProb
	return localProb



    def ncr(self, n, r):
        r = min(r, n-r)
        numer = reduce(op.mul, range(n, n-r, -1), 1)
        denom = reduce(op.mul, range(1, r+1), 1)
        return numer / denom
