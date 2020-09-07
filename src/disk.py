from mpmath import mpf

class Disk:
    #----------------------------
    # The 2 possible disk states
    #----------------------------
    STATE_NORMAL = "< state normal >"
    STATE_FAILED = "< state failed >"

    #----------------------------------
    # The 3 possible events
    #----------------------------------
    EVENT_FAIL = "<disk failure>"
    EVENT_DEGRADEDREBUILD = "<disk degraded rebuild>"
    EVENT_CRITICALREBUILD = "<disk critical rebuild>"
    EVENT_COPYBACK = "< copyback >"


    def __init__(self, diskId, repair_data):
        #--------------------------------
        # initialize the diskId and data
        #--------------------------------
        self.diskId = diskId
        #-------------------------------
        # initialize the state be normal
        #-------------------------------
        self.state = self.STATE_NORMAL
        #-------------------------
        # disk's priority
        #-------------------------
        self.priority = 0
        #--------------------------
        # disk's local clock
        #--------------------------
        self.clock = mpf(0)
        #-------------------------
        # disk's repair data
        #-------------------------
        self.repair_data = repair_data
        #--------------------
        # disk's repair time
        #---------------------
        self.repair_time = 0
        #----------------------------
        # disk's local/global repairs
        #----------------------------
        self.FODP_percent = {'local': 0, 'global': []}
        self.DP_percent = {'local': 0, 'global': 0}
        #-----------------------------
        # flag to local/global repairs
        #-----------------------------
        self.local_done = True
        self.global_done = True
        #-----------------------------
        # inter/intra Id for each disk
        #-----------------------------
        self.inter_intra_per_disk = {}


    def update_clock(self, curr_time):
        self.clock = curr_time
