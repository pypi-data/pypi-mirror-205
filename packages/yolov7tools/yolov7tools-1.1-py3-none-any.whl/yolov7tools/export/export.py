import argparse
import glob

import fiftyone as fo
from idtrackerai.animals_detection.yolov7 import *

def get_parser():

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="incomplete frame folder")
    ap.add_argument("--chunk", type=int)
    ap.add_argument("--dataset", type=str)
    return ap

def match_file(path, frame_number):
    matches=glob.glob(f"{path}/{frame_number}_*")
    assert len(matches) == 1
    return matches[0]
  

def read_failed_frames(path):
    with open(path, "r") as filehandle:
        lines = filehandle.readlines()
        frame_numbers = [int(line.strip()) for line in lines]
    return frame_numbers 

def detections2sample(detections, label):
    raise NotImplementedError

def main():

    args = get_parser().parse_args()

    chunk = args.chunk
    failed_frames = os.path.join(args.input, "integration", f"{str(chunk).zfill(6)}_failure.txt")
    frame_numbers = read_failed_frames(failed_frames)

    frames_folder = os.path.join(args.input, "yolov7")

    dataset = fo.load_dataset(args.dataset)

    labels_folder = os.path.join(args.input, "yolov7", "labels")
    for frame_number in frame_numbers:
       path = match_file(frames_folder, frame_number)
       filename=os.path.basename(path)
       key=os.path.splitext(filename)[0]
       chunk_fidx = key.split("_")[1]
       chunk, frame_idx = [int(e) for e in key.split("-")]

     
       label_file=get_label_file_path(labels_folder, frame_number, chunk, frame_idx)
       lines=read_yolov7_label(label_file)
       detections = [yolo_line_to_detection(line) for line in lines]
       sample = detections2sample(detections, "prediction")
       dataset.add_sample(sample)
       dataset.save()
