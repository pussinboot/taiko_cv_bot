import numpy as np
from skimage import io
import cv2

class NumberRecog:
	def __init__(self,path_to_files='../masks'):
		self.no_imgs = [None]*10
		self.last_score = 0
		for i in range(10):
		    filename = path_to_files+'/{}.png'.format(i)
		    self.no_imgs[i] = io.imread(filename)[:,:,:3]

	def test_img(self,img_to_test):
		res = []
		for i in reversed(range(7)):
		    arr = [np.mean(cv2.absdiff(img_to_test[:,12*i:12*(i+1),:],self.no_imgs[n])) \
		         for n in range(len(self.no_imgs))]
		    if min(arr) > 100: break
		    res += [np.argmin(arr)]
		    #print(min(arr))
		res.reverse()
		torstr = ''.join(map(str, res))
		tor = int(torstr)
		if abs(len(torstr) - len(str(self.last_score))) > 1:
			if self.last_score > 0:
				tor = self.last_score
		self.last_score = tor
		return tor

	def test(self,img_to_test):
		try:
			return self.test_img(img_to_test)
		except:
			return -1

if __name__ == '__main__':
	testng = NumberRecog()