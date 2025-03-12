import pygame, sys
import pygame.draw as pydraw
import pygame.gfxdraw
import time
import threading
import math

import draw

from utils.helpers import range2, OPPOSITE, in_bounds, nexts

class Interpolator:
	def __init__(self, start, end, duration, increment=None):
		self.start = start # Deprecated
		self.end = end
		self.increment = increment
		self.duration = duration
		self.done = False
		self.progress = 0
		self.time = 0
	def update(self):
		self.time += 1
		self.progress = min(self.time / self.duration, 1)
		if self.progress == 1.0: self.done = True
		# 1.0*20 = 20 # 1.0*20-15 = 5 + 15 = 20
		return (self.progress * (self.end - self.start)) + self.start
	def reset(self):
		self.time = 0
		self.progress = 0
		self.done = False
	def join(self, state_set, end_check, transform):
		def start_interpolation_cycle(self):
			if not end_check(self):
				state_set(transform(self.update()))
			return True
		threading.Thread(target=start_interpolation_cycle, args=(self,)).start()
		return False

class Application:
	def __init__(self, w=1000, h=800):
		self.width = w
		self.height = h
		self.running = True

		pygame.init()
		self.screen = pygame.display.set_mode((w, h), vsync=1)
		pygame.display.set_caption("Reversi", "Reversi")

		self.cheats_enabled = False
		self.game = "Othello"
		self.beginning_player = 1
		self.player_turn = self.beginning_player
		self.username1 = "Black"
		self.username2 = "White"
		self.winner = None
		self.grid = [[0 for _ in range(8)] for _ in range(8)]

		self.do_show_legal_moves = True
		self.legal_move_size = 1
		self.font = pygame.font.SysFont("Arial", 30)

		self.animation_legal = Interpolator(1, 20, 20)
		self.animation_flip = Interpolator(0, 255, 50)
		self.animation_place = Interpolator(0, 40, 50)
		self.animation_place_colorchange = Interpolator(0, 20, 50)

		self.animation_enabled = {
			"flip": True,
			"place": True,
			"legal": True
		}

	def main_loop(self):
		self.reset_board()
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE: self.reset_board()
					if self.cheats_enabled:
						if event.key == pygame.K_LALT: self.player_turn = 1
						if event.key == pygame.K_RALT: self.player_turn = 2
					if event.key == pygame.K_l: self.do_show_legal_moves = not self.do_show_legal_moves
					if event.key == pygame.K_c: self.cheats_enabled = not self.cheats_enabled
					if event.key == pygame.K_a:
						self.animation_enabled["flip"] = not self.animation_enabled["flip"]
						self.animation_enabled["place"] = not self.animation_enabled["place"]
						self.animation_enabled["legal"] = not self.animation_enabled["legal"]

			self.screen.fill((0,0,0))
			pygame.draw.rect(self.screen, (139,90,43), pygame.Rect(802,2,198,798))

			white_pieces, black_pieces = self.total_pieces

			text = draw.text(self.screen, self.font, self.username1, (255,255,255), (820, 50))
			pygame.draw.aaline(self.screen, (255,255,255), (820,80), (830+text.get_width(),80), 5)
			text = draw.text(self.screen, self.font, self.username2, (255,255,255), (820, 145))
			pygame.draw.aaline(self.screen, (255,255,255), (820,175), (830+text.get_width(),175), 5)

			self.draw_chip(0, 0, (0, 0, 0), 15, 830, 115)
			draw.text(self.screen, self.font, str(black_pieces), (255,255,255), (850, 100))
			self.draw_chip(0, 0, (255, 255, 255), 15, 830, 205)
			draw.text(self.screen, self.font, str(white_pieces), (255,255,255), (850, 190))

			self.draw_board_grid()
			self.draw_board_orientationpoints()
			self.draw_board_grid_lines()

			if self.do_show_legal_moves:
				if self.animation_enabled["legal"]:
					time.sleep(1/1000)
					def size_set(size):
						self.legal_move_size = size
					self.animation_legal.join(size_set, lambda self: self.done, int)
				else:
					self.legal_move_size = self.animation_legal.end
				self.draw_legal_moves(self.legal_move_size)

			self.draw_board_discs()

			if (self.is_player_able_to_play(1) or self.is_player_able_to_play(2)):
				draw.text(self.screen, self.font, self.game, (255,255,255), (850, 10))
			pygame.draw.aaline(self.screen, (255,255,255), (820,40), (980,40), 5)


			if self.player_turn != 0 and self.winner == None:
				pos = pygame.mouse.get_pos()
				gridposx = pos[0]//100
				gridposy = pos[1]//100
				if self.is_player_able_to_play(self.player_turn):
					newpos = (pos[0]//100*100 + 50, pos[1]//100*100 + 50)
					self.play_check_all(gridposx, gridposy, OPPOSITE[self.player_turn], self.player_turn, 0, OPPOSITE[self.player_turn], newpos)
				else:
					if self.game == "Othello": self.player_turn = OPPOSITE[self.player_turn]
					elif self.game == "Reversi": self.winner = 3

			if not(self.is_player_able_to_play(1) or self.is_player_able_to_play(2)):
				white_pieces, black_pieces = self.total_pieces
				if white_pieces > black_pieces:
					draw.text(self.screen, self.font, "White Wins", (255,255,255), (825, 10))
					self.winner = 2
				elif white_pieces < black_pieces:
					draw.text(self.screen, self.font, "Black Wins", (255,255,255), (825, 10))
					self.winner = 1
				else:
					draw.text(self.screen, self.font, "Draw", (255,255,255), (865, 10))
					self.winner = 3
				draw.text(self.screen, self.font, "Space to Reset", (255,255,255), (800, 760))
			if self.cheats_enabled and self.winner == None:
				draw.text(self.screen, self.font, "Cheats On", (255,125,125), (815, 760))
			if self.player_turn == 3:
				self.winner = 3
			pygame.display.update()



	def reset_board(self):
		self.grid = [[0 for _ in range(8)] for _ in range(8)]
		self.grid[4][4] = 2
		self.grid[3][3] = 2
		self.grid[4][3] = 1
		self.grid[3][4] = 1
		self.player_turn = self.beginning_player
		winner = None
		return self
	def check_line(self, x, y, val, piece, amount, continue_check=False, nextx=0, nexty=0):
		if in_bounds(x, y):
			if continue_check:
				if self.check_pos_value(x, y, val):
					return self.check_line(x+nextx, y+nexty, val, piece, amount+1, True, nextx, nexty)
				elif self.check_pos_value(x, y, piece):
					return amount+1
				return 0
			if self.check_pos_value(x, y, 0) and self.check_pos_value(x+nextx, y+nexty, val):
				return self.check_line(x+nextx, y+nexty, val, piece, amount+1, True, nextx, nexty)
		return 0
	def flip_line(self, x, y, val, piece, amount, nextx=0, nexty=0, rep=0):
		if in_bounds(x, y) and not rep <= 2:
			self.grid[y][x] = piece
			if self.animation_enabled["flip"]:
				self.draw_board_grid()
				self.draw_board_grid_lines()
				self.draw_board_orientationpoints()
				self.draw_board_discs()
				while not self.animation_flip.done:
					color = self.animation_flip.update()
					time.sleep(1/1000)
					draw.aacircle(self.screen, 50+100*x,50+100*y, 39, (color,color,color) if self.grid[y][x] == 2 else (255-color,255-color,255-color))
					pygame.display.update()
				self.animation_flip.reset()
			return self.flip_line(x+nextx, y+nexty, val, piece, amount+1, nextx=nextx, nexty=nexty, rep=rep-1)
		return self.grid
	def play_check_all(self, gridposx, gridposy, val, piece, amount, next_turn, newpos):
		mousedown = pygame.mouse.get_pressed()[0]
		if mousedown:
			self.animation_legal.reset()
		flips = []
		placable = False
		for i in range(len(nexts)):
			reps = self.check_line(gridposx, gridposy, val, piece, amount, False, nexts[i][0], nexts[i][1])
			if reps > 0:
				if not mousedown: draw.aacircle_outline(self.screen, newpos[0], newpos[1], 39, (0,30,0) if self.player_turn == 1 else (235,235,235), 5)
				else:
					flips.append([nexts[i], reps])
					placable = True
		if not placable: return False
		if self.animation_enabled["place"]:
			self.animation_place.start = 20 if self.do_show_legal_moves else 0
			self.animation_place.reset()
			self.animation_place_colorchange.reset()
			while not self.animation_place.done:
				size = int(self.animation_place.update())
				time.sleep(1/1000)
				colorchange = int(self.animation_place_colorchange.update())
				draw.aacircle(self.screen, 50+100*gridposx,50+100*gridposy, size, (30-colorchange,30-colorchange,30-colorchange) if self.player_turn == 1 else (200+colorchange,200+colorchange,200+colorchange))
				pygame.display.update()
		self.grid[gridposy][gridposx] = self.player_turn
		self.player_turn = next_turn
		for i in range(len(flips)):
			self.grid = self.flip_line(gridposx+flips[i][0][0], gridposy+flips[i][0][1], val, piece, amount, nextx=flips[i][0][0], nexty=flips[i][0][1], rep=flips[i][1])
	def check_all(self, gridposx, gridposy, val, piece, amount):
		for i in range(len(nexts)):
			if self.check_line(gridposx, gridposy, val, piece, amount, False, nexts[i][0], nexts[i][1]) > 0: return True
		return False
	def draw_legal_moves(self, size=20):
		for x, y in range2(8, 8):
			if self.check_all(x, y, OPPOSITE[self.player_turn], self.player_turn, 0):
				draw.aacircle(self.screen, 50+x*100,50+y*100, size, (30,30,30) if self.player_turn == 1 else (200,200,200))


	def is_player_able_to_play(self, player_turn):
		all_empty_spots = [(x, y) for x in range(8) for y in range(8) if self.grid[y][x] == 0]
		for i in all_empty_spots:
			if self.check_all(i[0], i[1], OPPOSITE[player_turn], player_turn, 0): return True
		return False
	def check_pos_value(self, x, y, value_to_check):
		if in_bounds(x, y):
			if self.grid[y][x] == value_to_check: return True
		return False
	@property
	def total_pieces(self):
		white_pieces, black_pieces = sum(self.grid[y][x] == 2 for x, y in range2(8, 8)), sum(self.grid[y][x] == 1 for x, y in range2(8, 8))
		return white_pieces, black_pieces
	@property
	def enable_cheats(self):
		self.cheats_enabled = True
		return self
	def set_username(self, p, name):
		if p == 1: self.username1 = name
		elif p == 2: self.username2 = name
		return self
	def draw_board_discs(self):
		for x, y in range2(8, 8):
			self.draw_chip(x, y, (0,0,0) if self.grid[y][x] == 1 else (255, 255, 255) if self.grid[y][x] == 2 else (0,0,0,0))
	def draw_board_grid(self):
		colorswitch = False
		for x in range(8):
			colorswitch = not colorswitch
			for y in range(8):
				colorswitch = not colorswitch
				if (x == 3 or x == 4) and (y == 3 or y == 4):
					pygame.draw.rect(self.screen, (0,170,0), (x*100, y*100, 100, 100))
				elif colorswitch:
					pygame.draw.rect(self.screen, (0,150,0), (x*100, y*100, 100, 100))
				elif not colorswitch:
					pygame.draw.rect(self.screen, (0,140,0), (x*100, y*100, 100, 100))
	def draw_board_grid_lines(self):
		for i in range(8):
			pygame.draw.line(self.screen, (0,0,0), (i*100,0), (i*100,800), 2)
			pygame.draw.line(self.screen, (0,0,0), (0,i*100), (800,i*100), 2)
	def draw_board_orientationpoints(self):
		draw.aacircle(self.screen, 201,201, 8, (0,0,0))
		draw.aacircle(self.screen, 601,201, 8, (0,0,0))
		draw.aacircle(self.screen, 201,601, 8, (0,0,0))
		draw.aacircle(self.screen, 601,601, 8, (0,0,0))
	def draw_chip(self, gridx, gridy, color, size=39, x=None, y=None):
		draw.aacircle(self.screen, x if x else 50+100*gridx, y if y else 50+100*gridy, size, color)


app = Application()
app.main_loop()