from fodp import FODP
import numpy as np
import logging

#------------------
# Logging Settings
#------------------
logger = logging.getLogger('Campaign')
logger.setLevel('DEBUG')
logger.addHandler(logging.StreamHandler())


class Campaign:
    def __init__(self, add_tier, plus_one, num_servers, num_disks_per_server, num_spares_per_server, kt, mt, kb, mb, top_type, bottom_type, ft, fb, diskCap, useRatio):
        #------------------------------------
        # whether add the additional tier
        #------------------------------------
        self.add_tier = add_tier
        self.plus_one = plus_one
        self.num_disks = num_servers * num_disks_per_server
        self.num_spares = num_servers * num_spares_per_server
        #---------------------------------------
        # setup servers and disks configurations
        #---------------------------------------
        self.num_servers = num_servers
        self.num_disks_per_server = num_disks_per_server
        self.num_spares_per_server = num_spares_per_server
        #---------------------------------------
        # setup groups and disks configurations
        #---------------------------------------
        self.num_groups = num_servers
        self.num_disks_per_group = num_disks_per_server
        self.num_spares_per_group = num_spares_per_server
        #---------------------------------------
        self.groups = range(self.num_groups)
        self.servers = range(num_servers)
        self.disks = range(self.num_disks)
        self.disks_per_server = {}
        for serverId in self.servers:
            if serverId == 0:
                self.disks_per_server[serverId] = np.array(range(num_disks_per_server))
            else:
                self.disks_per_server[serverId] = self.disks_per_server[serverId-1] + num_disks_per_server
        #-------------------------------------
        # setup erasure coding configurations
        #------------------------------------
        self.kt = kt
        self.mt = mt
        self.kb = kb
        self.mb = mb
        #------------------------------------
        # overlap fraction configurations
        #------------------------------------
        self.ft = ft
        self.fb = fb
        #------------------------------------
        # num stripesets for FODP
        #------------------------------------
        self.num_stripesets_per_server = fb * num_disks_per_server / (self.kb + self.mb)
        self.num_stripesets_across_servers = ft * num_servers / (self.kt + self.mt)
        #------------------------------------
        # calculate the repair data per disk
        #------------------------------------
        self.repair_data = diskCap * 1024 * 1024 * useRatio
        self.data_per_server = self.repair_data * (num_disks_per_server - num_spares_per_server) 
        self.data_per_system = self.data_per_server * num_servers
        self.data_per_FODP_stripeset = self.data_per_server / self.num_stripesets_per_server
        self.data_per_RAID_stripeset = self.data_per_server / ((num_disks_per_server-num_spares_per_server)/(self.kb+self.mb))
        #------------------------------------
        self.data_per_FODP_comb = self.repair_data * kb / (fb * ft)
        self.data_per_RAID_comb = self.repair_data * kb
        self.data_per_DP_comb = 0
        self.data_per_copyset_comb = 0
        self.data_per_group_comb = 0
        self.data_per_copyset_comb = 0
        #---------------------------------------------------------------
        # count the number of failures per (interId, intraId) stripeset
        #---------------------------------------------------------------
        self.bw_share = {}
        #--------------------------------------
        # setup the disk layout configurations
        #--------------------------------------
        self.top_type = top_type
        self.bottom_type = bottom_type
        #--------------------------------------
        if top_type == 0 and bottom_type == 0:
            self.tiered_RAID_layout()
        if top_type == 1 and bottom_type == 1:
            self.tiered_decluster_layout()
        if top_type == 2 and bottom_type == 2:
            self.tiered_FODP_layout()
            self.priority_per_set = {}
        if bottom_type == 3:
            self.flat_copyset_layout()
        if bottom_type == 4:
            self.flat_group_layout()
            


    def tiered_RAID_layout(self):
        logger.info(">>>>> Tiered RAID Generation >>>>>>")
        #----------------------------------
        # generate intra-server stripesets
        #----------------------------------
        self.tiered_RAID_intra_layout = {}
        self.RAID_stripeset_per_disk = {}
        for serverId in self.servers:
            data_disks = self.disks_per_server[serverId][0: self.num_disks_per_server - self.num_spares_per_server]
            #----------------------------------------------------------------------------------
            self.tiered_RAID_intra_layout[serverId] = FODP(data_disks, self.kb+self.mb, 1).stripesets
            #-------------------------------------
            # record intra stripeset for each disk
            #-------------------------------------
            for stripeset in self.tiered_RAID_intra_layout[serverId]:
                for diskId in stripeset:
                    self.RAID_stripeset_per_disk[diskId] = stripeset
        #----------------------------------
        # generate inter-server stripesets
        #----------------------------------
        if self.add_tier:
            self.tiered_RAID_layout = {}
            self.RAID_inter_intra_per_stripeset = {}
            self.tiered_RAID_inter_layout = FODP(self.servers, self.kt+self.mt, 1).stripesets
            num_RAID_arrays = (self.num_disks_per_server - self.num_spares_per_server) / (self.kb + self.mb)
            for interId in range(self.num_servers/(self.kt+self.mt)):
                for intraId in range(num_RAID_arrays):
                    self.tiered_RAID_layout[(interId, intraId)] = []
                    for serverId in self.tiered_RAID_inter_layout[interId]:
                        intraset = self.tiered_RAID_intra_layout[serverId][intraId]
                        self.tiered_RAID_layout[(interId, intraId)].append(intraset)
                        #-------------------------------------------------------
                        self.RAID_inter_intra_per_stripeset[tuple(intraset)] = (interId, intraId)
                    #-------------------------------------------------------
                    #print ">>>>>",interId,intraId,self.tiered_RAID_layout[(interId,intraId)]
            #for stripeset in self.RAID_inter_intra_per_stripeset:
            #    print "  @stripeset", stripeset, " - " ,self.RAID_inter_intra_per_stripeset[stripeset]
        


    def tiered_FODP_layout(self):
        logger.info(">>>>> Tiered FODP Generation >>>>>>")
        #----------------------------------
        # generate intra-server stripesets
        #----------------------------------
        self.tiered_FODP_intra_layout = {}
        self.FODP_stripesets_per_disk = {}
        for serverId in self.servers:
            self.tiered_FODP_intra_layout[serverId] = FODP(self.disks_per_server[serverId], self.kb+self.mb, self.fb).stripesets
            #-------------------------------------
            # record intra stripeset for each disk
            #-------------------------------------
            for stripeset in self.tiered_FODP_intra_layout[serverId]:
                print "- serverId -", serverId, ">", stripeset
                for diskId in stripeset:
                    if diskId not in self.FODP_stripesets_per_disk:
                        self.FODP_stripesets_per_disk[diskId] = [stripeset]
                    else:
                        self.FODP_stripesets_per_disk[diskId].append(stripeset)
        #----------------------------------
        # generate inter-server stripesets
        #----------------------------------
        if self.add_tier:
            self.tiered_FODP_layout = {}
            self.FODP_inter_intra_per_stripeset = {}
            self.tiered_FODP_inter_layout = FODP(self.servers, self.kt+self.mt, self.ft).stripesets
            #-------------------------------------------------------
            for interId in range(self.num_stripesets_across_servers):
                for intraId in range(self.num_stripesets_per_server):
                    #-------------------------------------------------------
                    self.tiered_FODP_layout[(interId, intraId)] = []
                    for serverId in self.tiered_FODP_inter_layout[interId]:
                        intraset = self.tiered_FODP_intra_layout[serverId][intraId]
                        self.tiered_FODP_layout[(interId, intraId)].append(intraset)
                        #-------------------------------------------------------
                        if tuple(intraset) not in self.FODP_inter_intra_per_stripeset:
                            self.FODP_inter_intra_per_stripeset[tuple(intraset)] = [(interId, intraId)]
                        else:
                            self.FODP_inter_intra_per_stripeset[tuple(intraset)].append((interId, intraId))
                    #-------------------------------------------------------
                    print ">>>>>",interId,intraId,self.tiered_FODP_layout[(interId,intraId)]
            for stripeset in self.FODP_inter_intra_per_stripeset:
                print "  @stripeset", stripeset, " - " ,self.FODP_inter_intra_per_stripeset[stripeset]




    def tiered_decluster_layout(self):
        logger.info(">>>>> Tiered Decluster Generation >>>>>>")
        #----------------------------------
        # generate intra-server stripesets
        #----------------------------------
        self.tiered_decluster_intra_layout = {}
        for serverId in self.servers:
            self.tiered_decluster_intra_layout[serverId] = self.disks_per_server[serverId]
        #----------------------------------
        # generate inter-server stripesets
        #----------------------------------
        if self.add_tier:
            self.DP_interIds_per_server = {}
            self.tiered_decluster_inter_layout = FODP(self.servers, self.kt+self.mt, self.ft).stripesets
            for interId in range(self.num_stripesets_across_servers):
                for serverId in self.tiered_decluster_inter_layout[interId]:
                    if serverId not in self.DP_interIds_per_server:
                        self.DP_interIds_per_server[serverId] = [interId]
                    else:
                        self.DP_interIds_per_server[serverId].append(interId)
            #print self.DP_interIds_per_server 



    def flat_group_layout(self):
        logger.info(">>>>> Flat Group Generation >>>>>>")
        #----------------------------------------------
        # generate random stripesets in groups
        #----------------------------------------------
        self.flat_group_layout = {}
        self.group_per_disk = {}
        self.servers_per_group = {}
        #------------------------------------------------------------------------------
        disks_permutation =  np.random.permutation(self.num_disks)
        disk_groups = disks_permutation.reshape(self.num_groups, self.num_disks_per_group)
        for groupId in self.groups:
            self.flat_group_layout[groupId] = disk_groups[groupId]
            #------------------------------------------------------------------------------
            self.servers_per_group[groupId] = [] 
            for diskId in disk_groups[groupId]:
                self.group_per_disk[diskId] = groupId
                serverId = diskId / self.num_disks_per_server
                if serverId not in self.servers_per_group[groupId]:
                    self.servers_per_group[groupId].append(serverId)
      


    def flat_copyset_layout(self):
        logger.info(">>>>> Flat Copyset Generation >>>>>>")
        #----------------------------------------------
        # generate copyset stripesets in groups
        #----------------------------------------------
        self.flat_copyset_layout = []
        self.copyset_stripesets_per_disk = {}
        #---------------------------------------------------------------
        num_permutations = self.num_disks_per_group / (self.kb+self.mb-1)
        print ">>>num_permutations", num_permutations
        for each in range(num_permutations):
            one_permutation = np.random.permutation(self.num_disks)
            one_permutation =  one_permutation[:((self.num_disks/(self.kb+self.mb)) * (self.kb+self.mb))]
            for stripeset in one_permutation.reshape(self.num_disks/(self.kb+self.mb), self.kb+self.mb):
                self.flat_copyset_layout.append(stripeset)
                for diskId in stripeset:
                    if diskId not in self.copyset_stripesets_per_disk:
                        self.copyset_stripesets_per_disk[diskId] = [stripeset]
                    else:
                        self.copyset_stripesets_per_disk[diskId].append(stripeset)
        #---------------------------------------------------------------
        self.group_per_disk = {}
        for diskId in self.disks:
            groupId = diskId / self.num_disks_per_group
            self.group_per_disk[diskId] = groupId
        #    print diskId, "-", self.copyset_stripesets_per_disk[diskId]


if __name__ == "__main__":
    sys = Campaign (add_tier=True, num_servers=2, num_disks_per_server=16, num_spares_per_server=2, kt=2, mt=1, kb=2, mb=2, top_type=1, bottom_type=3, ft=2, fb=1, diskCap=6, useRatio=1.0)

