#from app import app

from layout import app
from callbacks import *
from components import *
# import networkx as nx
# def get_recent_courses():
#     '''
#     This function construct a networkx graph for each student and saves it as an image in /assets/graphs/
#     '''
#     # Load the data
#     student_data = pd.read_pickle(r'data/AI_raw.pickle')
#     ids = [x.name for x in student_data.students]
#     # If folder assets/graphs/ does not exist, create it
#     if not os.path.exists('assets/graphs/'):
#         os.makedirs('assets/graphs/')
#     # For each student, construct a graph and save it as an image
#     for i,id in enumerate(ids):
#         # If graph already exists, skip
#         if os.path.exists('assets/graphs/'+id+'.png'):
#             continue
#         # Construct random networkx graph
#         G = nx.fast_gnp_random_graph(20, 0.5)
#         # Save graph as image
#         nx.draw(G, with_labels=True, font_weight='bold')
#         plt.savefig('assets/graphs/'+id+'.png')
#         plt.clf()
        

server = app.server

if __name__ == '__main__':
    #get_recent_courses()
    
    app.run_server(debug=True)
