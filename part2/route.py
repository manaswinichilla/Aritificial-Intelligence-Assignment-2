#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by:  admysore-hdeshpa-machilla
#
# Based on skeleton code by R. Shah and D. Crandall, January 2021
#

import sys
from heapq import *
import math

"""
def ParseFileAndStore():
This function parses the road-segments.txt, each line is stored in list
all these lists are stored in one list.
This function returns list of lists.
"""
def ParseFileAndStore():
    my_file = open("road-segments.txt", "r")
    content_list=[]
    while True:
        line = my_file.readline()
        line=line.strip()
        content_list.append((line.split(" ")))
        if not line:
            break
    return content_list[:-1]

"""
def successors(map, start):
returns Successors of a particular city sent as start. it traverses through the map, considers
the bi-directional nature of entries given, and returns list of lists of successors. 
each list in list of lists, will have next city, distance, speed, highway.
"""
def successors(map, start):
    successorsList=[]
    l=[]
    for i in range(len(map)):
        if(map[i][0]==start):
            successorsList.append([map[i][1], map[i][2], map[i][3], map[i][4]])
        elif(map[i][1]==start):
            successorsList.append([map[i][0], map[i][2], map[i][3], map[i][4]])
    return successorsList

"""
def NotinVisited(visited,next):
entry sent as next, will return false if next exits in visited, else True 
"""
def NotinVisited(visited,next):
    for i in visited:
        if(next[0]==i[1]):
            return False
    return True

"""
def returnSafe(next):
for some state next, we calculate the safe according to highway taken and returns value
"""
def returnSafe(next):
    if next[3].startswith("I-"):
        return int(next[1]) * (math.pow(10,-6))
    else:
        return int(next[1]) * (0.5 * math.pow(10,-6))

"""
def hOfs(map,start, end, cost):
This function, takes map , start, end, and cost. finds solution between start and end, using A*.
in each iteration, when entry is being pushed in fringe distance, segments, safe, and time are calculated
and stored in fringe. According to cost function, when goal is reached, respective value is returned. 
If no solution then -1 is returned.
In the get_route function this hOfs is called with start as the goal city and end as current city in
consideration. this is added with gOfs to form complete heuristic
"""
def hOfs(map,start, end, cost):
    fringe,visited = [],[]
    time,dist,safe,seg,costValue = 0,0,0,0,0
    fringe = [[costValue, start, seg, time, dist, safe]]
    heapify(fringe)
    while fringe:
        (costValue, start, seg, time, dist, safe) = heappop(fringe)
        visited.append([costValue, start, seg, time, dist, safe])
        t = time
        s = safe
        for next in successors(map, start):
            if next[0] == end:
                dist += int(next[1])
                time = t + (int(next[1]) / (int(next[2])))
                safe = s + returnSafe(next)
                seg+=1
                if(cost=="segments"):
                    return seg
                if(cost=="distance"):
                    return dist
                if(cost=="time"):
                    return time
                if(cost=="safe"):
                    return safe

            elif NotinVisited(visited, next):
                time = t + (int(next[1]) / int(next[2]))
                costValue = gOfs(map, end, seg-1, dist, next, cost)
                safe = s + returnSafe(next)
                data = [costValue, next[0], seg+1, time, dist + int(next[1]), safe]
                heappush(fringe, data)
    return -1

"""
def gOfs(map, end, length, dist, next, cost):
returns the distance, segments, safe length value of start city till current city under consideraton(next)
according to the cost respectively. 
"""
def gOfs(map, end, length, dist, next, cost):
    if cost=="segments":
        return length
    elif cost=="distance":
        return dist+int(next[1])
    elif cost=="time":
        return int(next[1])/int(next[2])
    elif cost=="safe":
        return returnSafe(next)

"""
def get_route(start, end, cost): 
get route starts from start state, adds it to fringe along with costValue, route_taken, time, 
 distance, safe, and highway. while the fringe is not empty, fringe with least costValue is popped, and
 the city(start) is added to visited. we explore the successors from here, if we find the goal state we return 
 the solution. If not, if the city is not already visited, route_taken, safe, distance, are updated
 Costvalue is g(s)+h(s) where g(s) is value(distance, segments, time or safe) from start to current
 and h(s), is value from end city to current state. All this data along with city are added to fringe. 
 This is continued untill end city is found or fringe is empty. if no solution is found [] is returned.   
"""
def get_route(start, end, cost):
    map=ParseFileAndStore()
    fringe,visited=[],[]
    route_taken=[]
    highway=""
    time,dist,safe,costValue=0,0,0,0
    fringe=[[costValue, start, route_taken, time, dist, safe, highway]]
    heapify(fringe)
    while fringe:
        (costValue, start, route_taken, time, dist,safe, highway)=heappop(fringe)
        route = (start, highway + " for " + str(dist) + " miles")
        route_taken.append(route)
        visited.append([costValue, start, route_taken, time, dist, safe])
        rt=route_taken
        t=time
        s=safe
        for next in successors(map, start):
            if next[0]==end:
                route = (next[0], next[3] + " for " + str(next[1]) + " miles")
                route_taken.append(route)
                route_taken.pop(0)
                time = t + (int(next[1]) / (int(next[2])))
                safe = s + returnSafe(next)
                return {"route-taken": route_taken,
                        "total-segments": len(route_taken),
                        "total-miles" : float(dist + int(next[1])),
                        "total-hours" : float(time),
                        "total-expected-accidents": float(safe)
                         }

            elif NotinVisited(visited,next):
                h=hOfs(map, end, next[0], cost)
                if h!=-1:
                    time=t+(int(next[1])/int(next[2]))
                    costValue=h+gOfs(map, end, len(route_taken)-1, dist, next, cost)
                    safe=s+returnSafe(next)
                    highway=next[3]
                    data=[costValue, next[0], route_taken , time, dist+int(next[1]),safe,highway]
                    heappush(fringe,data)
    return []


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv

    if cost_function not in ("segments", "distance", "time", "safe"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])
