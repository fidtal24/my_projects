import numpy as np

# cube faces
F = 0
B = 1
U = 2
D = 3
L = 4
R = 5

# directions
CW  = 0
CCW = 1

# colors
ORANGE = 0
RED    = 1
WHITE  = 2
YELLOW = 3
BLUE   = 4
GREEN  = 5

# tile posisions
FIRST = 0
MIDDLE = 1
LAST = 2
FIRST_2 = [FIRST, MIDDLE]
FIRST_2_FLIPPED = [MIDDLE, FIRST]
LAST_2 = [MIDDLE, LAST]
LAST_2_FLIPPED = [LAST, MIDDLE]
ALL = [FIRST, MIDDLE, LAST]
ALL_FLIPPED = [LAST, MIDDLE, FIRST]

# sheet sequences
SHEET_R_C_SEQ_CW  = [[FIRST, LAST_2_FLIPPED, LAST, FIRST_2], [FIRST_2, FIRST, LAST_2_FLIPPED, LAST]]
SHEET_R_C_SEQ_CCW = [[FIRST, FIRST_2, LAST, LAST_2_FLIPPED], [FIRST_2, LAST, LAST_2_FLIPPED, FIRST]]
SHEET_SEQ = [SHEET_R_C_SEQ_CW, SHEET_R_C_SEQ_CCW]

# side sequences
SIDE_SEQ_F = [[[U, LAST, ALL_FLIPPED], [L, ALL, LAST], [D, FIRST, ALL], [R, ALL_FLIPPED, FIRST]],
			  [[R, ALL_FLIPPED, FIRST], [D, FIRST, ALL], [L, ALL, LAST], [U, LAST, ALL_FLIPPED]]]
SIDE_SEQ_B = [[[R, ALL_FLIPPED, LAST], [D, LAST, ALL], [L, ALL, FIRST], [U, FIRST, ALL_FLIPPED]],
			  [[L, ALL, FIRST], [D, LAST, ALL], [R, ALL_FLIPPED, LAST], [U, FIRST, ALL_FLIPPED]]]
SIDE_SEQ_U = [[[F, FIRST, ALL], [R, FIRST, ALL], [B, FIRST, ALL], [L, FIRST, ALL]],
			  [[L, FIRST, ALL], [B, FIRST, ALL], [R, FIRST, ALL], [F, FIRST, ALL]]]
SIDE_SEQ_D = [[[L, LAST, ALL], [B, LAST, ALL], [R, LAST, ALL], [F, LAST, ALL]],
			  [[F, LAST, ALL], [R, LAST, ALL], [B, LAST, ALL], [L, LAST, ALL]]]
SIDE_SEQ_L = [[[F, ALL, FIRST], [U, ALL, FIRST], [B, ALL_FLIPPED, LAST], [D, ALL, FIRST]],
			  [[D, ALL, FIRST], [B, ALL_FLIPPED, LAST], [U, ALL, FIRST], [F, ALL, FIRST]]]
SIDE_SEQ_R = [[[U, ALL, LAST], [F, ALL, LAST], [D, ALL, LAST], [B, ALL_FLIPPED, FIRST]],
			  [[B, ALL_FLIPPED, FIRST], [D, ALL, LAST], [F, ALL, LAST], [U, ALL, LAST]]]
SIDE_SEQ = [SIDE_SEQ_F, SIDE_SEQ_B, SIDE_SEQ_U, SIDE_SEQ_D, SIDE_SEQ_L, SIDE_SEQ_R]

#strings to faces:
FACES_DICT = {"F": F, "B" : B, "U" : U, "D" : D, "L" : L, "R" : R}

# corners: (relative to the orientation)
CORNERS = [
			[[F, FIRST, FIRST], [U, LAST, FIRST],  [L, FIRST, LAST]],
			[[F, FIRST, LAST],  [U, LAST, LAST],   [R, FIRST, FIRST]],
			[[F, LAST, LAST],   [D, FIRST, LAST],  [R, LAST, FIRST]],
			[[F, LAST, FIRST],  [D, FIRST, FIRST], [L, LAST, LAST]],

			[[B, FIRST, FIRST], [U, FIRST, LAST],  [R, FIRST, FIRST]],
			[[B, FIRST, LAST],  [U, FIRST, FIRST], [L, FIRST, FIRST]],
			[[B, LAST, LAST],   [D, LAST, FIRST],  [L, LAST, FIRST]],
			[[B, LAST, FIRST],  [D, LAST, LAST],   [R, LAST, LAST]]
]

# edges: (relative to the orientation)
EDGES = [
		[[F, FIRST, MIDDLE], [U, LAST, MIDDLE]],
		[[F, MIDDLE, LAST],  [R, MIDDLE, FIRST]],
		[[F, LAST, MIDDLE],  [D, FIRST, MIDDLE]],
		[[F, MIDDLE, FIRST], [L, MIDDLE, LAST]],

		[[U, MIDDLE, FIRST], [L, FIRST, MIDDLE]],
		[[U, MIDDLE, LAST],  [R, FIRST, MIDDLE]],
		[[D, MIDDLE, LAST],  [R, LAST, MIDDLE]],
		[[D, MIDDLE, FIRST], [L, LAST, MIDDLE]],
		
		[[B, FIRST, MIDDLE], [U, FIRST, MIDDLE]],
		[[B, MIDDLE, LAST], [L, MIDDLE, FIRST]],
		[[B, LAST, MIDDLE], [D, LAST, MIDDLE]],
		[[B, MIDDLE, FIRST], [R, MIDDLE, LAST]]
]

# serves the bring_face_to_front method.
# orintation goes that: front, back, up, down, left, right
CUBE_ORIENTATIONS = [[[], [], [ORANGE, RED, BLUE, GREEN, YELLOW, WHITE], [ORANGE, RED, GREEN, BLUE, WHITE, YELLOW], [ORANGE, RED, YELLOW, WHITE, GREEN, BLUE], [ORANGE, RED, WHITE, YELLOW, BLUE, GREEN]],
					 [[], [], [RED, ORANGE, GREEN, BLUE, YELLOW, WHITE], [RED, ORANGE, BLUE, GREEN, WHITE, YELLOW], [RED, ORANGE, WHITE, YELLOW, GREEN, BLUE], [RED, ORANGE, YELLOW, WHITE, BLUE, GREEN]],
					 [[WHITE, YELLOW, GREEN, BLUE, RED, ORANGE], [WHITE, YELLOW, BLUE, GREEN, ORANGE, RED], [], [], [WHITE, YELLOW, ORANGE, RED, GREEN, BLUE], [WHITE, YELLOW, RED, ORANGE, BLUE, GREEN]],
					 [[YELLOW, WHITE, BLUE, GREEN, RED, ORANGE], [YELLOW, WHITE, GREEN, BLUE, ORANGE, RED], [], [], [YELLOW, WHITE, RED, ORANGE, GREEN, BLUE], [YELLOW, WHITE, ORANGE, RED, BLUE, GREEN]],
					 [[BLUE, GREEN, WHITE, YELLOW, RED, ORANGE], [BLUE, GREEN, YELLOW, WHITE, ORANGE, RED], [BLUE, GREEN, RED, ORANGE, YELLOW, WHITE], [BLUE, GREEN, ORANGE, RED, WHITE, YELLOW], [], []],
					 [[GREEN, BLUE, YELLOW, WHITE, RED, ORANGE], [GREEN, BLUE, WHITE, YELLOW, ORANGE, RED], [GREEN, BLUE, ORANGE, RED, YELLOW, WHITE], [GREEN, BLUE, RED, ORANGE, WHITE, YELLOW], [], []]
					]


# instructions_for_rotations:
EMPTY = [[], []]
F_B = [["U", "D'", "U", "D'"], [1, 0, 2, 3, 5, 4]]
F_U = [["U", "U", "R", "L'", "B", "B"], [3, 2, 0, 1, 4, 5]]
F_D = [["R'", "L", "D", "D", "B", "B"], [2, 3, 1, 0, 4, 5]]
F_L = [["U", "D'"], [5, 4, 2, 3, 0, 1]]
F_R = [["U'", "D"], [4, 5, 2, 3, 1, 0]]
U_L = [["U'", "F'", "B", "R'", "L'", "D'"], [0, 1, 5, 4, 2, 3]]
U_R = [["F", "B'", "R", "D", "U", "L"], [0, 1, 4, 5, 3, 2]]
U_D = [["U'", "F'", "B", "R'", "L'", "D'", "U'", "F'", "B", "R'", "L'", "D'"], [0, 1, 3, 2, 5, 4]]

#   [f-f], [f-b], [f-u], [f-d], [f-l], [f-r]
#   [b-f], [b-b], [b-u], [b-d], [b-l], [b-r]
#   [u-f], [u-b], [u-u], [u-d], [u-l], [u-r]
#   [d-f], [d-b], [d-u], [d-d], [d-l], [d-r]
#   [l-f], [l-b], [l-u], [l-d], [l-l], [l-r]
#   [r-f], [r-b], [r-u], [r-d], [r-l], [r-r]
ROTATIONS_OF_ORIENTATIONS = [
	[EMPTY, F_B,   F_U,   F_D,   F_L,   F_R  ],
	[F_B,   EMPTY, F_D,   F_U,   F_R,   F_L  ],
	[F_D,   F_U,   EMPTY, U_D,   U_L,   U_R  ],
	[F_U,   F_D,   U_D,   EMPTY, U_R,   U_L  ],
	[F_R,   F_L,   U_R,   U_L,   EMPTY, U_D  ],
	[F_L,   F_R,   U_L,   U_R,   U_D,   EMPTY]
]

# F-U, F-R, F-D, F-L, F-B
x = [F_U, F_R, F_D, F_L, F-B]

# color functions:
def red(text):
	return "\033[1;30;41m" + text + "\033[0m"

def orange(text):
	return "\033[1;35;48;5;208m" + text + "\033[0m"

def white(text):
	return "\033[1;30;47m" + text + "\033[0m"

def yellow(text):
	return "\033[1;30;43m" + text + "\033[0m"

def blue(text):
	return "\033[1;30;44m" + text + "\033[0m"

def green(text):
	return "\033[1;30;42m" + text + "\033[0m"


colors = [orange, red, white, yellow, blue, green]
def color(tile_val: int):
	return colors[tile_val](" ")

class Rubik:
	def __init__(self, cube):
		self.cube = cube
		self.changes_of_orientation = 0

	def rot_sheet(self, sheet, direction):
		row_seq, col_seq = SHEET_SEQ[direction]

		temp_row                                 = np.copy(self.cube[sheet, row_seq[0], col_seq[0]])
		self.cube[sheet, row_seq[0], col_seq[0]] = np.copy(self.cube[sheet, row_seq[1], col_seq[1]])
		self.cube[sheet, row_seq[1], col_seq[1]] = np.copy(self.cube[sheet, row_seq[2], col_seq[2]])
		self.cube[sheet, row_seq[2], col_seq[2]] = np.copy(self.cube[sheet, row_seq[3], col_seq[3]])
		self.cube[sheet, row_seq[3], col_seq[3]] = temp_row

	def rot_side_rows(self, side_seq):
		temp_row                      = np.copy(self.cube[tuple(side_seq[0])])
		self.cube[tuple(side_seq[0])] = np.copy(self.cube[tuple(side_seq[1])])
		self.cube[tuple(side_seq[1])] = np.copy(self.cube[tuple(side_seq[2])])
		self.cube[tuple(side_seq[2])] = np.copy(self.cube[tuple(side_seq[3])])
		self.cube[tuple(side_seq[3])] = temp_row

	def instruction_interpreter(self, instruction: str) -> tuple[int, int]:
		face = FACES_DICT[instruction[0]]
		direction = CW if len(instruction) == 1 else CCW
		return face, direction

	def rot(self, instruction: str):
		face, direction = self.instruction_interpreter(instruction)
		side_seq = SIDE_SEQ[face][direction]
		self.rot_side_rows(side_seq)
		self.rot_sheet(face, direction)

	def bring_face_to(self, face: int, to: int):
		desired_location = 0
		for i in range(6):
			if self.cube[i, MIDDLE, MIDDLE] == face:
				desired_location = i
		instructions_for_rotations = ROTATIONS_OF_ORIENTATIONS[desired_location][to]
		for instruction in instructions_for_rotations[0]:
			self.rot_sheet(*self.instruction_interpreter(instruction))
		if instructions_for_rotations[1] == []:
			faces_order = [0, 1, 2, 3, 4, 5]
		else:
			faces_order = instructions_for_rotations[1]
		self.cube = self.cube[faces_order]

	def bring_face_to_front(self, desired_front, ref_face: int, ref_location: int=R):
		self.bring_face_to(desired_front, F)
		self.bring_face_to(ref_face, ref_location)

	def print_cube_isometric(self):
		print("          ____")
		print("         |" + color(self.cube[B, FIRST, LAST]) + color(self.cube[B, FIRST, MIDDLE]) + color(self.cube[B, FIRST, FIRST]) +"|")
		print("         |" + color(self.cube[B, MIDDLE, LAST]) + color(self.cube[B, MIDDLE, MIDDLE]) + color(self.cube[B, MIDDLE, FIRST]) +"|")
		print("         |" + color(self.cube[B, LAST, LAST]) + color(self.cube[B, LAST, MIDDLE]) + color(self.cube[B, LAST, FIRST]) +"|")
		print("   ____   ____")
		print("  /" + color(self.cube[L, FIRST, LAST]) + color(self.cube[L, FIRST, MIDDLE]) + color(self.cube[L, FIRST, FIRST]) +"/  /" + color(self.cube[U, FIRST, FIRST]) + color(self.cube[U, FIRST, MIDDLE]) + color(self.cube[U, FIRST, LAST]) +"/" + color(self.cube[R, FIRST, LAST]) + "|")
		print(" /" + color(self.cube[L, MIDDLE, LAST]) + color(self.cube[L, MIDDLE, MIDDLE]) + color(self.cube[L, MIDDLE, FIRST]) +"/  /" + color(self.cube[U, MIDDLE, FIRST]) + color(self.cube[U, MIDDLE, MIDDLE]) + color(self.cube[U, MIDDLE, LAST]) +"/" + color(self.cube[R, FIRST, MIDDLE]) + color(self.cube[R, MIDDLE, LAST]) + "|")
		print("/" + color(self.cube[L, LAST, LAST]) + color(self.cube[L, LAST, MIDDLE]) + color(self.cube[L, LAST, FIRST]) +"/  /" + color(self.cube[U, LAST, FIRST]) + color(self.cube[U, LAST, MIDDLE]) + color(self.cube[U, LAST, LAST]) +"/" + color(self.cube[R, FIRST, FIRST]) + color(self.cube[R, MIDDLE, MIDDLE]) + color(self.cube[R, LAST, LAST]) + "|")
		print("       |" + color(self.cube[F, FIRST, FIRST]) + color(self.cube[F, FIRST, MIDDLE]) + color(self.cube[F, FIRST, LAST]) +"|" + color(self.cube[R, MIDDLE, FIRST]) + color(self.cube[R, LAST, MIDDLE]) + "/")
		print("       |" + color(self.cube[F, MIDDLE, FIRST]) + color(self.cube[F, MIDDLE, MIDDLE]) + color(self.cube[F, MIDDLE, LAST]) +"|" + color(self.cube[R, LAST, FIRST]) + "/")
		print("       |" + color(self.cube[F, LAST, FIRST]) + color(self.cube[F, LAST, MIDDLE]) + color(self.cube[F, LAST, LAST]) +"|/")
		print("          ____")
		print("         /" + color(self.cube[D, LAST, FIRST]) + color(self.cube[D, LAST, MIDDLE]) + color(self.cube[D, LAST, LAST]) + "/")
		print("        /" + color(self.cube[D, MIDDLE, FIRST]) + color(self.cube[D, MIDDLE, MIDDLE]) + color(self.cube[D, MIDDLE, LAST]) + "/")
		print("       /" + color(self.cube[D, FIRST, FIRST]) + color(self.cube[D, FIRST, MIDDLE]) + color(self.cube[D, FIRST, LAST]) + "/")

	def print_cube(self):
		print("    |" + color(self.cube[U, FIRST, FIRST])  + color(self.cube[U, FIRST, MIDDLE])  + color(self.cube[U, FIRST, LAST])  +"|")
		print("    |" + color(self.cube[U, MIDDLE, FIRST]) + color(self.cube[U, MIDDLE, MIDDLE]) + color(self.cube[U, MIDDLE, LAST]) +"|")
		print("    |" + color(self.cube[U, LAST, FIRST])   + color(self.cube[U, LAST, MIDDLE])   + color(self.cube[U, LAST, LAST])   +"|")
		print()
		print("|" + color(self.cube[L, FIRST, FIRST])  + color(self.cube[L, FIRST, MIDDLE])  + color(self.cube[L, FIRST, LAST])  +"|" + color(self.cube[F, FIRST, FIRST])  + color(self.cube[F, FIRST, MIDDLE])  + color(self.cube[F, FIRST, LAST])  + "|" + color(self.cube[R, FIRST, FIRST])  + color(self.cube[R, FIRST, MIDDLE])  + color(self.cube[R, FIRST, LAST])  + "|" + color(self.cube[B, FIRST, FIRST])  + color(self.cube[B, FIRST, MIDDLE])  + color(self.cube[B, FIRST, LAST])  + "|")
		print("|" + color(self.cube[L, MIDDLE, FIRST]) + color(self.cube[L, MIDDLE, MIDDLE]) + color(self.cube[L, MIDDLE, LAST]) +"|" + color(self.cube[F, MIDDLE, FIRST]) + color(self.cube[F, MIDDLE, MIDDLE]) + color(self.cube[F, MIDDLE, LAST]) + "|" + color(self.cube[R, MIDDLE, FIRST]) + color(self.cube[R, MIDDLE, MIDDLE]) + color(self.cube[R, MIDDLE, LAST]) + "|" + color(self.cube[B, MIDDLE, FIRST]) + color(self.cube[B, MIDDLE, MIDDLE]) + color(self.cube[B, MIDDLE, LAST]) + "|")
		print("|" + color(self.cube[L, LAST, FIRST])   + color(self.cube[L, LAST, MIDDLE])   + color(self.cube[L, LAST, LAST])   +"|" + color(self.cube[F, LAST, FIRST])   + color(self.cube[F, LAST, MIDDLE])   + color(self.cube[F, LAST, LAST])   + "|" + color(self.cube[R, LAST, FIRST])   + color(self.cube[R, LAST, MIDDLE])   + color(self.cube[R, LAST, LAST])   + "|" + color(self.cube[B, LAST, FIRST])   + color(self.cube[B, LAST, MIDDLE])   + color(self.cube[B, LAST, LAST])   + "|")
		print()
		print("    |" + color(self.cube[D, FIRST, FIRST])  + color(self.cube[D, FIRST, MIDDLE])  + color(self.cube[D, FIRST, LAST])  +"|")
		print("    |" + color(self.cube[D, MIDDLE, FIRST]) + color(self.cube[D, MIDDLE, MIDDLE]) + color(self.cube[D, MIDDLE, LAST]) +"|")
		print("    |" + color(self.cube[D, LAST, FIRST])   + color(self.cube[D, LAST, MIDDLE])   + color(self.cube[D, LAST, LAST])   +"|")
		print("\n")

cube = np.array([[[ORANGE, ORANGE, ORANGE],
				  [ORANGE, ORANGE, ORANGE],
				  [ORANGE, ORANGE, ORANGE]], # orange
				 [[RED, RED, RED],
				  [RED, RED, RED],
				  [RED, RED, RED]], # red
				 [[WHITE, WHITE, WHITE],
				  [WHITE, WHITE, WHITE],
				  [WHITE, WHITE, WHITE]], # white
				 [[YELLOW, YELLOW, YELLOW],
				  [YELLOW, YELLOW, YELLOW],
				  [YELLOW, YELLOW, YELLOW]], # yellow
				 [[BLUE, BLUE, BLUE],
				  [BLUE, BLUE, BLUE],
				  [BLUE, BLUE, BLUE]], # blue
				 [[GREEN, GREEN, GREEN],
				  [GREEN, GREEN, GREEN],
				  [GREEN, GREEN, GREEN]]]) # green
