"""
convert

Export annotations produced with idtrackerai (computer generated) on a video with behaving animals
to fiftyone for validation.

Throughout the code, the following names are used to refer to the data structures containing the annotations,
depending on the format in which they are

list_of_blobs: Annotations produced by idtrackerai
annotations: Intermediate state of the annotations, in a standard dictionary format with entries:
    - bounding_box
    - label
    - area
    - mask
    - confidence
    - iscrowd
    see process_blobs_in_frame for more info

samples: Annotations in fiftyone format
"""