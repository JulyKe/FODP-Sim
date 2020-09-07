import sys
import argparse
import numpy as np
from multiprocessing.pool import ThreadPool
from simulate import Simulate

def setup_parameters():
    #----------------------------------
    # add arguments from command line
    #----------------------------------
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-T', type=float, help="mission time", default=24)
    parser.add_argument('-addT', type=eval, help="add tier", choices=[True, False], default=False)
    parser.add_argument('-plus1', type=eval, help="plus one", choices=[True, False], default=False)
    parser.add_argument('-useP', type=eval, help="use priority", choices=[True, False], default=False)
    #------------------------------------------------------------------------------
    parser.add_argument('-M', type=int, help="#servers/machines", default=2)
    parser.add_argument('-D', type=int, help="#disks per server", default=20)
    parser.add_argument('-S', type=int, help="#spares per server", default=4)
    #------------------------------------------------------------------------------
    parser.add_argument('-kt', type=int, help="#top data chunks",default=2)
    parser.add_argument('-mt', type=int, help="#top parity chunks",default=1)
    parser.add_argument('-kb', type=int, help="#bottom data chunks",default=2)
    parser.add_argument('-mb', type=int, help="#bottom parity chunks",default=2)
    #------------------------------------------------------------------------------
    parser.add_argument('-ft', type=int, help="top fraction",default=1)
    parser.add_argument('-fb', type=int, help="bottom fraction",default=3)
    #------------------------------------------------------------------------------
    parser.add_argument('-typet', type=int, help="top placement type",default=1)
    parser.add_argument('-typeb', type=int, help="bottom placement type",default=1)
    #------------------------------------------------------------------------------
    parser.add_argument('-percent', type=float, help="failure percent",default=0.5)
    parser.add_argument('-rebuildIO', type=int, help="rebuild IO (MB/s)",default=50)
    parser.add_argument('-slaTime', type=int, help="SLA time (h)",default=0)
    parser.add_argument('-copybackIO', type=int, help="copyback IO (MB/s)",default=200)
    parser.add_argument('-networkBW', type=float, help="network bandwidth (Gbits/s)",default=1)
    #------------------------------------------------------------------------------
    parser.add_argument('-diskCap', type=float, help="disk capacity (TB)",default=16)
    parser.add_argument('-useRatio', type=float, help="disk used ratio",default=1.0)
    #------------------------------------------------------------------------------
    args = parser.parse_args()
    return args



def start(tasks_per_worker):
    (iterations_per_worker, traces_per_worker, mission_time, add_tier, plus_one, use_priority, num_servers, num_disks_per_server, num_spares_per_server, kt, mt, kb, mb, ft, fb, failure_percent, top_type, bottom_type, rebuildIO, slaTime, copybackIO, networkBW, diskCap, useRatio) = tasks_per_worker
    #------------------------------------
    # Initialize the simulation and run 
    #------------------------------------
    sim = Simulate(mission_time, add_tier, plus_one, use_priority, num_servers, num_disks_per_server, num_spares_per_server, kt, mt, kb, mb, ft, fb, failure_percent, top_type, bottom_type, rebuildIO, slaTime, copybackIO, networkBW, diskCap, useRatio)
    return sim.run_simulation(iterations_per_worker, traces_per_worker)


if __name__ == "__main__":
    #-------------------------------
    # >>> get the configurations >>>
    #-------------------------------
    args = setup_parameters()
    params = (args.T, args.addT, args.plus1, args.useP, args.M, args.D, args.S, args.kt, args.mt, args.kb, args.mb, args.ft, args.fb, args.percent, args.typet, args.typeb, args.rebuildIO, args.slaTime, args.copybackIO, args.networkBW, args.diskCap, args.useRatio)
    #---------------------------------------
    # calculate iterations per thread worker
    #---------------------------------------
    modelfile = open("model.txt",'a')
    total_iterations = 1
    num_threads = 1
    if total_iterations % num_threads != 0:
        print "totoal iterations should be divided by the number of threads"
        sys.exit(2)
    iterations_per_worker = [total_iterations / num_threads] * num_threads
    #----------------------------------------
    # assign different tasks for diff workers
    #----------------------------------------
    num_traces = 1
    traces_per_worker = np.split(np.arange(num_traces), num_threads)
    #----------------------------------------
    # assign the parameters for the workers
    #----------------------------------------
    tasks_per_worker = zip(iterations_per_worker, traces_per_worker)
    for workId in range(len(tasks_per_worker)):
        tasks_per_worker[workId] += params
    #----------------------------------------
    # start the simulation for diff workers
    #----------------------------------------
    pool = ThreadPool(num_threads)
    results = pool.map(start, tasks_per_worker)
    pool.close()
    pool.join()
    #----------------------------------------
    # collect the final results from workers
    #----------------------------------------
    prob_sum = 0
    local_sum = 0
    global_sum = 0
    loss_sum = 0
    for each in results:
        #-------------------------------
        print ">>>> each result", each
        for value in each:
            local_sum += value[1]
            global_sum += value[2]
            if len(value[3].keys())!= 0:
                prob_sum += 1
            loss_sum += value[4]
        #-------------------------------
    formatted_prob = float("{:.6f}".format(float(prob_sum)*100/total_iterations))
    formatted_local = float("{:.6f}".format(float(local_sum)*100/total_iterations))
    formatted_global = float("{:.6f}".format(float(global_sum)*100/total_iterations))
    formatted_loss = 0
    if prob_sum != 0:
    	formatted_loss = float("{:.6f}".format(float(loss_sum)*100/prob_sum))
    print ">>>>>>>>>>>>>>>> * final prob * ", formatted_prob, formatted_loss
    modelfile.write("- %f, %d, %d, %d, %f, %f\n" % (args.percent, args.fb, args.ft, args.typeb, formatted_prob, formatted_loss))
    modelfile.close()

