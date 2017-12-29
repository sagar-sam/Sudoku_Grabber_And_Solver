import cv2
import numpy as np
import time,sys
import matplotlib.pyplot as plt

class ocr :
	
	def __init__(self) :
		print "MACHINE LEARNING SEGMENT ACTIVATED...."
		print "Training Computer with Image Data....."
		self.samples = np.float32(np.loadtxt('feature_vector_pixels.data')) #loads the training data in a numpy array
		self.responses = np.float32(np.loadtxt('samples_pixels.data')) #loads the correct responses or lables in a numpy array
		self.model = cv2.ml.KNearest_create() #creates an instance for KNN ( for opencv version 2, use KNearest() instead of KNearest_create())
		self.model.train(self.samples,cv2.ml.ROW_SAMPLE,self.responses) #trains the computer with samples and responses
		print "Training complete. Model Ready for execution!"

	

	def recognize_digit(self, img) :
		self.feature = img.reshape((1,100)).astype(np.float32) #flattens the 2D array
		self.ret,self.results,self.neigh,self.dist = self.model.findNearest(self.feature,k=1) #returns the preidction
		self.integer = int(self.results.ravel()[0]) #results.ravel()[0] stores the required integer

		return self.integer


