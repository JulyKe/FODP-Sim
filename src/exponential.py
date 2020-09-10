import numpy as np
import random

# http://pageperso.lif.univ-mrs.fr/~francois.denis/IAAM1/numpy-html-1.14.0/reference/generated/numpy.random.exponential.html
# https://dfrieds.com/math/exponential-distribution.html
class Exponential:
    def __init__(self, S, percent, mtbf):
        self.S = S
        self.mtbf = mtbf
        self.percent = percent


    def generate_failures(self):
        MTTR = 6.6576
        trace_entry = []
        total_failed_devices = self.S * self.percent
        #-----------------------------------------------------------------
        failures1 =  random.sample(range(self.S), int(total_failed_devices))
        MTBF = self.mtbf * MTTR
        rand = np.random.RandomState(0)  # universal random seed
        time_between_fails1 = np.random.exponential(MTBF, total_failed_devices)
        print ">>>", time_between_fails1
        failure_times1 = []
        last_fail1 = 0
        for t1 in time_between_fails1:
            failure_times1.append(last_fail1 + t1)
            last_fail1 = last_fail1 + t1

        for i in range(len(failures1)):
            fail_time = failure_times1[i]
            diskId = failures1[i]
            print "-", diskId, fail_time
            trace_entry.append((fail_time, diskId))
        return trace_entry


if __name__ == "__main__":
    sim = Exponential(169, 0.15, 0.1)
    sim.generate_failures()

