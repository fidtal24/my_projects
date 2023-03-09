import rubik as r
import numpy as np
import random
import itertools
import patterns

# cubes
CURR = 0
DEST = 1

EDGES_IN_FACE = 4
CORNERS_IN_FACE = 4
SIDE_FACES = 4

DEFAULT = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], # orange
					[[1, 1, 1], [1, 1, 1], [1, 1, 1]], # red
					[[2, 2, 2], [2, 2, 2], [2, 2, 2]], # white
					[[3, 3, 3], [3, 3, 3], [3, 3, 3]], # yellow
					[[4, 4, 4], [4, 4, 4], [4, 4, 4]], # blue
					[[5, 5, 5], [5, 5, 5], [5, 5, 5]]]) # green

class InstructionsBuffer:
	def __init__(self):
		self.instructions = []

	def append(self, instruction: str):
		to_append = True
		relative_instruction = self.make_instruction_relative(instruction)

		if len(self.instructions) > 0:
			# case where the inverse of instruction is the last instruction in instructions.
			if (self.instructions[-1][0] == relative_instruction[0]) and\
			(len(self.instructions[-1]) != len(relative_instruction[0])):
				self.instructions.pop(-1)
				to_append = False
			elif len(self.instructions) > 1:
				# case where the last 2 instructions are identical to the current instruction.
				if (self.instructions[-1] == relative_instruction) and (self.instructions[-2] == relative_instruction):
					self.instructions.pop(-1)
					self.instructions.pop(-1)
					# replace the three identical instructions with their inverse.
					if len(instruction) == 1:
						relative_instruction += "'"
					else:
						relative_instruction = relative_instruction[0]

		if to_append:
			self.instructions.append(relative_instruction)

	def make_instruction_relative(self, instruction: str) -> str:
		relative_faces = ["F", "B", "U", "D", "L", "R"]
		absolute_faces = ["O", "R", "W", "Y", "B", "G"]
		relative_instruction = relative_faces[absolute_faces.index(instruction[0])]

		if len(instruction) > 1:
			relative_instruction += "'"

		return relative_instruction

	def print(self):
		print(self.instructions)

	def get_instruction_list(self) -> list[str]:
		return self.instructions

class Solver:
	def __init__(self, start_configuration, dest_pattern=patterns.DEFAULT):
		self.cubes = [r.Rubik(start_configuration), r.Rubik(dest_pattern)]
		self.instruction_buffer = InstructionsBuffer()

	def play(self, instructions: list[str]):
		relative_faces = ["F", "B", "U", "D", "L", "R"]
		absolute_faces = ["O", "R", "W", "Y", "B", "G"]
		for instruction in instructions:
			absolute_instruction = absolute_faces[self.get_middle_value(relative_faces.index(instruction[0]))]
			if len(instruction) == 2:
				absolute_instruction += "'"
			self.instruction_buffer.append(absolute_instruction)
			self.cubes[0].rot(instruction)

	def get_middle_value(self, face: int) -> np.ndarray:
		return self.val(CURR, [face, r.MIDDLE, r.MIDDLE])

	def shuffle(self, num_of_rotations):
		moves = ["F", "B", "U", "D", "L", "R"]
		directions = ["", "'"]
		instructions = []

		for i in range(num_of_rotations):
			instructions.append(random.choice(moves) + random.choice(directions))

		print("instruction: ", instructions)
		self.play(instructions)

	def val(self, cube: int, indices: list[int]) -> np.ndarray:
		return self.cubes[cube].get_val(*tuple(indices))

	def bring_face_to_front(self, cube: int, face: int, ref_face: int, ref_location: int=r.R):
		self.cubes[cube].bring_face_to_front(face, ref_face, ref_location)

	def bring_cubes_to_front(self, face: int, ref_face: int, ref_location: int):
		self.cubes[0].bring_face_to_front(face, ref_face, ref_location)
		self.cubes[1].bring_face_to_front(face, ref_face, ref_location)

	def solve(self) -> list[str]:
		algo_stages = [self.narkis, self.bottom_x, self.down_plus, self.down_rectangle, self.up_x,
		 			   self.thick_plus, self.twisted_corners, self.final_run]
		print("cube start:")
		self.print_solution()

		for stage in algo_stages:
			self.print_solution()
			print(stage.__name__, ":")
			stage()

		print("cube end:")
		# self.print_solution()
		print("Instructions to solve:")
		self.instruction_buffer.print()
		return self.instruction_buffer.get_instruction_list()

	def clean_orientations(self):
		l = []
		is_last_orientation = False
		for instruction in self.instruction_buffer:
			if len(instruction) > 5:
				if instruction[:5] == "bring":
					if len(l) == 0:
						is_last_orientation = True
					elif is_last_orientation:
						l.pop(-1)
				else:
					is_last_orientation = False
			l.append(instruction)
		self.instruction_buffer = l

	def print_solution(self):
		self.cubes[0].print_cube()

	def get_edge_vals(self, cube: int, edge: list[list[int]]) -> list[list[int]]:
		return [self.val(cube, edge[0]), self.val(cube, edge[1])]

	def get_corner_vals(self, cube: int, corner: list[list[int]]) -> list[list[int]]:
		return [self.val(cube, corner[0]), self.val(cube, corner[1]), self.val(cube, corner[2])]

	def narkis(self):
		surround_faces = [r.ORANGE, r.BLUE, r.RED, r.GREEN]
		self.bring_cubes_to_front(r.WHITE, r.ORANGE, r.U)
		dest_edges = []

		for i in range(EDGES_IN_FACE):
			dest_edges.append(self.get_edge_vals(DEST, r.EDGES[i]))

		for i in range(4):
			for face in surround_faces:
				if self.num_of_petals() == EDGES_IN_FACE:
					break

				for edge_num in range(EDGES_IN_FACE):
					self.bring_cubes_to_front(face, r.YELLOW, r.U)

					if edge_num == 0:
						self.bring_edge_to_up(0, dest_edges, 1, 1, [r.EDGES[5]], [["U"]], [["R"]])
					elif edge_num == 1:
						self.bring_edge_to_up(1, dest_edges, 3, 1,
											  [r.EDGES[5], r.EDGES[5], r.EDGES[0][::-1]],
											  [["U"], ["U"], ["U"]], [["R"], ["R'", "D'"], ["F'"]])
					elif edge_num == 2:
						self.bring_edge_to_up(2, dest_edges, 3, 2, [r.EDGES[0][::-1], r.EDGES[5],
											  r.EDGES[0][::-1]], [["U"], ["U"], ["U"]], [["F'"],
											  ["R"], ["F", "F"]])
					else:
						self.bring_edge_to_up(3, dest_edges, 2, 1, [r.EDGES[4], r.EDGES[0][::-1]],
											  [["U"], ["U"]], [["L'"], ["F"]])

	def bring_edge_to_up(self, edge_num: int, dest_edges: list, num_of_whiles: int,
	 					 whiles_in_if: int, while_cmp_edges: list[int],
	 					 while_instructions: list[list[str]],
						 after_while_instructions: list[list[str]]):
		edge = self.get_edge_vals(CURR, r.EDGES[edge_num])

		if edge in dest_edges:
			self.play_instructions_edge_to_up(dest_edges, whiles_in_if, while_cmp_edges,
											  while_instructions, after_while_instructions)
		elif edge[::-1] in dest_edges:
			whiles_in_else = num_of_whiles - whiles_in_if
			self.play_instructions_edge_to_up(dest_edges, whiles_in_else,
											  while_cmp_edges[whiles_in_if:],
											  while_instructions[whiles_in_if:],
											  after_while_instructions[whiles_in_if:])

	def play_instructions_edge_to_up(self, dest_edges: list, num_of_whiles: int,
									 while_cmp_edges: list[int],
									 while_instructions: list[list[str]],
									 after_while_instructions: list[list[str]]):
		for while_num in range(num_of_whiles):
			while self.get_edge_vals(CURR, while_cmp_edges[while_num]) in dest_edges:
				self.play(while_instructions[while_num])

			self.play(after_while_instructions[while_num])

	def num_of_petals(self) -> int:
		self.bring_cubes_to_front(r.WHITE, r.ORANGE, r.U)
		petals = 0
		curr_edges = []
		dest_edges = []
		back_edges_start_in_lut = 8

		for i in range(EDGES_IN_FACE):
			dest_edges.append(self.get_edge_vals(CURR, r.EDGES[i]))
			curr_edges.append(self.get_edge_vals(CURR, r.EDGES[i + back_edges_start_in_lut]))

		for curr_edge in curr_edges:
			if (curr_edge in dest_edges):
				petals += 1

		return petals

	def bottom_x(self):
		surround_faces = [r.ORANGE, r.BLUE, r.RED, r.GREEN]

		for face in surround_faces:
			self.bring_cubes_to_front(face, r.YELLOW, r.U)
			dest_middle_up_line = self.val(DEST, [r.F, r.FIRST_2, r.MIDDLE])

			for i in range(SIDE_FACES):
				curr_middle_up_line = self.val(CURR, [r.F, r.FIRST_2, r.MIDDLE])
				dest_edge = self.get_edge_vals(DEST, r.EDGES[2])
				curr_edge = self.get_edge_vals(CURR, r.EDGES[0])

				if (dest_middle_up_line == curr_middle_up_line).all() and (dest_edge == curr_edge):
					self.play(["F", "F"])
					break
				else:
					self.play(["U"])

	def down_plus(self):
		surround_faces = [r.ORANGE, r.BLUE, r.RED, r.GREEN]

		for face in surround_faces:
			self.bring_cubes_to_front(face, r.YELLOW, r.U)

			if self.is_r_d_corner_in_place():
				continue

			self.bring_cubes_to_front(face, r.YELLOW, r.U)
			r_d_dest_corner_colors = self.get_corner_vals(DEST, r.CORNERS[2])

			if self.is_corner_down(r_d_dest_corner_colors, face):
				for corner_face in surround_faces:
					self.bring_cubes_to_front(corner_face, r.YELLOW, r.U)
					r_d_curr_corner_colors = self.get_corner_vals(CURR, r.CORNERS[2])

					if self.are_corners_match(r_d_dest_corner_colors, r_d_curr_corner_colors):
						self.play(["R", "U", "R'"])
						break

			for i in range(CORNERS_IN_FACE):
				self.bring_cubes_to_front(face, r.YELLOW, r.U)
				r_u_curr_corner_colors = self.get_corner_vals(CURR, r.CORNERS[1])

				if self.are_corners_match(r_d_dest_corner_colors, r_u_curr_corner_colors):
					break

				self.play(["U"])

			while not self.is_r_d_corner_in_place():
				self.play(["R", "U", "R'", "U'"])

	def is_r_d_corner_in_place(self) -> bool:
		return self.get_corner_vals(CURR, r.CORNERS[2]) == self.get_corner_vals(DEST, r.CORNERS[2])

	def is_corner_down(self, colors: list[int], start_face: int) -> bool:
		surround_faces = [r.ORANGE, r.BLUE, r.RED, r.GREEN]

		for face in surround_faces:
			self.bring_face_to_front(CURR, face, r.YELLOW, r.U)
			curr_corner_colors = self.get_corner_vals(CURR, r.CORNERS[2])

			if self.are_corners_match(colors, curr_corner_colors):
				return True

		return False

	def are_corners_match(self, dest_colors: list[int], curr_colors: list[int]) -> bool:
		return self.are_same_lists(dest_colors, curr_colors)

	def are_same_lists(self, dest_colors: list[int], curr_colors: list[int]) -> bool:
		return (self.are_shifted_lists(dest_colors, curr_colors) or\
				self.are_shifted_lists(dest_colors, curr_colors[::-1]))

	def down_rectangle(self):
		surround_faces = [r.ORANGE, r.BLUE, r.RED, r.GREEN]

		for face in surround_faces:
			self.bring_cubes_to_front(face, r.YELLOW, r.U)

			if self.is_edge_straight_in_place():
				continue

			dest_colors = self.get_edge_vals(DEST, r.EDGES[1])

			for side_face in surround_faces:
				self.bring_face_to_front(CURR, side_face, r.YELLOW, r.U)

				if self.is_edge_in_middle_line(dest_colors):
					instructions = ["R", "U", "R'", "U'", "F'", "U'", "F"]
					self.play(instructions)
					break

			for i in range(SIDE_FACES):
				self.bring_face_to_front(CURR, face, r.YELLOW, r.U)
				front_coords = [r.F, r.FIRST, r.MIDDLE]
				up_coords = [r.U, r.LAST, r.MIDDLE]

				if (self.val(CURR, front_coords) == dest_colors[0]) and\
					(self.val(CURR, up_coords) == dest_colors[1]):
					instructions = ["U", "R", "U", "R'", "U'", "F'", "U'", "F"]
					self.play(instructions)
					break
				elif (self.val(CURR, front_coords) == dest_colors[1]) and\
					(self.val(CURR, up_coords) == dest_colors[0]):
					instructions = ["U", "U", "F'", "U'", "F", "U", "R", "U", "R'"]
					self.play(instructions)
					break
				else:
					self.play("U")
	
	def is_edge_straight_in_place(self) -> bool:
		return self.get_edge_vals(DEST, r.EDGES[1]) == self.get_edge_vals(CURR, r.EDGES[1])
	
	def is_edge_in_middle_line(self, dest_colors: list[int]) -> bool:
		curr_colors = self.get_edge_vals(CURR, r.EDGES[1])

		return (curr_colors == dest_colors) or (curr_colors == dest_colors[::-1])

	def up_x(self):
		if not self.is_x_shape():
			if self.is_up_point_shape():
				self.bring_face_to_front(CURR, r.ORANGE, r.BLUE)
				instructions = ["F"] + ["R", "U", "R'", "U'"] * 2 + ["F'"]
				self.play(instructions)
			elif self.is_up_r_shape():
				r_base = self.find_r_base()
				self.bring_face_to_front(CURR, r_base, r.YELLOW, r.U)
				instructions = ["F"] + ["R", "U", "R'", "U'"] + ["F'"]
				self.play(instructions)

			line_base = self.find_line_base()
			self.bring_face_to_front(CURR, line_base, r.YELLOW, r.U)
			instructions = ["F"] + ["R", "U", "R'", "U'"] + ["F'"]
			self.play(instructions)

	def is_up_point_shape(self) -> bool:
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		counter = 0

		for i in range(EDGES_IN_FACE):
			coords = r.EDGES[i][0]

			if (self.val(CURR, coords) == self.val(DEST, coords)):
				counter += 1

		return (counter < 2)

	def is_up_r_shape(self) -> bool:
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		r_shape_locations = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
		locations = []

		for i in range(EDGES_IN_FACE):
			coords = r.EDGES[i][0]

			if (self.val(CURR, coords) == self.val(DEST, coords)):
				locations.append(1)
			else:
				locations.append(0)

		return locations in r_shape_locations

	def is_x_shape(self) -> bool:
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		edges_order = [0, 2, 1, 3]
		four_edges = []
		dest_four_edges = []

		for i in edges_order:
			coords = r.EDGES[i][0]
			four_edges.append(self.val(CURR, coords))
			dest_four_edges.append(self.val(DEST, coords))

		return (four_edges == dest_four_edges)

	def find_r_base(self) -> int:
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		locations = []

		for i in range(EDGES_IN_FACE):
			coords = r.EDGES[i][0]

			if (self.val(CURR, coords) == self.val(DEST, coords)):
				locations.append(1)
			else:
				locations.append(0)

		if locations == [1, 1, 0, 0]:
			return 0
		elif locations == [0, 1, 1, 0]:
			return 4
		elif locations == [0 ,0, 1, 1]:
			return 1
		else:
			return 5

	def find_line_base(self) -> int:
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		horizon_coords = [[r.F, r.MIDDLE, r.FIRST], [r.F, r.MIDDLE, r.LAST]]
		horizon_src = [self.val(CURR, horizon_coords[0]), self.val(CURR, horizon_coords[1])]
		horizon_dest = [self.val(DEST, horizon_coords[0]), self.val(DEST, horizon_coords[1])]

		return r.BLUE if horizon_src == horizon_dest else r.ORANGE

	def thick_plus(self):
		are_4_plused = False
		intructions = ["R", "U", "R'", "U", "R", "U", "U", "R'"]

		while not are_4_plused:
			plused_edges = self.plused_edges()

			if len(plused_edges) == 4:
				self.bring_face_to_front(CURR, r.ORANGE, r.YELLOW, r.U)
				self.play(intructions)
			elif len(plused_edges) == 3:
				plused_edge = list(set(plused_edges) ^ set([r.ORANGE, r.BLUE, r.RED, r.GREEN]))[0]
				self.bring_face_to_front(CURR, plused_edge, r.YELLOW, r.U)
				self.play(intructions)
			elif len(plused_edges) == 2:
				self.bring_face_to_front(CURR, plused_edges[0], r.YELLOW, r.U)
				if plused_edges in [[r.U, r.D], [r.D, r.U], [r.L, r.R], [r.R, r.L]]:
					self.play(intructions)
				self.play(["U"] + intructions)
			else:
				are_4_plused = True

	def plused_edges(self):
		faces_to_check = [r.ORANGE, r.BLUE, r.RED, r.GREEN]
		plused_faces = []

		for face in faces_to_check:
			self.bring_cubes_to_front(face, r.YELLOW, r.U)
			tile_coords = r.EDGES[0][0]

			if self.val(CURR, tile_coords) != self.val(DEST, tile_coords):
				plused_faces.append(face)

		return plused_faces

	def twisted_corners(self):
		instructions = ["U", "R", "U'", "L'", "U", "R'", "U'", "L"]

		for i in range(CORNERS_IN_FACE):
			twisted_corners = self.count_twisted()

			if len(twisted_corners) == 0:
				self.bring_face_to_front(CURR, r.ORANGE, r.BLUE)
				self.play(instructions)
			elif len(twisted_corners) != CORNERS_IN_FACE:
				if twisted_corners[0] == 0:
					self.bring_face_to_front(CURR, r.BLUE, r.RED)
				elif twisted_corners[0] == 1:
					self.bring_face_to_front(CURR, r.ORANGE, r.BLUE)
				elif twisted_corners[0] == 2:
					self.bring_face_to_front(CURR, r.GREEN, r.ORANGE)
				else:
					self.bring_face_to_front(CURR, r.RED, r.GREEN)
				self.play(instructions)
			else:
				break

	def count_twisted(self):
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		twisted_corners = []

		for i in range(CORNERS_IN_FACE):
			if self.is_twisted_corner(i):
				twisted_corners.append(i)

		return twisted_corners

	def is_twisted_corner(self, corner_num: int) -> bool:
		curr_colors = []
		dest_colors = []

		for corner_side in r.CORNERS[corner_num]:
			curr_colors.append(self.val(CURR, corner_side))
			dest_colors.append(self.val(DEST, corner_side))

		return self.are_shifted_lists(curr_colors, dest_colors)

	def are_shifted_lists(self, l1: list[int], l2: list[int]) -> bool:
		for i in range(len(l1)):
			l1_new = l1[i:] + l1[:i]

			if l1_new == l2:
				return True

		return False

	def final_run(self):
		self.bring_cubes_to_front(r.YELLOW, r.ORANGE, r.R)
		corner_side = [r.F, r.FIRST, r.LAST]

		for i in range(CORNERS_IN_FACE):
			while self.val(CURR, corner_side) != self.val(DEST, corner_side):
				instructions = ["U", "R'", "U'", "R"]
				self.play(instructions)

			self.play(["F"])

		while not self.is_up_face_in_place():
			self.play(["F"])

	def is_up_face_in_place(self) -> bool:
		for corner_side in r.CORNERS[0]:
			if self.val(CURR, corner_side) != self.val(DEST, corner_side):
				return False

		return True
