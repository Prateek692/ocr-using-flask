import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def ocr_core(filename):  
    
    pil_image = Image.open(filename).convert('RGB') 
    open_cv_image = np.array(pil_image) 
    img = open_cv_image[:, :, ::-1].copy() 
    
    
    
    gray = get_grayscale(img)
    thresh = thresholding(gray)
    final_image=deskew(thresh)
    text = pytesseract.image_to_string(final_image) 
    return text





