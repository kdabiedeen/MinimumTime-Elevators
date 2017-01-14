#Kevin Dabiedeen
#108686247

import copy
import sys

class Elevator(object):
    currentFloor = 0
    up = True
    number = 0
    bottom = 0
    top = 0

    def __init__(self, number, bottom, top):
        self.currentFloor = int(bottom)
        self.number = int(number)
        self.bottom = int(bottom)
        self.top = int(top)

def make_elevator(number, bottom, top):
    elevator = Elevator(number, bottom, top)
    return elevator

timeList = list()

def run_simulation(time, curr, topFloor, arr, prev, visitedList):
    global timeList
    if(curr == topFloor):
        timeList.append(time)
        return time
    else:
        waiting = int(-1)
        timePass = int(-1)
        for e in arr:
            visited = False
            if e.number in visitedList:
                visited = True
            if((curr == e.bottom or curr == e.top) and e.number != prev.number and not visited):
                visitedList.append(e.number)
                x = copy.deepcopy(arr)
                timeWait = -1

                if((e.currentFloor == e.bottom and e.up == True) or (e.currentFloor == e.top and e.up == False)):
                    timeWait = 0
                else:
                    if(e.up == True):
                        timeWait = (e.top - e.currentFloor) + (e.top - e.bottom)
                    else:
                        timeWait = (e.currentFloor - e.bottom)

                timePass = e.top - e.bottom

                for j in range(0, timePass + timeWait):
                    x = updateElevators(1, x, time + j)

                if(curr == e.top):
                    timePass = 0 - timePass

                run_simulation(time + abs(timePass) + timeWait, curr + timePass, topFloor, x, e, visitedList)

def updateElevators(time, arr, mi):
    for elv in arr:
        elv = cycleElevator(elv, time)
    return arr

def cycleElevator(elv, time):
    cycles = time  / (elv.top - elv.bottom)
    unit = time % (elv.top - elv.bottom)

    while(cycles > 0):
        if(elv.up == True):
            elv.currentFloor = elv.top
        else:
            elv.currentFloor = elv.bottom
        elv.up = not elv.up
        cycles -= 1

    if(elv.currentFloor == elv.bottom and elv.up == False):
        elv.up = True
    elif(elv.currentFloor == elv.top and elv.up == True):
        elv.up = False;

    if(elv.up == True):
        elv.currentFloor += unit
    else:
        elv.currentFloor -= unit

    return elv

f = open(str(sys.argv[1]), "r")
i = 0;

numOfElevators = -1
topFloor = -1
elevArray = []

for line in iter(f):
    if(i == 0 and line.strip()):
        topFloor = int(line[4:line.index(")")])
        i += 1
    elif(i == 1 and line.strip()):
        numOfElevators = int(line[10:line.index(")")])
        i += 1
    elif(line.strip()):
        values = line[9:line.index(")")].split(",")
        j = 0;
        number = -1;
        bottom = -1;
        top = -1;
        for tup in values:
            if(j == 0):
                number = tup
            elif(j == 1):
                bottom = tup
            else:
                top = tup
            j += 1
        elev = make_elevator(number,bottom,top)
        elevArray.append(elev)
        i += 1
number = run_simulation(0, 0, int(topFloor), elevArray, make_elevator(-1, -1, -1), list())
y = min(int(s) for s in timeList)
print "min_time(" + str(y) + ")."

f.close()
