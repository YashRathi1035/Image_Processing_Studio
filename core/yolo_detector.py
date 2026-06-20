from ultralytics import YOLO

class YoloDetector:

    model = YOLO("yolov8n.pt")

    @staticmethod
    def detect(image):

        results = YoloDetector.model(
            image,
            conf=0.5
        )

        return results[0].plot()