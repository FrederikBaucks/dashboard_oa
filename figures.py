import get_courses 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
# Incorporate data
# df = pd.read_csv('data/df.csv')
# modul_data = pd.read_csv('data/Pflichtmodule.csv', sep=';')
# df_stud = pd.read_csv('data/df_stud.csv')
conn = sqlite3.connect('university.db')
df_stud = pd.read_sql_query("SELECT student_id, gpa, ability FROM Students", conn)
conn.close()
# student_data = pd.read_pickle(r'data/AI_raw.pickle')

def get_diff_fig(df):

    
    
#        for i in range(len(df['CO y-position'])):
    df = get_courses.reset_y_positions(df)
    
 #           if i>0:
  #              if (df['CO y-position'][i]-df['CO y-position'][i-1])>1:
   #                 course_count+=1    
    #        new_y_position.append(i+course_count)    
    #
    #print(new_y_position)
    fig = px.scatter(df, x='CO difficulty', y='CO y-position', color='covid_item',
                     width=500, height=max(300,30*df.shape[0]))
    #styling markers:
    fig.update_traces(
        marker=dict(size=8, symbol="hourglass", line=dict(width=0)),
        selector=dict(mode="markers"),
    )
    fig.update_yaxes(visible=True, showticklabels=True)
    fig.update_layout(
        yaxis = dict(
                    tickmode='array', #change 1
                    tickvals = df['CO y-position'], #change 2
                    ticktext = df['CO name'], #change 3
                    tickfont = dict(size=11)
                        ),
        yaxis_title=None
    )
    fig.add_traces([go.Scatter(x = -df['ci_min'], y = df['CO y-position'],
                            mode = 'markers', line_color = 'rgb(0, 0, 0, 0)',
                            #marker type 
                            marker_symbol = 'line-ew-open',
                            showlegend = False),
                    go.Scatter(x = -df['ci_max'], y = df['CO y-position'],
                            mode = 'markers', line_color = 'rgb(0, 0, 0,0 )',
                            marker_symbol = 'line-ew-open',
                            name = '95% confidence interval',
                            fill='tonexty', fillcolor = 'rgba(255, 0, 0, 0.2)')])
    return(fig)

def get_pred_fig(color, font_color, pred=0, mean_stud_perc=0):
    cred_pos = 0.92/100 
    fig = go.Figure(go.Indicator(
    domain = {'x': [0.2, 1], 'y': [0, 1]},
    value = pred*100,
    
    mode = "gauge+number",#+delta",
    #delta = {'reference': mean_stud_perc, 'color': 'orange'},

    title = {'text':"Pass Probability", 'font': {"size": 20}},
    #set gauge and round edges of bar

    gauge = {'axis': {'range': [None, 100]},
             'shape': 'bullet',
             'steps' : [
                {'range': [0, mean_stud_perc], 'color': "rgba(0, 120, 120, 0.3)"}],
                #{'range': [250, 400], 'color': "gray"}],
            #'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490},
             'bar': {'color': 'rgba(59,65,86, 0.9)', 'thickness': 0.5}
                        }))

    if mean_stud_perc!=0:
        fig.add_annotation( x=cred_pos*(mean_stud_perc)+0.089, y=1.6,
                        text="Stud PR",
                        font=dict(
                                family="sans serif",
                                size=18
                                ),
                        showarrow=False)
    fig.update_layout(paper_bgcolor = color,     autosize=True,)
    #height=200,)
    return fig

def get_ability_fig(df):
    fig = px.histogram(df, x="ability", nbins=15, color_discrete_sequence=['rgb(59,65,86, 0.3)'], opacity=0.7)
    return fig

def get_gpa_fig(df):
    fig = px.histogram(df_stud, x='gpa', nbins=19, color_discrete_sequence=['rgb(59,65,86, 0.3)'], opacity=0.7)
    return fig

def get_work_fig():
    w_df = pd.DataFrame()
    w_df['workload'] = get_courses.get_all_workloads()
    fig = px.histogram(w_df, x='workload', nbins=19, color_discrete_sequence=['rgb(59,65,86, 0.3)'], opacity=0.7)
    return fig

def get_credit_figure(student_mean, recom, curr):
    cred_pos = 0.92/40 

    indicator = go.Indicator(   mode = "number+gauge", value = curr,
                                domain = {'x': [0.2, 1], 'y': [0, 1]},
                                title = {'text':"Credits", 'font': {"size": 20}},
                                gauge = {
                                        'shape': "bullet",
                                        'axis': {'range': [None, 40]},
                                        'bgcolor': "white",
                                        'steps': [
                                            {'range': [0, student_mean], 'color': 'rgba(148,250,167, 0.3)'},
                                            {'range': [student_mean, recom], 'color': 'rgba(0, 120, 120, 0.3)'},
                                            {'range': [recom, 40], 'color': 'rgba(242,160,115, 0.3)'}],
                                        'bar': {'color': 'rgba(59,65,86, 0.9)', 'thickness': 0.5}
                                        }
                            )

    # Customize the appearance of the Indicator
    #indicator['gauge']['bordercolor'] = 'gray'
    #indicator['gauge']['borderwidth'] = 1
    #indicator['gauge']['bar']['color'] = 'gray'
    #indicator['gauge']['axis']['range'] = [0, 100]
    #indicator['gauge']['threshold']['line']['color'] = 'red'
    #indicator['gauge']['threshold']['line']['width'] = 4
    #indicator['gauge']['threshold']['thickness'] = 0.75

    fig = go.Figure(indicator)
    fig.add_annotation( x=cred_pos*recom+0.02, y=-.8,
                        text="Recom.",
                        font=dict(
                                family="sans serif",
                                size=18
                                ),
                        showarrow=False)
    #print(student_mean)
    if student_mean>0:
        #print(student_mean)
        fig.add_annotation( x=cred_pos*student_mean + 0.0015*student_mean, y=1.6,
                            text="Stud Mean",
                            font=dict(
                                    family="sans serif",
                                    size=18
                                    ),
                            showarrow=False)
    fig.update_layout(autosize=True,)
    #height=230,)
    return fig

