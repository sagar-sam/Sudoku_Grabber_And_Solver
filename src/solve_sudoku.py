
class solve_sudoku() :
	
	def __init__(self, sudkou_grid) :
		print "The sudoku shall not remain unsolved ! "
		self.sudoku=sudkou_grid
		self.all = []
		self.count=0
		if self.is_grid_safe() :
			self.solve()
		
			
		
		

	def safe(self, x, y, a):
		for i in range(9):
			if not i == y :
				if self.sudoku[x][i]==a:
					return False
			if not i == x :
				if self.sudoku[i][y]==a:
					return False
		if x<=2:
			if y<=2:
				for i in range(0,3):
					for j in range(0,3):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

			elif y<=5:
				for i in range(0,3):
					for j in range(3,6):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

			elif y<=8:
				for i in range(0,3):
					for j in range(6,9):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

		elif x<=5:
			if y<=2:
				for i in range(3,6):
					for j in range(0,3):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

			elif y<=5:
				for i in range(3,6):
					for j in range(3,6):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

			elif y<=8:
				for i in range(3,6):
					for j in range(6,9):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False
		elif x<=8:
			if y<=2:
				for i in range(6,9):
					for j in range(0,3):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

			elif y<=5:
				for i in range(6,9):
					for j in range(3,6):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False

			elif y<=8:
				for i in range(6,9):
					for j in range(6,9):
						if not i == x or not y == j :
							if self.sudoku[i][j]==a :
								return False
		return True

	def solve(self) :
		
		flag=0;
		x=0
		y=0
		for i in range(9):
			for j in range(9):
				if self.sudoku[i][j]==0:
					x=i
					y=j
					flag=1
					break
		if flag==1:
			for i in range(1,10):
				if self.safe(x, y, i) :
					self.sudoku[x][y]=i
					if(self.solve()):
						a=1
						
					self.sudoku[x][y]=0
			return False
		else :
			
			temp1 = []
			for i in range(9) :
				temp=[]
				for j in range(9) :
					temp.append(self.sudoku[i][j])
				temp1.append(temp)
			self.all.append(temp1)
			self.count+=1
			return True

	def is_grid_safe(self) :
		for i in range(9) :
			for j in range(9) :
				if not self.sudoku[i][j] == 0 :
					if not self.safe(i,j,self.sudoku[i][j]) :
						return False

		return True

