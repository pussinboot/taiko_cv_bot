# %load id_number.py
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

	def clean_img(self,img_to_clean,thresh=25):
		r, g, b = img_to_clean[:,:,0], img_to_clean[:,:,1], img_to_clean[:,:,2]
		mask = (abs(r - g) > thresh) & (abs(g-b) > thresh)
		img_to_clean[mask] = [0,255,0]
		return img_to_clean

	def test_img(self,img_to_test,thresh=50):
		res = []
		img_to_test = self.clean_img(img_to_test)
		for i in reversed(range(7)):
		    arr = [np.mean(cv2.absdiff(img_to_test[:,12*i:12*(i+1),:],self.no_imgs[n])) \
		         for n in range(len(self.no_imgs))]
		    if min(arr) > thresh: break
		    res += [np.argmin(arr)]
		    #print(min(arr))
		res.reverse()
		torstr = ''.join(map(str, res))
		tor = int(torstr)
		if tor  < self.last_score:
			tor = self.last_score
		else:
			self.last_score = tor
		return tor

	def reset(self):
		self.last_score = 0
    
	def test(self,img_to_test):
		try:
			return self.test_img(img_to_test)
		except:
			return self.last_score

if __name__ == '__main__':
	testng = NumberRecog()