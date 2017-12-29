import cv2
import numpy as np
from matplotlib import pyplot as plt
import ocr
import solve_sudoku as ss
import math

class image_processing() :
	
	def __init__(self, image) :
		print "The image needs some touch up...."
		self.sudoku_grid = [[0 for i in range(9)] for j in range(9)]
		self.ocr_object=ocr.ocr()
		self.img=image

	def preprocess(self) :
		try:
			self.img = cv2.resize(self.img,(800,1024), interpolation=cv2.INTER_AREA)
		except:
			pass
		self.blur = cv2.bilateralFilter(self.img,11,17,17)
		self.th2 = cv2.adaptiveThreshold(self.blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
		            cv2.THRESH_BINARY,11,3)
		self.kernel = np.ones((3,3),np.uint8);
		self.kernel1 = np.ones((5,5),np.uint8);
		self.th4=cv2.bitwise_not(self.th2)
		self.th4=cv2.erode(self.th4,self.kernel,iterations=1)
		self.th4=cv2.dilate(self.th4,self.kernel1,iterations=1)
		self.canvas = np.zeros(self.img.shape, np.uint8)
		self.canvas1 = np.zeros(self.img.shape, np.uint8)
		self.canvas.fill(255)
		self.th4=cv2.bitwise_not(self.th4)

	def find_contour(self) :
		self.im2,self.contours,self.hierarchy = cv2.findContours(self.th4, 1, 2)
		self.area=cv2.contourArea(self.contours[0])
		self.temp2=cv2.contourArea(self.contours[0])
		for i in self.contours :
			temp=cv2.contourArea(i)
			
			if temp > self.area :
				self.area=temp


		for i in self.contours :
			temp=cv2.contourArea(i)
			
			if temp > self.temp2 and temp!=self.area :
				self.temp2=temp

		for i in self.contours:
			if cv2.contourArea(i) == self.temp2:
				cv2.drawContours(self.canvas,[i],0,(0,250,0),3)
				self.a=i
				

	def find_corners(self) :
		self.peri = cv2.arcLength(self.a,True)
		self.approx = cv2.approxPolyDP(self.a,0.02*self.peri,True)
		x,y,w,h=cv2.boundingRect(self.a)
		left_topcorner = [x,y]
		right_bottomcorner = [x+w,y+h]
		left_bottomcorner = [x,y+h]
		right_topcorner = [x+w,y]
		temp1=10000
		x=[0,0]
		for i in self.approx :
			if math.sqrt(((i[0][0]-left_topcorner[0])*(i[0][0]-left_topcorner[0])) + ((i[0][1]-left_topcorner[1])*(i[0][1]-left_topcorner[1]))) < temp1 :
				x=i[0]
				temp1 = math.sqrt(((i[0][0]-left_topcorner[0])*(i[0][0]-left_topcorner[0])) + ((i[0][1]-left_topcorner[1])*(i[0][1]-left_topcorner[1])))
			
			#print i[0][1]
		left_topcorner=x

		temp1=10000
		x=[0,0]
		for i in self.approx :
			if math.sqrt(((i[0][0]-left_bottomcorner[0])*(i[0][0]-left_bottomcorner[0])) + ((i[0][1]-left_bottomcorner[1])*(i[0][1]-left_bottomcorner[1]))) < temp1 :
				x=i[0]
				temp1 = math.sqrt(((i[0][0]-left_bottomcorner[0])*(i[0][0]-left_bottomcorner[0])) + ((i[0][1]-left_bottomcorner[1])*(i[0][1]-left_bottomcorner[1])))
			
			#print i[0][1]
		left_bottomcorner=x

		temp1=10000
		x=[0,0]
		for i in self.approx :
			if math.sqrt(((i[0][0]-right_topcorner[0])*(i[0][0]-right_topcorner[0])) + ((i[0][1]-right_topcorner[1])*(i[0][1]-right_topcorner[1]))) < temp1 :
				x=i[0]
				temp1 = math.sqrt(((i[0][0]-right_topcorner[0])*(i[0][0]-right_topcorner[0])) + ((i[0][1]-right_topcorner[1])*(i[0][1]-right_topcorner[1])))
			
			#print i[0][1]
		right_topcorner=x

		temp1=10000
		x=[0,0]
		for i in self.approx :
			if math.sqrt(((i[0][0]-right_bottomcorner[0])*(i[0][0]-right_bottomcorner[0])) + ((i[0][1]-right_bottomcorner[1])*(i[0][1]-right_bottomcorner[1]))) < temp1 :
				x=i[0]
				temp1 = math.sqrt(((i[0][0]-right_bottomcorner[0])*(i[0][0]-right_bottomcorner[0])) + ((i[0][1]-right_bottomcorner[1])*(i[0][1]-right_bottomcorner[1])))
			
			#print i[0][1]
		right_bottomcorner=x


		#print approx
		self.h1=np.array([left_topcorner, right_topcorner, right_bottomcorner, left_bottomcorner],np.float32)
		

	def straighten_image(self) :
		self.h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
		self.retval = cv2.getPerspectiveTransform(self.h1,self.h)	# apply perspective transformation
		self.warp = cv2.warpPerspective(self.th4,self.retval,(450,450))
		self.original_img = cv2.warpPerspective(self.img, self.retval, (450,450))

	def isolate_digits(self) :
		

		h,w=self.warp.shape
		self.w = Width=w/9;
		self.h = Height=h/9;
		self.xcor=[]
		self.ycor=[]
		x=0
		y=0

		for i in range(1,10) :
			self.xcor.append(x+(i-1)*Width)
			self.ycor.append(y+(i-1)*Height)

		count=0
		for a in range(0,9) :
			for b in range(0,9) :
				crop_img=self.warp[self.ycor[b]:self.ycor[b]+Height,self.xcor[a]+5:self.xcor[a]+Width-7]
				canvas = np.zeros(crop_img.shape, np.uint8)
				canvas.fill(255)
				height, width = crop_img.shape
				crop_img=cv2.bitwise_not(crop_img)
				crop_img=cv2.erode(crop_img,self.kernel1,iterations=1)
				crop_img=cv2.dilate(crop_img,self.kernel,iterations=1)
				crop_img=cv2.bitwise_not(crop_img)
				digit_height=0
				digit_width=0
				columns=0
				rows=0
				black_pixels=0
				row_start=0
				row_end=0
				col_start=0
				col_end=0
				temp_x=0
				for y in range(height/2,height) :
					black_pixels=0
					for x in range(0,width) :
						if crop_img[y,x] < 255 :
							
							crop_img[y,x]=0
							black_pixels+=1

					if black_pixels > 3   :
						digit_height+=1
						row_end=y
					else :
						break



				black_pixels=0
				for y in range((height/2)-1,0,-1) :
					black_pixels=0
					for x in range(0,width) :
						if crop_img[y,x] < 255 :
							black_pixels+=1
							crop_img[y,x]=0

					if black_pixels > 3 :
						digit_height+=1
						row_start=y
					else :
						
						break

				if digit_height > height/2 :

					flag=0
					temp_width=0
					temp_col_start=0
					temp_col_end=0
					max_width=5
					for x in range(0,width) :
						
						black_pixels=0
						for y in range(row_start,row_end) :
							if crop_img[y,x] < 255 :
								black_pixels+=1
								crop_img[y,x]=0

						if black_pixels > 2 and flag==0 :
							temp_col_start=x
							temp_width=1
							flag=1

						elif black_pixels <=2 and flag==1 :
							temp_col_end=x
							flag=0
							if temp_width > max_width :
								max_width = temp_width
								col_start=temp_col_start
								col_end=temp_col_end
								temp_width=0
								
								print col_start, col_end

						elif black_pixels > 2 and flag==1 :
							temp_width+=1
							temp_col_end=x
							if temp_width > max_width :
								max_width = temp_width
								col_start=temp_col_start
								col_end=temp_col_end


						elif black_pixels <=2 and flag==0 :
							continue

					if max_width <=5 :
						continue

					else :
						digit=crop_img[row_start:row_end, col_start:col_end]
						digit=cv2.resize(digit,(10,10),interpolation=cv2.INTER_AREA)
						digit=cv2.bitwise_not(digit)
						integer=self.ocr_object.recognize_digit(digit)
						#print b,",",a," = ",integer
						self.sudoku_grid[b][a]=integer
						count+=1

		print "The extracted sudoku grid is as follows - "
		print self.sudoku_grid
		
		return self.sudoku_grid

	def print_grid(self):
    		for i in range(9):
			for j in range(9):
				if not self.sudoku_grid[i][j]==0:
					cv2.putText(self.original_img, str(self.sudoku_grid[i][j]), (self.ycor[j]+self.h/2, self.xcor[i]+self.w/2), cv2.FONT_HERSHEY_SIMPLEX,1 , (255,0,0), 2, cv2.LINE_AA)
		plt.imshow(self.original_img, 'gray')
		plt.show()
		cv2.imwrite('image.jpg', self.original_img)

	def paint_image(self, solved_sudoku) :
		for i in range(9) :
			for j in range(9) :
				if self.sudoku_grid[i][j] == 0 :
					cv2.putText(self.original_img, str(solved_sudoku[i][j]), (self.ycor[j]+self.h/2, self.xcor[i]+self.w/2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)





	