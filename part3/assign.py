#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: admysore-hdeshpa-machilla
#
# Based on skeleton code by R. Shah and D. Crandall, January 2021
#

import sys

"""
def ParseFileAndStore():
This function parses the input_file, each line is stored in list
all these lists are stored in one list.
This function returns list of lists.
"""
def ParseFileAndStore(input_file):
    my_file = open(input_file, "r")
    content_list=[]
    while True:
        line = my_file.readline()
        line=line.strip()
        content_list.append((line.split(" ")))
        if not line:
            break
    return content_list[:-1]

"""
def returnStudents(original):
Returns list of students who filled the survey. (start name of every line in file)
"""
def returnStudents(original):
    students=[]
    for i in range(len(original)):
        students.append(original[i][0])
    return students

"""
def returnStudentAndPref(original):
Returns dictionary with keys as students and values names preferred.
"""
def returnStudentAndPref(original):
    pref={}
    for i in range(len(original)):
        pref[original[i][0]]=original[i][1]
    return pref

"""
def returnStudentAndPref(original):
Returns dictionary with keys as students and values names to be excluded.
"""
def returnStudentExcl(original):
    excl = {}
    for i in range(len(original)):
        excl[original[i][0]] = original[i][2]
    return excl

"""
def returnExhaustiveList(students, studentsPref, studentsExcl, naivesol):
this function makes teams of size 1, 2 and 3. it then makes a list of teams that have complaints less than the 
naive solution we have printed first, since the idea is to find solution, with cost decreasing each
time we yeild. We can proceed further from this list of teams in search of more optimal solutions. 
"""
def returnExhaustiveList(students, studentsPref, studentsExcl, naivesol):
    exhaustiveList=[]
    teamsOfOne = successors(students, 1, studentsPref, studentsExcl)
    teamsOfTwo = successors(students, 2, studentsPref, studentsExcl)
    teamsofThree = successors(students, 3, studentsPref, studentsExcl)
    for team in teamsOfOne+teamsOfTwo+teamsofThree:
         if(team[0]<naivesol[1]):
             exhaustiveList.append(team)
    return exhaustiveList

"""
def successors(students, teamsize, studentPref, studentExcl):
according to team size given, it returns list with team combinations of 1/2/3 along with their complaints.
"""
def successors(students, teamsize, studentPref, studentExcl):
    teamsOfOne=[]
    teamsOfTwo=[]
    teamsOfThree=[]
    if(teamsize==1):
        for team in students:
            teamsOfOne.append([returnComplaints(team, studentPref, studentExcl), team])
        return teamsOfOne
    elif(teamsize==2):
        for i in range(len(students)):
            for j in range(i+1, len(students)):
                team=students[i]+'-'+students[j]
                teamsOfTwo.append([returnComplaints(team, studentPref, studentExcl), team])
        return teamsOfTwo
    if(teamsize==3):
        for i in range(len(students)):
            for j in range(i+1, len(students)-1):
                team=students[i]+'-'+students[j]+'-'+students[j+1]
                teamsOfThree.append([returnComplaints(team, studentPref, studentExcl), team])
        return teamsOfThree

"""
def returnStudentDifference(students, visited):
it returns list of names in students that are not in visited.
"""
def returnStudentDifference(students, visited):
     notvisited=[name for name in students if name not in visited]
     if(len(notvisited)<1):
         return []
     else:
         return notvisited

"""
def returnStudentCommon(students, visited):
it returns list of names in students that are in visited.
"""
def returnStudentCommon(students, visited):
    visited = [name for name in students if name in visited]
    if (len(visited) < 1):
        return []
    else:
        return visited

"""
def returnComplaints(team, studentPref, studentExcl):
given a team, this function returns total no of complaints. we first collect students in the team. 
we iterate through students, we calculate complaints in 3 categories, first team size(length difference)
second number of preferred students he didn't get, and third, the excluded students he got. the total cost 
is returned at the end of function. 
"""
def returnComplaints(team, studentPref, studentExcl):
    pref=[]
    complaints=0
    students=team.split("-")
    for name in students:
        pref=studentPref[name].split("-")
        excl=studentExcl[name].split(",")
        if(len(students)!=len(pref)):
            complaints+=1

        notPrefStudents = returnStudentDifference(pref,students)
        complaints+=len(notPrefStudents)
        for i in notPrefStudents:
            if(i=="zzz"):
                complaints=complaints-1

        exclStudents = returnStudentCommon(excl,students)
        complaints += 2*len(exclStudents)
    return complaints

"""
def naiveSolution(students, studentPref):
This function is to print the first naive solution to the user. It just iterates through the students from 
first, and assigns teams according to their preferences. It won't add names if they have already been visited,
and if visited has all the students, it stops and returns the solution.
"""
def naiveSolution(students, studentPref):
    solution=[]
    visited=[]
    team=[]
    sol=""
    index=0
    while(len(visited)<len(students)):
        name=students[index]
        team = studentPref[name].split("-")
        sol=""
        for j in range(len(team)):
            if(team[j]=='zzz'):
                name=returnStudentDifference(students, visited)
                if (len(name)<1):
                    break
                else:
                    sol=sol+name[0]+'-'
                    visited.append(name[0])
            elif team[j] not in visited:
                sol=sol+team[j]+'-'
                visited.append(team[j])
        if len(sol) >0:
            solution.append(sol[:-1])
        index+=1
    return solution

"""
def isIn(visited, membersofItem):
If a name in membersOfItem is there in visited it returns False, else True
"""
def isIn(visited, membersofItem):
    for name in membersofItem:
        if name in visited:
            return False
    return True

"""
def yeildNaiveSolution(students, studentsPref, studentsExcl):
It calls the naive solution method to get the first solution, iterates throught the teams, sums up the 
complaints, and returns a list of naive solution and its total complaints
"""
def yeildNaiveSolution(students, studentsPref, studentsExcl):
    solution = naiveSolution(students, studentsPref)
    total = 0
    for sol in solution:
        c = returnComplaints(sol, studentsPref, studentsExcl)
        total += c
    return [solution, total]

"""
def yeildIntermediateSolution(team, exhaustiveList, students):
With a team sent to function, this function tries to find best possible set of teams with least complaints. 
it picks up choices from exhastive list which has teams of 1,2,3 with complaints less than naive cost. 
it returns the set of teams with total cost.
"""
def yeildIntermediateSolution(team, exhaustiveList, students):
    sol = []
    visited = []
    cost = 0
    sol.append(team[1])
    membersOfTeam = team[1].split("-")
    for s in membersOfTeam:
        visited.append(s)
    for item in exhaustiveList:
        membersOfItem = item[1].split("-")
        if (len(students) == len(visited)):
            break
        if isIn(visited, membersOfItem):
            sol.append((item[1]))
            for name in membersOfItem:
                visited.append(name)
            cost += item[0]

    return [sol,cost]

"""
def solver(input_file):
first we parse the file, we get students, dictionary with preferences and dictionary with exclusions.
We yeild the naive solution to the user, we then make a exhaustive list of teams of size 1,2,3 that have
complaints less than naive. we sort this and make a copy of it in listOfTeams. for each team in listOfTeams
we call the yeildIntermediateSolution, to find the best possible set of teams from choices in exhasutive list.
if the retured solution has complaints less than what we saw till now, we yeild that back to user. 
This stops when we have looked at all teams in listOfTeams or if we have found a solution with zero complaints
"""
def solver(input_file):

    initialStorage=ParseFileAndStore(input_file)
    students=returnStudents(initialStorage)
    studentsPref=returnStudentAndPref(initialStorage)
    studentsExcl=returnStudentExcl(initialStorage)

    naivesol=yeildNaiveSolution(students, studentsPref, studentsExcl)
    first_sol = {"assigned-groups": naivesol[0], "total-cost": naivesol[1]}
    yield (first_sol)

    exhaustiveList= returnExhaustiveList(students, studentsPref, studentsExcl, naivesol)

    minimumComplaints = naivesol[1]
    exhaustiveList.sort()
    listOfTeams = exhaustiveList.copy()

    while listOfTeams:
        if(minimumComplaints != 0):
            team = listOfTeams.pop(0)
            teamsAndCost=yeildIntermediateSolution(team, exhaustiveList, students)
            if (teamsAndCost[1] < minimumComplaints):
                minimumComplaints = teamsAndCost[1]
                interm_sol = {"assigned-groups": teamsAndCost[0], "total-cost": teamsAndCost[1]}
                yield (interm_sol)
        else:
            break

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected an input filename"))

    solver(sys.argv[1])

    for result in solver(sys.argv[1]):
         print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
         print("\nAssignment cost: %d \n" % result["total-cost"])
