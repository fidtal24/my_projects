import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from pygame.math import Vector3
import random
import rubik
import cube_solver as solver
import patterns

# rotatioin matrix LUT
trig_rot_mat_lut = []
for deg in range(360):
	theta = np.radians(deg)
	c, s = np.cos(theta), np.sin(theta)
	trig_rot_mat_lut.append([[[c, 1 - c], [1 - c, -s], [1 - c, s]],
						[[1 - c, s], [c, 1 - c], [1 - c, -s]],
						[[1 - c, -s], [1 - c, s], [c, 1 - c]]])

# cube geometry and appearance
# colors
ORANGE = (1, 0.5, 0)
RED = (1, 0, 0)
YELLOW = (1, 1, 0)
WHITE = (1, 1, 1)
BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
BLACK = (0, 0, 0)
colors = [ORANGE, RED, WHITE, YELLOW, BLUE, GREEN, BLACK]

vertices = (
	(1, -1, -1),
	(1, 1, -1),
	(-1, 1, -1),
	(-1, -1, -1),
	(1, -1, 1),
	(1, 1, 1),
	(-1, -1, 1),
	(-1, 1, 1)
)

edges = (
	(0, 1),
	(0, 3),
	(0, 4),
	(2, 1),
	(2, 3),
	(2, 7),
	(6, 3),
	(6, 4),
	(6, 7),
	(5, 1),
	(5, 4),
	(5, 7)
)

size = (0.5, 0.5, 0.5)

def game_init():
	pygame.init()

	# Set up the display
	screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
	glClearColor(0.5, 0.5, 0.5, 1.0)
	# Set up the 3D rendering engine (PyOpenGL)
	glViewport(0, 0, 800, 600)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 800/600, 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)

	# isometric view
	glTranslatef(0.0, 0.0, -10)
	glRotatef(30, 1, 0, 0)
	glRotatef(-30, 0, 1, 0)

	# Enable depth testing
	glEnable(GL_DEPTH_TEST)


class Rubik3D:
	def __init__(self, start=patterns.DEFAULT):
		self.rubik = rubik.Rubik(start)
		self.cubes = [
			# front sheet
			Cube([-1, -1, -1], size),
			Cube([0, -1, -1], size),
			Cube([1, -1, -1], size),
			Cube([-1, 0, -1], size),
			Cube([0, 0, -1], size),
			Cube([1, 0, -1], size),
			Cube([-1, 1, -1], size),
			Cube([0, 1, -1], size),
			Cube([1, 1, -1], size),
			# middle sheet
			Cube([-1, -1, 0], size),
			Cube([0, -1, 0], size),
			Cube([1, -1, 0], size),
			Cube([-1, 0, 0], size),
			Cube([0, 0, 0], size),
			Cube([1, 0, 0], size),
			Cube([-1, 1, 0], size),
			Cube([0, 1, 0], size),
			Cube([1, 1, 0], size),
			# back sheet
			Cube([-1, -1, 1], size),
			Cube([0, -1, 1], size),
			Cube([1, -1, 1], size),
			Cube([-1, 0, 1], size),
			Cube([0, 0, 1], size),
			Cube([1, 0, 1], size),
			Cube([-1, 1, 1], size),
			Cube([0, 1, 1], size),
			Cube([1, 1, 1], size),
		]

	def get_val(self, face, row, col):
		return self.rubik.get_val(face, row, col)

	def update_colors(self):
		# front sheet
		self.cubes[0].colors = [6, self.get_val(rubik.B, 2, 2), 6, self.get_val(rubik.D, 2, 0), self.get_val(rubik.L, 2, 0), 6]
		self.cubes[1].colors = [6, self.get_val(rubik.B, 2, 1), 6, self.get_val(rubik.D, 2, 1), 6, 6]
		self.cubes[2].colors = [6, self.get_val(rubik.B, 2, 0), 6, self.get_val(rubik.D, 2, 2), 6, self.get_val(rubik.R, 2, 2)]
		self.cubes[3].colors = [6, self.get_val(rubik.B, 1, 2), 6, 6, self.get_val(rubik.L, 1, 0), 6]
		self.cubes[4].colors = [6, self.get_val(rubik.B, 1, 1), 6, 6, 6, 6]
		self.cubes[5].colors = [6, self.get_val(rubik.B, 1, 0), 6, 6, 6, self.get_val(rubik.R, 1, 2)]
		self.cubes[6].colors = [6, self.get_val(rubik.B, 0, 2), self.get_val(rubik.U, 0, 0), 6, self.get_val(rubik.L, 0, 0), 6]
		self.cubes[7].colors = [6, self.get_val(rubik.B, 0, 1), self.get_val(rubik.U, 0, 1), 6, 6, 6]
		self.cubes[8].colors = [6, self.get_val(rubik.B, 0, 0), self.get_val(rubik.U, 0, 2), 6, 6, self.get_val(rubik.R, 0, 2)]
		# middle sheet
		self.cubes[9].colors =  [6, 6, 6, self.get_val(rubik.D, 1, 0), self.get_val(rubik.L, 2, 1), 6]
		self.cubes[10].colors = [6, 6, 6, self.get_val(rubik.D, 1, 1), 6, 6]
		self.cubes[11].colors = [6, 6, 6, self.get_val(rubik.D, 1, 2), 6, self.get_val(rubik.R, 2, 1)]
		self.cubes[12].colors = [6, 6, 6, 6, self.get_val(rubik.L, 1, 1), 6]
		self.cubes[13].colors = [6, 6, 6, 6, 6, 6]
		self.cubes[14].colors = [6, 6, 6, 6, 6, self.get_val(rubik.R, 1, 1)]
		self.cubes[15].colors = [6, 6, self.get_val(rubik.U, 1, 0), 6, self.get_val(rubik.L, 0, 1), 6]
		self.cubes[16].colors = [6, 6, self.get_val(rubik.U, 1, 1), 6, 6, 6]
		self.cubes[17].colors = [6, 6, self.get_val(rubik.U, 1, 2), 6, 6, self.get_val(rubik.R, 0, 1)]
		# back sheet
		self.cubes[18].colors = [self.get_val(rubik.F, 2, 0), 6, 6, self.get_val(rubik.D, 0, 0), self.get_val(rubik.L, 2, 2), 6]
		self.cubes[19].colors = [self.get_val(rubik.F, 2, 1), 6, 6, self.get_val(rubik.D, 0, 1), 6, 6]
		self.cubes[20].colors = [self.get_val(rubik.F, 2, 2), 6, 6, self.get_val(rubik.D, 0, 2), 6, self.get_val(rubik.R, 2, 0)]
		self.cubes[21].colors = [self.get_val(rubik.F, 1, 0), 6, 6, 6, self.get_val(rubik.L, 1, 2), 6]
		self.cubes[22].colors = [self.get_val(rubik.F, 1, 1), 6, 6, 6, 6, 6]
		self.cubes[23].colors = [self.get_val(rubik.F, 1, 2), 6, 6, 6, 6, self.get_val(rubik.R, 1, 0)]
		self.cubes[24].colors = [self.get_val(rubik.F, 0, 0), 6, self.get_val(rubik.U, 2, 0), 6, self.get_val(rubik.L, 0, 2), 6]
		self.cubes[25].colors = [self.get_val(rubik.F, 0, 1), 6, self.get_val(rubik.U, 2, 1), 6, 6, 6]
		self.cubes[26].colors = [self.get_val(rubik.F, 0, 2), 6, self.get_val(rubik.U, 2, 2), 6, 6, self.get_val(rubik.R, 0, 0)]

	def get_instructions_to_solve(self, dest) -> list[str]:
		s = solver.Solver(self.rubik, dest)
		return s.solve()

# Define a class for your 3D object
class Cube:
	def __init__(self, position, size):
		self.mini_cube_type = np.sum(np.abs(np.array(position)))
		self.position = tuple(position)
		self.size = size
		self.rotation = [0, 0, 0]
		self.colors = colors

	def update(self, angle, pos):
		# Update the cube's rotation based on the elapsed time (dt)
		self.rotation[0] += angle[0]
		self.rotation[1] += angle[1]
		self.rotation[2] += angle[2]
		self.position = pos

	def render(self):
		# Set up the cube's transformation (position, rotation, size)
		glPushMatrix()
		glTranslatef(*tuple(self.position))
		glRotatef(self.rotation[0], 1, 0, 0)
		glRotatef(self.rotation[1], 0, 1, 0)
		glRotatef(self.rotation[2], 0, 0, 1)
		glScalef(*self.size)

		# Draw the cube with different colors for each face
		glBegin(GL_QUADS)
		# Front face (orange)
		glColor3f(*colors[self.colors[rubik.F]])
		glVertex3f(-1, -1, 1)
		glVertex3f(1, -1, 1)
		glVertex3f(1, 1, 1)
		glVertex3f(-1, 1, 1)

		# Back face (red)
		glColor3f(*colors[self.colors[rubik.B]])
		glVertex3f(-1, -1, -1)
		glVertex3f(1, -1, -1)
		glVertex3f(1, 1, -1)
		glVertex3f(-1, 1, -1)

		# Up face (yellow)
		glColor3f(*colors[self.colors[rubik.U]])
		glVertex3f(-1, 1, -1)
		glVertex3f(1, 1, -1)
		glVertex3f(1, 1, 1)
		glVertex3f(-1, 1, 1)

		# Down face (white)
		glColor3f(*colors[self.colors[rubik.D]])
		glVertex3f(-1, -1, -1)
		glVertex3f(1, -1, -1)
		glVertex3f(1, -1, 1)
		glVertex3f(-1, -1, 1)

		# Left face (blue)
		glColor3f(*colors[self.colors[rubik.L]])
		glVertex3f(-1, -1, -1)
		glVertex3f(-1, 1, -1)
		glVertex3f(-1, 1, 1)
		glVertex3f(-1, -1, 1)

		# Right face (green)
		glColor3f(*colors[self.colors[rubik.R]])
		glVertex3f(1, -1, -1)
		glVertex3f(1, 1, -1)
		glVertex3f(1, 1, 1)
		glVertex3f(1, -1, 1)

		glEnd()

		glLineWidth(2)
		glBegin(GL_LINES)
		glColor3fv((0, 0, 0))
		for edge in edges:
			for vertex in edge:
				glVertex3fv(vertices[vertex])
		glEnd()

		# Pop the cube's transformation matrix off the stack
		glPopMatrix()


# defining a font
# smallfont = pygame.font.SysFont('Corbel',35)
# color = (255,255,255)
# # rendering a text written in
# # this font
# text = smallfont.render('quit' , True , color)

class CubeRotator:
	def __init__(self):
		self.cube3d = Rubik3D(patterns.CHECKER_BOARD)

		right =      [cube for cube in self.cube3d.cubes if list(cube.position)[0] ==  1]
		left  =      [cube for cube in self.cube3d.cubes if list(cube.position)[0] == -1]
		up    =      [cube for cube in self.cube3d.cubes if list(cube.position)[1] ==  1]
		down  =      [cube for cube in self.cube3d.cubes if list(cube.position)[1] == -1]
		front =      [cube for cube in self.cube3d.cubes if list(cube.position)[2] ==  1]
		back  =      [cube for cube in self.cube3d.cubes if list(cube.position)[2] == -1]
		mid_left  =  [cube for cube in self.cube3d.cubes if list(cube.position)[0] ==  0]
		mid_up =     [cube for cube in self.cube3d.cubes if list(cube.position)[1] ==  0]
		mid_front  = [cube for cube in self.cube3d.cubes if list(cube.position)[2] ==  0]

		self.sheet_axis = [Vector3(0, 0, 1), Vector3(0, 0, 1), Vector3(0, 1, 0),
						   Vector3(0, 1, 0), Vector3(1, 0, 0), Vector3(1, 0, 0)]
		self.sheets = [front, back, up, down, left, right, mid_left, mid_up, mid_front]
		self.face_angles = [[0, 0, 1], [0, 0, -1], [0, 1, 0], [0, -1, 0], [-1, 0, 0], [1, 0, 0]]
		self.relative_faces = ["F", "B", "U", "D", "L", "R"]

	def get_rotation_matrix(self, num, angle, direction):
		axis_num = 0
		for i in range(3):
			if angle[i] != 0:
				axis_num = i

		rot_mat = trig_rot_mat_lut[(direction * angle[axis_num]) % 360]
		u = self.sheet_axis[num].normalize()
		x, y, z = u
		dim_mat = [[[1, x ** 2], [x * y, z],  [x * z, y]],
				   [[y * x, z],  [1, y ** 2], [y * z, x]],
				   [[z * x, y],  [z * y, x],  [1, z ** 2]]]

		rotation_matrix = np.empty((3, 3))
		for i in range(3):
			for j in range(3):
				rotation_matrix[i, j] = np.dot(dim_mat[i][j], rot_mat[i][j])

		return rotation_matrix

	def rotate(self, faces: list[int], direction: list[int], is_animated: bool):
		angle_inc = 1 if is_animated else 90
		angle_3d = [angle_inc * face_angle for face_angle in self.face_angles[faces[0]]]
		rotation_matrix = self.get_rotation_matrix(faces[0], angle_3d, direction[0])

		for i in range(90 if is_animated else 1):
			for face in faces:
				sheet_of_cubes = []
				for cube in self.sheets[face]:
					sheet_of_cubes.append(Vector3(*tuple(cube.position)))

				# Rotate the sheet of small cubes
				for i, cube in enumerate(sheet_of_cubes):
					sheet_of_cubes[i] = Vector3(*np.dot(rotation_matrix, cube))

				# Update the cubes' rotations
				clock.tick(240)
				for i, cube in enumerate(self.sheets[face]):
					cube.update([angle * direction[faces.index(face)] for angle in angle_3d], list(sheet_of_cubes[i]))

			# Clear the screen
			if is_animated:
				glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
				# Render the cubes
				for cube in self.cube3d.cubes:
					cube.render()

			# Flip the display
			pygame.display.flip()

	def instruction_interpreter(self, instruction: str):
		whole_cube = {0: [1, 8], 1: [0, 8], 2: [3, 7], 3: [2, 7], 4: [5, 6], 5: [4, 6]}
		faces = []
		directions = []
		faces.append(self.relative_faces.index(instruction[0]))
		# if len(instruction) > 0:

		directions.append(1 if (len(instruction) > 1) and (instruction[1] == "'") else -1)
		if (len(instruction) > 0) and (instruction[-1] == "_"):
			faces.extend(whole_cube.get(faces[0]))
			directions.extend([directions[0], directions[0]])

		return faces, directions

	def animated_rotation(self, instruction: str):
		face, directions = self.instruction_interpreter(instruction)
		self.rotate(face, directions, True)
		self.rotate(face, [-1 * dir for dir in directions], False)

if __name__ == "__main__":
	game_init()
	cube_rotator = CubeRotator()
	instructions = ["F_", "F'_", "U_", "U'_", "L_", "L'_",
					"F", "F", "B'", "B'", "U", "U", "D'", "D'", "L", "L", "R'", "R'",
					"F'", "F'", "B", "B", "U'", "U'", "D", "D", "L'", "L'", "R", "R"]
	i = 0

	# Start the game loop
	clock = pygame.time.Clock()
	orientations = {"F": (0, 2), "F'": (0, 3), "L": (2, 5), "L'": (3, 5), "U": (5, 1), "U'": (4, 0)}
	l = len(instructions)
	while True:
		cube_rotator.cube3d.update_colors()
		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()
		if instructions[i][-1] == "_":
			front, right = orientations.get(instructions[i][:-1])
			front_color = cube_rotator.cube3d.rubik.get_val(front, 1, 1)
			right_color = cube_rotator.cube3d.rubik.get_val(right, 1, 1)
			cube_rotator.cube3d.rubik.bring_face_to_front(front_color, right_color)
		else:
			cube_rotator.cube3d.rubik.play([instructions[i]])
		cube_rotator.animated_rotation(instructions[i])
		i += 1
		i %= l
