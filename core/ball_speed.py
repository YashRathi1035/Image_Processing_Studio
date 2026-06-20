import cv2
import numpy as np

class BallSpeedTrackbar:
    def __init__(self):
        self.cm_per_pixel = 0.05
        self.previous_center = None
        self.total_distance = 0

        cv2.namedWindow("Ball Trackbar")
        cv2.createTrackbar("LH", "Ball Trackbar", 0, 255, self.nothing)
        cv2.createTrackbar("LS", "Ball Trackbar", 0, 255, self.nothing)
        cv2.createTrackbar("LV", "Ball Trackbar", 0, 255, self.nothing)
        cv2.createTrackbar("UH", "Ball Trackbar", 255, 255, self.nothing)
        cv2.createTrackbar("US", "Ball Trackbar", 255, 255, self.nothing)
        cv2.createTrackbar("UV", "Ball Trackbar", 255, 255, self.nothing)
        cv2.createTrackbar("Min Area", "Ball Trackbar", 100, 5000, self.nothing)
        cv2.createTrackbar("CM x1000", "Ball Trackbar", 50, 500, self.nothing)

    def process(self, frame, fps):
        lh = cv2.getTrackbarPos("LH", "Ball Trackbar")
        ls = cv2.getTrackbarPos("LS", "Ball Trackbar")
        lv = cv2.getTrackbarPos("LV", "Ball Trackbar")
        uh = cv2.getTrackbarPos("UH", "Ball Trackbar")
        us = cv2.getTrackbarPos("US", "Ball Trackbar")
        uv = cv2.getTrackbarPos("UV", "Ball Trackbar")
        min_area = cv2.getTrackbarPos("Min Area", "Ball Trackbar")
        self.cm_per_pixel = (cv2.getTrackbarPos("CM x1000", "Ball Trackbar") / 1000)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([lh, ls, lv])
        upper = np.array([uh, us, uv])
        mask = cv2.inRange(hsv, lower, upper)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            cv2.imshow("Ball Mask", mask)
            return frame
        
        largest = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest) < min_area:
            cv2.imshow("Ball Mask", mask)
            return frame
        
        (x,y), radius = cv2.minEnclosingCircle(largest)
        center = (int(x), int(y))

        speed = 0
        
        if self.previous_center is not None:
            pixel_distance = np.sqrt((center[0] - self.previous_center[0])**2 + 
                                     (center[1] - self.previous_center[1])**2)
            
            real_distance = pixel_distance * self.cm_per_pixel

            t = 1/fps

            speed = real_distance/t
            self.total_distance += real_distance
        self.previous_center = center
        cv2.circle(frame, center, int(radius), (0, 255, 0), 2)
        cv2.putText(frame, f"Speed : {speed}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Distance : {self.total_distance}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Ball Mask", mask)
        return frame


    def nothing(self, x):
        pass