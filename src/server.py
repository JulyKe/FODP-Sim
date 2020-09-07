from heapq import *
class Server:
    #----------------------------
    # The 2 possible disk states
    #----------------------------
    STATE_NORMAL = "< state normal >"
    STATE_FAILED = "< state failed >"

    #----------------------------------
    # The 2 possible events
    #----------------------------------
    EVENT_FAIL = "<server failure>"
    EVENT_REPAIR = "<server repair>"

    def __init__(self, serverId, num_spares, networkBW):
        #-----------------------------------
        # initialize the serverId and state
        #-----------------------------------
        self.serverId = serverId
        self.state = Server.STATE_NORMAL
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


    
