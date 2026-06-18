import cv2
import numpy as np

class Segmentation:

    @staticmethod
    def threshold(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return th
    
    @staticmethod
    def adaptive(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return th
    
    ## Watershed to be added later

    @staticmethod
    def kmeans(image):
        twoD = image.reshape((-1, 3))
        twoD = np.float32(twoD)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k=4

        ret, label, centers = cv2.kmeans(twoD, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers)
        result = centers[label.flatten()]
        result = result.reshape(image.shape)
        return result