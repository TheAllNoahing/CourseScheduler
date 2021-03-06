# contains functions to process and display data from settings after modification by subfile.py functions

import courses as src
import gui
import settings, subfile

useGUI = True

# use for stub-code
def donothing():
    pass

def coursesToStr():
    courses = settings.courses
    if len(courses) == 0:
        return "No Courses Loaded"
    st = ""
    for c in courses:
        st += str(c)
    return st

def scheduleToStr():
    st = ("| Time | Monday | Tuesday | Wednesday | Thursday | Friday |\n")
    st += str(updateWeek())
    return st

def profsToStr():
    st = ""
    for p in settings.professors:
        st += str(p)
    return st

def openGUI():
    app = gui.SchedulerAppGUI()
    app.mainloop()

def help():
    with open("help.txt", r) as help:
        print(help)

def viewSelected():
    courses = settings.courses
    for c in courses:
        if c.include:
            print(c)
        else:
            continue

def viewCourses():
    if len(settings.courses) == 0:
        print("No Courses")
    else:
        for c in settings.courses:
            print(c)

def viewProfs():
    for p in settings.professors:
        print(p)

def updateWeek():
    # start with a blank week
    wk = src.Week()
    for course in settings.courses:
        for meeting in course.meetings:
            for day in wk.days:
                if meeting == day.name:
                    # check times
                    for indx, time in enumerate(day.timeslots):
                        if indx >= (course.start - 9) * 2 and indx < (course.end - 9) * 2:
                            if type(time) is src.Course:
                                if time is course and course.include == True:
                                    pass
                                elif time is course and course.include == False:
                                    day.timeslots[indx] = None
                                elif course.include == True:
                                    day.timeslots[indx] = src.Conflict(time)
                                    day.timeslots[indx].competitors.append(course)
                                else:
                                    pass
                            elif type(time) is src.Conflict:
                                if course in time.competitors and course.include == True:
                                    pass
                                elif course in time.competitors and course.include == False:
                                    day.timeslots[indx].competitors.remove(course)
                                    if len(day.timeslots[indx].competitors) == 1:
                                        day.timeslots[indx] = day.timeslots[indx].competitors[0]
                                elif course.include == True:
                                    day.timeslots[indx].competitors.append(course)
                                else:
                                    pass
                            elif course.include == True:
                                day.timeslots[indx] = course
                            else:
                                pass
    return wk

# TODO: make header modular based on # of timeslots
def viewSchedule():
    print("| Day | 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
           " 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
           " 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM | 7:00 - 7:30 PM |" +
           " 7:30 - 8:00 PM | 8:00 PM - 8:30 PM | 8:30 - 9:00 PM |\n")
    print(updateWeek())

# for command-line interface
def editSInput():
    action = raw_input("| Include | Exclude | Replace | Clear | Back | Help |")
    if action == "Include":
        include()
    elif action == "Exclude":
        exclude()
    elif action == "Replace":
        exclude()
        include()
    elif action == "Clear Courses":
        answer = raw_input("Are you sure you want to clear the schedule? This change is irreversible. Y/N")
        if answer == "Y":
            print("Clearing...")
            waitForInput(excludeAll())
        elif answer == "N":
            editSInput()
        else:
            print("Did not understand input, returning to edit menu.")
            editSInput()
    elif action == "Back":
        waitForInput()
    elif action == "Help":
        help()
    else:
        print("Command not recognized, please try again")
        editSInput()
    waitForInput(updateWeek())

def editSchedule():
    print("|__ Current Schedule __|")
    viewSchedule()
    editSInput()

def weekToMarkdown():
    mkd = ("| Time | Monday | Tuesday | Wednesday | Thursday | Friday |\n" +
           ("|---" + ("|---" * 4) + "|---|\n"))
    return (mkd + str(updateWeek()))

# for command-line interface
def waitForInput():
    action = raw_input("| Random | Reset to Default | Add Professor | Assign Professor | Remove Professor | Add Course | Remove Course | View Courses | View Professors | View Schedule | Edit Schedule | Save | Quit | Help |\n")
    if action == "Random" or action == "rand":
        subfile.randomSession()
        waitForInput()
    elif action == "Add Professor" or action == "ap":
        subfile.addProf()
        waitForInput()
    elif action == "Assign Professor" or action == "asp":
        subfile.assignProf()
        waitForInput()
    elif action == "Remove Professor" or action == "rp":
        subfile.deleteProf()
        waitForInput()
    elif action == "Add Course" or action == "Add" or action == "a":
        subfile.addCourse()
        waitForInput()
    elif action == "Remove Course" or action == "Remove" or action == "r":
        subfile.removeCourse()
        waitForInput()
    elif action == "View Courses" or action == "View C" or action == "vc":
        viewCourses()
        waitForInput()
    elif action == "View Professors" or action == "vp":
        viewProfs()
        waitForInput()
    elif action == "Edit Courses" or action == "Edit C" or action == "ec":
        pass
    elif action == "View Schedule" or action == "View S" or action == "vs":
        viewSchedule()
        waitForInput()
    elif action == "Edit Schedule" or action == "Edit S" or action == "es":
        subfile.editSchedule()
        waitForInput()
    elif action == "Help" or action == "h":
        pass
    elif action == "Reset to Default" or action == "rd":
        subfile.default()
        waitForInput()
    elif action == "Quit" or action == "q":
        print("Exiting...")
        subfile.saveCourses()
        quit()
    elif action == "Save" or action == "s":
        print("Saving...")
        try:
            subfile.saveCourses()
        except:
            print("Save unsuccessful")
            waitForInput()
        print("Save successful!")
        waitForInput()
    else:
        print("Command not recognized. Try again, or enter 'Help' for instructions.")
        waitForInput()

def main():
    settings.init()
    subfile.loadCourses()
    # subfile.default()
    if useGUI == True:
        openGUI()
    else:
        waitForInput()

if __name__ == "__main__":
    main()
