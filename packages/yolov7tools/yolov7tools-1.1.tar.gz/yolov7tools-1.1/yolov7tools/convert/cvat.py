import fiftyone as fo
import fiftyone.brain as fob

def annotate_dataset(dataset, anno_key, classes, label_type="instances", unique=0, interval=None, indices=None, overwrite=False):

    if isinstance(dataset, str):
        dataset = fo.load_dataset(dataset)
    elif isinstance(dataset, fo.Dataset):
        pass
    else:
        raise ValueError("Please pass a fiftyone dataset name or a dataset instance")

    if indices is not None:
        ids=[]
        for sample in dataset:
            ids.append(sample["id"])
        view=dataset[[ids[i] for i in indices]]
    else:
        view=dataset

    if interval is not None:
        view = dataset[interval[0]:interval[1]]

    else:
        view = dataset

    if unique>0:
        dataset = view
        results = fob.compute_similarity(dataset, brain_key="img_sim")
        results.find_unique(unique)
        view = dataset.select(results.unique_ids)
        vis_results = fob.compute_visualization(dataset, brain_key="img_vis")
        plot = results.visualize_unique(visualization=vis_results)
        plot.show()
        
    # Upload the samples and launch CVAT
    anno_results = view.annotate(
        # A unique identifer for this run
        anno_key,
        label_field="ground_truth",
        label_type=label_type,
        classes=classes,
        launch_editor=True,
        backend="cvat",
        task_size=max(100, unique),
    )

    import ipdb; ipdb.set_trace()
    view.load_annotations(anno_key, cleanup=True)
    return