from cube_solver import Solver
import numpy as np

DEFAULT = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], # orange
					[[1, 1, 1], [1, 1, 1], [1, 1, 1]], # red
					[[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
					[[3, 3, 3], [3, 3, 3], [3, 3, 3]], # yellow
					[[4, 4, 4], [4, 4, 4], [4, 4, 4]], # blue
					[[5, 5, 5], [5, 5, 5], [5, 5, 5]]]) # green

CHECKER_BOARD = np.array([[[0, 1, 0], [1, 0, 1], [0, 1, 0]], # orange
						  [[1, 0, 1], [0, 1, 0], [1, 0, 1]], # red
						  [[2, 3, 2], [3, 2, 3], [2, 3, 2]], # white
						  [[3, 2, 3], [2, 3, 2], [3, 2, 3]], # yellow
						  [[4, 5, 4], [5, 4, 5], [4, 5, 4]], # blue
						  [[5, 4, 5], [4, 5, 4], [5, 4, 5]]]) # green

final_run_test = np.array([[[0, 0, 0], [0, 0, 0], [3, 0, 5]], # orange
						   [[1, 1, 1], [1, 1, 1], [5, 1, 3]], # red
						   [[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
						   [[4, 3, 0], [3, 3, 3], [4, 3, 1]], # yellow
						   [[4, 4, 4], [4, 4, 4], [1, 4, 0]], # blue
						   [[5, 5, 5], [5, 5, 5], [3, 5, 3]]]) # green

twisted_corners_test = np.array([[[0, 0, 0], [0, 0, 0], [4, 0, 3]], # orange
								 [[1, 1, 1], [1, 1, 1], [5, 1, 3]], # red
								 [[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
								 [[3, 3, 0], [3, 3, 3], [5, 3, 1]], # yellow
								 [[4, 4, 4], [4, 4, 4], [0, 4, 1]], # blue
								 [[5, 5, 5], [5, 5, 5], [4, 5, 3]]]) # green

thick_plus_test = np.array([[[0, 0, 0], [0, 0, 0], [1, 0, 5]], # orange
							[[1, 1, 1], [1, 1, 1], [0, 5, 5]], # red
							[[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
							[[4, 3, 3], [3, 3, 3], [0, 3, 3]], # yellow
							[[4, 4, 4], [4, 4, 4], [3, 4, 3]], # blue
							[[5, 5, 5], [5, 5, 5], [1, 1, 4]]]) # green

up_x_test = np.array([[[0, 0, 0], [0, 0, 0], [3, 3, 5]], # orange
					  [[1, 1, 1], [1, 1, 1], [5, 3, 3]], # red
					  [[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
					  [[1, 4, 0], [1, 3, 0], [0, 5, 1]], # yellow
					  [[4, 4, 4], [4, 4, 4], [4, 3, 4]], # blue
					  [[5, 5, 5], [5, 5, 5], [3, 3, 3]]]) # green

down_rectangle_test = np.array([[[0, 0, 0], [0, 0, 3], [4, 0, 5]], # orange
								[[1, 1, 1], [1, 1, 4], [3, 5, 1]], # red
								[[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
								[[3, 4, 0], [4, 3, 0], [5, 3, 4]], # yellow
								[[4, 4, 4], [3, 4, 3], [3, 1, 1]], # blue
								[[5, 5, 5], [1, 5, 5], [3, 5, 0]]]) # green

down_plus_test = np.array([[[5, 0, 1], [5, 0, 1], [2, 4, 1]], # orange
						   [[3, 1, 5], [4, 1, 0], [0, 4, 5]], # red
						   [[2, 2, 0], [2, 2, 2], [2, 2, 3]], # white
						   [[4, 0, 3], [5, 3, 5], [0, 1, 4]], # yellow
						   [[1, 4, 0], [3, 4, 0], [3, 1, 1]], # blue
						   [[5, 5, 4], [3, 5, 3], [4, 3, 2]]]) # green

bottom_x_test = np.array([[[2, 4, 2], [3, 0, 4], [1, 5, 1]], # orange
						  [[2, 4, 5], [3, 1, 5], [0, 0, 3]], # red
						  [[2, 3, 0], [3, 2, 0], [1, 0, 0]], # white
						  [[3, 2, 3], [2, 3, 2], [0, 2, 5]], # yellow
						  [[1, 1, 4], [1, 4, 5], [4, 4, 5]], # blue
						  [[4, 5, 5], [1, 5, 0], [4, 1, 3]]]) # green

narkis_test = np.array([[[0, 4, 1], [3, 0, 1], [0, 2, 0]], # orange
						[[1, 3, 2], [5, 1, 2], [1, 1, 5]], # red
						[[5, 5, 4], [4, 2, 2], [4, 0, 5]], # white
						[[5, 4, 2], [1, 3, 0], [3, 3, 4]], # yellow
						[[0, 1, 3], [0, 4, 4], [1, 5, 3]], # blue
						[[2, 5, 2], [2, 5, 0], [4, 3, 3]]]) # green

fault_test = np.array([[[4, 4, 4], [0, 0, 0], [0, 0, 0]], # orange
					   [[5, 1, 1], [5, 1, 1], [5, 1, 1]], # red
					   [[0, 5, 5], [2, 2, 2], [2, 2, 2]], # white
					   [[3, 3, 3], [3, 3, 3], [1, 4, 4]], # yellow
					   [[2, 1, 1], [2, 4, 4], [2, 4, 4]], # blue
					   [[0, 0, 3], [5, 5, 3], [5, 5, 3]]]) # green

c = Solver(DEFAULT, CHECKER_BOARD)
# c.play(["U'", "B'"])
# c.print_solution()
# print("starting narkis")
# c.narkis()
# c.print_solution()
# print("starting bottom_x")
# c.bottom_x()
# c.print_solution()
# print("starting down_plus")
# c.down_plus()
# c.print_solution()
# print("starting down_rectangle")
# c.down_rectangle()
# c.print_solution()
# print("starting up_x")
# c.up_x()
# c.print_solution()
# print("starting thick_plus")
# c.thick_plus()
# c.print_solution()
# print("starting twisted_corners")
# c.twisted_corners()
# c.print_solution()
# print("starting final_run")
# c.final_run()
# c.print_solution()
# c.solve()
# c.shuffle(10)
c.play(['D', "U'", 'R', 'R', 'B', "R'", "F'", 'F', 'F', 'B'])
c.print_solution()
c.play(['D', 'L', 'B', 'D', 'F', 'D', "R'", 'F', 'D', "F'", 'D', 'L', "R'", 'F', 'F', 'D', 'L', 'L', 'B', 'B', 'D', "R'", 'D', "R'", 'D', 'L', 'D', "L'", "D'", 'F', 'D', "F'", 'D', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", 'R', 'D', "R'", 'D', 'F', 'D', "F'", "D'", 'B', 'D', "B'", "D'", "L'", "D'", 'L', 'D', "F'", "D'", 'F', 'D', 'L', 'D', "L'", 'R', 'D', "R'", "D'", "B'", "D'", 'B', 'B', 'D', "B'", "D'", "L'", "D'", 'L', 'D', 'D', 'R', 'D', "R'", "D'", "B'", "D'", 'B', "D'", "R'", "D'", 'R', 'D', 'F', 'D', "F'", 'L', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "L'", 'D', 'L', 'D', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', 'D', "L'", 'D', 'L', "D'", "R'", 'D', "L'", "D'", 'R', 'D', 'L', "D'", "R'", 'D', "L'", "D'", 'R', 'L', "F'", "L'", 'F', 'L', "F'", "L'", 'F', 'D', 'D', 'L', "F'", "L'", 'F', 'L', "F'", "L'", 'F', 'D', 'L', "F'", "L'", 'F', 'L', "F'", "L'", 'F', 'D'])
# c.solve()
c.print_solution()