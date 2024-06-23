import pygame, asyncio
# import math
from queue import PriorityQueue
from collections import deque

pygame.init()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


# A* algorithm
def astar_algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return


		current = open_set.get()[2]
		open_set_hash.remove(current)
		# print(open_set_hash)
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


# dijkstra algorithm
def dijkstra_algorithm(draw, grid, start, end):
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	dist = {spot: float("inf") for row in grid for spot in row}
	dist[start] = 0
	

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[1]
		open_set_hash.remove(current)
		# print(open_set_hash)
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_dist = dist[current] + 1

			if temp_dist < dist[neighbor]:
				came_from[neighbor] = current
				dist[neighbor] = temp_dist
				if neighbor not in open_set_hash:
					open_set.put((dist[neighbor],neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

# bfs algorithm
def bfs_algorithm(draw, grid, start, end):
	open_set = deque()

	came_from = {}
	dist = {spot: float("inf") for row in grid for spot in row}
	dist[start] = 0
	open_set.append(start)

	while open_set:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.popleft()
	
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_dist = dist[current] + 1

			if temp_dist < dist[neighbor]:
				came_from[neighbor] = current
				dist[neighbor] = temp_dist
				open_set.append(neighbor)
				neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

	


def main_algos(win, width,algo):

	ROWS = 50
	grid = make_grid(ROWS, width)
	if algo == 1:
		pygame.display.set_caption('Astar algorithm')
	elif algo == 2:
		pygame.display.set_caption('Dijkstra algorithm')
	elif algo == 3:
		pygame.display.set_caption('BFS algorithm')

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					if algo == 1:
						astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == 2:
						dijkstra_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == 3:
						bfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.display.set_caption('Pathfinding Visualiser')

	
	
	return

















WIDTH = 750
HEIGHT = 750
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pathfinding Visualiser')
main_menu = False
font = pygame.font.Font('freesansbold.ttf', 24)
bg = pygame.transform.scale(pygame.image.load('Logo.png'), (400, 390))
ball = pygame.transform.scale(pygame.image.load('Logo.png'), (450, 400))

menu_command = 0


class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = font.render(self.text, True, 'black')
        screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False


def draw_menu():
    command = -1
    pygame.draw.rect(screen, 'black', [100, 100, 500, 500])
    screen.blit(bg, (150, 180))
    pygame.draw.rect(screen, 'green', [100, 100, 500, 500], 5)
    pygame.draw.rect(screen, 'white', [100, 120,500, 40], 0, 5)
    pygame.draw.rect(screen, 'gray', [100, 120, 500, 40], 5, 5)
    txt = font.render('***Select the Pathfinding Algorithm***', True, 'black')
    screen.blit(txt, (132, 125))
    # menu exit button
    menu = Button('<-----Exit Menu', (220, 500))
    menu.draw()
    button1 = Button('A* Algorithm', (220, 220))
    button1.draw()
    button2 = Button('Dijkstra Algorithm', (220, 270))
    button2.draw()
    button3 = Button('BFS Algorithm', (220, 320))
    button3.draw()
    if menu.check_clicked():
        command = 0
    if button1.check_clicked():
        main_algos(screen,WIDTH,1)
    if button2.check_clicked():
        main_algos(screen,WIDTH,2)
    if button3.check_clicked():
        main_algos(screen,WIDTH,3)
    return command


def draw_game():
    txt = font.render('***Visualise Pathfinding algorithms!***', True, 'black')
    screen.blit(txt, (130,70))
    menu_btn = Button("LET's GO ----->", (270, 600))
    menu_btn.draw()
    menu = menu_btn.check_clicked()
    screen.blit(ball, (155, 175))
    return menu

async def main():
	run = True
	main_menu = False
	while run:
		screen.fill('light blue')
		timer.tick(fps)
		
		if main_menu:
			menu_command = draw_menu()
			if menu_command != -1:
				main_menu = False
		else:
			main_menu = draw_game()
						

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		pygame.display.flip()
		await asyncio.sleep(0)
	pygame.quit()
	

asyncio.run(main())

