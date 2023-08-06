from yolov7tools.detection import Detection

def load_detection(line):

    data=line.strip("\n").split(" ")
    id, x, y, w, h, conf=data[:6]
    return Detection(int(id), float(conf), float(x), float(y), float(w), float(h))
    

