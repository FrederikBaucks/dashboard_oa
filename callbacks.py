from app import app
from dash.dependencies import Input, Output, State

from dash import dcc, html
from dash import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import figures
import get_courses
import dash_bootstrap_components as dbc
from components import colors
import sqlite3
import os
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import plotly.graph_objects as go
import networkx as nx
from course_matrix import net_graph


DATABASE_LOC = 'university.db'
no_stud_chosen = 'no student yet'

# read data from database
conn = sqlite3.connect(DATABASE_LOC)
df_stud = pd.read_sql_query("SELECT student_id, gpa, ability FROM Students", conn)
modul_data = pd.read_sql_query("SELECT course_name," \
                                      "recommended_semester,"\
                                      "credits,"\
                                      "department FROM Courses", conn
                                      )
conn.close()




@app.callback(
    Output('network-graph', 'figure'),
    [Input('student_dropdown', 'value')])
def update_graph(student_id):
    # call the net_graph function to update the graph
    if student_id != 'no student yet':
        fig = net_graph(student_id)
    else:
        fig = net_graph()
    return fig

#Callback for the personal info card to update the information based on the selected student

# @app.callback(
#     Output('personal_info', 'children'),
#     [Input('student_dropdown', 'value')]
# )
# def update_student_info(student_id):
#     if student_id != 'no student yet':
#         student_index = [x for x in range(len(student_data.students)) if student_data.students[x].name == student_id][0]
#         last_semester = max(student_data.students[student_index].times)
#         email = student_id+'@rub.de'
#     else:
#         last_semester = 'None'
#         email = 'None'

#     personal_info_card = dbc.Table(
#                                         [
#                                             html.Tbody(
#                                                 [
#                                                     html.Tr([html.Td("Name:"), html.Td(student_id)]),
#                                                     html.Tr([html.Td("Address:"), html.Td(email)]),
#                                                     html.Tr([html.Td("Student ID:"), html.Td(student_id)]),
#                                                     html.Tr([html.Td("Year of Study:"), html.Td(last_semester)]),
#                                                 ]
#                                             )
#                                         ],
#                                         bordered=True,
#                                         dark=False,
#                                         hover=True,
#                                         responsive=False,
#                                         striped=True,
#                                         id='personal_info'
#                                     )
#     return personal_info_card

@app.callback(
    Output('personal_info_table', 'children'),
    [Input('student_dropdown', 'value')]
)
def update_student_info(student_id):
    if student_id != 'no student yet':
        # call student data from database
        stud_conn = sqlite3.connect(DATABASE_LOC)
        student_data = pd.read_sql_query("SELECT gpa, ability FROM Students WHERE student_id = '" + student_id + "'", stud_conn)
        stud_conn.close()
        try:
            last_semester = student_data['relative_semester']
        except:
            last_semester = np.random.randint(1,12)
        email = student_id+'@edu.de'
    else:
        last_semester = 'None'
        email = 'None'

    new_table_body = html.Tbody(
        [
            html.Tr([html.Td("Name:"), html.Td(student_id)]),
            html.Tr([html.Td("Address:"), html.Td(email)]),
            html.Tr([html.Td("Student ID:"), html.Td(student_id)]),
            html.Tr([html.Td("Year of Study:"), html.Td(last_semester)]),
        ]
    )

    return new_table_body

# @app.callback(
#     Output('academic_history', 'children'),
#     [Input('student_dropdown', 'value')]
# )
# def update_academic_history(student_id):
#     if student_id != 'no student yet':
        
#         student_index = [x for x in range(len(student_data.students)) if student_data.students[x].name == student_id][0]
#         gpa = np.mean(student_data.students[student_index].grades)
#         semester = max(student_data.students[student_index].discreteTimes)
#         ects = 'none'
#         ects_per_semester = 'none'
#     else:
#         gpa = 0
#         semester = 'None'
#         ects = 'None'
#         ects_per_semester = 'None'
#     academic_history_card = dbc.Table(
#                                             [
#                                                 html.Tbody(
#                                                     [
#                                                         html.Tr([html.Td("Average Grade:"), html.Td(round(gpa, 2))]),
#                                                         html.Tr([html.Td("Number of Semesters:"), html.Td(semester)]),
#                                                         html.Tr([html.Td("ECTS:"), html.Td(ects)]),
#                                                         html.Tr([html.Td("ECTS per Semester:"), html.Td(ects_per_semester)]),
#                                                     ]
#                                                 )
#                                             ],
#                                             bordered=True,
#                                             dark=False,
#                                             hover=True,
#                                             responsive=False,
#                                             striped=True,
#                                             id='academic_history',
#                                             style={'margin':0}
#                                         ),
#     return academic_history_card


@app.callback(
    Output('academic_history_table', 'children'),
    [Input('student_dropdown', 'value')]
)
def update_academic_history(student_id):
    if student_id != 'no student yet':
        student_index = [x for x in range(len(df_stud)) if df_stud[student_id][x] == student_id][0]
        gpa = df_stud['gpa'][student_index] #np.mean(student_data.students[student_index].grades)
        semester = np.random.randint(1,12)  #max(student_data.students[student_index].discreteTimes)
        ects = 45
        ects_per_semester = 9
    else:
        gpa = 0
        semester = 1
        ects = 45
        ects_per_semester = 9

    new_table_body = html.Tbody(
        [
            html.Tr([html.Td("Average Grade:"), html.Td(round(gpa, 2))]),
            html.Tr([html.Td("Number of Semesters:"), html.Td(semester)]),
            html.Tr([html.Td("ECTS:"), html.Td(ects)]),
            html.Tr([html.Td("ECTS per Semester:"), html.Td(ects_per_semester)]),
        ]
    )

    return new_table_body


@app.callback(
    Output('textarea', 'value'),
    [Input('student_dropdown', 'value')],
)
def update_output_textarea_save(value):
    filename = 'notes/' + str(value) + '.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write("")  # Writes an empty string to create the file if it doesn't exist
        return ""  # Return an empty string to be displayed in the textarea
    else:
        with open(filename, 'r') as f:
            content = f.read()  # Reads the content of the file
        return content  # Returns the content to be displayed in the textarea

@app.callback(
    Output('student_dropdown', 'value'),  # Output can be a dummy value
    [Input('textarea', 'n_blur')],
    [State('student_dropdown', 'value'),
     State('textarea', 'value')]
)
def save_content(n_blur, value, text_area_value):
    if n_blur:  # if textarea has lost focus
        filename = 'notes/' + str(value) + '.txt'
        with open(filename, 'w') as f:
            f.write(text_area_value)  # Writes the new content to the file
    return value  # Return the value to the dummy output


@app.callback(
    Output('popup_id_next_semester', 'displayed'),
    Input('help_button_next_semester', 'n_clicks'),
)
def show_popup_2(n_clicks):
    if n_clicks is None:
        return False
    else:
        return True



@app.callback(
        Output(component_id='thermo meter', component_property='figure'),
        Input(component_id='possible_courses', component_property='selected_rows'),
        Input(component_id='student_dropdown', component_property='value')
)
def update_chosen_workload(selected_rows, value):
    student_id = value
    courses_to_incl = []
    mu_w = get_courses.get_mean_stud_workload(student_id=student_id)
    for student in student_data.students:
            if student_id==student.name:
                courses_to_incl = get_courses.get_courses_by_student(student)
            
    selected_courses = np.array(courses_to_incl)[selected_rows]
    selected_w = get_courses.get_course_workload_sum(selected_courses)
    fig=figures.get_credit_figure(student_mean=mu_w, recom=30, curr=selected_w)
    return fig


@app.callback(
        Output(component_id='pred_score', component_property='figure'),
        Input(component_id='possible_courses', component_property='selected_rows'),
        Input(component_id='student_dropdown', component_property='value')
)
def update_selection_prob(selected_rows, value):
    if len(selected_rows)>0:
        student_id = value
        for student in student_data.students:
            if student_id==student.name:
                courses_to_incl = get_courses.get_courses_by_student(student)
                gpa = get_courses.get_stud_gpa(student_id=student_id)
        
        
        selected_courses = np.array(courses_to_incl)[selected_rows]
        abi = get_courses.get_abi(student_id)
        #print(abi)
        difs = []
        for course_name in selected_courses:
            difs.append(get_courses.get_mean_diff(course_name))
        pass_prob=1
        for diff in difs:
            pass_prob=pass_prob*get_courses.get_pass_prob(abi, diff)
        figure = figures.get_pred_fig(color=colors.bright_grey, font_color=colors.font_color, pred = pass_prob, mean_stud_perc=gpa)
    else:
        gpa_set=False
        student_id = value
        for student in student_data.students:
            if student_id==student.name:
                gpa = get_courses.get_stud_gpa(student_id=student_id)
                gpa_set=True
        if gpa_set:
            figure = figures.get_pred_fig(color=colors.bright_grey, font_color=colors.font_color, mean_stud_perc=gpa)
        else:
            figure = figures.get_pred_fig(color=colors.bright_grey, font_color=colors.font_color)
    return(figure)




@app.callback(
        Output(component_id='possible_courses', component_property='columns'),
        Output(component_id='possible_courses', component_property='data'),
        Output(component_id='possible_courses', component_property='selected_rows'),
        Input(component_id='student_dropdown', component_property='value'),
        Input(component_id='possible_courses', component_property='selected_rows'),
        Input(component_id='sum_win_slider', component_property='value')
)
def update_possible_courses(stud_value,selected_rows, sem_value):
    selected_student = stud_value
    courses_to_incl=[]
    for student in student_data.students:
        if selected_student==student.name:
            courses_to_incl = get_courses.get_courses_by_student(student)
    temp_df = pd.DataFrame()
    credits = []
    sem = []
    area = []
    if sem_value==1:
        #summer
        odd=False
        no_slider_value = False
    elif sem_value==2:
        #winter
        odd=True
        no_slider_value=False
    else:
        no_slider_value = True

    not_sel_rows = []
    row_count = 0
    sem_filtered_courses = []
    for course in courses_to_incl:
        ind = np.where(modul_data['course_name']==course)[0][0]
        if no_slider_value == False:
            if odd:
                if np.mod(modul_data['recommended_semester'][ind],2) == 0:
                    not_sel_rows.append(row_count)
                    print(no_slider_value, course)
                    continue
            if odd==False:
                if np.mod(modul_data['recommended_semester'][ind],2) == 1:
                    not_sel_rows.append(row_count)
                    print(no_slider_value, course)
                    continue
        sem_filtered_courses.append(course)
        row_count+=1

        credits.append(modul_data['credits'][ind])
        sem.append(modul_data['recommended_semester'][ind])
        area.append(modul_data['department'][ind])
    temp_df['courses'] = sem_filtered_courses
    temp_df['semester'] = sem
    temp_df['credits'] = credits

    if selected_student == 'no student yet':
        abi = -10
    else:
        abi = get_courses.get_abi(selected_student)
    probs = []
    for course_name in sem_filtered_courses:
        diff = get_courses.get_mean_diff(course_name)
        probs.append("{:.1f}".format(100 * get_courses.get_pass_prob(abi, diff)))
    print(probs)
    temp_df['pass prob.'] = probs


    data = temp_df.to_dict('records')
    print(selected_rows)
    if len(selected_rows)>0:
        for elem in not_sel_rows:
            if elem in selected_rows:
                selected_rows.remove(elem)
        sort_selected_rows = []
        #find selected row inds in sem_filtered courses
        sel_course_names = np.array(courses_to_incl)[selected_rows]
        for c_name in sel_course_names:
            #some course is left in semester choice
            if len(np.where(np.array(sem_filtered_courses)==c_name)[0])>0:
                sort_selected_rows .append(np.where(np.array(sem_filtered_courses)==c_name)[0][0])
            #no course is left in semester choice
            else:
                sort_selected_rows=[]
        selected_rows=sort_selected_rows
    else:    
        selected_rows=[]
    columns = [{"name": i, "id": i} for i in temp_df.columns]
    return columns, data, selected_rows


@app.callback(
        Output(component_id='difficulty', component_property='figure'),
        [Input(component_id = 'student_dropdown', component_property = 'value'),
        Input(component_id = 'possible_courses', component_property = 'selected_rows')]
)
def update_diff_figure(value, selected_rows):
    selected_student = value
    red_needed = False
    for student in student_data.students:
        if selected_student==student.name:
            courses_to_incl = get_courses.get_courses_by_student(student)
            #print(courses_to_incl[0])
            courses_to_incl_eng = get_courses.translate_courses(courses_to_incl)
            #print('flag1', courses_to_incl_eng[0])
            red_df  = get_courses.get_red_df(courses_to_incl_eng)
            #print('flag2',red_df.shape)
            red_needed=True
            if len(selected_rows)>0:
                courses_to_incl_eng = np.array(courses_to_incl_eng)[selected_rows]
                red_df  = get_courses.get_red_df(courses_to_incl_eng)
                    
    if red_needed:
        fig = figures.get_diff_fig(red_df)
        #print(red_df.shape)
    #else: 
     #   continue
        #fig = figures.get_diff_fig(df)
    return fig


@app.callback(
        Output(component_id='student_data_table_raw', component_property='data'),
        Output(component_id='student_data_table_raw', component_property='columns'),
        Input(component_id = 'semester-slider', component_property = 'value'),
        Input(component_id = 'student_dropdown', component_property = 'value')
)
def update_table_raw_data(slider_value, student_value):

    enroll_conn = sqlite3.connect(DATABASE_LOC)
    temp_df =  pd.read_sql_query("SELECT * FROM Enrollments WHERE student_id = '" + str(student_value) + "'", conn)
    
    
    # df_stud = pd.read_sql_query("SELECT student_id, gpa, ability FROM Students", conn)
    # modul_data = pd.read_sql_query("SELECT course_name," \
    #                                     "recommended_semester,"\
    #                                     "credits,"\
    #                                     "department FROM Courses", conn
    #                                     )
    conn.close()
    #raw_df = pd.read_csv('data/raw.csv', low_memory=False)
    #selected_student = student_value
    #Find all rows using 'ID' column in raw data that belong to selected student:
    #sel_stud_rows = np.where(raw_df['ID']==selected_student)[0]
    #construct new dataframe with only selected rows:
    #temp_df = raw_df.iloc[sel_stud_rows]
    data = temp_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in temp_df.columns]
    return data, columns



@app.callback(
        Output(component_id='student_data_table', component_property='data'),
        Output(component_id='student_data_table', component_property='columns'),
        Input(component_id = 'semester-slider', component_property = 'value'),
        Input(component_id = 'student_dropdown', component_property = 'value')
)
def update_table_data(slider_value, student_value):
    temp_df = pd.DataFrame()
    selected_student = student_value

    for student in student_data.students:
        if selected_student == student.name:
            credits = []
            for course in student.courseNames:
                ind = np.where(modul_data['course_name']==course)[0][0]
                credits.append(modul_data['credits'][ind])
            credits = np.array(credits)
            if slider_value==1:
                last_semester = np.max(student.discreteTimes)
                c_inds = np.where(student.discreteTimes==last_semester)[0]
                temp_df['courses'] = student.courseNames[c_inds]
                temp_df['semester'] = student.times[c_inds]
                temp_df['credits'] = credits[c_inds]
                temp_df['grades'] = student.grades[c_inds]
            
            else:
                temp_df['courses'] = student.courseNames
                temp_df['semester'] = student.times
                temp_df['credits'] = credits
                temp_df['grades'] = student.grades
    data = temp_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in temp_df.columns]
    return data, columns



@app.callback(
        Output(component_id='student_data_table', component_property='style_data_conditional'),
        Input(component_id = 'student_dropdown', component_property = 'value')
)
def update_table_style_data_conditional(value):
    temp_df = pd.DataFrame()
    selected_student = value
    for student in student_data.students:
        if selected_student == student.name:
            temp_df['courses'] = student.courseNames
            temp_df['semester'] = student.times
            temp_df['grades'] = student.grades
            color = np.zeros(len(student.grades))
            color[student.grades>=50]=1
            color_list=[]
            for i in range(len(color)):
                if color[i]==0:
                    color_list.append('#FF9A6E')
                else:
                    color_list.append('#6EFFA2')
            temp_df['color'] = color_list
        
    style_data_conditional=[{   'if': {'row_index': i, 'column_id': 'grades'},
                                'background-color': temp_df['color'][i], 
                                'color': '#333739'
                            } 
                            for i in range(temp_df.shape[0])
                            ]
   
    return style_data_conditional



#run a @app.callback from the file callbacks.py





@app.callback(
    Output(component_id='gpa_hist', component_property='figure'),
    Input(component_id='student_dropdown', component_property='value')
)
def update_figure(value):
    selected_student=value
    if len(np.array(df_stud[df_stud.student_id == selected_student]['gpa']))>0:
        gpa = float(np.array(df_stud[df_stud.student_id == selected_student]['gpa'])[0])
    else:
        gpa=-100
    fig = figures.get_gpa_fig(df_stud)
    if selected_student!='no_students':
        if gpa!=-100:
            fig.add_vline(x=gpa, line_dash = 'dash', line_color = 'firebrick')
    return fig

@app.callback(
    Output(component_id='work_hist', component_property='figure'),
    Input(component_id='student_dropdown', component_property='value')
)
def update_work_figure(value):
    selected_student=value
    mu_w = get_courses.get_mean_stud_workload(selected_student)
    figure = figures.get_work_fig()
    if value!=no_stud_chosen:
        figure.add_vline(x=mu_w, line_dash = 'dash', line_color = 'firebrick')
    return figure


@app.callback(
    Output(component_id='dd-output-container', component_property='children'),
    Input(component_id='student_dropdown', component_property='value')
)
def update_output(value):
    return f'You have selected student ' + str(value)

