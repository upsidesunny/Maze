import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random as rd

class Wilson:
    def __init__(self, mazeSize, mode="fast-random", colors=["black", "white", "red"]):
        s = 2*mazeSize+1 
        self.mazeSize = s
        self.mode, self.order = mode.split("-")
        self.data = np.zeros((s, s))

        self.space = []     # all posible cells
        self.maze = []      # all visited cells
        self.path = []      # path to be added to the solution 

        self.colors = colors # >= 3, only first 3 will be used
                             # 1st: unvisited cells / walls
                             # 2nd: final paths
                             # 3rd: temporary paths
        self.bounds = [colors.index(x) for x in colors]
        self.figure = plt.figure()



    def __createPlot(self):
        plt.ion()

        cmap = matplotlib.colors.ListedColormap(self.colors)
        norm = matplotlib.colors.BoundaryNorm(self.bounds, cmap.N-1)

        axis = self.figure.add_subplot()
        axis.set_xticks(ticks=[])
        axis.set_yticks(ticks=[])
        self.mazeImage = axis.imshow(self.data, cmap=cmap, norm=norm)



    def __updatePlot(self, time=0.001):
        self.mazeImage.set_data(self.data)
        self.figure.canvas.draw()
        plt.pause(time) # delay between plot updates
        self.figure.canvas.flush_events()



    def __createStateSpace(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if i%2==1 and j%2==1: # all non-wall cells
                    self.space.append([i, j])
    


    def __pickCell(self, color):
        if self.order == "sequential":
            idx = 0
        if self.order == "random":
            idx = rd.randint(0, len(self.space)-1) # a random cell

        cell = self.space.pop(idx)
        self.data[cell[0]][cell[1]] = self.colors.index(color)
        return cell
    

    
    def __explore(self):
        valid = False
        while not valid:
            direction = rd.randint(0, 3)
            new = [[self.path[-1][0], self.path[-1][1]]]
            for i in range(2):
                if direction == 0: # up
                    new.append([new[-1][0]-1, new[-1][1]])
                if direction == 1: # down
                    new.append([new[-1][0]+1, new[-1][1]])
                if direction == 2: # left
                    new.append([new[-1][0], new[-1][1]-1])
                if direction == 3: # right
                    new.append([new[-1][0], new[-1][1]+1])

            # within boundaries
            if new[-1][0] >= 0 and new[-1][1] >= 0 and new[-1][0] < self.mazeSize and new[-1][1] < self.mazeSize:
                valid = True

        self.path += new
        for cell in new:
            self.data[cell[0]][cell[1]] = 2 #red


    
    def __checkLoop(self):
        firstOccur = self.path.index(self.path[-1]) + 1
        if firstOccur != len(self.path):
            self.path , loop= self.path[:firstOccur], self.path[firstOccur:-1] # separate loop from path
            for cell in loop:
                self.data[cell[0]][cell[1]] = 0 # black


    
    def __addPath(self):
        self.maze += self.path
        for cell in self.path:
            self.data[cell[0]][cell[1]] = 1 # white
            if cell in self.space:
                self.space.remove(cell)



    def generate(self):
        self.__createPlot() 
        self.__createStateSpace() 

        self.maze.append(self.__pickCell(self.colors[1])) # white

        # until all cells in state space are visited
        while len(self.space) != 0:
            # pick another cell to start a path
            self.path = [self.__pickCell(self.colors[2])] # red
            # extends the path until it intersects with any cells that are included in the maze
            while self.path[-1] not in self.maze:
                # extends the path by selecting a random direction
                self.__explore()
                # if the path intersects with itself (forms a loop), erase the loop
                self.__checkLoop()

                if self.mode == "detailed":
                    self.__updatePlot()

            # add the entire valid path to the maze
            self.__addPath()
            self.__updatePlot()
        
        self.__updatePlot()
        print("end of wilson's algorithm") 
        plt.ioff()
        plt.show()
        return self.data



class Kruskal:
    def __init__(self, mazeSize, colors=["black", "white", "red"]):
        s = 2*mazeSize+1
        self.mazeSize = s
        self.data = np.zeros((s, s))

        self.space = []   # all possible cells
        self.maze = []    # all visited cells
        self.current = [] # 2 "adjacent" cells with a wall between

        self.colors = colors # >= 3, only first 3 will be used
                             # 1st: unvisited cells / walls
                             # 2nd: final paths
                             # 3rd: temporary paths
        self.bounds = [colors.index(x) for x in colors]
        self.figure = plt.figure()



    def __createPlot(self):
        plt.ion()

        cmap = matplotlib.colors.ListedColormap(self.colors)
        norm = matplotlib.colors.BoundaryNorm(self.bounds, cmap.N-1)

        axis = self.figure.add_subplot()
        axis.set_xticks(ticks=[])
        axis.set_yticks(ticks=[])
        self.mazeImage = axis.imshow(self.data, cmap=cmap, norm=norm)


    
    def __updatePlot(self, time=0.001):
        self.mazeImage.set_data(self.data)
        self.figure.canvas.draw()
        plt.pause(time) # delay between plot updates
        self.figure.canvas.flush_events()



    def __createStateSpace(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if i%2==1 and j%2==1:
                    self.space.append([[i, j]])



    def __explore(self):
        valid = False
        while not valid:
            group = self.space[rd.randint(0, len(self.space)-1)]
            cell = group[rd.randint(0, len(group)-1)]
            self.current = [cell]
            dir = rd.randint(0, 3)
            for i in range(2):
                if dir == 0: # up
                    self.current.append([self.current[-1][0]-1, self.current[-1][1]])
                if dir == 1: # down
                    self.current.append([self.current[-1][0]+1, self.current[-1][1]])
                if dir == 2: # left
                    self.current.append([self.current[-1][0], self.current[-1][1]-1])
                if dir == 3: # right
                    self.current.append([self.current[-1][0], self.current[-1][1]+1])

            if self.current[-1][0] >= 0 and self.current[-1][1] >= 0 and self.current[-1][0] < self.mazeSize and self.current[-1][1] < self.mazeSize:
                valid = True



    def __compare(self):
        color = self.data[self.current[1][0]][self.current[1][1]]
        self.data[self.current[1][0]][self.current[1][1]] = 2
        self.__updatePlot() 
        self.data[self.current[1][0]][self.current[1][1]] = color

        for group in self.space:
            for cell in group:
                if cell == self.current[0]:
                    gp1 = self.space.index(group)
                if cell == self.current[-1]:
                    gp2 = self.space.index(group)
        # break the wall between if the two cells are not from the same group
        if gp1 != gp2:
            self.space[gp1] += self.space[gp2]
            self.space.pop(gp2)
            for cell in self.current:
                self.data[cell[0]][cell[1]] = 1



    def generate(self):
        self.__createPlot()
        self.__createStateSpace()

        # until all cells in state space form one and only one group
        while len(self.space) != 1:
            # selects two cells with a wall in between
            self.__explore()
            # compare whether the two cells on either side of the wall belong to the same group
            self.__compare()

        print("end of kruskal algorithm")   
        plt.ioff()
        plt.show()
        return self.data



class Prim:
    def __init__(self, mazeSize, colors=["black", "white", "red"]):
        s = 2*mazeSize+1 
        self.mazeSize = s
        self.data = np.zeros((s, s))

        self.space = []    # all possible cells 
        self.maze = []     # all visited cells
        self.adjacent = [] # all adjacent cells or visited cells, and their parant correspondingly

        self.colors = colors # >= 3, only first 3 will be used
                             # 1st: unvisited cells / walls
                             # 2nd: final paths
                             # 3rd: adjacent cells
        self.bounds = [colors.index(x) for x in colors]
        self.figure = plt.figure()



    def __createPlot(self):
        plt.ion()

        cmap = matplotlib.colors.ListedColormap(self.colors)
        norm = matplotlib.colors.BoundaryNorm(self.bounds, cmap.N-1)

        axis = self.figure.add_subplot()
        axis.set_xticks(ticks=[])
        axis.set_yticks(ticks=[])
        self.mazeImage = axis.imshow(self.data, cmap=cmap, norm=norm)



    def __updatePlot(self, time=0.001):
        self.mazeImage.set_data(self.data)
        self.figure.canvas.draw()
        plt.pause(time) # delay between plot updates
        self.figure.canvas.flush_events()



    def __createStateSpace(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if i%2==1 and j%2==1:
                    self.space.append([i, j])



    def __pickInitial(self, color):
        idx = rd.randint(0, len(self.space)-1)
        cell = self.space.pop(idx)
        self.data[cell[0]][cell[1]] = self.colors.index(color)
        return cell
    


    def __addNeighbours(self):
        parent = self.maze[-1]
        neighbours = [[parent[0]-2, parent[1]], [parent[0]+2, parent[1]], [parent[0], parent[1]-2], [parent[0], parent[1]+2]]
        for neighbour in neighbours:
            if neighbour not in self.maze and neighbour[0] >= 0 and neighbour[1] >= 0 and neighbour[0] < self.mazeSize and neighbour[1] < self.mazeSize:
                self.adjacent.append([neighbour, parent])
                self.data[neighbour[0]][neighbour[1]] = 2 #red



    def __connect(self):
        idx = rd.randint(0, len(self.adjacent)-1)
        next, parent = self.adjacent.pop(idx)
        # remove all of the same neighbour cell but with other parents
        newAdj = []
        for item in self.adjacent:
            if item[0] != next:
                newAdj.append(item)
        self.adjacent = newAdj

        self.data[next[0]][next[1]] = 1
        # add the wall to the path
        wall = self.__findMiddle(next, parent)
        self.data[wall[0]][wall[1]] = 1

        self.maze.append(next)
        self.space.remove(next)



    def __findMiddle(self, cell1, cell2):
        midX = int(abs(cell1[0] + cell2[0]) /2)
        midY = int(abs(cell1[1] + cell2[1]) /2)
        return [midX, midY] 
    


    def generate(self):
        self.__createPlot()
        self.__createStateSpace()

        # pick a cell as the initial cell to be included in the maze
        self.maze.append(self.__pickInitial(self.colors[1]))
        self.__updatePlot()

        # until all cells in state space are visited 
        while len(self.space) != 0:
            # store all neighbour cells of the latest cell added to the maze
            self.__addNeighbours()
            # extends the maze by selecting a random neighbour cell
            self.__connect()
            self.__updatePlot()

        self.__updatePlot()
        print("end of prim algorithm")   
        plt.ioff()
        plt.show()
        return self.data