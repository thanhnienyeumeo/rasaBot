import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue
from os import remove, path
class Graph:
    def __init__(self, list = [], heuristic = [], id = 0, directed = False):
        self.id = str(id)
        self.directed = directed
        self.cnt = len(list)
        self.heuristic = heuristic
        self.list_node = list
        self.adj_list = {}
        
        self.g = nx.Graph(directed = directed, data=True)
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
        self.list_node.append(a)
        self.heuristic.append(weight)
        self.cnt+=1

    def GreedyAlgorithm(self, st, en):
        ans = ''
        step = 0
        pre = {}
        queue_node = [st]
        path = []
        explored = set()
        g = {}
        g[st] = 0
        while len(queue_node):
            current_node = None
            #get current_node
            for u in queue_node:
                if current_node == None or g[u] + self.heuristic[self.list_node.index(u)] < g[current_node] + self.heuristic[self.list_node.index(current_node)]:
                    current_node = u
            
            if(current_node in explored): continue #node was explored already
            explored.add(current_node)
            ans += str(step) + '\t'
            step += 1
            ans += current_node + '\t'

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
                ans += ('Đích\n')
                return ans + '\n' + result + '; Chi phí là: ' + str(cost)
            
            explored.add(current_node)
            queue_node.remove(current_node)


            #ans += (current_node)
            for neighbour,weight in self.adj_list[current_node]:
                if neighbour in explored: continue
                queue_node.append(neighbour)
                g[neighbour] = 0
                pre[neighbour] = current_node

            for i in queue_node:
                ans += (f'{i}{pre[i].lower()}({g[neighbour] + self.heuristic[self.list_node.index(i)]}) ')
            ans += '\n'
            
            
        return ans + '\n' + 'Không tim thấy đường đi'


    def AStarAlgorithm(self, st, en):
        #becuase of repeat node, can't use priority queue easily
        ans = ''
        step = 0
        pre = {}
        g = {}
        queue_node = [st]
        g[st] = 0
        path = []
        
        while len(queue_node):
            current_node = None
            #chon nut co ham f nho nhat
            for u in queue_node:
                if current_node == None or g[u] + self.heuristic[self.list_node.index(u)] < g[current_node] + self.heuristic[self.list_node.index(current_node)]:
                    current_node = u
            
            #print(current_node)
            ans += str(step) + '\t'
            step += 1
            ans += current_node + '\t'
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
                ans += ('Đích\n')
                return ans + '\n' + result + '; Chi phí là: ' + str(total_cost)

            for neighbour,weight in self.adj_list[current_node]:
                g_neighbour = g[current_node] + weight
                if neighbour not in g or g_neighbour < g[neighbour]:  #chua co o hang doi hoac co chi phi nho hon (them nut lap)
                    g[neighbour] = g_neighbour
                    pre[neighbour] = current_node
                    if neighbour not in queue_node: queue_node.append(neighbour)
            
            queue_node.remove(current_node)
            for i in queue_node:
                ans += (f'{i}{pre[i].lower()}({g[neighbour] + self.heuristic[self.list_node.index(i)]}) ')
            ans += '\n'
            
            
        return ans + '\n' + 'Không tim thấy đường đi'



    def DFSAlgorithm(self, st, en, upper = 100000):
        #becuase of repeat node, can't use priority queue easily
        ans = ''
        step = 0
        g = {}
        queue_node = [(st, 0, None)]
        g[st] = 0
        path = []
        
        while len(queue_node):
            current_node, f, pre_node = queue_node.pop()
            
            #print(current_node)
            ans += str(step) + '\t'
            step += 1
            ans += current_node + '\t'

            if current_node == en: #ket thuc
                path = []
                total_cost = 0
                current = (current_node, f, pre_node)
                while pre_node != None:
                    path.append(current_node)
                    total_cost += self.edge_cost[(pre_node[0], current_node)]
                    #return to the pre node
                    current_node, f, pre_node = pre_node

                path.append(current_node)
                result = ''
                for i in path:
                    result += i
                    if path.index(i) != len(path) - 1: #not the last
                        result += ' <-- '
                ans += ('Đích\n')
                if upper == 100000: return ans + '\n' + result + '; Chi phí là: ' + str(total_cost)
                return [True, ans + '\n' + result + '; Chi phí là: ' + str(total_cost)]

            for neighbour,weight in self.adj_list[current_node]:
                g_neighbour = f + weight
                if neighbour not in g and g_neighbour + self.heuristic[self.list_node.index(neighbour)] <= upper:  #chua co o hang doi hoac co chi phi nho hon step
                    queue_node.append((neighbour, g_neighbour, (current_node, f, pre_node)))
                    
            for i,f,pre in queue_node:
                ans += (f'{i}{pre[0].lower()}({f + self.heuristic[self.list_node.index(i)]}) ')
            ans += '\n'
            
        if upper == 100000: return ans + '\n' + 'Không tim thấy đường đi'
        return [False, ans + '\n']
    #def BFS(self, st, en):

    def AStarDFSAlgorithm(self, st, en, step: int):
        i = 0
        res = self.GreedyAlgorithm(st, en)
        if 'Không tim thấy đường đi' in res:
            return f'Error: Không có đường đi từ {st} đến {en}'
        ANS = ''
        while True:
            ANS+=(f'i = {i}: \n\n')
            ANS+=('STT\tĐỉnh\tHàng đợi\n')
            end, ans = self.DFSAlgorithm(st, en, i)
            ANS += ans
            i += step
            if end: return ANS

    def showGraph(self):
        for node in self.list_node:
            print(f'{node}({self.heuristic[self.list_node.index(node)]}): {self.adj_list[node]}')
        pos=nx.kamada_kawai_layout(self.g)
       # pos = nx.nx_agraph.graphviz_layout(self.g)
        label_pos = {k: (v[0], v[1] + 0.1) for k, v in pos.items()}
        labels = nx.get_edge_attributes(self.g,'weight')
        labels_node = nx.get_node_attributes(self.g,'h')
        nx.draw(self.g, pos = pos, with_labels = True, )
        nx.draw_networkx_labels(self.g, pos = label_pos, labels = labels_node, horizontalalignment = 'left', verticalalignment ='bottom')
        nx.draw_networkx_edge_labels(self.g,pos,edge_labels=labels)
        imgPath = './actions/graph/' + self.id + '.png'
        if path.isfile(imgPath): remove(imgPath)
        plt.savefig(imgPath)
        plt.close()

def greedy( st, en, graph ):
        print(f"Đường đi từ {st} đến {en} bằng thuật toán tham lam là: ")
        print('STT\tĐỉnh\tHàng đợi\n')
        return graph.GreedyAlgorithm(st, en)

def AStar( st, en, graph ):
        print(f"Đường đi từ {st} đến {en} bằng thuật toán A* là: ")
        print('STT\tĐỉnh\tHàng đợi\n')
        return graph.AStarAlgorithm(st, en)
        
def AStarDFS( st, en, graph: Graph, step = 1):
        print(f"Đường đi từ {st} đến {en} bằng thuật toán A* sâu dần là: ")
        
        return graph.AStarDFSAlgorithm(st, en, step)
def test():      
    a = Graph(['A', 'B', 'C', 'D', 'E', 'F', 'G','H', 'I', 'K'], [123,82,118,115,72,40,0,70,40,30], directed = True)
    a.addNode('S', 125)
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
    a.showGraph()
    # print(greedy('S', 'G',a))
    print(AStar('S', 'G',a))
    print(AStarDFS('S', 'G',a, 50))
test()
    
#test()
# b = Graph(['A','B'], [1,2], id = 2)
    # b.addNode('F', 4)
    # #b.addEdge('A', 'B', 2)
    # b.showGraph()
    # b.addNode
    
# c = Graph([],[],id = 1000)
# c.addNode('A', 3)
# c.addNode('B', 5)
# c.addEdge('A','B',10)
# c.addNode('C',3)
# c.addNode('E',10)
# c.addNode('P',100)
# c.showGraph()