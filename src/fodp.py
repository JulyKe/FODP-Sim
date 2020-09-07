#!/usr/bin/python

import numpy as np
from mols import MOLS
import sys
#-----------------------------------------
#  fractional overlap declustered parity
#-----------------------------------------
class FODP:
    def __init__(self, disks, size_set, ratio):
        #----------------------
        # initialize stripesets
        #----------------------
        self.stripesets = []
        #----------------------
        # generate stripesets
        #----------------------
        self.generate_stripesets(disks, size_set, ratio)




    #---------------------------------------------------------------
    # Two ways of generating stripesets: columns and row-columns
    #---------------------------------------------------------------
    def generate_stripesets(self, disks, size_set, ratio):
        self.disk_matrix = np.array(disks).reshape(size_set, len(disks)/size_set)
        print "\n>>>>> Disk Matrix >>>>>\n",self.disk_matrix, "\n"
        #-------------------------------------
        # if the number of disks is not enough
        #-------------------------------------
        if len(disks) < size_set ** 2:
            self.generate_column_stripesets(disks, size_set)
        #--------------
        # otherwise
        #--------------
        else:
            self.generate_column_stripesets(disks, size_set)
            self.generate_row_stripesets(disks, size_set)
        #---------------------------
        # for other MOLS stripesets
        #---------------------------
        if ratio > 1:
            order_n = len(disks) / size_set
            self.generate_MOLS_stripesets(disks, size_set, order_n, ratio-2)


    #---------------------------------------------------------------
    # A set of row based stripesets according to the disk matrix
    #---------------------------------------------------------------
    def generate_row_stripesets(self, disks, size_set):
        for rowId in range(size_set):
            rowSet = self.disk_matrix[rowId,:]
            self.stripesets.append(rowSet.tolist())
        

    #---------------------------------------------------------------
    # A set of column based stripesets according to the disk matrix
    #---------------------------------------------------------------
    def generate_column_stripesets(self, disks, size_set):
        for columnId in range(len(disks)/size_set):
            columnSet = self.disk_matrix[:,columnId]
            self.stripesets.append(columnSet.tolist())
        

    #----------------------------------------------------------------------------------------------------
    # A set of LS that are pairwise orthogonal is called a set of mutually orthogonal Latin squares(MOLS)
    #----------------------------------------------------------------------------------------------------
    def generate_MOLS_stripesets(self, disks, size_set, order_n, new_ratio):
        mols = MOLS(order_n, new_ratio)
        #----------------------------
        # generate coordinate matrix     
        #----------------------------
        for square in mols.squares:
            #print ">>>>>>>>>>>>>>>>>",square
            for array in square:
                stripeset = []
                rowId = 0
                for columnId in array[0:size_set]:
                    stripeset.append(self.disk_matrix[rowId,columnId])
                    rowId += 1
                self.stripesets.append(stripeset)
    

if __name__ == "__main__":
    fodp = FODP(range(28),4, 5)
    count = 0
    for stripeset in fodp.stripesets:
        count += 1
        print ">",stripeset
    print count

