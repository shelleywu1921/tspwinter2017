from __future__ import division

import networkx as nx
from timeit import default_timer as timer


## this is the testing file for domgraph.py
## Testing create_dom_graph and find_stable_set


'''
create_dom_graph(domfilename, surplus_bound, node_num_upper_bound) takes in domfile, surplus_bound, node_num_upper_bound, and create a graph G whose nodes correspond to the dominoes in domfile. (u,v) is an edge in G, if and only if the dominoes represented by u and v intersect.

    It also prints the running time in seconds

    However, the program stops when the number of eligible nodes in G reaches node_num_upper_bound.
    
Returned value:
    G

Requirements:
    * domfile is a .dom file. see math.uwaterloo.ca/~bico/qss
    * surplus_bound is a float, between 0 and 1. Only dominoes whose surplus <= surplus bound will be considered.
    * node_num_upper_bound: int
    
Example:
create_dom_graph('pr76.dom', 0.5, 5000)

Note:
The best choices for surplus_bound and node_num_upper_bound varies depending on domfile.
'''


def create_dom_graph(domfilename,surplus_bound,node_num_upper_bound):
 start=timer()
 domfile=open(domfilename,'r')
 firstline=domfile.readline().split()
 num_of_dom=int(firstline[1])
 
 G=nx.Graph()
 for i in range(num_of_dom): 
   line=domfile.readline().split()
   surplus=float(line[0])
   if surplus<=surplus_bound:
     Asize=int(line[1]) 
     Bsize=int(line[2])
     A=set(map(int, line[3:3+Asize]))
     B=set(map(int,line[3+Asize:]))
     vertices=set(map(int, line[3:])) 
  
     G.add_node(i, surplus=surplus, Asize=Asize, Bsize=Bsize, A=A, B=B, vertices= vertices)
    
     if G.number_of_nodes()==node_num_upper_bound:
      break
     
 domfile.close()
 print('number of nodes in the graph G: %d' % (G.number_of_nodes()))
  
 for u in G.nodes():
	for v in G.nodes():
	  uteeth =G.node[u]['vertices']
	  vteeth=G.node[v]['vertices']
	  if (v!=u) and not uteeth.isdisjoint(vteeth):
		G.add_edge(u,v)

 print('number of edges in the graph G: %d' % (G.number_of_edges()))
 end=timer()
 print('running time: %.5f seconds' % (end-start)) 
 return G

'''
## testing for create_dom_graph
## passed
def test_create_dom_graph_pr76():
 G=create_dom_graph('pr76.dom',1, 100000)
 assert G.number_of_nodes()==66
 assert G.node[0]['vertices']==set([59,39,40])
 assert G.has_edge(0,1)
 assert not G.has_edge(0,3)

## passed
def test_create_dom_graph_att532():
    G=create_dom_graph('att532.dom',0.5, 5000)
    assert G.number_of_nodes()==5000
    assert G.node[0]['vertices']==set([529,527,528])
    assert G.node[0]['surplus']==0.0006
    assert G.node[0]['Asize']==1
    assert G.node[0]['Bsize']==2
'''


## More_testings

'''
>>> import domgraph as dg
>>> G=dg.create_dom_graph('att532.dom',0.5, 5000)
number of nodes in the graph G: 5000
running time: 97.29837 seconds
>>> G.number_of_edges()
11450125
>>> G.number_of_nodes()
5000

'''




'''
find_stable_set(G, total_surplus_bound) takes a graph G that represents a domfile (i.e. a graph produced by create_dom_graph, and total_surplus_bound, and returns an odd stable set of G and its total surplus (the sum of the surpluses of everything in the odd stable set). Moreover, its total surplus < total_surplus_bound.

Returned value:
    [ listof_candidate_dom, total_surplus]
    
Requirements:
    * G: a graph produced by create_dom_graph, representing a collection of dominoes
    * total_surplus_bound: a float between 0 and 1
    
Example:
G =create_dom_graph('pr76.dom', 0.5, 5000)
find_stable_set(G, 0.75)

Note:

'''


def find_stable_set(G, total_surplus_bound):
  max_stable_set=nx.maximal_independent_set(G)
  if len(max_stable_set)< 3: 
	return None
  max_stable_set.sort(key=lambda x: G.node[x]['surplus']) 
  first_node=max_stable_set[0]
  candidate_dom =[ first_node ]
  total_surplus=G.node[first_node]['surplus']

  for i in range(1, len(max_stable_set)):
	if i%2 ==1:
	  pass
	else:
	  i_minus_one_node=max_stable_set[i-1]
	  i_node=max_stable_set[i]
	  i_minus_one_surplus=G.node[i_minus_one_node]['surplus']
          i_surplus=G.node[i_node]['surplus']

	  if total_surplus + i_minus_one_surplus + i_surplus < total_surplus_bound:
		candidate_dom=candidate_dom+[i_minus_one_node, i_node]
		total_surplus=total_surplus+i_minus_one_surplus+i_surplus
	  else:
		break

  return [candidate_dom,total_surplus]



def run_find_stable_set_n_times(G,surplus_bound, ntimes):
 start =timer()
 counter3=0
 counter5=0
 counter7=0
 counter9=0
 counter11=0
 for i in range(ntimes):
  stable=find_stable_set(G,surplus_bound)
  num_of_dom=len(stable[0])
  surplus=stable[1]
  if num_of_dom>=11:
   counter11+=1
  elif num_of_dom==3:
   counter3+=1
  elif num_of_dom==5:
   counter5+=1  
  elif num_of_dom==7:
   counter7+=1   
  elif num_of_dom==9:
   counter9+=1
  print('number of dominoes: %d, surplus: %.4f'%(num_of_dom, surplus)) 
 
 end=timer()
 print('3 dominoes: %d, which is %.3f '% (counter3, counter3/ntimes))
 print('5 dominoes: %d, which is %.3f '% (counter5, counter5/ntimes))
 print('7 dominoes: %d, which is %.3f '% (counter7, counter7/ntimes))
 print('9 dominoes: %d, which is %.3f '% (counter9, counter9/ntimes))
 print('>=11 dominoes: %d, which is %.3f '% (counter11, counter11/ntimes))
 
       
 print('running time: %.5f seconds' %(end-start))



