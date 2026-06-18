import cv2
import numpy as np

class ImageFilters:

    @staticmethod
    def gaussian(image):
        return cv2.GaussianBlur(image, (7,7), 0)
    
    @staticmethod
    def laplacian(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)

        return np.uint8(np.absolute(lap))
    
    @staticmethod
    def canny(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 100, 200)
        return canny
    
    @staticmethod
    def median(image):
        return cv2.medianBlur(image, 5)
    
    @staticmethod
    def sobel(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
        sobelx = np.uint8(np.absolute(sobelx))
        sobely = np.uint8(np.absolute(sobely))
        sobel = cv2.bitwise_or(sobelx, sobely)
        return sobel
    
    @staticmethod
    def blur(image):
        return cv2.blur(image, (7, 7))
    
    @staticmethod
    def bilateral(image):
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    @staticmethod
    def grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)