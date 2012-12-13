import os
import sys
from PIL import Image, ImageDraw
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageEnhance
from PIL import ImageOps
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
	bbox = ImageChops.difference(im1, im2).getbbox()
	print bbox
	return bbox is None
	#return ImageChops.difference(im1, im2).getbbox() is None

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
	#test
	scr = get_screenshot()
	im = scr.crop(region)
	im.save(os.path.join(path_to_test, 'left_bank.png'))
	return check_equal(im, sample)
	#end test

	#scr = get_screenshot()
	#if region:
	#	scr.crop((region))

	#sample_w, sample_h = sample.size
	#scr_sz = scr.size
	#for xi in range(0, scr_sz[0] - sample_w):
	#	for yi in range(0, scr_sz[1] - sample_h):
	#		test_area = scr.crop((xi, yi, xi + sample_w, yi + sample_h))
	#		if check_equal(sample, test_area):
	#			return (xi, yi)
	#	print(xi)
	#return None

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
	regions = {}
	width, height  = im_left.size
	region_width = 0
	n_regions = 0
	im = im_left
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

def ocr_char(im):
	im_w, im_h = im.size
	for ocr_value, ocr_item in ocr_images.iteritems():
		if ocr_item.size >= im.size:
			ocr_w, ocr_h = ocr_item.size
			for x in xrange(0, ocr_w - im_w + 1):
				for y in xrange(0, ocr_h - im_h + 1):
					ocr_part = ocr_item.crop((x, y, x + im_w, y + im_h))
					# now equality test goes perfect, but maybe we should choose the closest match (the smallest bbox)
					if check_equal(im, ocr_part):
						return ocr_value
					#result = check_equal(im, ocr_part)
					#ocr_part.save(os.path.join(path_to_test, 'ocr_{}_{}_{}_left.png'.format(result, x, y)))

def ocr(regions):
	if regions:	
		''.join([ocr_char(im.crop(regions[r])) for r in regions])
	else:
		None
	#print(r, ocr_val)
	#imx.save(os.path.join(path_to_test, '{}_left_money_region.png'.format(r)))

def get_filename(path):
	return os.path.split(os.path.splitext(path)[0])[1]
	
path_to_cards = '..\\img\\cards'
path_to_test = '..\\img\\test'
path_to_ocr = '..\\img\\ocr'
path_to_markers = '..\\img\\markers'

card_sample_files = get_imlist(path_to_cards, 'png')
card_ocr_files = get_imlist(path_to_ocr, 'png')
card_images = [Image.open(f) for f in card_sample_files]
ocr_images = {get_filename(f): posterize_wb(Image.open(f).convert('L')) for f in card_ocr_files}

scr = get_screenshot()
x0, y0 = get_marker_location(os.path.join(path_to_markers, 'hand_16_40.png'))
x1_left, y1_left, x2_left, y2_left = offset_left
x1_right, y1_right, x2_right, y2_right = offset_right
money_left = scr.crop((x1_left + x0, y1_left + y0, x2_left + x0, y2_left + y0))
money_right = scr.crop((x1_right + x0, y1_right + y0, x2_right + x0, y2_right + y0))
money_left.save(os.path.join(path_to_test, 'left_money.png'))
money_right.save(os.path.join(path_to_test, 'right_money.png'))
im_left = posterize_wb(money_left)
im_right = posterize_wb(money_right)
im_left.save(os.path.join(path_to_test, 'left_money_wb.png'))
im_right.save(os.path.join(path_to_test, 'right_money_wb.png'))
im_left.save(os.path.join(path_to_test, 'left_money_wb.png'))
regions = find_regions(im_left)	
str = ocr(regions)
if str:
	if (str[0] == '$'):
		str = str[1:]
	if str.isdigit():	
		value = (int(str))
		print(value)
	else:
		print('ERROR: OCR value is not digit: {}'.format(str))
else:
	print('ERROR: OCR cannot recognize area:')




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