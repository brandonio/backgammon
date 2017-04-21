import random

class Board:
	board = {}
	whiteout = []
	blackout = []
	whiteeat = []
	blackeat = []
	curoll = []
	compdubs = 0
	humandubs = 0
	winner = ""
	curplayer = "w" #will switch b/w "w" and "b" and starts with "w"
	compIsWhite = True

	def __init__(self, board):
		self.board = board
		self.compIsWhite = firstRoll()

	def cur():
		return self.curplayer

	def ciw(self):
		return self.compIsWhite

	def changePlayer(self):
		if self.curplayer == "w":
			self.curplayer = "b"
		elif self.curplayer == "b":
			self.curplayer = "w"

	def whoWon(self):
		if len(self.whiteeat) == 15:
			if self.compIsWhite:
				print("The computer won!")
			else:
				print("You won!")
		elif len(self.blackeat) == 15:
			if not self.compIsWhite:
				print("The computer won!")
			else:
				print("You won!")

	def isWinner(self):
		if len(self.whiteeat) == 15 or len(self.blackeat) == 15:
			return True
		else:
			return False

	def canFinish(self):
		tot = 0
		r = []
		if self.curplayer == "w":
			r = range(19, 25)
		else:
			r = range(1, 7)
		for i in r:
			if self.board[i] and self.board[i][0].color == self.curplayer:
				tot += len(self.board[i])
		if tot == 15:
			return True
		else:
			return False

	def isClear(self, a, b, rolls):
		if b < a:
			a, b = b, a
		if len(rolls) > 2:
			for i in rolls:
				a += i
				if not self.sameColor(a, self.ignore):
					print("The opponent is blocking that path. Try again.")
					return False
		if len(rolls) == 1:
			print("this should never be printed")
		if self.sameColor(a + rolls[0], self.ignore) or self.sameColor(a + rolls[1], self.ignore):
			return True
		else:
			print("The opponent is blocking that path. Try again.")
			return False

	def path(self, dist):
		if dist == 0:
			return []
		if dist in self.curoll:
			return [dist]
		elif len(self.curoll) == 1:
			return []
		elif len(self.curoll) == 2:
			if sum(self.curoll) == dist:
				return self.curoll
			else:
				return []
		x = self.curoll[0]
		if dist % x != 0:
			return []
		elif dist/x <= len(self.curoll):
			ret = []
			for i in range(int(dist/x)):
				ret.append(x)
			return ret
		else:
			return []

	def canMove(self, f=print):
		if self.curplayer == "w" and not self.whiteout:
			return True
		elif self.curplayer == "b" and not self.blackout:
			return True
		else:
			f("You have eaten pieces you need to play first. ", end="")
			return False

	def isEmpty(self, a, x=1):
		if not self.board[a] or len(self.board[a]) < x:
			return True
		else:
			return False

	def direction(self, a, b):
		if self.curplayer == "w" and a < b:
			return True
		elif self.curplayer == "b" and a > b:
			return True
		else:
			print("You are trying to move in the wrong direction. Try again.")
			return False

	def canEat(self, b):
		if len(self.board[b]) == 1:
			return True
		else:
			return False

	def sameColor(self, b, f=print):
		if self.isEmpty(b):
			return True #not needed tbh
		elif self.board[b][0].color == self.curplayer:
			return True
		elif self.canEat(b):
			return True
		else:
			f("The opponent is blocking position " + str(b) + ". Try again.")
			return False

	def isValid(self, a, b, x):
		if a not in range(1, 25) or b not in range(1, 25):
			print("Those are not valid positions. Try again.")
			return False
		elif self.isEmpty(a, x):
			print("There are not enough pieces at position " + str(a) + ". Try again.")
			return False
		elif self.curplayer != self.board[a][0].color:
			print("You cannot move your opponent's piece. Try again.")
			return False
		elif self.direction(a, b) and (self.isEmpty(b, x) or self.sameColor(b) or self.canEat(b)): #and self.canMove():
			return True
		else:
			return False

	def dubs(self, r): #this function is actually so crucial lol
		self.curoll = r
		if len(r) == 4:
			if self.compIsWhite:
				self.compdubs += 1
			else:
				self.humandubs += 1
		if not self.canMove(self.ignore):
			opens = []
			if self.compIsWhite:
				for i in range(1, 7):
					if self.isEmpty(i):
						opens.append(i)
			else:
				for i in range(19, 25):
					if self.isEmpty(i):
						opens.append(25 - i)
			s = set(r)
			opens = set(opens)
			if not s.intersection(opens):
				return False
			else:
				return True
		else:
			return True


	def parse(self, r):
		if len(r) < 2:
			print("You need to enter at least a starting and ending position. Try again.")
			return False
		elif len(r) > 3:
			print("You entered too many numbers. Try again.")
			return False
		elif len(r) == 3:
			if r[2] < 1 or r[2] > len(self.curoll):
				print("You cannot move that many times. Try again.")
				return False
		x = self.path(abs(r[0] - r[1]))
		if not x:
			print("You cannot reach that position. Try again.")
			return False
		if len(x) * r[2] > len(self.curoll):
			print("You cannot move that many pieces that far. Try again.")
			return False
		if not self.isValid(r[0], r[1], r[2]) or not self.isClear(r[0], r[1], x):
			return False
		else:
			return x

	def setCuroll(self, lst):
		self.curoll = lst

	def ignore(self, *args, **kwargs):
		x = 0 #pointless

	def handle(self):
		r = []
		self.canMove()
		s = input("Make your move...")
		for i in s.split():
			if i.isdigit():
				r.append(int(i))
		if len(r) == 2:
			r.append(1)
		x = self.parse(r)
		while not x:
			r = []
			self.canMove()
			s = input("Make your move...")
			for i in s.split():
				if i.isdigit():
					r.append(int(i))
			if len(r) == 2:
				r.append(1)
			x = self.parse(r)
		# if 
		ret = []
		for i in range(r[2]):
			self.move(r[0], r[1])
			ret.extend(x)
		return ret

	def move(self, a, b):
		if len(self.board[b]) == 1 and self.board[b][0].color != self.curplayer:
			if self.curplayer == "w":
				self.blackout.append(self.board[b].pop())
			else:
				self.whiteout.append(self.board[b].pop())
		self.board[b].append(self.board[a].pop())

	def prettyprint(self):
		def newprint(*args, **kwargs):
			print("\033[4m"+args[0]+"\033[0m", end="")
		print("The rolls are: ", end="")
		print(str(list(self.curoll))[1:len(str(list(self.curoll))) - 1]) #disgusting way to print the rolls
		# print(" and ", end="")
		height = 0
		for i in range(13, 25):
			if len(self.board[i]) > height:
				height = len(self.board[i])
		print("\033[4m  24 23 22 21 20 19        18 17 16 15 14 13  \033[0m")
		i = 1
		while i <= height:
			for x in range(24, 12, -1):
				if x == 24:
					print("| ", end="")
				if len(self.board[x]) >= i:
					if self.board[x][0].color == "w":
						piece = "\u26AA"
					else:
						piece = "\u26AB"
					print(piece + "  ", end="")
				else:
					print("   ", end="")
				if x == 19:
					if self.blackout and len(self.blackout) >= i:
						print(" |\u26AB |  ", end="")
					else:
						print(" |  |  ", end="")
				if x == 13:
					print("|  ", end="")
			i += 1
			print()
		for i in range(2):
			print("|                    |  |                    |")
		height = 0
		for i in range(1, 14):
			if len(self.board[i]) > height:
				height = len(self.board[i])
		i = height
		func = print
		while i > 0:
			for x in range(1, 13):
				if i == 1:
					func = newprint
				if x == 1:
					func("| ", end="")
				if len(self.board[x]) >= i:
					if self.board[x][0].color == "w":
						piece = "\u26AA"
					else:
						piece = "\u26AB"
					func(piece + "  ", end="")
				else:
					func("   ", end="")
				if x == 6:
					if self.whiteout and len(self.whiteout) >= i:
						func(" |\u26AA |  ", end="")
					else:
						func(" |  |  ", end="")
				if x == 12:
					func("|", end="")
			i -= 1
			print()
		print("  01 02 03 04 05 06        07 08 09 10 11 12  ")
		print()	

def firstRoll():
	print(" A high roll wins and the winner will play as white.")
	print("Rolling...")
	x = random.randint(1, 6)
	y = random.randint(1, 6)
	while x == y:
		x = random.randint(1, 6)
		y = random.randint(1, 6)
	if x > y:
		print("The computer rolled a " + str(x) + " and you rolled a " + str(y) + ", so the computer will be white and you will be black.")
		return True #computer is white and goes first
	else:
		print("You rolled a " + str(y) + " and the computer rolled a " + str(x) + ", so you will be white and the computer will be black.")
		return False #computer is black and goes second

def intro():
	print("Welcome to Brandon's Backgammon Bot!")
	print("-------------------------------------")
	print("Enter two or three numbers to make a move. For example: '3 8' means you want to move a piece from position 3 to position 8 and '3 8 2' means you want to move 2 pieces from position 3 to position 8.")
	print("Let's get started! Who will go first? ", end="")

def p(i):
	for x in range(i):
		print()

def start():
	intro()
	gb = Board(makeNew())
	lst = ["It is the computer's turn. ", "It is your turn. "]
	isComp = gb.ciw()
	p(2)
	if not isComp:
		lst = lst[::-1]
	ind = 0
	while not gb.isWinner():
		print(lst[ind], end="")
		ind = 1 - ind
		r = roll()
		if not gb.dubs(r):
			print("You are unable to move so your turn will be skipped.")
		else:
			while r:
				gb.prettyprint()
				usedRolls = gb.handle()
				for i in usedRolls:
					r.remove(i)
				gb.setCuroll(r)
		for i in range(4):
			print()
		isComp = not isComp
		gb.changePlayer()
	gb.whoWon()

def roll():
	ret = []
	ret.append(random.randint(1, 6))
	ret.append(random.randint(1, 6))
	if (ret[0] == ret[1]):
		ret.append(ret[0])
		ret.append(ret[0])
	return ret

class Piece:
	color = ""

	def __init__(self, color):
		self.color = color

	def color(self):
		return self.color

def makeNew():
	b = {}
	for i in range(0, 26):
		b[i] = []
	b[1] = [Piece("w") for x in range(2)]
	b[12] = [Piece("w") for x in range(5)]
	b[17] = [Piece("w") for x in range(3)]
	b[19] = [Piece("w") for x in range(5)]
	b[6] = [Piece("b") for x in range(5)]
	b[8] = [Piece("b") for x in range(3)]
	b[13] = [Piece("b") for x in range(5)]
	b[24] = [Piece("b") for x in range(2)]
	return b

# def shouldEat(p, n):

start()
