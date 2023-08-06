import argparse
import fiftyone as fo
from fiftyone import ViewField as F
import ipdb

def main():

    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    args=ap.parse_args()

    dataset=fo.load_dataset(args.dataset)
    session=fo.launch_app(dataset, address="0.0.0.0", port=5151)
    ipdb.set_trace()
main()
