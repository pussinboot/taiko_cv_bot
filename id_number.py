import numpy as np
from skimage import io
import cv2

class NumberRecog:
	def __init__(self):
		self.no_imgs = [None]*10
		for i in range(10):
		    filename = './masks/{}.png'.format(i)
		    self.no_imgs[i] = io.imread(filename)

	def test_img(self,img_to_test):
		res = []
		for i in reversed(range(7)):
		    arr = [np.mean(cv2.absdiff(img_to_test[:,12*i:12*(i+1),:],self.no_imgs[n])) \
		         for n in range(len(new_imgs))]
		    if min(arr) > 75: break
		    res += [np.argmin(arr)]
		    #print(min(arr))
		res.reverse()
		return int(''.join(map(str, res)))

	def test(self,img_to_test):
		try:
			self.test_img(img_to_test)
		except:
			return -1