# contains classes and helper methods to construct and print Courses, Days, and Weeks

import numpy
import math

def numToTimeS(d):
    minute, hr = math.modf(d)
    am = True
    m = int(minute * 60)
    if m == 0:
        m = "00"
    if hr > 12:
        hr = hr - 12
        am = False
    if hr == 12:
        am = False
    r = str(int(hr)) + ":" + str(m)
    if am == True:
        r += " AM"
    else:
        r += " PM"
    return r

# TODO
# courses can be...
# lecture with section
# seminar

# class Course(object):
    # requirement fulfilled
    # # of credits
    # name
    # id
    # include
    # professors
    # q
    # location
    # semester

# lecture courses...
# can have meetings which are different for section and lecture

# class Lecture(Course):
    # Times
        # Times[0] = lecture times
            # days
            # time start
            # time end
        # Times[1] = section times
            # days
            # time start
            # time end

# seminars...
# only have constant meetings


# class Seminar(Course):
    # days
    # time start
    # time end


class Course(object):
    def __init__(self, name = "default name", meetings = [], start = 0, end = 2, include = False, ID = 00000, profs = None, q = 0):
        self.name = name
        self.meetings = meetings
        self.start = start
        self.end = end
        self.ID = ID
        self.include = include
        if profs == None:
            self.profs = []
        else:
            self.profs = profs
        self.q = q
 
    def printProfs(self):
        st = ""
        for ix, p in enumerate(self.profs):
            if ix < len(self.profs) - 2:
                st += p.name + ", "
            elif ix < len(self.profs) - 1:
                st += p.name + ", and "
            else:
                st += p.name
        return st

    def __str__(self):
        return "\nCourse: " + self.name + "\nMeets: " + str(self.meetings) + "\nBegins: " + numToTimeS(self.start) + "\nEnds: " + numToTimeS(self.end) + "\nID: " + str(self.ID) + "\nIncluded: " + str(self.include) + "\nTaught by: " + self.printProfs() + "\nQ Score: " + str(self.q) + "\n"

    def addProf(self, p):
        try:
            self.profs.append(p)
            if self not in p.courses:
                p.addCourseDirect(self)
        except:
            pass

    def removeProf(self, p):
        try:
            self.profs.remove(p)
            if self in p.courses:
                p.addCourseDirect(self)
        except:
            pass

class Day(object):
    size = 24
    name = "day"
    start = 0.0
    
    def __init__ (self, name, start):
        self.name = name
        self.timeslots = numpy.empty(self.size, dtype=object)
        self.start = start

class Conflict(object):

    def __init__(self, seed):
        self.competitors = [seed]

    def __str__(self):
        st = "Conflicting courses: "
        for c in self.competitors:
            st += (c.name + ";")
        return st

class Week(object):
    def __init__(self):
        self.days = [Day("Monday", 9), Day("Tuesday", 9), Day("Wednesday", 9), Day("Thursday", 9), Day("Friday", 9)]

    def __str__(self):
        st = ""
        for i in range(len(self.days[0].timeslots)):
            s = ""
            for day in self.days:
                if day.timeslots[i] == None:
                    s+= "| No Class "
                elif type(day.timeslots[i]) is Course:
                    s+="| " + day.timeslots[i].name
                else: 
                    con = ""
                    for c in day.timeslots[i].competitors:
                        con += c.name + "; "
                    s+="| conflict between " + con
            st += "| " + numToTimeS((i*.5) + day.start) + " - " + numToTimeS((i*.5) + .5 + day.start) + s + " |\n"
        return st
