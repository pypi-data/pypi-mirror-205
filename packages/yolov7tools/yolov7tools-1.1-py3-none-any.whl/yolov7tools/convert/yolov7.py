import os.path
from typing import Union

import fiftyone as fo


def fiftyone2yolov7(dataset: Union[str, fo.Dataset], output_dir, indices=None, label_field="ground_truth", split=None):
    """Export a fiftyone dataset to the filesystem with yolov7 format (ready for training)

    This function needs to be called once for each split of the same dataset
    (you should have a fifyone dataset for each split and export them separately)

    Args:
        dataset (str, fo.Dataset): Name of the fiftyone dataset or a fiftyone Dataset instance
        output_dir (str): Path where the yolov7 dataset will be placed.
            It should be a folder where the different splits (train, val test) will live
            The folder for each split is created on the spot,
            based on the presence of train, val or test in the name of the fiftyone dataset 
        label_field (str, optional): ??. Defaults to "ground_truth".

    Returns:
        export_dir (str): Path of the exported dataset
    """

    if isinstance(dataset, str):
        dataset = fo.load_dataset(dataset)
    elif isinstance(dataset, fo.Dataset) or isinstance(dataset, fo.core.view.DatasetView):
        pass
    else:
        raise ValueError("Please pass a fiftyone dataset name or a dataset instance")
    
    if indices is not None:
        ids=[]
        for sample in dataset:
            ids.append(sample["id"])
    
        view=dataset[[ids[i] for i in indices]]
        
    else:
        view = dataset

    view.export(
        export_dir=output_dir,
        dataset_type=fo.types.YOLOv5Dataset,
        label_field=label_field,
        split=split
    )

    return output_dir