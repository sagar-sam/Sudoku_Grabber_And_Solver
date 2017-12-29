import cv2
import ocr 
import preprocessing as ip
import solve_sudoku as ss
from matplotlib import pyplot as plt

def start(filename):
	print "filename is ",filename

	#filename = "53.jpg"
	try:
		img=cv2.imread(filename,0)
		plt.imshow(img, 'gray')  #original image
		plt.show()
	except:
		print "oops! unable to open image, try again"
		import pathgui
		return
	print "Before preprocess"
	image_object=ip.image_processing(img)
	print "After preprocess object"
	image_object.preprocess()
	print "After preprocessing"
	image_object.find_contour()
	plt.imshow(image_object.canvas, 'gray')
	plt.show()
	print "After contour"
	image_object.find_corners()
	print "After corners"
	image_object.straighten_image()
	print "After straight image"
	sudoku_grid=image_object.isolate_digits()
	image_object.print_grid()
	solver_object=ss.solve_sudoku(sudoku_grid)
	print "The given sudoku grid has ",solver_object.count, " solutions."
	if solver_object.count > 0 :
		image_object.paint_image(solver_object.all[0])
		plt.imshow(image_object.original_img, 'gray')   #output
		plt.show()

	import pathgui


#start("1.JPG")