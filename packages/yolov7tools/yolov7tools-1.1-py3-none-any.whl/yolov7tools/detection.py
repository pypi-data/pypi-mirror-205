from dataclasses import dataclass
import numpy as np

@dataclass(order=True)
class Detection:

    class_id: int
    conf: float
    x: float
    y: float
    w: float
    h: float


    @property
    def area(self):
        return self.w * self.h

    @property
    def angle(self):
        """
        Compute angle between center of image and centroid of YOLOv7 detection
        
        Returns:
        
        * angle (float): Orientation of the detection (0 points North and 90 points East)
        """
    
        if getattr(self, "_angle", None) is None:
    
            centroid_with_detection_centroid_at_00 = (self.x - 0.5, self.y - 0.5)
        
            angle = np.rad2deg(np.arctan2(*centroid_with_detection_centroid_at_00[::-1]))
        
            if angle > 180:
                angle -= 360
        
            if angle < - 180:
                angle += 360
        
            self._angle=angle
    
        return self._angle
    
