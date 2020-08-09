import random
from tkinter import *
from tkinter import font as tkfont
from copy import deepcopy
from PIL import Image, ImageTk

MARGIN = 20  # Pixels around the board
SIDE = 100  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class SudokuGame(object):

	solvedGrid = 0
	unsolvedGrid = 0
	diffi = " "
	gameOver = False

	difficulty = {
	"Easy": 16,
	"Medium": 32,
	"Hard": 48,
	"Very hard": 64,
	}
	
	def checkWin(self): #if the user grid is the same as the solution then the game is over
		if self.userGrid == self.solvedGrid:
			self.gameOver = True
			return True

	def start(self, diffi):
		grid = self.makeZeroGrid()
		grid = self.newRandGrid(grid)#randomizes the first line to build unique grid
		self.solvedGrid = self.sudokuSolver(grid)#generates random solution
		ulist = deepcopy(self.solvedGrid)
		self.diffi = diffi
		self.unsolvedGrid = self.unsolvedGridGenerator(ulist,self.difficulty[diffi])#makes and unsolved grid based on set difficulty
		self.userGrid = deepcopy(self.unsolvedGrid)#sets user grid to display as unsolved grid

	def makeZeroGrid(self): #function to generate empty board
		grid = []
		for i in range(9): #fill the board with 0s
			grid.append([0 for j in range(9)])
		return grid

	def checkBoard(self,grid): #function to check if a given board is valid
		for i in range(9): #check the rows
			for j in range(1,10):
				if grid[i].count(j) > 1:
					#print(f"error row {i}")
					return False 
		for k in range(9): #check the columns
			column = [row[k] for row in grid]
			for l in range(1,10):
				if column.count(l) > 1:
					#print(f"error column {l}")
					return False
		for bound in range(0,7,3): #check the squares
			for box in range(0,7,3):
				sqr = [grid[i][bound:bound+3] for i in range(box,box+3)]
				sqr = [y for x in sqr for y in x]
				for l in range(1,10):
					if sqr.count(l) > 1:
						#print(f"error sqr {l}")
						return False
		return True

	def find_empty(self,grid):
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 0:
					return (i, j) #goes through each spot and returns coord if empty
		return False

	def sudokuSolver(self,grid):#recursion to check if the grid is full if valid and returns olution
		find = self.find_empty(grid)
		if not find:
			return True
		else:
			row, col = find
		for i in range(1,10):
			grid[row][col] = i
			if self.checkBoard(grid):
				if self.sudokuSolver(grid):
					return grid
			grid[row][col] = 0

	def newRandGrid(self,grid):
		i = 0
		while 0 in grid[0]:
			randomint = random.randint(1,9)
			if randomint not in grid[0]:
				grid[0][i] = randomint
				i += 1
		return grid

	def unsolvedGridGenerator(self,grid,numsToRm):
		count = 0
		numSolns = 0
		blankSpots = []
		while count < numsToRm:
			x = random.randint(0,8)#picks random grid point
			y = random.randint(0,8)
			#temp = probGrid[x][y]
			for i in range(1,10):
				grid[x][y] = i#tries 1-9 at the point
				if self.checkBoard(grid):
					if self.sudokuSolver(grid):#if that is valid then solve rest of board
						numSolns += 1#each time it finds a solution when that point is changed it records that as a solution
			if numSolns == 1:#if there is one unique solution it increases the count
				blankSpots.append([x,y])#records valid blank spots
				count += 1
			numSolns = 0#resets colution record
			for i in range(len(blankSpots)):#resets board since solver fills in old blank poitns
				grid[blankSpots[i][0]][blankSpots[i][1]] = 0

		return grid

class SudokuUI(Frame):

#Credit required for Lynn Root whose website http://newcoder.io/gui/part-1/ provided the walkthrough to make the GUI and whose code I borrow from greatly in order to then build upon for extra functions for the user and overall as a learning experience for tkinter
	
	def __init__(self, parent, game):#defines important object variables
		self.game = game
		Frame.__init__(self,parent)
		self.parent= parent
		self.genFont = tkfont.Font(family="Prusia", size=12, weight="bold")
		self.initUI()
		self.row, self.col = 0, 0

	def updateDiffButton(self):#cycles through the different difficulties and generates a new game at that difficulty
		if game.diffi == "Easy":
			self.diffi = "Medium"
			game.start("Medium")
		elif game.diffi == "Medium":
			self.diffi = "Hard"
			game.start("Hard")
		elif game.diffi == "Hard":
			self.diffi = "Very hard"
			game.start("Very hard")		
		elif game.diffi == "Very hard":
			self.diffi = "Easy"
			game.start("Easy")

		self.row, self.col = -1, -1#removes the cursor
		self.canvas.delete("victory")#removes victory condition if met
		self.canvas.delete("winner")
		self.drawPuzzle()#redraws game and changes difficulty button text
		self.drawCursor()
		self.game.gameOver = False
		diffText.set(f"Difficlty = {game.diffi}")
		
	def initUI(self):

		self.parent.title("Simple Sudoku")#title the game and create window
		self.pack(fill = BOTH, expand = 1)
		self.canvas = Canvas(self, width = WIDTH, height = HEIGHT)
		self.canvas.pack(fill = BOTH, side = LEFT)

		#self.image = self.canvas.create_image(0,0, image = photo)#draws bg image
		
		#draws the buttons
		newGButton = Button(self, font = self.genFont, text = "New Game", command = self.newGame)
		newGButton.pack(fill = X)
		diffText.set(f"Difficlty = {game.diffi}")
		diffButton = Button(self, font = self.genFont, textvariable = diffText, command = self.updateDiffButton)
		diffButton.pack(fill = X)
		clearButton = Button(self, font = self.genFont, text = "Clear Answers", command = self.clearAns)
		clearButton.pack(fill = X)
		solveButton = Button(self, font = self.genFont, text = "Solve Puzzle", command = self.solvePuzzle)
		solveButton.pack(fill = X)


		self.drawGrid()
		self.drawPuzzle()
		
		#key functions
		self.canvas.bind("<Button-1>", self.cellClicked)
		self.canvas.bind("<BackSpace>", self.keyPressed)
		self.canvas.bind("Delete", self.keyPressed)
		self.canvas.bind("<Up>", self.keyUp)
		self.canvas.bind("<Down>", self.keyDown)
		self.canvas.bind("<Left>", self.keyLeft)
		self.canvas.bind("<Right>", self.keyRight)
		self.canvas.bind("<Key>", self.keyPressed)
	
	#moves cursor based on key direction pressed
	def keyUp(self,event):
		if  0 < self.row <= 8 and 0 <= self.col <= 8:
			self.row -= 1
			self.drawCursor()

	def keyDown(self,event):
		if  0 <= self.row < 8 and 0 <= self.col <= 8:
			self.row += 1
			self.drawCursor()

	def keyRight(self,event):
		if  0 <= self.row <= 8 and 0 <= self.col < 8:
			self.col += 1
			self.drawCursor()

	def keyLeft(self,event):
		if  0 <= self.row <= 8 and 0 < self.col <= 8:
			self.col -= 1
			self.drawCursor()
	
	def drawVictory(self):#draws circle notifying win if user finishes board
		x0 = y0 = MARGIN + SIDE * 2
		x1 = y1 = MARGIN + SIDE * 7
		self.canvas.create_oval(x0, y0, x1, y1, tags = "victory", fill = "light blue",
		outline = "orange")
		x = y = MARGIN + 4 * SIDE + SIDE / 2
		self.canvas.create_text(x, y, text = "You Win!", tags = "winner", fill = "white",
		font = self.genFont)

	def clearAns(self):#removes user input
		if self.game.gameOver:#disabled if user won
			return
		for i in range(9):
			for j in range(9):
				self.game.userGrid[i][j] = self.game.unsolvedGrid[i][j]
		self.col, self.row = -1, -1
		self.drawPuzzle()
		self.drawCursor()

	def keyPressed(self, event):
		if self.game.gameOver:
			return
		#if user presses a number adds that number to the board and draws it
		if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
			self.game.userGrid[self.row][self.col] = int(event.char)
			self.drawPuzzle()
			self.drawCursor()
			if self.game.checkWin():#checks win each time new number inserted
				self.drawVictory()
		elif self.row >= 0 and self.col >= 0 and self.game.unsolvedGrid[self.row][self.col] == 0:#if delete key is pressed it removes the number
			self.game.userGrid[self.row][self.col] = 0
			self.drawPuzzle()
			self.drawCursor()

	#highlights cell when a user clocks on it
	def cellClicked(self, event):
		if self.game.gameOver:
			return
		x, y = event.x, event.y
		if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
			self.canvas.focus_set()
			row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
			if (row, col) == (self.row, self.col):
				self.row, self.col = -1, -1
			elif self.game.unsolvedGrid[row][col] == 0:
				self.row, self.col = row, col
			self.drawCursor()

	def drawCursor(self):
		if self.game.gameOver:
			return
		self.canvas.delete("cursor")
		if self.row >= 0 and self.col >= 0:
			x0 = MARGIN + self.col * SIDE + 1
			y0 = MARGIN + self.row * SIDE + 1
			x1 = MARGIN + (self.col + 1) * SIDE - 1
			y1 = MARGIN + (self.row + 1) * SIDE - 1
			self.canvas.create_rectangle(
			x0, y0, x1, y1, outline="blue", tags="cursor", width = 3)


	def solvePuzzle(self):
		if self.game.gameOver:
			return
		self.canvas.delete("numbers")
		for i in range(9):
			for j in range(9):
				correctAnswer = self.game.solvedGrid[i][j]
				x = MARGIN + j * SIDE + SIDE // 2
				y = MARGIN + i * SIDE + SIDE // 2
				color = "black"
				self.canvas.create_text(
				x, y, text = correctAnswer, tags = "numbers", fill = color,
					font = self.genFont)


	def drawGrid(self):

		for i in range(10):
			color = "black"
			thick = 3 if i % 3 == 0 else 1

			x0 = MARGIN + i * SIDE
			y0 = MARGIN
			x1 = MARGIN + i * SIDE
			y1 = HEIGHT - MARGIN
			self.canvas.create_line(x0, y0, x1, y1, fill=color, width = thick)

			x0 = MARGIN
			y0 = MARGIN + i * SIDE
			x1 = WIDTH - MARGIN
			y1 = MARGIN + i * SIDE
			self.canvas.create_line(x0, y0, x1, y1, fill=color, width = thick)

	def drawPuzzle(self):
		self.canvas.delete("numbers")
		for i in range(9):
			for j in range(9):
				answer = self.game.userGrid[i][j]
				if answer != 0:
					x = MARGIN + j * SIDE + SIDE // 2
					y = MARGIN + i * SIDE + SIDE // 2
					original = self.game.solvedGrid[i][j]
					color = "black" if answer == original else "red"
					self.canvas.create_text(
					x, y, text = answer, tags = "numbers", fill = color,
					font = self.genFont)
	def newGame(self):
		self.game.start(game.diffi)
		self.game.gameOver = False
		self.canvas.delete("victory")
		self.canvas.delete("winner")
		self.row, self.col = -1, -1
		self.drawPuzzle()
		self.drawCursor()
	








game = SudokuGame() #create a new game object
game.start("Easy")#start a new easy game
root = Tk()
diffText = StringVar()#defines variable text to update for game difficulty
#image = Image.open("woodbg.jpg") # open source image from https://www.freepik.com/free-vector/wood-texture_849626.htm
#image = image.resize((WIDTH*2, HEIGHT*2), Image.ANTIALIAS)
#photo = ImageTk.PhotoImage(image)#load image

root.tk.call('tk', 'scaling', 4.0)
SudokuUI(root,game)#start the UI
root.mainloop()
