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
import math
import numpy as np

class Edge:
    def __init__ (self, origin=None, destination=None):
        self.origin = origin
        self.weight = 1 
        self.destination = destination

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.weight, self.destination)

    # Compare edges based on origin and destination
    def __eq__(self, other): 
        return (self.origin == other.origin) and (self.destination == other.destination)

    # This ensures edges with the same origin and destination are treated as equal in a set or dict
    def __hash__(self):
        return hash((self.origin, self.destination))        


class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0   
        self.pageIndex = 0

    def __repr__(self):
        return f"{self.code}\t{self.outweight}\t{self.name}"
    
    def add_destination(self, destination_airport, weight=1):
        """
        Adds a destination airport to the current airport.
        If the destination already exists, the weight is increased.
        
        Parameters:
        destination_airport: Airport
            The destination airport to which a route is being added.
        weight: int, optional
            The weight of the route (default is 1). Used for calculating distance or cost.
        """
        # Check if the destination is already in the routes list
        if destination_airport.code in self.routeHash:
            # If already exists, update the weight
            self.routeHash[destination_airport.code] += weight
        else:
            # If not, add the new destination and initialize its weight
            self.routes.append(destination_airport)
            self.routeHash[destination_airport.code] = weight

        # Optionally update the outgoing weight (outweight) if needed (e.g., for routing calculations)
        self.outweight += weight


edgesHash = dict() # hash key origin IATA code -> weight
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
    print(f"Reading Routes file from {fd}")
    routesTxt = open(fd, "r", encoding="utf-8");
    missing_IATA_code = {"origin" : [], "destination" : []}
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            origin = temp[2]
            destination = temp[4]

            # ensure that origin and destination have the correct format
            if len(origin) == 3 and origin.isalpha() and len(destination) == 3 and destination.isalpha():
                if origin not in airportHash:
                    missing_IATA_code["origin"].append(destination)
                    new_airport = Airport(origin, "NaN")
                    airportHash[origin] = new_airport
                    airportList.append(new_airport)

                elif destination not in airportHash:
                    missing_IATA_code["destination"].append(origin)
                    new_airport = Airport(destination, "NaN")
                    airportHash[destination] = new_airport
                    airportList.append(new_airport)                 

                airportHash[origin].add_destination(airportHash[destination])
        except Exception as inst:
            pass

    print(f"There are {len(missing_IATA_code["origin"])} origin and {len(missing_IATA_code["destination"])} destinations")
        
def computePageRanks(airports_list, airport_hash, epsilon=1e-2, L=0.85, max_iter=100):
    n = len(airports_list)
    
    # New weights for airports
    P = np.ones(n) / n

    # Create a random teleportation vector (1-L)/n to be added each time
    teleport = (1 - L) / n
    
    # Iterate for a maximum of `max_iter` iterations or until convergence
    for iteration in range(max_iter):
        # Initialize the new PageRank vector Q with zeros
        Q = np.zeros(n)
        
        # For each node i, calculate the new PageRank value
        for j in range(n):
            link_sum = 0
            for airport in airportList:
                for code, weight in airport.routeHash.items():
                    link_sum += (airport_hash[code].pageIndex * weight) / airport.outweight
            
            # Update the PageRank value for node i (equation 8 and 9)
            Q[j] = L * link_sum + teleport
        
        # Check if the difference between the new and old PageRank vectors is smaller than epsilon
        if np.linalg.norm(Q - P, 1) < epsilon:
            print(f"Converged after {iteration + 1} iterations")
            return Q
        
        # Update P to the new PageRank vector Q for the next iteration
        P = Q
    
    # If we reach the maximum number of iterations, we return the result
    print(f"Reached max iterations ({max_iter})")
    return Q

def outputPageRanks():
    page_rank_list = [(airport.pageIndex, airport.name) for airport in airportList]
    page_rank_list.sort(key=lambda x: x[0], reverse=True)
    
    return page_rank_list

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks(airportList, airportHash)
    time2 = time.time()
    iterations
    """
    outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)
    """


if __name__ == "__main__":
    main()
