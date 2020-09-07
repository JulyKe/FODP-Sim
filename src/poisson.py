#~/usr/bin/python
import numpy as np
import random
#----------------------------------------------------------------------------------
# suppose you want to simulate percent%failure events in t time, arrival rate 0.01%
#----------------------------------------------------------------------------------
class Poisson:
    def __init__(self, N, percent, period):
        self.N = N
        self.percent = percent
        self.period = period


    def generate_failures(self):
        trace_entry = []
        total_failed_disks = self.N * self.percent
        failures =  random.sample(range(self.N), int(total_failed_disks))
        #--------------------------------------------------
        # Average seconds between failures
        #--------------------------------------------------
        MTTR = 6.6576
        #tau = self.period / float(total_failed_disks)
        #tau = 93.2068
        tau = 1.0*MTTR
        print('%f seconds between failures'%tau)
        print "--", self.N, total_failed_disks, failures, tau
        rand = np.random.RandomState(0)  # universal random seed
        time_between_fails = np.random.poisson(tau, total_failed_disks)
        #time_between_fails = [6, 4, 1, 3, 5, 4, 1, 6, 5, 7, 4, 1, 4, 8, 7, 7, 2, 1, 2, 1, 6, 2, 2, 5, 2]
        #time_between_fails = [5, 12, 6, 5, 3, 3, 6, 6, 5, 4, 10, 10, 7, 11, 4, 5, 4, 7, 6, 3, 2, 7, 2, 4, 8]
        #time_between_fails =  [9, 16, 9, 9, 15, 4,  14,  9, 12, 7, 11, 4, 2, 12,  8,  5, 11,  5,  9, 15,  6, 12, 12, 11, 19]
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
    poisson = Poisson(169, 0.15, 120.0)
    poisson.generate_failures()
