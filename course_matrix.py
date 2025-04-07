#Import data from data folder
import pandas as pd
import numpy as np
import os
import networkx as nx
DATABASE_LOC = 'university.db'
import sqlite3
# student_data = pd.read_pickle(r'data/AI_raw.pickle')
# courses = pd.read_csv('data/Pflichtmodule.csv', sep=';')

pass_color = '#7bed9a'
import plotly.graph_objects as go
def course_matrix(student_data, courses):
    # Get all courses
    course_names = courses['Modul'].values
    # Construct attendence matrix as numpy array for each student 
    for student in student_data.students:
        attendence_matrix = np.zeros((len(course_names), len(course_names)))
        # Go through each course
        for i, course in enumerate(student.courseNames):
            # Get index of course in course_names
            course_index = np.where(course_names == course)[0][0]
            # First count number of tries of the course and add it to the diagonal
            no_tries = len(student.courseNames[student.courseNames == course])
            attendence_matrix[course_index, course_index] = no_tries

            # Then find courses that were taken after this course using student.discreteTimes and add them to the matrix
            # Get all courses that were taken after this course
            courses_after = student.courseNames[student.discreteTimes == student.discreteTimes[i]+1]
            # Get indices of courses in course_names
            course_indices = np.where(np.isin(course_names, courses_after))[0]
            # Add 1 to the corresponding entries in the matrix
            attendence_matrix[course_index, course_indices] += 1
        print(attendence_matrix)
        # Save matrix as in data/student_matrices/ and construct folder if it does not exist
        if not os.path.exists('data/student_matrices/'):
            os.makedirs('data/student_matrices/')
        np.save('data/student_matrices/'+student.name+'.npy', attendence_matrix)    
    return attendence_matrix
import matplotlib.pyplot as plt


def curved_edges(G, pos, node_trace, edge_pairs, dist_ratio=0.2, bezier_precision=20):
    edge_trace = []
    for edge in G.edges():
        if G.edges[edge]['weight'] > 1:
            u, v = edge
            weight = G[u][v]['weight']-2  # Access the edge's weight directly
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            dx = x1 - x0
            dy = y1 - y0
            dr = np.sqrt(dx*dx+dy*dy) * dist_ratio  # Control point distance
            dtheta = np.arctan2(dy, dx)  # Angle between the 2 points
            theta = np.pi/2 - dtheta  # Perpendicular to the original angle

            # Bezier control point. We add an offset for 'height' based on theta
            cx = (x0 + x1) / 2 + dr * np.cos(theta)
            cy = (y0 + y1) / 2 + dr * np.sin(theta)

            # Generate the Bezier curve
            bezier_curve = np.array(
                [(1-t)**2*np.array([x0,y0]) + 2*(1-t)*t*np.array([cx,cy]) + t**2*np.array([x1,y1]) for t in np.linspace(0, 1, bezier_precision)]
            )
            if u!=v:
                if weight > 1:
                    color = 'orange'
                else:
                    color = '#F2F2F7'
                end = len(bezier_curve)

                #print(edge_pairs, u,v)
                if (u,v) in edge_pairs:
                    edge_trace.append(go.Scatter(x=bezier_curve[:,0], y=bezier_curve[:,1], mode='lines', 
                                            line=dict(color=color, width=weight+5), hoverinfo='none'))  # Use the weight here
                
    for edge in G.edges():
        if G.edges[edge]['weight'] > 1:
            u, v = edge
            weight = G[u][v]['weight']-2  # Access the edge's weight directly
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            dx = x1 - x0
            dy = y1 - y0
            dr = np.sqrt(dx*dx+dy*dy) * dist_ratio  # Control point distance
            dtheta = np.arctan2(dy, dx)  # Angle between the 2 points
            theta = np.pi/2 - dtheta  # Perpendicular to the original angle

            # Bezier control point. We add an offset for 'height' based on theta
            cx = (x0 + x1) / 2 + dr * np.cos(theta)
            cy = (y0 + y1) / 2 + dr * np.sin(theta)

            # Generate the Bezier curve
            bezier_curve = np.array(
                [(1-t)**2*np.array([x0,y0]) + 2*(1-t)*t*np.array([cx,cy]) + t**2*np.array([x1,y1]) for t in np.linspace(0, 1, bezier_precision)]
            )

            # If the vertices are the same, make a loop from u to v
            if u == v:  # loop handling
                t = np.linspace(0, 2*np.pi, bezier_precision*40)
                drop_x = 0.2 * np.sin(t) + x0  # Creating the drop shape along the x-axis
                drop_y = -(0.4 * np.cos(t)) + y0  # Creating the drop shape along the y-axis
                path = list(zip(drop_x, drop_y)) 
                # Get current node corresponding to u
                node = u
                # Get the nodes marker color
                node_color = node_trace.marker.color[node_trace.text.index(node)]

                if node_color != pass_color:
                    if weight > 2:
                        if weight >=3:
                            weight = 3
                        color = 'darkred'
                    elif weight > 1:
                        color = 'red'
                    else:
                        color = 'orange'
                else: 
                    color = 'lightgray'
                
                edge_trace.append(go.Scatter(x=drop_x, y=drop_y, mode='lines', 
                                    line=dict(color=color, width=(weight)*3), hoverinfo='none'))
                #print(weight)
            
            else:
                continue

                
    return edge_trace



def net_graph(student_id='', time_sort=False, ):
    if student_id == '':
        # return empty figure
        fig = go.Figure()
        fig.update_layout(
            title='No student selected',
            title_x=0.5,
            title_y=0.9,
            title_font_size=30,
            showlegend=False,
            plot_bgcolor='white',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        return fig

    # Load the data of courses and student
    conn = sqlite3.connect(DATABASE_LOC)
    course_data = pd.read_sql_query("SELECT course_name," \
                                      "recommended_semester,"\
                                      "credits,"\
                                      "department FROM Courses", conn
                                      )
    
    # att_mat = np.load('data/student_matrices/'+student_id+'.npy')
    stud_group = pd.read_pickle('data/AI_raw.pickle')
    # Find student in student group
    for student in stud_group.students:
        if student.name == student_id:
            stud = student
            break
    #print(att_mat)
    # Create networkx graph

    G = nx.DiGraph() 

    # Add weighted edges
    for i, row in enumerate(att_mat):
        for j, weight in enumerate(row):
            G.add_edge(course_data['course_name'][i], course_data['course_name'][j], weight=weight+1)


    mapping = dict(zip(G, course_data['course_name']))
    G = nx.relabel_nodes(G, mapping)

   
    
    # Create coordinates for the graph nodes 
    pos = {}
    counter = [0,0,0,0,0,0]
    for i in range(len(course_data['course_name'])):
        pos[course_data['course_name'][i]]=(course_data['recommended_semester'][i], counter[course_data['recommended_semester'][i]-1])
        counter[course_data['recommended_semester'][i]-1]+=1

    if time_sort:
        # Create coordinates according to students progress
        pos = {}
        counter = [0,0,0,0,0,0]
        for i in range(len(course_data['course_name'])):
            if course_data['course_name'][i] in stud.courses:
                pos[course_data['course_name'][i]]=(stud.courses[course_data['course_name'][i]]['semester'], counter[stud.courses[course_data['course_name'][i]]['semester']-1])
                counter[stud.courses[course_data['course_name'][i]]['semester']-1]+=1
            else:
                pos[course_data['course_name'][i]]=(0, 0)


    
    for stud in stud_group.students:
        if stud.name == student_id:
            temp = stud
    
    stud = temp
    edge_pairs = []
    cur_semester = -1
    cur_semester = np.max(stud.discreteTimes)
    last_semester = cur_semester-1
    cur_courses = [x for i,x in enumerate(stud.courseNames) if stud.discreteTimes[i] == cur_semester]
    last_courses = [x for i,x in enumerate(stud.courseNames) if stud.discreteTimes[i] == last_semester]
    # Translate these courses to the corresponding nodes
    cur_nodes = [x for x in G.nodes if x in cur_courses]
    last_nodes = [x for x in G.nodes if x in last_courses]

    # Define nodes data for Plotly
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)


    node_trace = go.Scatter(
                                x=node_x, y=node_y,
                                mode='markers + text',
                                hoverinfo='text',
                                text=list(G.nodes()), 
                                textposition='middle center',  
                                textfont=dict(
                                    family="sans serif",
                                    size=14,
                                    color="black"
                                ),
                                marker=dict(
                                    showscale=False,
                                    #colorscale='YlGnBu',
                                    reversescale=True,
                                    color=['darkgrey' for i in range(len(G.nodes))],
                                    size=40,
                                    #colorbar=dict(
                                    #    thickness=15,
                                    #    title='Node Connections',
                                    #    xanchor='left',
                                    #    titleside='right'
                                    #),
                                    line_width=[0 for i in range(len(G.nodes))]))
    
    # Cange Node Color to green if corresponding course (text) is passed by student
    upd_colors = []
    line_width = []
    for i, node in enumerate(node_trace['text']):
        # Find highest grade corresponding to course in stud courses
        course_inds = [i for i, x in enumerate(stud.courseNames) if x == node]
        if len(course_inds) == 0:
            upd_colors.append('lightgrey')
            continue
        grade = max(stud.grades[course_inds])
        if grade >= 50:
            upd_colors.append('#7bed9a')
            # Change color of i-th position in the node_trace['marker']['color'] tuple to green
            continue
        else: 
            upd_colors.append('#ed7f7b')
    for node in G.nodes():
        if node in cur_nodes:
            # line_width = 1
            line_width.append(2)
        else:
            line_width.append(0)
    node_trace['marker']['color'] = upd_colors
    node_trace['marker']['line_width'] = line_width

    

    #print(cur_nodes)
    #print(last_nodes)
    # Create edge pairs
    for cur_node in cur_nodes:
        for last_node in last_nodes:
            edge_pairs.append((last_node, cur_node))
    #print(edge_pairs)


    edge_trace = curved_edges(G, pos, node_trace, edge_pairs)
    #print(edge_trace)
    

    
    #print([x for x in G.edges.data() if x[2]['weight'] > 1])
    # Create final layout
    figure = go.Figure(data=edge_trace ,
                       layout=go.Layout(
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),
                       )
    # Add edges to the figure
    figure.add_traces([node_trace])
    #Set background color
    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)'
    )
    # Double figure height
    figure.update_layout(
        autosize=True,
    )

        
    

    return figure

    
if __name__ == '__main__':
    stud_id = student_data.students[3].name
    fig = net_graph(stud_id)
    
    fig.show()