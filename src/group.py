from heapq import *
class Group:
    def __init__(self, groupId, disks, num_spares, networkBW):
        #-----------------------------------
        # initialize the groupId and disks
        #-----------------------------------
        self.groupId = groupId
        self.disks = disks
        #-------------------------------------------
        # initialize the total and available spares
        #-------------------------------------------
        self.num_spares = num_spares
        self.avail_spares = num_spares
        #-------------------------------------
        # initialize the bw and available bw
        #-------------------------------------
        self.availBW = networkBW 
        #----------------------------------------------
        # server shares bandwidth for multiple repairs
        #----------------------------------------------
        self.share = 0
        #------------------------------
        # wait_queue for each server
        #------------------------------
        self.wait_queue = []


    
