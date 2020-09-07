from server import Server
from disk import Disk
from heapq import *
#--------------------------------------------------------------------------
# repair-time = cross-rack repair traffic / available cross-rack bandwidth
#--------------------------------------------------------------------------
class Network:
    def __init__(self, sys, networkBW):
        self.sys = sys
        self.disks = {}
        self.servers = {}
        self.repairs = dict()
        self.networkBW = networkBW*1024/8.0


    def estimate_RAID_time(self, diskId, serverId):
        intraset = self.sys.RAID_stripeset_per_disk[diskId]
        (interId, intraId) = self.sys.RAID_inter_intra_per_stripeset[tuple(intraset)]
        self.repairs[(interId, intraId, diskId)] = {'fails':[], 'helps':[], 'time': 0}
        #-------------------------------------------------------------------
        if (interId, intraId, serverId) not in self.sys.bw_share:
            self.sys.bw_share[(interId, intraId, serverId)] = 1
        else:
            self.sys.bw_share[(interId, intraId, serverId)] += 1
        print "",interId, intraId, diskId, serverId, self.sys.bw_share[(interId, intraId, serverId)]
        #-------------------------------------------------------------------
        for each_server in self.sys.tiered_RAID_inter_layout[interId]:
            if each_server == serverId:
                self.repairs[(interId, intraId, diskId)]['fails'].append(each_server)
            else:
                self.repairs[(interId, intraId, diskId)]['helps'].append(each_server)
                if self.sys.bw_share[(interId, intraId, serverId)] == 1:
                    self.servers[each_server].share += 1
        print diskId, " - RAID network repair - ", interId, intraId, diskId, self.repairs[(interId, intraId, diskId)]
        #-------------------------------------------------------------------
        self.disks[diskId].inter_intra_per_disk[(interId, intraId)] = True
        self.repairs[(interId, intraId, diskId)]['time'] = self.estimate_network_repair_time(interId, intraId, diskId)
        print "    >>> estimate network RAID wo/P repair >>>[", diskId, "]", "time->", self.repairs[(interId, intraId, diskId)]['time']


    def estimate_group_time(self, diskId, groupId):
        self.repairs[(groupId, 0, diskId)] = {'fails':[], 'helps':[], 'time': 0}
        #---------------------------------------------------------
        serverId = diskId / self.sys.num_disks_per_server
        if (groupId, 0, serverId) not in self.sys.bw_share:
            self.sys.bw_share[(groupId, 0, serverId)] = 1
        else:
            self.sys.bw_share[(groupId, 0, serverId)] += 1
        #---------------------------------------------------------
        for each_server in self.sys.servers_per_group[groupId]:
            if each_server == serverId:
                self.repairs[(groupId, 0, diskId)]['fails'].append(each_server)
            else:
                self.repairs[(groupId, 0, diskId)]['helps'].append(each_server)
                if self.sys.bw_share[(groupId, 0, serverId)] == 1:
                    self.servers[each_server].share += 1
        print diskId, " - group network repair - ", groupId, 0, diskId, self.repairs[(groupId, 0, diskId)]
        #-------------------------------------------------------------------
        self.disks[diskId].inter_intra_per_disk[(groupId, 0)] = True
        self.sys.data_per_group_comb = self.disks[diskId].repair_data * self.sys.kb / len(self.repairs[(groupId, 0, diskId)]['helps'])
        self.repairs[(groupId, 0, diskId)]['time'] = self.estimate_network_repair_time(groupId, 0, diskId)
        print "    >>> estimate network group wo/P repair >>>[", diskId, "]", "time->", self.repairs[(groupId, 0, diskId)]['time']



    def estimate_copyset_time(self, diskId, groupId):
        for intraId in range(len(self.sys.copyset_stripesets_per_disk[diskId])):
            self.repairs[(groupId, intraId, diskId)] = {'fails':[], 'helps':[], 'time': 0}
            serverId = diskId / self.sys.num_disks_per_server
            #---------------------------------------------------------
            if (groupId, intraId, serverId) not in self.sys.bw_share:
                self.sys.bw_share[(groupId, intraId, serverId)] = 1
            else:
                self.sys.bw_share[(groupId, intraId, serverId)] += 1
            #---------------------------------------------------------
            stripeset = self.sys.copyset_stripesets_per_disk[diskId][intraId]
            for each_disk in stripeset:
                each_server = each_disk / self.sys.num_disks_per_server
                if each_server == serverId:
                    self.repairs[(groupId, intraId, diskId)]['fails'].append(each_server)
                else:
                    self.repairs[(groupId, intraId, diskId)]['helps'].append(each_server)
                    if self.sys.bw_share[(groupId, intraId, serverId)] == 1:
                        self.servers[each_server].share += 1
            print diskId, " - copyset network repair - ", groupId, intraId, self.repairs[(groupId, intraId, diskId)]
            #-------------------------------------------------------------------
            self.disks[diskId].inter_intra_per_disk[(groupId, intraId)] = True
            self.sys.data_per_copyset_comb = (self.disks[diskId].repair_data / len(self.sys.copyset_stripesets_per_disk[diskId])) * self.sys.kb / (len(self.repairs[(groupId, intraId, diskId)]['fails'])-1 + len(self.repairs[(groupId, intraId, diskId)]['helps']))
            self.repairs[(groupId, intraId, diskId)]['time'] = self.estimate_network_repair_time(groupId, intraId, diskId)
            print "    >>> estimate network copyset wo/P repair >>>[", diskId, "]", "time->", self.repairs[(groupId, intraId, diskId)]['time']


    

    def estimate_decluster_time(self, diskId, serverId, global_percent, failures_per_server):
        for interId in self.sys.DP_interIds_per_server[serverId]:
            self.repairs[(interId, 0, diskId)] = {'fails':[], 'helps':[], 'time': 0}
            #---------------------------------------------------------------
            if (interId, 0, serverId) not in self.sys.bw_share:
                self.sys.bw_share[(interId, 0, serverId)] = 1
            else:
                self.sys.bw_share[(interId, 0, serverId)] += 1
            #---------------------------------------------------------------
            for each_server in self.sys.tiered_decluster_inter_layout[interId]:
                if each_server == serverId:
                    self.repairs[(interId, 0, diskId)]['fails'].append(each_server)
                else:
                    self.repairs[(interId, 0, diskId)]['helps'].append(each_server)
                    if self.sys.bw_share[(interId, 0, serverId)] == 1:
                        self.servers[each_server].share += 1
            print diskId, " - DP network repair - ", interId, 0, diskId, self.repairs[(interId, 0, diskId)]
            #-------------------------------------------------------------------
            self.disks[diskId].inter_intra_per_disk[(interId, 0)] = True
            self.sys.data_per_DP_comb = self.disks[diskId].repair_data * global_percent * self.sys.kb / self.sys.ft
            self.repairs[(interId, 0, diskId)]['time'] = self.estimate_network_repair_time(interId, 0, diskId)
            print "    >>> estimate network DP wo/P repair >>>[", diskId, "]", "time->", self.repairs[(interId, 0, diskId)]['time']



    def estimate_FODP_time(self, diskId, serverId):
        for stripeset in self.disks[diskId].FODP_percent['global']:
            for (interId, intraId) in self.sys.FODP_inter_intra_per_stripeset[tuple(stripeset)]:
                self.repairs[(interId, intraId, diskId)] = {'fails':[], 'helps':[], 'time': 0}
                #-------------------------------------------------------------------
                if (interId, intraId, serverId) not in self.sys.bw_share:
                    self.sys.bw_share[(interId, intraId, serverId)] = 1
                else:
                    self.sys.bw_share[(interId, intraId, serverId)] += 1
                print "",interId, intraId, diskId, serverId, self.sys.bw_share[(interId, intraId, serverId)]
                #-------------------------------------------------------------------
                for each_server in self.sys.tiered_FODP_inter_layout[interId]:
                    if each_server == serverId:
                        self.repairs[(interId, intraId, diskId)]['fails'].append(each_server)
                    else:
                        self.repairs[(interId, intraId, diskId)]['helps'].append(each_server)
                        if self.sys.bw_share[(interId, intraId, serverId)] == 1:
                            self.servers[each_server].share += 1
                print diskId, " - FODP network repair - ", interId, intraId, self.repairs[(interId, intraId, diskId)]
        #-------------------------------------------------------------------
        for stripeset in self.disks[diskId].FODP_percent['global']:
            for (interId, intraId) in self.sys.FODP_inter_intra_per_stripeset[tuple(stripeset)]:
                self.disks[diskId].inter_intra_per_disk[(interId, intraId)] = True
                self.repairs[(interId, intraId, diskId)]['time'] = self.estimate_network_repair_time(interId, intraId, diskId)
                print "    >>> estimate network FODP wo/P repair >>>[", diskId, "]", "time->", self.repairs[(interId, intraId, diskId)]['time']



    def estimate_network_repair_time(self, interId, intraId, diskId):
        bws = []
        for helpId in self.repairs[(interId, intraId, diskId)]['helps']:
            print "   ++++", helpId, " - share - ", self.servers[helpId].share, self.servers[helpId].availBW
            if self.servers[helpId].share == 0:
                bws.append(self.servers[helpId].availBW)
            else:
                bws.append(self.servers[helpId].availBW / self.servers[helpId].share)
        #----------------------------------------------------------------------
        if self.sys.top_type == 0 and self.sys.bottom_type == 0:
            network_time = self.sys.data_per_RAID_comb / float(min(bws) * 3600) 
            return network_time
        #----------------------------------------------------------------------
        if self.sys.top_type == 1 and self.sys.bottom_type == 1:
            network_time = self.sys.data_per_DP_comb / float(min(bws) * 3600) 
            return network_time
        #----------------------------------------------------------------------
        if self.sys.top_type == 2 and self.sys.bottom_type == 2:
            network_time = self.sys.data_per_FODP_comb / float(min(bws) *3600)
            return network_time
        #----------------------------------------------------------------------
        if self.sys.bottom_type == 3:
            network_time = self.sys.data_per_copyset_comb / float(min(bws) *3600)
            return network_time
        #----------------------------------------------------------------------
        if self.sys.bottom_type == 4:
            network_time = self.sys.data_per_group_comb / float(min(bws) *3600)
            return network_time
            




    def generate_repair_event(self, diskId, curr_time, events_queue):
        #----------------------------------------------------------------------
        if self.sys.top_type == 0 and self.sys.bottom_type == 0:
            if diskId not in self.sys.RAID_stripeset_per_disk:
                print "  -> RAID spare drive fail <-  ", diskId
                return
            intraset = self.sys.RAID_stripeset_per_disk[diskId]
            if len(self.get_failed_disks_per_stripeset(intraset)) > self.sys.mb:
                (interId, intraId) = self.sys.RAID_inter_intra_per_stripeset[tuple(intraset)]
                if (interId, intraId, diskId) not in self.repairs or self.repairs[(interId, intraId, diskId)]['time'] == 0:
                    return
                print " > global generate", diskId, self.repairs[(interId, intraId, diskId)]
                network_time  = self.repairs[(interId, intraId, diskId)]['time']
                heappush(events_queue, (curr_time + network_time, Server.EVENT_REPAIR, (interId, intraId, diskId)))
                print "--------> wo/P push ", interId, intraId, diskId, Server.EVENT_REPAIR, network_time, " Until", curr_time + network_time
        #----------------------------------------------------------------------
        if self.sys.top_type == 1 and self.sys.bottom_type == 1:
            print "-"
        #----------------------------------------------------------------------
        if self.sys.top_type == 2 and self.sys.bottom_type == 2:
            for stripeset in self.disks[diskId].FODP_percent['global']:
                for (interId, intraId) in self.sys.FODP_inter_intra_per_stripeset[tuple(stripeset)]:
                    network_time  = self.repairs[(interId, intraId, diskId)]['time']
                    heappush(events_queue, (curr_time + network_time, Server.EVENT_REPAIR, (interId, intraId, diskId)))
                    print "--------> wo/P push ", interId, intraId, diskId, Server.EVENT_REPAIR, network_time, " Until", curr_time + network_time
        #----------------------------------------------------------------------
        if self.sys.bottom_type == 3:
            for intraId in range(len(self.sys.copyset_stripesets_per_disk[diskId])):
                groupId = self.sys.group_per_disk[diskId]
                network_time = self.repairs[(groupId, intraId, diskId)]['time']
                heappush(events_queue, (curr_time + network_time, Server.EVENT_REPAIR, (groupId, intraId, diskId)))
                print "--------> wo/P push ", groupId, intraId, diskId, Server.EVENT_REPAIR, network_time, " Until", curr_time + network_time
        #----------------------------------------------------------------------
        if self.sys.bottom_type == 4:
            groupId = self.sys.group_per_disk[diskId]
            network_time = self.repairs[(groupId, 0, diskId)]['time']
            heappush(events_queue, (curr_time + network_time, Server.EVENT_REPAIR, (groupId, 0, diskId)))
            print "--------> wo/P push ", groupId, 0, diskId, Server.EVENT_REPAIR, network_time, " Until", curr_time + network_time



    def get_failed_disks_per_stripeset(self, stripeset):
        fail_per_stripeset = []
        for diskId in stripeset:
            if self.disks[diskId].state == Disk.STATE_FAILED:
                fail_per_stripeset.append(diskId)
        return fail_per_stripeset

