import rubik as r
import cube_solver as solver
import pygame
import test

WIDTH = 1600
HEIGHT = 900

GRAY   = (127, 127, 127)
ORANGE = (255, 100,   0)
RED    = (255,   0,   0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255,   0)
BLUE   = (  0,   0, 255)
GREEN  = (  0, 255,   0)

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("rubik's cube 2d")

def draw_window():
	WIN.fill(GRAY)
	pygame.display.update()

def draw_front(cube: r.Rubik):
	colors_dict = {r.ORANGE:ORANGE, r.RED:RED, r.WHITE:WHITE, r.YELLOW:YELLOW, r.BLUE:BLUE, r.GREEN:GREEN}
	front = cube.cube[r.F]
	# print(cube.cube[r.F])
	tile_dims = [40, 40]
	start_tiles = [40, 40]
	for i in range(3):
		for j in range(3):
			tile = pygame.Rect(start_tiles[0] + (j * 40), start_tiles[1] + (i * 40), tile_dims[0], tile_dims[1])
			pygame.draw.rect(WIN, colors_dict[front[i][j]], tile)

	pygame.display.update()

def main():
	cube = r.Rubik(test.CHECKER_BOARD)
	c = solver.Solver(test.DEFAULT, test.CHECKER_BOARD)
	c.play(['D', "U'", 'R', 'R', 'B', "R'", "F'", 'F', 'F', 'B'])
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		draw_window()
		draw_front(c.cubes[0])

	pygame.quit()


if __name__ == "__main__":
	main()