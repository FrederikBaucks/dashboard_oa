import pandas as pd
import numpy as np


def get_courses_by_student(student):
    '''
    Input: 
    student - StudentObject according to Classes

    Output:
    next_courses - list of course names

    Description:
    function extracting potential next courses for a student given the students passed courses, and recommended semester for courses. 
    '''
    modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
    pot_courses = []
    for course in modul_data['Modul']:
        c_inds = np.where(student.courseNames==course)[0]
        if len(c_inds)==0:
            pot_courses.append(course)
        else:
            if (student.grades[c_inds]>=50).any():
                continue
            else:
                pot_courses.append(course)
    return(pot_courses)

def get_red_df(pot_courses):
    '''
    Input: 
    pot_courses - list of courses to reduce the df with

    Output:
    red_df - reduced pandas data frame containg the intersection of course offerings with the given courses

    Decription:
    Reducing the df to according to a list of courses in order to show only relevant courses in the difficult plot. 
    '''
    df = pd.read_csv('data/df.csv')
    # delete_count=0
    delete_list = []
    for row in range(df.shape[0]):
        
        #row=row-delete_count
        #print(row)
        #print(row , df['CO name'].shape)
        row_stays = False
        for course in pot_courses:
            #print('before', course, df['CO name'][row])
            #if course == 'Statistics':
                #print(course, df['CO name'][row], course in df['CO name'][row])
            if course in df['CO name'][row]:
                
                row_stays=True
                #print('true', course, df['CO name'][row])
        if row_stays==False:
            #df = df.drop([row]) 
            #delete_count+=1   
            if row not in delete_list:
                delete_list.append(row)
                #df = df.reset_index(drop=True)   
                #print('false', course, df['CO name'][row])  
            
    #print('c',df.shape)
    return(df.drop(delete_list))

def translate_courses(ger_courses):
    modul_engl = pd.read_csv('data/Pflichtmodule_englisch_short.csv', sep=',')['Modul']
    modul = pd.read_csv('data/Pflichtmodule.csv', sep=';')['Modul']
    engl_names = []
    for ger_c in ger_courses:
        c_ind = np.where(np.array(modul)==ger_c)[0][0]
        engl_names.append(modul_engl[c_ind])
    #print(engl_names)
    return(engl_names)


def reset_y_positions(df):
    
    new_y_position=[]
    course_count=0
    cur_inds  = np.array(df['CO y-position'])[::-1]
    if len(cur_inds)>0:
        for i in range(len(cur_inds)):
            if i>0:
                diff = cur_inds[i]-cur_inds[i-1]
                #print(diff)
                if diff>1:
                    course_count+=1  
            new_y_position.append(i+course_count) 
        df['CO y-position'] = new_y_position[::-1]
    return(df)


def get_abi(student_id):
    df_stud = pd.read_csv('data/df_stud.csv')
    ind = np.where(np.array(df_stud['student_id'])==student_id)[0][0]
    abi = df_stud['ability'][ind]
    return(abi)

def get_mean_diff(course_name):
    df = pd.read_csv('data/df.csv')
    eng_name = translate_courses([course_name])
    rows = []
    for i in range(len(df['CO name'])):
        if 'I' in eng_name[0]:
            dist = ' '
        else:
            dist = ''
        if eng_name[0]+dist in df['CO name'][i]:
            rows.append(i)
    
    diff = np.mean(df['CO difficulty'][rows])
    #print(rows, dist, eng_name[0])
    #print(diff)
    return(diff)

def get_pass_prob(abi, diff):
    prob = (np.exp(abi-diff))/(1+np.exp(abi-diff))
    return prob

def get_course_workload_sum(course_list):
    sum_w = 0
    modul = pd.read_csv('data/Pflichtmodule.csv', sep=';')['Modul']
    credits = pd.read_csv('data/Pflichtmodule.csv', sep=';')['Mind. Umfang Modul (LP)']
    for course in course_list:
        ind = np.where(modul==course)[0][0]
        sum_w+=credits[ind]
    return(sum_w)

def get_mean_stud_workload(student_id):
    mu_w = 0
    student_data = pd.read_pickle('data/AI_raw.pickle')
    for student in student_data.students:
        if student.name == student_id:
            for sem in np.unique(student.discreteTimes):
                sem_inds = np.where(student.discreteTimes == sem)[0]
                passed_inds = sem_inds[np.where(student.grades[sem_inds]>=50)[0]]
                work = get_course_workload_sum(student.courseNames[passed_inds])
                mu_w+=work
            if len(np.unique(student.discreteTimes))>0:
                mu_w = mu_w/len(np.unique(student.discreteTimes))
            else:
                mu_w = 0
    return(mu_w)

def get_all_workloads():
    w = [0] #pd.read_csv('data/df_work.csv')
    #w = w['workload']
    #for student in student_data.students:
    #    w_s = get_mean_stud_workload(student.name)
    #    w.append(w_s)
    return(np.array(w))

def get_first_tries(student):
    first_try_inds = []
    for course in np.unique(student.courseNames):
        inds = np.where(student.courseNames==course)[0]
        if len(inds)>1:
            min = np.argmin(student.discreteTimes[inds]).astype(int)
            min_ind = inds[min]
            first_try_inds.append(min_ind)
        else:
            first_try_inds.append(inds[0])
    return(first_try_inds)


def get_stud_gpa(student_id):
    student_data = pd.read_pickle('data/AI_raw.pickle')
    
    for student in student_data.students:
        first_try_inds = get_first_tries(student)
        if student.name == student_id:
            grades = student.grades[first_try_inds]
            gpa = 100 * len(grades[grades>=50])/len(grades)
            #print(gpa)
            #gpa = np.mean(student.grades)
    return gpa

if __name__ == '__main__':
    modul_data = pd.read_csv('data/Pflichtmodule_englisch_short.csv', sep=',')
    modul_data['Modul']##
    student_data = pd.read_pickle(r'data/AI_raw.pickle')
    s = student_data.students[10]
    get_first_tries(s)
    course=['Objektorientierte Modellierung', 'Hoehere Mathematik I']
    #engl_c  =translate_courses(courses)
    #stud = pd.read_csv('data/df_stud.csv')['student_id'][0]
    #stud = len(student_data.students)
    #abi = get_abi(stud)
    #diff = get_mean_diff(course)
    #print(abi-4, diff, get_pass_prob(abi-4, diff))
    #student_id = '0502icuow'
    #print(get_mean_stud_workload(student_id=student_id))
