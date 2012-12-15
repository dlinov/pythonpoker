import os
import sys
from PIL import Image, ImageDraw
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageEnhance
from PIL import ImageOps
import cv2
import numpy as np

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

def get_imlist(path, ext):
	return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(ext)]
	
def get_screenshot():
	return ImageGrab.grab()

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
	"""
	Gets card from specified location
	"""
	scr = get_screenshot()
	x, y = location
	card = scr.crop((x, y, x + 12, y + 30))
	for i in range(0, len(card_images)):
		if check_equal(card, card_images[i]):
			return os.path.split(os.path.splitext(card_sample_files[i])[0])[1]

def contains_button(img_path, location):
	"""
	Checks if screen contains button
	"""
	scr = get_screenshot()
	x, y = location	
	img = Image.open(img_path)
	w, h = img.size
	elem = scr.crop((x, y, x + w, y + h))
	return check_equal(img, elem)

def contains_elem(sample, region):
	"""
	Checks if elem exists in specified region.
	If region = None whole screen is checked.
	Returns location within region or None if elem not found 
	"""
	scr = get_screenshot()
	im = scr.crop(region)
	im.save(os.path.join(path_to_test, 'left_bank.png'))
	return check_equal(im, sample)

def posterize_wb(image):
	"""
	Converts image into pure white-black one
	"""
	image = ImageOps.grayscale(image)
	image = ImageOps.posterize(image, 1)
	contrast = ImageEnhance.Contrast(image)
	image = contrast.enhance(4.0)
	return image

def find_regions(im):
	"""
	Returns areas for ocr
	"""
	regions = {}
	width, height  = im.size
	region_width = 0
	n_regions = 0
	# from left to the right
	for xi in xrange(0, width):
		# from top to the bottom
		for yi in xrange(0, height):
			# if is not black, then current column is not black at whole
			# so we need to grow its width
			if im.getpixel((xi, yi)) != 0:
				region_width += 1
				break;
		else:
			# now we know that whole column is black, so we can save region if its width > 0		
			if region_width > 0:
				regions[n_regions] = (xi - region_width, 0, xi - 1, height)
				region_width = 0
				n_regions += 1

	return regions

def ocr_char(im):
	im_w, im_h = im.size
	for ocr_value, ocr_item in ocr_images.iteritems():
		if ocr_item.size >= im.size:
			ocr_w, ocr_h = ocr_item.size
			# we should compare only items with close sizes
			#if ocr_w / im_w < 1.5 and ocr_w - im_w < 2 or ocr_h / im_h < 1.5 and ocr_h - im_h < 2:
			if im_w > 0: # a bit dirty hack against false positives
				for x in xrange(0, ocr_w - im_w + 1):
					for y in xrange(0, ocr_h - im_h + 1):
						ocr_part = ocr_item.crop((x, y, x + im_w, y + im_h))
						# now equality test goes perfect, but maybe we should choose the closest match (the smallest bbox)
						if check_equal(im, ocr_part):
							return ocr_value.split('_')[0]
						#result = check_equal(im, ocr_part)
						#ocr_part.save(os.path.join(path_to_test, 'ocr_{}_{}_{}_left.png'.format(result, x, y)))

def ocr(im):
	im = posterize_wb(im)
	im.save(os.path.join(path_to_test, 'area.png'))
	regions = find_regions(im)
	if regions:
		# join all not-None characters (well recognized)
		return ''.join(filter(lambda x: x, [ocr_char(im.crop(regions[r])) for r in regions]))
	#print(r, ocr_val)
	#imx.save(os.path.join(path_to_test, '{}_left_money_region.png'.format(r)))

def get_filename(path):
	return os.path.split(os.path.splitext(path)[0])[1]

# TODO: change to class fields
path_to_buttons = '..\\img\\buttons'
path_to_cards = '..\\img\\cards'
path_to_test = '..\\img\\test'
path_to_ocr = '..\\img\\ocr'
path_to_markers = '..\\img\\markers'

buttons_list = get_imlist(path_to_buttons, 'png')
card_sample_files = get_imlist(path_to_cards, 'png')
card_ocr_files = get_imlist(path_to_ocr, 'png')

button_images = {get_filename(f): Image.open(f) for f in buttons_list}
card_images = [Image.open(f) for f in card_sample_files]
ocr_images = {get_filename(f): posterize_wb(Image.open(f).convert('L')) for f in card_ocr_files}