import numpy as np
#--------------------------------------------------------------------------------------------------------------------
# MOLS - two latin squares are mutually orthogonal if there exists for each ordered pair (i,j) appeared exactly once
#--------------------------------------------------------------------------------------------------------------------
class MOLS:
    def __init__(self, order_n, num_squares):
        self.squares = []
        self.read_mols_file(order_n)
        for i in range(num_squares):
            self.squares.append(self.create_latin_square(i))


    def read_mols_file(self, n):
        self.latin_squares = {}
        mols_file = "../input/mols"+str(n)
        with open(mols_file,"r") as reader:
            squareId = 0
            nextLines = 0
            for line in reader.readlines():
                #-------------------------------------------------
                if nextLines == n+1:
                    squareId += 1
                #-------------------------------------------------
                if line.strip() == "Latin Square "+str(squareId)+":":
                    print "Square-", squareId
                    self.latin_squares[squareId] = []
                    nextLines = 0
                else:
                    print line.strip()
                    self.latin_squares[squareId].append(line.strip())
                    nextLines += 1
                #-------------------------------------------------
        #print self.latin_squares


    def create_latin_square(self, squareId):
        latin_square = []
        for row in self.latin_squares[squareId]:
            if row == "":
                continue
            array = []
            for num in row.split(","):
                if num != '':
                    array.append(int(num))
            latin_square.append(array)
        return latin_square


if __name__ == "__main__":
    mols = MOLS(7,4)

