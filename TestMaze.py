import MazeGenerator as gen
import MazeSolver as sol

maze = gen.Wilson(20) # maze size is required
data = maze.generate()

solver = sol.DeadEndFill(data) # maze (2d-array) is required
solver.solve()