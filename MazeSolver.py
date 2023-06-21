import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Dijkstra:
    def __init__(self, data, colors=['black', 'white', 'red', 'green']):
        self.data = data
        self.start = [1, 1]                   # starting point of the maze
        self.end = [len(data)-2, len(data)-2] # goal of the maze

        self.current = [self.start]                             # all cells to be visited in the next step
        self.traversed = [{"cell": self.start, "parent": None}] # all visited cells, and their parent correspondingly

        self.colors = colors # >= 4, only first 4 will be used
                             # 1st: walls
                             # 2nd: all paths
                             # 3rd: visited paths
                             # 4th: final path (solution)
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



    def __explore(self):
        next = []
        # find all neighbours of all cells in an iteration
        for path in self.current:
            for cell in self.__neighbour(path):
                if self.data[cell[0]][cell[1]] == 1:
                    if cell[0] > 0 and cell[1] > 0 and cell[0] < len(self.data) and cell[1] < len(self.data):
                        self.traversed.append({"cell": cell, "parent": path})
                        next.append(cell)
                        self.data[cell[0]][cell[1]] = 2
                        self.__updatePlot()
        return next
    


    def __neighbour(self, cell):
        return [[cell[0]-1, cell[1]], [cell[0]+1, cell[1]], [cell[0], cell[1]-1], [cell[0], cell[1]+1]]
    


    def __backTrack(self):
        self.data[self.current["cell"][0]][self.current["cell"][1]] = 3
        for item in self.traversed:
            if item["cell"] == self.current["parent"]:
                self.current = item



    def __displayPathOnly(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] == 2:
                    self.data[i][j] = 1



    def solve(self):
        self.__createPlot()
        self.data[self.start[0]][self.start[1]] = 2

        while self.end not in self.current:
            # extends the path and store all newly added cells for next iteration
            self.current = self.__explore()
        
        # mark the starting cell (goal) for backtracking
        for item in self.traversed:
            if item["cell"] == self.end:
                self.current = item
        
        # backtracking
        while self.current["parent"] != None:
            # connect the parent
            self.__backTrack()
            self.__updatePlot() 
            
        self.data[self.start[0]][self.start[1]] = 3
        self.__displayPathOnly() 

        self.__updatePlot()
        print("end of dijkstra algorithm")   
        plt.ioff()
        plt.show()



class Astar:
    def __init__(self, data, heurFunc="Manhattan", colors=['black', 'white', 'red', 'green']):
        self.data = data
        self.start = [1, 1]                   # starting point of the maze
        self.end = [len(data)-2, len(data)-2] # goal of the maze

        self.heurCost = [] # predicted costs of all cells to the goal
        self.heurFunc = heurFunc

        self.chosen = {"cell": self.start, "parent": None} # the selected cell, and the parent correspondingly
        self.active = [self.chosen]                        # all possible cells, and their parent correspondingly
        self.traversed = [self.chosen]                     # all visited cells, and their parent correspondingly

        self.colors = colors # >= 4, only first 4 will be used
                             # 1st: walls
                             # 2nd: all paths
                             # 3rd: visited paths
                             # 4th: final path (solution)
        self.bounds = [colors.index(item) for item in colors]
        self.figure = plt.figure()



    def __createPlot(self):
        plt.ion()

        cmap = matplotlib.colors.ListedColormap(self.colors)
        norm = matplotlib.colors.BoundaryNorm(self.bounds, cmap.N-1)

        self.axis = self.figure.add_subplot()
        self.axis.set_xticks(ticks=[])
        self.axis.set_yticks(ticks=[])
        self.mazeImage = self.axis.imshow(self.data, cmap=cmap, norm=norm)



    def __updatePlot(self, time=0.001):
        self.mazeImage.set_data(self.data)
        self.figure.canvas.draw()
        plt.pause(time) # delay between plot updates
        self.figure.canvas.flush_events()



    def __setHeurCost(self, heurFunc):
        # Manhattan distance
        if heurFunc == "Manhattan":
            for i in range(len(self.data)):
                temp= []
                for j in range(len(self.data[i])):
                    if int(self.data[i][j]) == 1:
                        cost = self.end[0]-i + self.end[1]-j # dist
                        temp.append(cost)
                    else:
                        temp.append(float("inf"))
                self.heurCost.append(temp)
        # BFS with back propagation
        elif heurFunc == "BackBFS":
            cell = self.end
            cost = 0
            h_traversed = []
            h_active = [cell]
            h_next= [[cell, None]]

            # until the starting point is reached
            while self.start not in [x[0] for x in h_traversed]:
                current, parent = h_next.pop(0)
                h_active.pop(0)
                if current not in [x[0] for x in h_traversed]:
                    h_traversed.append((current, parent, cost))
                    cell = current
                    neighbours = [[cell[0]-1, cell[1]], [cell[0]+1, cell[1]], [cell[0], cell[1]-1], [cell[0], cell[1]+1]]
                    for neighbour in neighbours:
                        if self.data[neighbour[0]][neighbour[1]] == 1 and neighbour[0] >= 0 and neighbour[1] >= 0 and neighbour[0] < len(self.data) and neighbour[1] < len(self.data):
                            h_next.append([neighbour, current])
                # depth + 1
                if len(h_active) == 0:
                    for path in h_next:
                        h_active.append(path)
                    cost += 1
            
            # map costs to cells
            self.heurCost = np.full((len(self.data), len(self.data)), float("inf"))
            for item in h_traversed:
                cell = item[0]
                if self.data[cell[0]][cell[1]] == 1:
                    self.heurCost[cell[0]][cell[1]] = item[2]
                    # display only on small maze
                    if len(self.data) <= 21: # =10x10
                        self.axis.text(cell[1],cell[0], item[2], ha='center', va='center')
                        self.__updatePlot()
            


    def __addNeighbours(self):
        self.active.remove(self.chosen)

        cell = self.chosen["cell"]
        neighbours = [[cell[0]-1, cell[1]], [cell[0]+1, cell[1]], [cell[0], cell[1]-1], [cell[0], cell[1]+1]]
        for neighbour in neighbours:
            # limitation of boundaries are omitted, and replaced by wall detection
            if self.heurCost[neighbour[0]][neighbour[1]] != float("inf") and neighbour not in [item["cell"] for item in self.traversed]:
                self.active.append({"cell": neighbour, "parent": self.chosen["cell"]})



    def __findMinimum(self):
        min = float("inf")
        for cell in [item["cell"] for item in self.active]:
            if self.heurCost[cell[0]][cell[1]] < min:
                min = self.heurCost[cell[0]][cell[1]]
        return min
    


    def __explore(self, minCost):
        for item in self.active:
            cell = item["cell"]
            if self.heurCost[cell[0]][cell[1]] == minCost:
                self.traversed.append(item)
                self.chosen = item
                self.data[cell[0]][cell[1]] = 2



    def __backTrack(self):
        for text in self.axis.texts:
            text.set_visible(False)
        self.__updatePlot()  

        for item in self.traversed:
            cell= item["cell"]
            if cell == self.chosen["parent"]:
                self.chosen = item
                self.data[cell[0]][cell[1]] = 3  



    def __displayPathOnly(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] == 2:
                    self.data[i][j] = 1
        

    def solve(self):
        self.__createPlot()
        self.__setHeurCost(self.heurFunc)
        self.data[self.start[0]][self.start[1]] = 2

        # until goal is reached
        while self.heurCost[self.chosen["cell"][0]][self.chosen["cell"][1]] != 0:
            self.__addNeighbours()

            # choose the minimum-cost move
            minCost = self.__findMinimum()
            # add the move to visited
            self.__explore(minCost)
            self.__updatePlot()

        # mark the starting cell (goal) for backtracking
        self.chosen = self.traversed[-1]
        self.data[self.chosen["cell"][0]][self.chosen["cell"][1]] = 3
        
        # backtracking
        while self.chosen["parent"] != None:
            # connects the parent
            self.__backTrack()
            self.__updatePlot()

        self.__displayPathOnly() 

        self.__updatePlot()
        print("end of astar algorithm")   
        plt.ioff()
        plt.show()   



class DeadEndFill:
    def __init__(self, data, colors=['black', 'white', 'red', 'green']):
        self.data = data
        self.start = [1, 1]                   # starting point of the maze
        self.end = [len(data)-2, len(data)-2] # goal of the maze

        self.active = [0] # cells to be explored in the next iteration

        self.colors = colors # >= 4, only first 4 will be used
                             # 1st: walls
                             # 2nd: unvisited / accepted paths
                             # 3rd: visited (=rejected) paths
                             # 4th: final path (solution)
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



    def __checkCellType(self, cell):
        lst = [self.data[cell[0]-1][cell[1]], self.data[cell[0]+1][cell[1]], self.data[cell[0]][cell[1]-1], self.data[cell[0]][cell[1]+1]]
        return lst.count(1) # 1: dead end
                            # 2: path
                            # 3: junction
                            # 4: junction



    def __explore(self):
        self.active = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                # start and end are compulsory
                if [i, j] != self.start and [i, j] != self.end:
                    # dead end
                    if self.data[i][j] == 1 and self.__checkCellType([i, j]) == 1:
                        self.active.append([i, j])
        
        for cell in self.active:
            self.data[cell[0]][cell[1]] = 2 #red



    def __displayFinalPath(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == 1:
                    self.data[i][j] = 3
                elif self.data[i][j] == 2:
                    self.data[i][j] = 1



    def solve(self):
        self.__createPlot()

        # until no dead end in the path
        while len(self.active) != 0:
            # add all dead ends to the "rejected list"
            self.__explore()
            self.__updatePlot()
        
        self.__displayFinalPath()

        print("end of dead end fill algorithm")   
        plt.ioff()
        plt.show()


class WallFollow:
    def __init__(self, data, mode="left", colors=['black', 'white', 'red', 'green']):
        self.data = data
        self.start = [1, 1]                   # starting point of the maze
        self.end = [len(data)-2, len(data)-2] # goal of the maze

        self.cell = self.start                            # current cell
        self.directions = ["right", "down", "left", "up"] # possible directions
        self.direction = "right"                          # current direction

        self.traversed = [self.start] # all visited cells

        # Left-hand or right-hand follower
        if mode == "left":
            self.k = 0
        elif mode== "right":
            self.k = 2

        self.colors = colors # >= 4, only first 4 will be used
                             # 1st: walls
                             # 2nd: unvisited / accepted paths
                             # 3rd: visited (=rejected) paths
                             # 4th: final path (solution)
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



    def __findNextPossible(self):
        cell = self.cell
        neighbours = [[cell[0]-1, cell[1]], [cell[0], cell[1]+1], [cell[0]+1, cell[1]], [cell[0], cell[1]-1]]
        side = (self.directions.index(self.direction)+self.k)%4
        front = (self.directions.index(self.direction)+1)%4
        return neighbours[side], neighbours[front]



    def __explore(self, newCell):
        if newCell not in self.traversed:
            self.traversed.append(newCell)
            self.data[self.cell[0]][self.cell[1]] = 3
        else:
            self.data[self.cell[0]][self.cell[1]] = 2



    def __displayPathOnly(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] == 2:
                    self.data[i][j] = 1 


    def solve(self):
        self.__createPlot()

        # until goal is reached
        while self.cell != self.end:
            # find possible move
            side, front = self.__findNextPossible()
            self.data[side[0]][side[1]]
            self.data[front[0]][front[1]]

            # rotate to the "hand direction"
            if self.data[side[0]][side[1]] != 0:
                self.direction = self.directions[(self.directions.index(self.direction)+3+self.k)%4]
                self.__explore(side)
                self.cell = side

            # move forward
            elif self.data[front[0]][front[1]] != 0:
                self.__explore(front)
                self.cell = front

            # rotate to the opposite of the "hand direction"
            else:
                self.direction = self.directions[(self.directions.index(self.direction)+1+self.k)%4]
            self.__updatePlot()
        self.data[self.end[0]][self.end[1]] = 3

        self.__displayPathOnly()
        
        self.__updatePlot()
        print("end of wall follow algorithm")   
        plt.ioff()
        plt.show()
