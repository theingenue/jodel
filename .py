import random
import collections
import igraph
import operator
from operator import itemgetter
import itertools
import time
import math

class Graph():
    def __init__(self, n):
        self.graph_size = n
        self.edge_list = {}      # Keys are the vertices and the values are the set of neighbours
        self.edge_cnt = 0        # Number of edges
        self.vertex_colour = {}  # Where the colour of each edge is stored
        self.vertex_degree = {}  # Degree of each vertex
        for x in range(1, n+1):
            self.edge_list[x] = set()
            self.vertex_colour[x] = 0

    def add_edge(self, a, b):
        """ Add edge between the vertices a and b to graph"""
        if a > self.order():
            print "Can not add edge because", a, "is not a vetex in the graph."
        elif b > self.order():
            print "Can not add edge because", b, "is not a vetex in the graph."
        elif a != b:
            self.edge_list[a].add(b)
            self.edge_list[b].add(a)
            self.edge_cnt = self.edge_cnt + 1

    def print_graph(self):
        """Print graph to console"""
        if self.is_empty():
            print "Graph is empty!"
        else:
            for j in range(1, self.graph_size +1):
                    print "vertex",j, "neighbours", self.edge_list[j],"colour",self.vertex_colour[j]

    def clear_edges(self):
        """Clear sets (edges)"""
        for j in range(1, self.order()+1):
            self.edge_list[j].clear()
        self.edge_cnt=0

    def order(self):
        """return n = number of vertices"""
        return self.graph_size

    def size(self):
        """Return the number of edges in the graph"""
        return self.edge_cnt

    def remove_edge(self, a, b):
        """remove an edge"""
        if b in self.edge_list[a]:
            self.edge_list[a].remove(b)
            self.edge_list[b].remove(a)
            self.edge_cnt = self.edge_cnt - 1

    def is_empty(self):
        """Check if the graph is empty"""
        if self.edge_cnt!=0:
            return False
        return True

    def is_complete(self):
        """Check if the graph is complete (all vertices are connected to each other)"""
        if self.edge_cnt==self.order()*(self.order()-1)/2:
            return True
        return False

    #
    # def naive_colouring(self):
    #     ### random colours but can have duplicates
    #     for k in range(1, self.order() + 1):
    #         self.vertex_colour[k]=random.randint(0, self.order())
    #
    #     ### vertex colour is added in order from 1 to vertex's number then values are shuffled (no duplicate colours)
    #     for k in range(1, self.order() + 1):
    #         self.vertex_colour[k] = k
    #     values = list( )
    #     random.shuffle(values)
    #     self.vertex_colour= dict(zip(self.vertex_colour.keys(), values))
    #     print (self.vertex_colour)

    def colour_count(self):
        """Count colours in the graph"""
        if self.vertex_colour[1] == 0:
            return 0
        else:
            colour_set = set(self.vertex_colour.values()) # colours are a set to remove duplicates, then it gets the len
            return (len(colour_set))

    def clear_colour(self):
        for vertex in range(1, self.order() + 1):
            self.vertex_colour[vertex]=0


    def degree_lowest(self):
        """Arrange a dict of vertices and edges starting from the lowest degree"""
        vertex_degree={}
        for v in range(1, self.order() + 1):
            vertex_degree[v] = len(self.edge_list[v])
        sorted_degree = sorted(vertex_degree.items(), key=operator.itemgetter(1))
        order_lowest = []
        for a, b in sorted_degree:
            order_lowest.append(a)
        return order_lowest

    def degree_highest(self):
        """Order the vertices by highest degree"""
        l = self.degree_lowest()
        l.reverse()
        return l

    def is_proper(self):
        """Check if graph is coloured properly"""
        for vertex in range(1, self.graph_size + 1):
            for neighbour in self.edge_list[vertex]:
                if self.vertex_colour[vertex] == self.vertex_colour[neighbour]:
                    return False
        return True


    def colour_greedy(self,order_deg):
        """Colour graphs using the greedy algorithm depending on the vertex degree"""
        for x in range(1,self.graph_size +1):
            self.vertex_colour[x]=0
        if order_deg == "l":
            v = self.degree_lowest()
        elif order_deg == "h":
            v = self.degree_highest()
        elif order_deg == "n":
            v= range(1,self.graph_size +1)
        for j in range(0, len(v)):
            nb = list(self.edge_list[v[j]])  # place the neighbours in a list
            colour = {}  # empty colour dict
            for i in range(1, self.graph_size + 1):  # loop to set all colours to be available
                colour[i] = True
            # loop checks if all the vertex neighbours have a colour, if they do, the colour is "false" (unavailable)
            for x in nb:
                nb_colour = self.vertex_colour[x]
                if nb_colour != 0:  # if the neighbour has a colour
                    colour[nb_colour] = False
                    # change the colour to be not available
                    # loop to find the first available colour so we will loop till we find the first true
            for i in range(1, len(colour) + 1):  # find the first available colour
                if colour[i] is True:
                    self.vertex_colour[v[j]] = i
                    break



    def random_graph(self, p):
        """Generate a random graph"""
        self.clear_edges()
        for v1 in range(1, self.graph_size + 1):
            for v2 in range(v1, self.graph_size + 1):
                if v1 != v2 and random.random() < p:
                    self.add_edge(v1,v2)

    def colour_brute(self):
        """Colours graph using the Brute Force algorithm"""
        for palette_size in range(1, self.order()+1):
            for assignment in itertools.product(range(1,palette_size), repeat=self.order()):
                self.vertex_colour = dict(zip(self.edge_list.keys(), assignment))
                if self.is_proper():
                    return
        print "Complete graph! %d colours needed." %(self.order())

    def is_safe(self, c, nb):
        """check if colour is safe"""
        for x in nb:
            if self.vertex_colour[x] == c:
                return False
        return True

    def backtracking(self, m, v):
        if (v == self.order()+1):
            return True

        for c in range(1, m + 1):
            nb = list(self.edge_list[v])
            if self.is_safe(c, nb):
                self.vertex_colour[v] = c
                if self.backtracking(m, v + 1) == True:
                    return True
            g.vertex_colour[v]=0
        return False

    def colour_backtracking(self, m):
        """Call this function to colour graph using the Backtracking Recursive Algorithm """
        if self.backtracking(m, 1) == False:
            print"can't color with %d colours" % (m)
            return False
        return True

g= Graph(100)
g.random_graph(0.5)

g.colour_backtracking(3)
g.print_graph()
####GCU WITH DIF V ORDERINGS:
# def gcu(self, m, v, v_order):
#     if (v == self.order()):
#         return True
#
#     for c in range(1, m + 1):
#         nb = list(self.edge_list[v_order[v]])
#         if self.is_safe(c, nb):
#             self.vertex_colour[v_order[v]] = c
#             if self.gcu(m, v + 1, v_order) == True:
#                 return True
#         g.vertex_colour[v_order[v]] = 0
#     return False
#
# def colour_backtracking(self, m, order_deg):
#     if order_deg == "l":
#         v_order = self.degree_lowest()
#     elif order_deg == "h":
#         v_order = self.degree_highest()
#     elif order_deg == "n":
#         v_order = range(1, self.graph_size + 1)
#     if self.gcu(m, 0, v_order) == False:
#         print"can't color with %d colours" % (m)
#         return False
#     return True

#################time comparison#####################################
#

################### Bipartite graph ###################
# g = Graph(8)
# g.add_edge(1,4)
# g.add_edge(1,6)
# g.add_edge(1,8)
# g.add_edge(2,3)
# g.add_edge(2,5)
# g.add_edge(2,7)
# g.add_edge(3,2)
# g.add_edge(3,6)
# g.add_edge(3,8)
# g.add_edge(4,1)
# g.add_edge(4,5)
# g.add_edge(4,7)
# g.add_edge(5,2)
# g.add_edge(5,4)
# g.add_edge(5,8)
# g.add_edge(6,1)
# g.add_edge(6,3)
# g.add_edge(6,7)
# g.add_edge(7,2)
# g.add_edge(7,4)
# g.add_edge(7,6)
# g.add_edge(8,1)
# g.add_edge(8,3)
# g.add_edge(8,5)
# g.colour_brute()
# print g.colour_count()
# g.clear_colour()
# for i in range(1, g.order()):
#     g.clear_colour()
#     start_time = time.time()
#     if g.colour_backtracking(i):
#         break
# end_time = time.time() - start_time
# print end_time
# print g.colour_count()
# start_time = time.time()
# g.colour_brute()
# end_time = time.time() - start_time
# g.print_graph()
# print end_time
# m = g.colour_count()
# start_time = time.time()
# for colour in range (1, m + 1):
#     m = m - 1
#     tracking = g.colour_backtracking(m)
#     end_time = time.time() - start_time
#     print "gcu time", end_time
#     if tracking:
#         print "backtracking coloured the graph with %d colours" % (m)
#     if not tracking:
#         break
######################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%(not sure what these are )%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# data = open("data.txt", "w+")
# i = 500
# # p = 0.5
# while i <= 16000:
#     i = i * 2
#     # p = p + 0.1
#     p= 0.5
#     g = graph(i)
#     g.random_graph(p)
#     data.write(("%d\t%f\t%d\t" % (i, p, g.edge_cnt)))
#     start_time = time.time()
#     g.colour_greedy("n")
#     end_time = time.time() - start_time
#     data.write(("%d\t, %f\t" % (g.colour_count(), end_time)))
#
#     start_time = time.time()
#     g.colour_greedy("h")
#     end_time = time.time() - start_time
#     data.write(("%d\t, %f\n" % (g.colour_count(), end_time)))
#     # p = p + 0.1
#     g.clear()
# data.close()
######################

# data = open("data.txt", "w+")
# g.random_graph(0.5)
# g.add_edge(1,2)
# g.add_edge(1,3)
# g.add_edge(2,5)
# g.add_edge(2,3)
# g.add_edge(3,4)
# g.add_edge(4,5)
# g.add_edge(5,3)
# g.colour_backtracking(11)
# g.print_graph()
# print "GCU", g.colour_count()
# g.colour_greedy("h")
# g.print_graph()
# print "Greedy", g.colour_count()
# g.random_graph(0.2)
# for i in range(1, n+1):
#     start_time = time.time()
#     if g.colour_backtracking(i):
#         print"Can colour with %d" % (i)
#         break
#     end_time = time.time() - start_time
#     data.write(("%d\t, %f\t" % (g.edge_cnt, end_time)))
#     print end_time
# data.close()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# data = open("data-graph.txt", "w+")
# i = 20
# while i <= 40:
#     p = 0.2
#     while p < 1.0:
#         g = Graph(i)
#         g.random_graph(p)
#         # start_time = time.time()
#         # g.colour_brute()
#         # end_time = time.time() - start_time
#         # print "Brute coloured graph with %d vertices, in %d colours %f p in %f seconds." %(i, g.colour_count() ,p, end_time)
#         # data.write(("%d\t, %f\t, %d\t, %f\n" % (i, p, g.edge_cnt,end_time)))
#         # g.clear_colour()
#         m = i - 1
#         total_time = 0
#         while m >= 1:
#             start_time = time.time()
#             tracking = g.colour_backtracking(m)
#             end_time = time.time() - start_time
#             total_time += end_time
#             colour_count  = g.colour_count()
#             if tracking:
#                 print "GCU coloured graph with %d vertices, in %d colours %f p in %f seconds." % (i, g.colour_count(), p, end_time)
#                 data.write(("%d\t, %f\t, %d\t, %f\n" % (i, p, g.edge_cnt, end_time)))
#             if not tracking:
#                 break
#             m = min(m - 1, colour_count - 1)
#         data.write(("%d\n" % (total_time)))
#         print "total time: %f" %(total_time)
#         p = p + 0.2
#
#     i = i + 1
#
# data.close()

################# Colouring comparison: Greedy l, h, n, Brute  ###########
# data = open("data.txt", "w+")
#  #
# i = 5
# p = 0.0
# while i <= 30:
#     i = i + 1
#     p = p + 0.1
#     p= 0.1
#     while p < 1.0:
#         g = graph(i)
#         g.random_graph(p)
#         data.write(("%d\t%f\t%d\t" % (i, p, g.edge_cnt)))
#
#         g.colour_greedy("l")
#         data.write(("%d\t" % (g.colour_count())))
#
#         g.colour_greedy("h")
#         data.write(("%d\t" % (g.colour_count())))
#
#         g.colour_greedy("n")
#         data.write(("%d\t" % (g.colour_count())))
#
#         g.colour_brute()
#         data.write(("%d\n" % (g.colour_count())))
#         p = p + 0.1
#         g.clear()
# data.close()


################# time comparison: Greedy l, h, n, Brute  ###########
# data = open("data.txt", "w+")
# i = 1
# while i <= 9:
#     i = i + 1
#     p= 0.1
#     while p < 1.0:
#         g = graph(i)
#         g.random_graph(p)
#         data.write(("%d\t%f\t%d\t" % (i, p, g.edge_cnt)))
#
        # start_time = time.time()
        # g.colour_greedy("l")
        # end_time = time.time() - start_time
        # data.write(("%d\t, %f\t" % (g.colour_count(), end_time)))
        #
        # start_time = time.time()
        # g.colour_greedy("h")
        # end_time = time.time() - start_time
        # data.write(("%d\t, %f\t" % (g.colour_count(), end_time)))
#
#         start_time = time.time()
#         g.colour_greedy("n")
#         end_time = time.time() - start_time
#         data.write(("%d\t, %f\t" % (g.colour_count(), end_time)))
#
#         start_time = time.time()
#         g.colour_brute()
#         end_time = time.time() - start_time
#         data.write(("%d\t, %f\n" % (g.colour_count(), end_time)))
#
#         p = p + 0.1
#         g.clear()
# data.close()
######################################################

################# loop 50, 100, 500... etc ###########
# data = open("data.txt", "w+")
# half = False
# i = 10
# p = 0.0
# while i <= 10000:
#     p= p+0.1
#     if half == True:
#         j = i // 2
#         half = False
#     else:
#         j = i
#         i = i * 10
#         half = True
#     p=0.1
#     while p <= 1:
#         g = graph(j)
#         g.random_graph(p)
#         data.write(("%d\t%f\t%d\t" % (j, p,g.edge_cnt)))
#         g.colour_greedy("l")
#         data.write(("%d\t" % (g.colour_count())))
#         g.colour_greedy("h")
#         data.write(("%d\t" % (g.colour_count())))
#         g.colour_greedy("n")
#         data.write(("%d\n" % (g.colour_count())))
#         g.clear()
#         p = p + 0.1
#         g.clear()
# data.close()
##########################################################
