import cv2
import numpy as np

class Morphology:
     @staticmethod
     def dilate(image):
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          return cv2.dilate(gray, (7, 7), iterations=2)
     
     @staticmethod
     def erode(image):
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          return cv2.erode(gray, (7, 7), iterations=2)
     
     @staticmethod
     def gradient(image):
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          return cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, (7, 7))
     
     @staticmethod
     def tophat(image):
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          return cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, (7, 7))