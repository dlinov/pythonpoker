import os
from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
import cv2
import numpy as np

def get_imlist(path, ext):
	return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(ext)]
	
def get_screenshot():
	return ImageGrab.grab()

def pil2cv(pil_img):
	pil_image = pil_img.convert('RGB') 
	open_cv_image = np.array(pil_image) 
	# Convert RGB to BGR 
	return open_cv_image[:, :, ::-1].copy()

def check_equal(im1, im2):
	#bbox = ImageChops.difference(im1, im2).getbbox()
	#print bbox
	#return bbox is None
	return ImageChops.difference(im1, im2).getbbox() is None

def get_marker_location(path):
	scr = pil2cv(get_screenshot())
	templ = cv2.imread(path)
	if templ is not None:
		result = cv2.matchTemplate(scr, templ, cv2.TM_CCOEFF_NORMED)
		y, x = np.unravel_index(result.argmax(),result.shape)
		return (x, y)
	else:
		raise IOError()

def get_card(location):
	scr = get_screenshot()
	x, y = location
	card = scr.crop((x, y, x + 12, y + 30))
	for i in range(0, len(card_images)):
		if check_equal(card, card_images[i]):
			return os.path.split(os.path.splitext(card_sample_files[i])[0])[1]



path_to_cards = '..\\img\\cards'
#path_to_test = '..\\img\\test'
#path_to_markers = '..\\img\\markers'

#print(get_marker_location())

card_sample_files = get_imlist(path_to_cards, 'png')
card_images = [Image.open(f) for f in card_sample_files]
#print('samples found: {}'.format(len(card_sample_files)))
##card_images = [cv2.imread(f) for f in card_sample_files]

#test_image_full = Image.open('..\\img\\test\\fullscreen.png')
#im = test_image_full.crop((62, 209, 74, 239))
##im = test_image_full.crop((77, 213, 89, 243))
## im.save(os.path.join(path_to_test, 'sample.png'))
##cv_im = pil2cv(im)

#for i in range(0, len(card_images)):
#	if check_equal(im, card_images[i]):
#		print(card_sample_files[i])
#print('search completed')