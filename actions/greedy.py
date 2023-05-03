import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue
from os import remove, path
class Graph:
    def __init__(self, list: list, heuristic: list, id = 0, directed = False):
        self.id = str(id)
        self.directed = directed
        self.cnt = len(list)
        self.heuristic = heuristic
        self.list_node = list
        self.adj_list = {}
        
        self.g = nx.Graph(directed = directed, data=True)
        #self.pos = []
        count = 0
        for i in list:
            self.g.add_node(i, h = heuristic[list.index(i)])
            self.adj_list[i] = []
        self.edge_cost = {}

    def addEdge(self, a, b, weight):
        self.g.add_edge(a,b, weight = weight)
       # print(a,b)
        self.adj_list[a].append((b,weight))
        self.edge_cost[(a,b)] = weight
        if not self.directed:
            self.adj_list[b].append((a, weight))
            self.edge_cost[(b,a)] = weight

    def addNode(self, a, weight):
        self.g.add_node(a, h = weight)
        self.adj_list[a] = []
        self.cnt+=1

    def GreedyAlgorithm(self, st, en):
        pre = {}
        q = PriorityQueue()
        q.put((0, st))
        path = []
        explored = set()
        while not q.empty():
            current_node = q.get()[1]
            if(current_node in explored): continue #node was explored already
            explored.add(current_node)

            if current_node == en: #ket thuc
                path = []
                cost = 0
                while pre.get(current_node):
                    path.append(current_node)
                    cost += self.edge_cost[(pre[current_node], current_node)]
                    current_node = pre[current_node]
                path.append(current_node)
                result = ''
                for i in path:
                    result += i
                    if path.index(i) != len(path) - 1: #not the last
                        result += ' <-- '
                return result + '; Chi phi la: ' + str(cost)
            
            explored.add(current_node)
            for neighbour,weight in self.adj_list[current_node]:
                if neighbour in explored: continue
                q.put((self.heuristic[self.list_node.index(neighbour)], neighbour))
                pre[neighbour] = current_node
        return 'Khong tim thay duong di'


    def AStarAlgorithm(self, st, en):
        #becuase of repeat node, can't use priority queue easily
        pre = {}
        g = {}
        queue_node = [st]
        g[st] = 0
        path = []
        
        while len(queue_node):
            current_node = None
            for u in queue_node:
                if current_node == None or g[u] + self.heuristic[self.list_node.index(u)] < g[current_node] + self.heuristic[self.list_node.index(current_node)]:
                    current_node = u
            
            #print(current_node)

            if current_node == en: #ket thuc
                path = []
                total_cost = 0
                while pre.get(current_node):
                    path.append(current_node)
                    total_cost += self.edge_cost[(pre[current_node], current_node)]
                    current_node = pre[current_node]
                path.append(current_node)
                result = ''
                for i in path:
                    result += i
                    if path.index(i) != len(path) - 1: #not the last
                        result += ' <-- '
                return result + '; Chi phi la: ' + str(total_cost)

            for neighbour,weight in self.adj_list[current_node]:
                f_neighbour = g[current_node] + weight
                if neighbour not in g or f_neighbour < g[neighbour]:    
                    g[neighbour] = f_neighbour
                    pre[neighbour] = current_node
                    if neighbour not in queue_node: queue_node.append(neighbour)
            
            queue_node.remove(current_node)

        return 'Khong tim thay duong di'

    def showGraph(self):
        pos=nx.kamada_kawai_layout(self.g)
       # pos = nx.nx_agraph.graphviz_layout(self.g)
        labels = nx.get_edge_attributes(self.g,'weight')
        labels_node = nx.get_node_attributes(self.g,'h')
        nx.draw(self.g, pos = pos, with_labels = True, )
        nx.draw_networkx_labels(self.g, pos, labels = labels_node, horizontalalignment = 'left', verticalalignment ='bottom')
        nx.draw_networkx_edge_labels(self.g,pos,edge_labels=labels)
        imgPath = './actions/graph/' + self.id + '.png'
        if path.isfile(imgPath): remove(imgPath)
        plt.savefig(imgPath)
        plt.close()
def greedy( st, en, graph ):
        print(f"Đường đi từ {st} đến {en} bằng thuật toán tham lam là: ")
        return graph.GreedyAlgorithm(st, en)
def AStar( st, en, graph ):
        print(f"Đường đi từ {st} đến {en} bằng thuật toán A* là: ")
        return graph.AStarAlgorithm(st, en)
def test():      
    a = Graph(['A', 'B', 'C', 'D', 'E', 'F', 'G','H', 'I', 'K', 'S'], [123,82,118,115,72,40,0,70,40,30,125])
    a.addEdge('S', 'A', 55)
    a.addEdge('S', 'B', 42)
    a.addEdge('S', 'C', 48)
    a.addEdge('S', 'E', 72)
    a.addEdge('B', 'C', 40)
    a.addEdge('A', 'D', 45)
    a.addEdge('B', 'F', 40)
    a.addEdge('F', 'G', 55)
    a.addEdge('C', 'F', 68)
    a.addEdge('E', 'G', 82)
    a.addEdge('G', 'K', 38)
    a.addEdge('G', 'I', 47)
    a.addEdge('I', 'H', 50)
    a.addEdge('D', 'E', 45)
    #a.showGraph()
    b = Graph(['A','B'], [1,2], id = 2)
    b.addNode('F', 4)
    #b.addEdge('A', 'B', 2)
    b.showGraph()
    b.addNode
    print(greedy('S', 'G',a))
    print(AStar('S', 'G',a))
# c = Graph([],[],id = 1000)
# c.addNode('A', 3)
# c.addNode('B', 5)
# c.addEdge('A','B',10)
# c.addNode('C',3)
# c.addNode('E',10)
# c.addNode('P',100)
# c.showGraph()