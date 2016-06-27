import numpy as np
from skimage import io
import cv2

class Recognizer:
	def __init__(self,path_to_files='./masks'):
		self.no_imgs = [None]*10
		for i in range(10):
			filename = path_to_files+'/{}.png'.format(i)
			self.no_imgs[i] = self.clean_img(io.imread(filename)[:,:,:3])
		self.messup_img =  self.clean_img(io.imread(path_to_files+'/messup.png')[35:67,101:153,:3])
		self.gob_names = ['good','okay','bad']
		gob_thresh = [100,90,95]
		self.gobs = {}
		for i in range(3):
			img = self.clean_img(io.imread('../masks/{}.png'.format(self.gob_names[i])))
			self.gobs[self.gob_names[i]] = Gob_Signal(img,gob_thresh[i])
		
		self.no_thresh = 60
		self.messup_thresh = 60

		self.reset()

	def reset(self):
		self.last_score = 0
		self.messed_up = False

	def clean_img(self,img_to_clean):
		img_to_clean = img_to_clean[:,:,:3]
		rgb = [0,255,0]
		mask = np.where(np.all(img_to_clean == rgb,axis=-1))
		img_to_clean[mask] = [-1,-1,-1]
		return img_to_clean

	def no_test(self,img_to_test):
		try:
			return self.no_tester(img_to_test)
		except:
			return self.last_score

	def no_tester(self,img_to_test,thresh=-1,debug=False):
		if thresh < 0: thresh = self.no_thresh
		res = []
		img_to_test = self.clean_img(img_to_test)
		for i in reversed(range(7)):
		    arr = [np.mean(cv2.absdiff(img_to_test[:,12*i:12*(i+1),:],self.no_imgs[n])) \
		         for n in range(len(self.no_imgs))]
		    if min(arr) > thresh: break
		    res += [np.argmin(arr)]
		res.reverse()
		torstr = ''.join(map(str, res))
		tor = int(torstr)
		if debug: return tor
		if tor  < self.last_score:
			tor = self.last_score
		return tor

	def messup_test(self,img_to_test):
		res = self.messup_tester(img_to_test)
		if res != self.messed_up:
			self.messed_up = res
			if res:
				print('mess up !!')
				return True
		return False

	def messup_tester(self,img_to_test, thresh=-1,debug=False):
		if thresh < 0: thresh = self.messup_thresh
		res = np.mean(cv2.absdiff(img_to_test,self.messup_img))
		if debug: return res
		return res < thresh

	def test_frame(self,frame):
		score = self.no_test(frame[52:68,-94:-10,:])
		delta_score = score - self.last_score # remember score is strictly increasing))
		self.last_score = score
		messup = self.messup_test(frame[35:67,101:153,:])
		tor =  {'score':score,'delta_score':delta_score,'messup':messup}
		for n in self.gob_names:
			tor[n] = self.gob[n].test(frame[50:75,15:45,:3])
		return tor

class Gob_Signal:
	def __init__(self,img,thresh):
		self.img = img
		self.thresh = thresh
		self.last_on = False

	def test(self,img_to_test):
		# tests if gob JUST got detected, flips off when no longer detected
		test_res = np.mean(cv2.absdiff(img_to_test,self.img))
		res = test_res - thresh
		if not self.last_on:
			if res < 0:
				self.last_on = True
				return True
		else:
			if res > 0:
				self.last_on = False
		return False

if __name__ == '__main__':
	test_check = Recognizer('../masks')