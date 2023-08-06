import argparse
from yolov7tools.convert.cvat import annotate_dataset

def main():

    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset")
    ap.add_argument("--anno-key")
    ap.add_argument("--unique", type=int, default=0)
    ap.add_argument("--label-type")
    ap.add_argument("--classes", nargs="+", type=str)
    ap.add_argument("--interval", type=int, nargs="+")
    args=ap.parse_args()

    annotate_dataset(args.dataset, anno_key=args.anno_key, classes=args.classes, label_type=args.label_type, unique=args.unique, interval=args.interval)
main()
