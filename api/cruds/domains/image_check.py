import cv2
import numpy as np

a = '../.././data/cache/26.1549935-127.6885488-20_google.png'
# b = '../.././data/cache/26.1549935-127.6885488-20_google-2.png'
b = '../.././data/cache/26.1549935-127.6885488-20_yahoo.png'

def equal_image(a, b):
  im_a = cv2.imread(a)
  im_b = cv2.imread(b)
  return np.array_equal(im_a, im_b)
