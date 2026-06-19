import cv2
import numpy as np

class ImageTransform:
    
    @staticmethod
    def rotate(image, angle=45):
        height, width = image.shape[:2]
        center = (width//2, height//2)

        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        rotated = cv2.warpAffine(image, matrix, (width, height))
        return rotated
    
    @staticmethod
    def resize(image, scale = 1.5):
        height, width = image.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)

        return cv2.resize(image, (new_width, new_height))
    
    @staticmethod
    def perspective(image):
        rows, cols = image.shape[:2]

        pts1 = np.float32([
            [50, 50],
            [300, 50],
            [50, 300],
            [300, 300]
        ])
        pts2 = np.float32([
            [0, 0],
            [300, 0],
            [100, 300],
            [250, 300]
        ])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(image, matrix, (cols, rows))
        return result