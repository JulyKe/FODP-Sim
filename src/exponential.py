import numpy as np
import random

# http://pageperso.lif.univ-mrs.fr/~francois.denis/IAAM1/numpy-html-1.14.0/reference/generated/numpy.random.exponential.html
# https://dfrieds.com/math/exponential-distribution.html
class Exponential:
    def __init__(self, S, percent, MTBF, cascade_factor):
        self.S = S
        self.percent = percent
        self.MTBF = MTBF
        self.cascade_factor = cascade_factor

    def generate_failures(self):
        trace_entry = []
        total_failed_devices = self.S * self.percent
        #-----------------------------------------------------------------
        failures1 =  random.sample(range(self.S), int(total_failed_devices))
        MTBF1 = self.MTBF
        rand = np.random.RandomState(0)  # universal random seed
        time_between_fails1 = np.random.exponential(MTBF1, total_failed_devices)
        #print ">>>", time_between_fails1
        failure_times1 = []
        last_fail1 = 0
        for t1 in time_between_fails1:
            failure_times1.append(last_fail1 + t1)
            last_fail1 = last_fail1 + t1

        #-----------------------------------------------------------------
        failures2 =  random.sample(failures1, int(0.3*len(failures1)))
        MTBF2 = MTBF1/self.cascade_factor
        collect = []
        for i in range(len(failures1)):
            deviceId = failures1[i]
            fail_time = failure_times1[i]
            #print "1-", deviceId, fail_time
            trace_entry.append((fail_time, deviceId))
            collect.append(deviceId)
            if deviceId in failures2:
                cascade_time = fail_time
                num_cascades = random.choice(range(3,11))
                time_between_fails2 = np.random.exponential(MTBF2, num_cascades)
                for t2 in time_between_fails2:
                    frange = [ele for ele in range(self.S) if ele not in collect and ele not in failures1]
                    cascade_time = cascade_time + t2
                    if len(frange) == 0:
                        continue
                    cascadeId = random.choice(frange)
                    #print "    2-", cascadeId, cascade_time
                    trace_entry.append((cascade_time, cascadeId))
                    collect.append(cascadeId)
        return trace_entry
        
        

if __name__ == "__main__":
    sim = Exponential(8064, 0.05, 32, 100.0)
    sim.generate_failures()


