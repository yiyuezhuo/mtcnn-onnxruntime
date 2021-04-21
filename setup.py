import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="mtcnn-onnxruntime",
    version="0.0.1",
    author="linxiaohui, yiyuezhuo",
    author_email="yiyuezhuo@gmail.com",
    install_requires=[
        "opencv-python",
        # "onnxruntime", # "Default" backend is still using opencv, since "onnxruntime" or `onnxruntime-gpu` can be chosen according to the hardware specification. 
    ],
    extras_require = { # `pip install mtcnn-onnxruntime[cpu]` or `pip install mtcnn-onnxruntime[gpu]``
        'cpu': [
            'onnxruntime'
        ],
        'gpu':[
            'onnxruntime-gpu'
        ]
    },
    description="MTCNN face detection using onnx runtime or OpenCV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yiyuezhuo/mtcnn-onnxruntime",
    packages=setuptools.find_packages(),
    package_data={
        'mtcnn_ort': ['pnet.onnx', 'rnet.onnx', 'onet.onnx']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires='>=3.6',
)
