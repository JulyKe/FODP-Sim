#~/usr/bin/python
import numpy as np
import random
#----------------------------------------------------------------------------------
# suppose you want to simulate percent%failure events in t time, arrival rate 0.01%
#----------------------------------------------------------------------------------
class Poisson:
    def __init__(self, N, percent, mtbf):
        self.N = N
	self.mtbf = mtbf
        self.percent = percent


    def generate_failures(self):
        trace_entry = []
        total_failed_disks = self.N * self.percent
        failures =  random.sample(range(self.N), int(total_failed_disks))
        #--------------------------------------------------
        # Average seconds between failures
        #--------------------------------------------------
        MTTR = 6.6576
        MTBF = self.mtbf * MTTR
        print('%f seconds between failures'% MTBF)
        print "--", self.N, total_failed_disks, failures, MTBF
        rand = np.random.RandomState(0)  # universal random seed
        time_between_fails = np.random.poisson(MTBF, total_failed_disks)
        print ">>>", time_between_fails
        failure_times = []
        last_fail = 0
        for t in time_between_fails:
            failure_times.append(last_fail + t)
            last_fail = last_fail + t

        for i in range(len(failures)):
            fail_time = failure_times[i]
            diskId = failures[i]
            print "-", diskId, fail_time
            trace_entry.append((fail_time, diskId))
        return trace_entry
        


if __name__ == "__main__":
    poisson = Poisson(169, 0.15, 1.0)
    poisson.generate_failures()
