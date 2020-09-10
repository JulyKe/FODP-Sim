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
    def __init__(self, plus_one, num_servers, num_disks_per_server, num_spares_per_server, k, m, fb, dp_type, diskCap, useRatio):
        #------------------------------------
        # whether plus one on top of FODP
        #------------------------------------
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
        self.k = k
        self.m = m
        self.fb = fb
        #------------------------------------
        # calculate the repair data per disk
        #------------------------------------
        self.repair_data = diskCap * 1024 * 1024 * useRatio
        self.data_per_server = self.repair_data * (num_disks_per_server - num_spares_per_server) 
        self.data_per_system = self.data_per_server * num_servers
        #------------------------------------
        # num stripesets for FODP
        #------------------------------------
        self.num_stripesets_per_server = fb * num_disks_per_server / (self.k + self.m)
        self.data_per_FODP_stripeset = self.data_per_server / self.num_stripesets_per_server
        #------------------------------------
        # num stripesets for RAID
        #------------------------------------
	self.num_stripesets_per_RAID_server = (num_disks_per_server-num_spares_per_server)/(self.k+self.m)
        self.data_per_RAID_stripeset = self.data_per_server /  self.num_stripesets_per_RAID_server
        #------------------------------------
        # setup the disk layout configurations
        #--------------------------------------
        self.dp_type = dp_type
        if dp_type == 0:
            self.tiered_RAID_layout()
        if dp_type == 1:
            self.tiered_decluster_layout()
        if dp_type == 2:
            self.tiered_FODP_layout()
            


    def tiered_RAID_layout(self):
        logger.info(">>>>> Tiered RAID Generation >>>>>>")
        #----------------------------------
        # generate intra-server stripesets
        #----------------------------------
        self.tiered_RAID_intra_layout = {}
        self.RAID_stripeset_per_disk = {}
        for serverId in self.servers:
            data_disks = self.disks_per_server[serverId][0: self.num_disks_per_server - self.num_spares_per_server]
            #----------------------------------------------------------------------------------------
            self.tiered_RAID_intra_layout[serverId] = FODP(data_disks, self.k+self.m, 1).stripesets
            #-------------------------------------
            # record intra stripeset for each disk
            #-------------------------------------
            for stripeset in self.tiered_RAID_intra_layout[serverId]:
                for diskId in stripeset:
                    self.RAID_stripeset_per_disk[diskId] = stripeset


    def tiered_FODP_layout(self):
        logger.info(">>>>> Tiered FODP Generation >>>>>>")
        #----------------------------------
        # generate intra-server stripesets
        #----------------------------------
        self.tiered_FODP_intra_layout = {}
        self.FODP_stripesets_per_disk = {}
        for serverId in self.servers:
            #----------------------------------------------------------------------------------------
            self.tiered_FODP_intra_layout[serverId] = FODP(self.disks_per_server[serverId], self.k+self.m, self.fb).stripesets
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



    def tiered_decluster_layout(self):
        logger.info(">>>>> Tiered Decluster Generation >>>>>>")
        #----------------------------------
        # generate intra-server stripesets
        #----------------------------------
        self.tiered_decluster_intra_layout = {}
        for serverId in self.servers:
            self.tiered_decluster_intra_layout[serverId] = self.disks_per_server[serverId]



if __name__ == "__main__":
    sys = Campaign (plus_one=True, num_servers=2, num_disks_per_server=16, num_spares_per_server=2, k=2, m=1, fb=2, dp_type=1, diskCap=6, useRatio=1.0)

