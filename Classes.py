import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def newRep (vector):
#Function that gives an int as Semester instead of e.g. 'WS17/18' for the hole array.
    tempVector=np.zeros(len(vector))
    for i in range(len(vector)):
        if vector[i].find('SS')!= (-1):
            tempVector[i] = float(vector[i][2:])
        elif vector[i].find('WS')!= (-1):
            tempVector[i] = float(vector[i][2:4])+0.5
    tempVector = tempVector.astype(np.float)
    #print(vector)
    newVector = np.zeros(len(vector))
    #print(vector)
    start = np.min(tempVector)
    #print(start)
    current=start
    counter = 0
    

    
    while current<=np.max(tempVector):
        indexList = np.where(tempVector==current)
        #print(current, np.max(vector))
        for i in range(len(indexList)):
            newVector[indexList[i]]=counter
                
        counter += 1
        current += 0.5    
    return newVector



class Student:
    def __init__(self, name, grades=[], times=[], discreteTimes=[], courseNames=[], workloads=[], time_rank=[]):
            self.name = name
            self.grades = np.array(grades)
            self.times = np.array(times)
            self.courseNames = np.array(courseNames)
            self.discreteTimes = np.array(discreteTimes)
            self.setDiscreteTimeValueVector()
            self.workloads = np.array(workloads)
            self.workloads = np.zeros(len(self.times))
            self.time_rank = np.zeros(len(self.discreteTimes))
            
    def pop(self, index):
        self.grades=np.delete(self.grades, index)
        self.times=np.delete(self.times, index)
        self.courseNames=np.delete(self.courseNames, index)
        self.discreteTimes=np.delete(self.discreteTimes, index)
        return self.grades, self.times, self.courseNames, self.discreteTimes

    def pop_without_discreteTimes(self, index):
        self.grades=np.delete(self.grades, index)
        self.times=np.delete(self.times, index)
        self.courseNames=np.delete(self.courseNames, index)
        return self.grades, self.times, self.courseNames

    def zero_mean_grades(self):
        gpa = np.mean(self.grades)
        self.grades = self.grades-gpa
        return self.grades 

    def setGrade(self, value):
        self.grades = np.append(self.grades,value)
        return self.grades
    
    def setTime(self, value):
        self.times = np.append(self.times,value)
        return self.times
    
    def setDiscreteTimeValueVector(self):
        if(self.times != []):
            self.discreteTimes = newRep(self.times)
        return self.discreteTimes    
    
    def setExam(self, grade, time, courseName):
        if len(self.grades)!=len(self.times):
            print('Warning: grades and times vectors have different length!', len(self.grades), 'vs.', len(self.times))
        if len(self.grades)!=len(self.courseNames):
            print('Warning: grades and times vectors have different length!', len(self.grades), 'vs.', len(self.courseNames))
        
        self.grades = np.append(self.grades,grade)
        self.times = np.append(self.times,time)
        self.courseNames = np.append(self.courseNames, courseName)
        return self.grades, self.times, self.courseNames
    def setWorkload(self, value):
        self.workloads = np.append(self.workloads,value)
    def getGrades(self):
        print(self.grades)
        return(self.grades)

class StudentGroup:
    def __init__(self, name, members=[], students=[]):
            self.name = name
            self.students = students
            self.members = members
    
    #def __del__(self):
    #    self.students=[]
    #    self.members=[]
    #    print('Destructor called, StudentGroup __',self.name,'__ deleted.')
    
    def append(self, NewStudent):
        self.students.append(NewStudent)
        self.members.append(NewStudent.name)
        return self.students, self.members
		
#	def popStudent(self, Student):
#		self.
		
    
#def intersectionOfGroups(A,B, listOfCourses):#
#	bolA=True
#	bolB=True
#	for course in listOfCourses:
#		for student in A.students:
#		
#			if not course in A.courseNames:
#				bolA=False
#
#	return (intersection)
#
