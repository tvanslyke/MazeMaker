from random import shuffle, random
from itertools import chain
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm

class Node(object):
    
    
    def __init__(self, pos, state = 0):
        self.pos = pos
        self.state = state
        self.adj = set()
        self.corners = set()
        
    @staticmethod 
    def Connect(grid, status_bar = True):
        total = len(grid)
        print "Constructing graph."
        for i, row in enumerate(grid):
            pcent = i* 100.0/total
            count = int(pcent/2)
            for node in row:
                node.connect(grid, dims = (len(grid[0]),len(grid)))
            sys.stdout.write('|%s\r' %( "#"* count + "_" * (50 - count) + "|{:3.0f}%".format(pcent) ))
    def connect(self, grid, dims = None):
        if dims is None:
            dims = len(grid[0]),len(grid)
        adj = 1
        corner = 1+1j
        for _ in xrange(4):
            x, y = int(self.pos[0] + corner.real ), int(self.pos[1] + corner.imag)
            if 0 <= x < dims[0] and 0 <= y < dims[1]:
                self.corners.add(grid[y][x])
            x, y = int(self.pos[0] + adj.real), int(self.pos[1] + adj.imag)
            if 0 <= x < dims[0] and 0 <= y < dims[1]:
                node = grid[y][x] 
            else:
                adj *= 1j
                corner *= 1j
                continue

            if node in self.adj:
                adj *= 1j
                corner *= 1j
                continue
            self.adj.add(node)
            node.adj.add(self)
            adj *= 1j
            corner *= 1j
        
            
    def makepath(self, prettiness = 0):
        previous_node = None
        for node in self.adj:
            if node.state:
                if previous_node:
                    return False
                previous_node = node
           
        for corner in self.corners:
            if corner.state:
                if corner in previous_node.adj:
                    continue
                else:
                    return False
        self.state = 1
        adj = [item for item in self.adj]
        to_visit = []
        for node in iter(adj):
            if node.state:
                continue
            for other in set.union(node.adj, node.corners):
                if other is self or other in self.adj:
                    continue
                if other.state:

                    break
            else:
                to_visit.append(node)
        shuffle(to_visit)
        if prettiness > 0:
            try:
                dx, dy = self.pos[0] - previous_node.pos[0], self.pos[1] - previous_node.pos[1]
                preferred = self.pos[0] + dx, self.pos[1] + dy
                preferred = [1 if node.pos == (preferred) else 0 for node in to_visit ]
                preferred = preferred.index(1)
                if random() < prettiness:
                    to_visit[0], to_visit[preferred] = to_visit[preferred], to_visit[0]
            except AttributeError:
                pass
            except ValueError:
                pass
        return iter(to_visit)
        
            
        
        
class Maze(object):
    
    def __init__(self, dims = (10, 10), root = ( 0, 0),):
        self.root = root
        self.maze = [[0 for _ in xrange(dims[0])] for _ in xrange(dims[1])]
        self.grid = [[Node((x, y))  for x in xrange(dims[0])] 
                                    for y in xrange(dims[1])]
        Node.Connect(self.grid)
    
    def construct(self, animate = False, prettiness = .25):
        to_flip = []
        path_stack = iter([self.grid[self.root[1]][self.root[0]]])
        if animate:
            plt.ion()
            fig = plt.figure(1)
            ax = fig.gca()
            image = ax.imshow(self.maze, cmap = 'Greys_r', interpolation = "nearest")
            image.autoscale()
        while True:
            try:
                node = next(path_stack)
            except:
                break
            valid_path = node.makepath(prettiness = prettiness)
            if valid_path:
                path_stack = chain(valid_path, path_stack)
                if animate:
                    
                    self.maze[node.pos[1]][node.pos[0]] = 1
                    image.set_data(self.maze)
                    image.autoscale()
                    fig.canvas.draw()
        plt.ioff()

            
if __name__ == '__main__':
    maze = Maze((100, 100))
    maze.construct(True, prettiness = .5)
    plt.imshow(maze.maze, cmap = 'Greys_r', interpolation = "nearest")
    plt.show()
    
    
    
    
    
    
        