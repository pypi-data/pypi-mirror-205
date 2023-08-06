from setuptools import setup, find_packages

setup(
    name="yolov7tools",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "fiftyone",
        "tqdm",
        "joblib",
    ],
    entry_points={
        "console_scripts": [
            "fiftyone-dataset=yolov7tools.bin.launch_fiftyone:main",
            "cvat-dataset=yolov7tools.bin.launch_cvat:main",
        ],
    }
)
