import numpy as np
import rubik as r

DEFAULT = np.array([[[r.ORANGE, r.ORANGE, r.ORANGE], [r.ORANGE, r.ORANGE, r.ORANGE], [r.ORANGE, r.ORANGE, r.ORANGE]],
					[[r.RED, r.RED, r.RED], [r.RED, r.RED, r.RED], [r.RED, r.RED, r.RED]],
					[[r.WHITE, r.WHITE, r.WHITE], [r.WHITE, r.WHITE, r.WHITE], [r.WHITE, r.WHITE, r.WHITE]],
					[[r.YELLOW, r.YELLOW, r.YELLOW], [r.YELLOW, r.YELLOW, r.YELLOW], [r.YELLOW, r.YELLOW, r.YELLOW]],
					[[r.BLUE, r.BLUE, r.BLUE], [r.BLUE, r.BLUE, r.BLUE], [r.BLUE, r.BLUE, r.BLUE]],
					[[r.GREEN, r.GREEN, r.GREEN], [r.GREEN, r.GREEN, r.GREEN], [r.GREEN, r.GREEN, r.GREEN]]])

CHECKER_BOARD = np.array([[[r.ORANGE, r.RED, r.ORANGE], [r.RED, r.ORANGE, r.RED], [r.ORANGE, r.RED, r.ORANGE]],
						  [[r.RED, r.ORANGE, r.RED], [r.ORANGE, r.RED, r.ORANGE], [r.RED, r.ORANGE, r.RED]],
						  [[r.WHITE, r.YELLOW, r.WHITE], [r.YELLOW, r.WHITE, r.YELLOW], [r.WHITE, r.YELLOW, r.WHITE]],
						  [[r.YELLOW, r.WHITE, r.YELLOW], [r.WHITE, r.YELLOW, r.WHITE], [r.YELLOW, r.WHITE, r.YELLOW]],
						  [[r.BLUE, r.GREEN, r.BLUE], [r.GREEN, r.BLUE, r.GREEN], [r.BLUE, r.GREEN, r.BLUE]],
						  [[r.GREEN, r.BLUE, r.GREEN], [r.BLUE, r.GREEN, r.BLUE], [r.GREEN, r.BLUE, r.GREEN]]])