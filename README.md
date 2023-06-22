# Maze

## Introduction
This is a python project to create and solve a maze with various algorithms  
These project contains two modules:  
`MazeGenerator.py` contains maze generation algorithms, while  
`MazeSolver.py` contains maze solving algorithms  

## Dependencies
`matplotlib`, `matplotlib.pyplot`, `numpy`, and `random`

## How to Use
`MazeGenerator.py` can be directly imported. Every algorithm will return a 2-d array storing the information of the maze generated.  
`MazeSolver.py` is best used along with `MazeGenerator.py`. The return value from maze generation algorithms can be used as the parameter `data`.

## Progress
### `MazeGenerator.py`
- Wilson's algorithm
- Kruskal's algorithm
- Prim's algorithm

### `MazeSolver.py`
- Dijkstra's algorithm
- A* search algorithm
  - Cost = Manhattan distance
  - Cost = BFS + back propagation
- Dead-end filling algorithm
- Wall following algorithm
  - Left-hand rule
  - Right-hand rule


## Future Development
### `MazeGenerator.py`
- Depth-first search algorithm (recursive backtracker)
- Recursive division algorithm
- Aldous-Broder algorithm
- Tessellation algorithm
  
### `MazeSolver.py`
- Flood fill algorithm
