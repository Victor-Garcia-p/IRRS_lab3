"""
Complete/modify the provided python program so it
    reads airports.txt and routes.txt into appropriate data structures,
    computes the page rank of every airport, and
    writes down a list of pairs (page rank, airport name) ordered by decreasing page rank

    Challenge: deal with sink nodes (airport with no flights departing but some flights arriving).
    When we have adjencency matrix and we normalize we will do 0/0. How to solve this?
"""

#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None, destination=None):
        self.origin = origin
        self.weight = 1 
        self.destination = destination

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.weight, self.destination)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0   

    def __repr__(self):
        return f"{self.code}\t{self.pageIndex}\t{self.name}"

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r", encoding="utf-8");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')

            # do not consider airports without IATA code
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print(f"There were {cont} Airports with IATA code")


def readRoutes(fd):
    print("Reading Routes file from {fd}")
    # write your code

def computePageRanks():
    # write your code
    """
    1. n = number of vertices in G;
    2. P = any vector of length n and sum 1 (for example, the all 1/n vector);
    3. L = the chosen damping factor, between 0 and 1;
    4. while (not stopping condition) {
    5. Q = the all-0 n-vector;
    6. for i in 0..n-1 {
    7. Q[i] = L * sum { P[j] * w(j,i) / out(j) :
    8. there is an edge (j,i) in G }
    9. + (1-L)/n;
    10. }
    11. P = Q;
    12. }
    """

def outputPageRanks():
    # write your code
    print("h")
    return 0

def main(argv=None):
    readAirports("airports.txt")
    
    """
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)
    """


if __name__ == "__main__":
    main()
