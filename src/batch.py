import numpy as np
import random
# http://pageperso.lif.univ-mrs.fr/~francois.denis/IAAM1/numpy-html-1.14.0/reference/generated/numpy.random.exponential.html
# https://dfrieds.com/math/exponential-distribution.html
class Batch:
    def __init__(self, S, percent, mtbf, cascade_factor):
        self.S = S
        self.mtbf = mtbf
        self.percent = percent
        self.cascade_factor = cascade_factor

    def generate_failures(self):
        trace_entry = []
        total_failed_devices = self.S * self.percent
        failures =  random.sample(range(self.S), int(total_failed_devices))
        print failures
        #-----------------------------------------------------------------
        initial_ratio = 0.2
        failures1 =  failures[:int(initial_ratio*total_failed_devices)] # 0.1 intial failures
        print failures1
        MTTR = 6.6576
        MTBF1 = self.mtbf * MTTR
        MTBF2 = MTBF1/self.cascade_factor
        rand = np.random.RandomState(0)  # universal random seed
        #-----------------------------------------------------------------
        time_between_fails1 = np.random.exponential(MTBF1, total_failed_devices)
        #print ">>>", time_between_fails1
        failure_times1 = []
        last_fail1 = 0
        for t1 in time_between_fails1:
            failure_times1.append(last_fail1 + t1)
            last_fail1 = last_fail1 + t1
        #-----------------------------------------------------------------
        index = -1
        failures2 =  failures[int(initial_ratio*total_failed_devices):] # 0.1 intial failures
        print failures2
        average_cascade = int( (1 - initial_ratio) / initial_ratio)
        for i in range(len(failures1)):
            deviceId = failures1[i]
            fail_time = failure_times1[i]
            print "1-", deviceId, fail_time
            trace_entry.append((fail_time, deviceId))
            #---------------------------------------------------------------
            cascade_time = fail_time
            num_cascades = np.random.choice(range(average_cascade-2, average_cascade+3))
            time_between_fails2 = np.random.exponential(MTBF2, num_cascades)
            for t2 in time_between_fails2:
                cascade_time = cascade_time + t2
                index = index + 1
                if index >= int((1-initial_ratio)*total_failed_devices)-1:
                    break
                cascadeId = failures2[index]
                trace_entry.append((cascade_time, cascadeId))
                print "    2-", cascadeId, cascade_time
        print len(trace_entry)
        return trace_entry
        
        

if __name__ == "__main__":
    sim = Batch(8064, 0.01, 32, 10.0)
    sim.generate_failures()

