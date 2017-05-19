import random

class Board:
	board = {}
	whiteout, blackout, whitefin, blackfin, curoll = [], [], [], [], []
	whitedubs, blackdubs = 0, 0
	curplayer = "w" #will switch b/w "w" and "b" and starts with "w"
	winner, name1, name2 = "", "", ""
	fiw = True

	def __init__(self, board):
		self.board = board
		self.fiw, self.name1, self.name2 = firstRoll()

	def isClear(self, a, b, rolls):
		if b < a:
			a, b = b, a
		if len(rolls) > 2:
			for i in rolls:
				a += i
				if not self.sameColor(a):
					return False
				if self.canEat(a) and self.board[a][0].color != self.curplayer:
					if self.curplayer == "w":
						self.whiteout.append(self.board[a].pop())
					else:
						self.blackout.append(self.board[a].pop())
			return True
		first = a + rolls[0]
		second = 0
		if rolls[1]:
			second = a + rolls[1]
		if self.sameColor(first, False) or (second and self.sameColor(second, False)):
			if self.canEat(first) and self.board[first][0].color != self.curplayer:
				if self.curplayer == "w":
					self.whiteout.append(self.board[first].pop())
				else:
					self.blackout.append(self.board[first].pop())
			if second and self.canEat(second) and self.board[second][0].color != self.curplayer:
				if self.curplayer == "w":
					self.whiteout.append(self.board[second].pop())
				else:
					self.blackout.append(self.board[second].pop())
			return True
		else:
			print(self.opponent() + " is blocking that path. Try again.")
			return False

	def canMove(self, f=False):
		if self.curplayer == "w" and not self.whiteout:
			return True
		if self.curplayer == "b" and not self.blackout:
			return True
		if f:
			print("You have eaten pieces you need to play first. ", end="")
		return False

	def isValid(self, a, b, x):
		f = True
		if b == 0:
			f = False
			if self.curplayer == "w":
				print("That is where " + self.opponent() + " eats pieces. You eat at 25. Try again.")
				return False
			elif not self.canFinish():
				print("You cannot eat pieces yet. Try again.")
				return False
		if b == 25:
			f = False
			if self.curplayer == "b":
				print("That is where " + self.opponent() + " eats pieces. You eat at 0. Try again.")
				return False
			elif not self.canFinish():
				print("You cannot eat pieces yet. Try again.")
				return False
		if a == 0:
			f = False
			if self.curplayer == "b":
				print("Those are not valid positions. Try again.")
				return False
			elif self.canMove():
				print("You do not have any pieces to bring back into play. Try again.")
				return False
		if a == 25:
			f = False
			if self.curplayer == "w":
				print("Those are not valid positions. Try again.")
				return False
			elif self.canMove():
				print("You do not have any pieces to bring back into play. Try again.")
				return False
		if a not in range(0, 26) or b not in range(0, 26):
			print("Those are not valid positions. Try again.")
			return False
		if f:
			if self.isEmpty(a, x):
				if x == 1:
					print("There are no pieces at position " + str(a) + ". Try again.")
				else:
					print("There are not enough pieces at position " + str(a) + ". Try again.")
				return False
			if self.curplayer != self.board[a][0].color:
				print("You cannot move " + self.opponent() + "'s piece. Try again.")
				return False
			if self.direction(a, b) and (self.isEmpty(b) or self.sameColor(b) or self.canEat(b)) and self.canMove(True):
				return True
			else:
				return False
		else:
			if a == 0:
				arr = self.whiteout
			elif a == 25:
				arr = self.blackout
			if len(arr) < x:
				string = ""
				if x == 1:
					string = " 1 piece "
				else:
					string = " " + str(x) + " pieces "
				print("You do not have" + string + "to bring back into play. Try again.")
				return False
			if self.direction(a, b) and (self.isEmpty(b) or self.sameColor(b) or self.canEat(b)):
				return True
			else:
				return False
			
	def path(self, dist, f):
		arr = []
		if self.curplayer == "w":
			arr = self.whiteout
		else:
			arr = self.blackout
		if dist == 0:
			print("You cannot move 0 steps. Try again.")
			return []
		if dist in self.curoll:
			return [dist]
		elif len(self.curoll) == 1 or len(arr) > 1:
			if f:
				return []
			else:
				if dist <= self.curoll[0]: # = not needed since it woulda been caught but oh well
					return [self.curoll[0]]
				else:
					return []
		elif len(self.curoll) == 2:
			if f:
				if sum(self.curoll) == dist:
					# if len(arr) > 1:
					# 	print("You still have other pieces to move. Try again.")
					# 	return []
					# else:
					return self.curoll
				else:
					return []
			else:
				if dist <= self.curoll[0]:
					return [self.curoll[0]]
				if dist <= self.curoll[1]:
					return [self.curoll[1]]
				if dist <= sum(self.curoll):
					return self.curoll
				else:
					return []
		val = self.curoll[0]
		if not f:
			ret = []
			s = 0
			i = 0
			while s < dist and i < len(self.curoll):
				ret.append(v)
				s += v
				i += 1
			if s < dist:
				return []
			else:
				return ret
		else:
			if dist % val != 0:
				return []
			elif int(dist/val) <= len(self.curoll):
				ret = []
				for i in range(int(dist/val)):
					ret.append(val)
				# if len(arr) > 1:
				# 	if len(ret) > 1:
				# 		print("You still have other pieces to move. Try again.")
				# 		return []
				# else:
				return ret
			else:
				return []

	def parse(self, r):
		f = True
		if len(r) < 3:
			print("You need to enter at least a starting and ending position. Try again.")
			return False
		elif len(r) > 3:
			print("You entered too many numbers. Try again.")
			return False
		if r[2] < 1 or r[2] > len(self.curoll):
			print("You cannot move " + str(r[2]) + " times. Try again.")
			return False
		if r[0] == 0 or r[0] == 25:
			print("Those are not valid positions. Try again.")
			return False
		if r[1] == 0 or r[1] == 25:
			f = False
			if not self.canFinish():
				print("You cannot eat pieces yet. Try again.")
				return False
		if r[0] == 'x':
			# f = False
			if self.canMove():
				print("You do not have any eaten pieces to bring into play. Try again.")
				return False
			else:
				if self.curplayer == "w":
					r[0] = 0
				else:
					r[0] = 25
		x = self.path(abs(r[0] - r[1]), f)
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

	def handle(self):
		x = []
		f = False
		while not x:
			r = []
			# self.canMove()
			if not self.canMove():
				f = True
				s = input("Notice that you have pieces out of play. Make your move...")
			else:
				s = input("Make your move...")
			spl = s.split()
			for i in spl:
				if i.isdigit():
					r.append(int(i))
			if 'x' in spl:
				r.insert(0, 'x')
			if len(r) == 2:
				r.append(1)
			x = self.parse(r)
		ret = []
		for i in range(r[2]):
			self.move(r[0], r[1], f)
			ret.extend(x)
		return ret

	def names(self):
		return self.name1, self.name2

	def setCuroll(self, lst):
		self.curoll = lst

	# def ignore(self, *args, **kwargs):
	# 	x = 0 #pointless

	def move(self, a, b, f):
		if f:
			if a == 0 or a == 25:			
				if self.curplayer == "w":
					self.board[b].append(self.whiteout.pop())
				elif self.curplayer == "b":
					self.board[b].append(self.blackout.pop())
			if b == 0 or b == 25:
				if self.curplayer == "w":
					self.whitefin.append(self.board[a].pop())
				elif self.curplayer == "b":
					self.blackfin.append(self.board[a].pop())
		else:
			if len(self.board[b]) == 1 and self.board[b][0].color != self.curplayer:
				if self.curplayer == "w":
					self.blackout.append(self.board[b].pop())
				elif self.curplayer == "b":
					self.whiteout.append(self.board[b].pop())
			self.board[b].append(self.board[a].pop())

	def prettyprint(self):
		def newprint(*args, **kwargs):
			print("\033[4m"+args[0]+"\033[0m", end="")
		print("Your rolls are: ", end="")
		print(str(list(self.curoll))[1:len(str(list(self.curoll))) - 1]) #disgusting way to print the rolls
		# print(" and ", end="")
		height = 0
		for i in range(13, 25):
			if len(self.board[i]) > height:
				height = len(self.board[i])
		print("\033[4m  24 23 22 21 20 19         18 17 16 15 14 13  \033[0m")
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
						print(" | \u26AB |  ", end="")
					else:
						print(" |   |  ", end="")
				if x == 13:
					print("|", end="")
			i += 1
			print()
		height = 0
		for i in range(1, 14):
			if len(self.board[i]) > height:
				height = len(self.board[i])
		i = max(height, 5)
		num = 2
		if 5 > height:
			num += 5 - height
		for v in range(num):
			print("|                    |   |                    |")
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
						func(" | \u26AA |  ", end="")
					else:
						func(" |   |  ", end="")
				if x == 12:
					func("|", end="")
			i -= 1
			print()
		print("  01 02 03 04 05 06         07 08 09 10 11 12  ")
		if self.whitefin:
			n = ""
			if self.fiw:
				n = self.name1
			else:
				n = self.name2
			print(n + "'s eaten pieces (" + str(len(whitefin)) + "): ", end="")
			for i in range(len(self.whitefin)):
				print("\u26AA", end="")
			print()
		if self.blackfin:
			n = ""
			if self.fiw:
				n = self.name2
			else:
				n = self.name1
			print(n + "'s eaten pieces (" + str(len(blackfin)) + "): ", end="")
			for i in range(len(self.blackfin)):
				print("\u26AB", end="")
			print()
		print()	

	def isEmpty(self, a, x=1):
		if not self.board[a] or len(self.board[a]) < x:
			return True
		else:
			return False

	def sameColor(self, b, f=True):
		if self.isEmpty(b):
			return True
		if self.canEat(b):
			return True
		if self.board[b][0].color == self.curplayer:
			return True
		if f:
			print(self.opponent() + " is blocking position " + str(b) + ". Try again.")
		return False

	def opponent(self):
		if self.curplayer == "w":
			if self.fiw:
				return self.name2
			else:
				return self.name1
		elif self.curplayer == "b":
			if self.fiw:
				return self.name1
			else:
				return self.name2

	def isWinner(self):
		if len(self.whitefin) == 15 or len(self.blackfin) == 15:
			return True
		else:
			return False

	def dubs(self, r): #this function is actually so crucial lol
		self.curoll = r
		if len(r) == 4:
			if self.curplayer == "w":
				self.whitedubs += 1
			else:
				self.blackdubs += 1
		if not self.canMove():
			opens = []
			if self.curplayer == "w":
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

	# def cur():
	# 	return self.curplayer

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

	def ciw(self):
		return self.fiw

	def changePlayer(self):
		if self.curplayer == "w":
			self.curplayer = "b"
		elif self.curplayer == "b":
			self.curplayer = "w"

	def whoWon(self):
		if len(self.whitefin) == 15:
			if self.fiw:
				print(name1 + " won! Congratulations!")
				print("You rolled " + str(len(self.whitedubs)) + " doubles and " + self.opponent() + " rolled " + str(len(self.blackdubs)) + ".")
			else:
				print(name2 + " won! Congratulations!")
				print("You rolled " + str(len(self.blackdubs)) + " doubles and " + self.opponent() + " rolled " + str(len(self.whitedubs)) + ".")
		elif len(self.blackfin) == 15:
			if self.fiw:
				print(name2 + " won! Congratulations!")
				print("You rolled " + str(len(self.blackdubs)) + " doubles and " + self.opponent() + " rolled " + str(len(self.whitedubs)) + ".")
			else:
				print(name1 + " won! Congratulations!")
				print("You rolled " + str(len(self.whitedubs)) + " doubles and " + self.opponent() + " rolled " + str(len(self.blackdubs)) + ".")

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
		if self.curplayer == "w":
			tot += len(self.whitefin)
		else:
			tot += len(self.blackfin)
		if tot == 15:
			return True
		else:
			return False



def firstRoll():
	name1 = input("Who will roll first?\n").title()
	name2 = input("Who will roll second?\n").title()
	print("Rolling...")
	x = random.randint(1, 6)
	y = random.randint(1, 6)
	while x == y:
		# print("It was a tie! We'll roll again!")
		x = random.randint(1, 6)
		y = random.randint(1, 6)
	print(name1 + " rolled a " + str(x), end="")
	print(" and " + name2 + " rolled a " + str(y), end="")
	b = True
	if x > y:
		print(", so " + name1 + " will be white and " + name2 + " will be black.")
		b = True #computer is white and goes first
	else:
		print(", so " + name2 + " will be white and " + name1 + " will be black.")
		b = False #computer is black and goes second
	return b, name1, name2

def intro():
	print("Welcome to Brandon's Backgammon Game!")
	print("-------------------------------------")
	print("Making moves is relatively straightforward.")
	print("For example: '3 8' means you want to move a piece from position 3 to position 8 and '3 8 2' means you want to move 2 pieces from position 3 to position 8. White eats at 25 and Black eats at 0, so '22 25' means white wants to eat a piece at position 22. To bring an eaten piece back into play, use 'x' as your STARTING position, regardless of your color. For example: 'x 3' means you are white and want to move an eaten piece to position 3.")
	input("Press the enter key once you understand how to play!")

def p(i=1):
	for x in range(i):
		print()

def start():
	intro()
	print("Great! Let's get started! ", end="")
	gb = Board(makeNew())
	n1, n2 = gb.names()
	lst = ["It is " + n1 + "'s turn. ", "It is " + n2 + "'s turn. "]
	p(2)
	if not gb.ciw():
		lst = lst[::-1]
	ind = 0
	while not gb.isWinner():
		print(lst[ind], end="")
		ind = 1 - ind
		r = roll()
		if not gb.dubs(r):
			print("You rolled " + str(list(r))[1:len(str(list(r))) - 1])
			print("You are unable to move so your turn will be skipped.")
		else:
			while r:
				gb.prettyprint()
				usedRolls = gb.handle()
				for i in usedRolls:
					r.remove(i)
				gb.setCuroll(r)
		p(8)
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
