import logging
import os.path
import itertools
import numpy as np
import cv2
from idtrackerai.utils.py_utils import read_json_file
from idtrackerai.animals_detection.segmentation_utils import (
    _filter_contours_by_area,
    segment_frame
)
import joblib
from tqdm import tqdm

from yolov7tools.constants import EXTENSION

logger = logging.getLogger(__name__)

def annotate_experiment(store, chunks, images_path):

    llobs={}
    annotations={}
    for chunk in chunks:
        print(chunk)
        list_of_blobs, annot = annotate_chunk(store, chunk=chunk, framerate=30*store._metadata["framerate"], images_path=images_path)
        llobs[chunk]=list_of_blobs
        annotations.update(annot)
        
    return llobs, annotations

def annotate_chunk(store, chunk, framerate, images_path, list_of_blobs=None, resolution=None):
    
    """
    Return list of annotations 
    """

    if list_of_blobs is None:

        list_of_blobs = np.load(
            os.path.join(
                store._basedir, "idtrackerai", f"session_{str(chunk).zfill(6)}", "preprocessing", "blobs_collection.npy"
            ),
            allow_pickle=True
        ).item()
        
        list_of_blobs.reconnect_from_cache()

    blobs_in_video = list_of_blobs.blobs_in_video[
        list_of_blobs._start_end_with_blobs[0]:
        list_of_blobs._start_end_with_blobs[1]+1
    ]
    
    if resolution is None:
        resolution = (
            # width
            store.get(4),
            # height
            store.get(3)
        )

    annotations = process_blobs_in_video(store, blobs_in_video, framerate, images_path, resolution=resolution)
    return list_of_blobs, annotations

def apply_segmentation_criteria(frame, config):
    """
    Segment a frame following the idtrackerai preprocessing algorithm

    Args:
        frame (np.ndarray): Gray frame depicting a scene of an experiment
        config (_type_): Dictionary describing segmentation parameters to be applied to segment the frame.
        Must contain:
            _intensity: dictionary with a key "value" and whose value is a list of two elements, with the min and max thresholds of pixel intensity 
            _area: dictionary with a key "value" and whose value is a list of two elements, with the min and max thresholds of blob area
            _roi:  dictionary with a key "value" and whose value is formatted as idtrackerai exports the ellipsoid roi
    Returns:
        result (tuple): The segmented frame and the list of contours in the segmented frame, respectively
    """

    roi_contour = np.array(eval(config["_roi"]["value"][0][0])).reshape((-1, 1, 2))
    roi_mask = np.zeros_like(frame)
    roi_mask = cv2.drawContours(roi_mask, [roi_contour], -1, 255, -1)

    frame_canvas = np.zeros_like(frame)
    segmented_frame = segment_frame(frame, config["_intensity"]["value"][0], config["_intensity"]["value"][1], None, roi_mask, False)
    _, contours, hierarchy = cv2.findContours(
        segmented_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    # Filter contours by size
    good_contours_in_full_frame = _filter_contours_by_area(
        contours, config["_area"]["value"][0], config["_area"]["value"][1]
    )

    final_frame = cv2.drawContours(frame_canvas.copy(), good_contours_in_full_frame, -1, 255, -1)
    return final_frame, good_contours_in_full_frame


def annotate_images(images_path, conf_file, verbose=True, n_jobs=1):
    
    annotations={}

    config = read_json_file(conf_file)
    
    images = sorted(os.listdir(images_path))
    images = [image for image in images if image.endswith(EXTENSION)]

    if n_jobs > 1:
        verbose=False
    
    if verbose:
        iterable=tqdm(images)
    else:
        iterable = images

    output = joblib.Parallel(n_jobs=n_jobs)(
        joblib.delayed(annotate_image)(images_path, filename, config, i)
        for i, filename in enumerate(iterable)
    )

    for i, filename in enumerate(iterable):
        if output[i] is not None:
            annotations[os.path.join(images_path, filename)] = output[i]

    return annotations


def annotate_image(images_path, filename, config, i):
    
    annotations = []
    
    if i % 500 == 0:
        print(f"Annotating {i}th image")


    path = os.path.join(images_path, filename)
    assert os.path.exists(path), f"{path} not found"

    logger.debug(f"Reading image {path}")

    frame = cv2.imread(path)
    
    if frame is None:
        print(f"Could not read {path}")
        return

    if len(frame.shape) > 2:
        frame=frame[:,:,0]

    _, contours = apply_segmentation_criteria(frame, config)
    
    for contour in contours:
        
        contour_attrs = annotate_contour(frame, contour)

        annotations.append({
            "bounding_box": contour_attrs["bbox_norm"],
            "label": "fly",
            "area": contour_attrs["area"],
            "mask": contour_attrs["mask"],
            "confidence": 1,
            "iscrowd": None
        })
    
    return annotations


def annotate_contour(frame, contour):

    attrs = {}
    
    # area of the contour
    attrs["area"] = cv2.contourArea(contour)

    # bounding box of the contour
    bbox = cv2.boundingRect(contour)
    orig_shape = frame.shape

    attrs["bbox_norm"] = [
        bbox[0] / orig_shape[1],
        bbox[1] / orig_shape[0],
        bbox[2] / orig_shape[1],
        bbox[3] / orig_shape[0],
    ]
    
    # mask of the contour (relative to the bounding box!)
    frame_canvas = np.zeros_like(frame)
    mask = cv2.drawContours(frame_canvas, [contour], -1, 255, -1)
    unraveled = np.stack(np.where(mask == 255), axis=1)

    unraveled[:, 0] -= bbox[1] # bbox[1] has the Y coordinate, which comes in the first axis (height) of unraveled
    unraveled[:, 1] -= bbox[0] # bbox[0] has the X coordinate, which comes in the second axis (width) of unraveled

    mask = np.zeros((bbox[3], bbox[2]))
    mask[unraveled[:, 0], unraveled[:, 1]] = 1
    mask=mask==1
        
    attrs["mask"] = mask

    return attrs


def process_blobs_in_video(store, blobs_in_video, framerate, images_path, resolution):
    
    """
    Return annotations for frames in the video
    
    Arguments:
        store: imgstore.VideoStore
        blobs_in_video (idtrackerai.list_of_blobs.ListOfBlobs)
        framerate (int): Skip these many frames every time (pass 1 to process all frames)
        images_path (str): Directory where the images will be saved with jpg extension
    """

    annotations = {}
        
    for blobs_in_frame in blobs_in_video:

        if len(blobs_in_frame) == 0:
            continue

        frame_number = blobs_in_frame[0].frame_number
        
        there_are_crossings = any([blob.is_a_sure_crossing()  for blob in blobs_in_frame])

        if frame_number % framerate != 0 and not there_are_crossings:
            continue


        file_name = os.path.join(
                images_path,
                f"{os.path.basename(store._basedir)}_{frame_number}.jpg"
        )

        if not os.path.exists(file_name):
            store.set(1, frame_number)
            ret, frame = store.read()
            orig_shape = frame.shape

            if ret:
                frame = cv2.resize(frame, resolution)
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                cv2.imwrite(file_name, frame)
        else:
            orig_shape = (store.get(4), store.get(3))
        
        scale_factor = orig_shape[0] / resolution[0]
        # > 1 if images become smaller and < 1 if bigger
            
        annotations.update(
            process_blobs_in_frame(blobs_in_frame, file_name, orig_shape, scale_factor)
        )
    
    return annotations
    

def process_blobs_in_frame(blobs_in_frame, file_name, orig_shape, scale_factor):

    """
    Return all annotations for the pass frame
    
    
    Arguments:
    
        * blobs_in_frame (list of idtrackerai.blob.Blob instances). The function takes from each blob:       
             - bounding_box_full_resolution: coordinates of the bounding box in the original frame
             - pixels: x, y coordinats of the pixels making up the contour of the animal
             - is_a_crossing: True if the blob has been classified as crossing by the crossing detector and it has 2 overlapping blobs in the immediate future or past (or both).
             - area: Size of the contour
        * file_name (str): Name of the file with which the corresponding frame will be saved
        * orig_shape (tuple): Size of the original frame
        * scale_factor (float): If > 1, the annotation is scaled down compared to the original image (original shape)
    
    Returns:
    
      annotation: A dictionary with one entry. The key is file_name and the value is a list of dictionaries,
          where each dictionary contains the following attributes for annotated animal:
              - bounding_box: (x, y, w, h) in the saved image of this annotation
              - label: class of the annotation
              - area: size of the contour
              - mask: white where the animal is detected and black elsewhere
              - confidence: how sure we are of this annotation
              - iscrowd: True if more than one animal makes up this annotation          
    """
    
    annotations = []
    for identity, blob in enumerate(blobs_in_frame):

        bbox = [int(e) for e in itertools.chain(*list(blob.bounding_box_full_resolution))]
        bbox[2] -= bbox[0]
        bbox[3] -= bbox[1]
        
        # Bounding box coordinates should be relative values
        # in [0, 1] in the following format:
        # [top-left-x, top-left-y, width, height]

        y_coords, x_coords = list(np.unravel_index(blob.pixels, orig_shape))


        mask = np.zeros(orig_shape, dtype=np.uint8)
        mask[
            y_coords,
            x_coords
        ] = 255
        

        contour = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1][0]

        bbox = cv2.boundingRect(contour)

        bbox_norm = [
            bbox[0] / orig_shape[1],
            bbox[1] / orig_shape[0],
            bbox[2] / orig_shape[1],
            bbox[3] / orig_shape[0],
        ]        
        mask = mask[
            bbox[1]:bbox[1]+bbox[3],
            bbox[0]:bbox[0]+bbox[2],
        ]

        if scale_factor != 1:
            dsize = (
                int(bbox[2] / scale_factor),
                int(bbox[3] / scale_factor)
            )

            mask = cv2.resize(mask, dsize)

        mask=mask==255

        if blob.is_a_crossing:
            iscrowd=1
        else:
            iscrowd=0

        annotations.append({
            "bounding_box": bbox_norm,
            "label": "fly",
            "area": blob.area,
            "mask": mask,
            "confidence": 1,
            "iscrowd": iscrowd
        })

    return {file_name: annotations}
