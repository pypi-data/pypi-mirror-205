import glob
import os.path
from yolov7tools.constants import EXTENSION
import fiftyone as fo

def make_dataset(annotations, images_path, dataset_name):
    """Transform a dictionary of annotations into a fiftyone dataset

    Args:
        annotations (dict): Each key is a filename (no path) of an image file that has been annotated, and the value is a list of annotations,
            one annotation per object annotated in the frame
        images_path (str): Path to the image files referred to in the annotations arg
        dataset_name (str): Name of the resulting fiftyone dataset

    Returns:
        dataset (fiftyone.Dataset)

    """
    # Create samples for your data
    samples = []
    for filepath in glob.glob(os.path.join(images_path, f"*.{EXTENSION}")):

        filename=filepath#os.path.basename(filepath)

        sample = fo.Sample(filepath=filename)

        # Convert detections to FiftyOne format
        detections = []

        if filename not in annotations:
            # warnings.warn(f"{filepath} not found")
            continue

        for obj in annotations[filename]:

            detections.append(
                fo.Detection(**obj)
            )

        # Store detections in a field name of your choice
        sample["ground_truth"] = fo.Detections(detections=detections)

        samples.append(sample)

    # Create dataset
    dataset = fo.Dataset(dataset_name)
    dataset.add_samples(samples)

    return dataset