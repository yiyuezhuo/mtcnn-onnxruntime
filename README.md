# MTCNN-onnx-runtime

Adapted from [linxiaohui/mtcnn-opencv](https://github.com/linxiaohui/mtcnn-opencv).  Modifications include uses of onnx runtime as inference backend and provide a raw output API. Maybe this package should be a fork but I have already had a [forked version](https://github.com/yiyuezhuo/mtcnn-opencv) to address [another problem](https://github.com/linxiaohui/mtcnn-opencv), so I made a new package.

MTCNN Face Detector using ONNX-runtime OpenCV, no reqiurement for tensorflow/pytorch.

## INSTALLATION
Select one method from below:

   * `pip install mtcnn-onnxruntime`: Use existing onnxruntime version in environment to run, if no onnxruntime is in the environment, `opencv` will be used as backend.
   * `pip install mtcnn-onnxruntime[cpu]`: Install `mtcnn-onnxruntime` with `onnxruntime`
   * `pip install mtcnn-onnxruntime[gpu]`: Install `mtcnn-onnxruntime` with `onnxruntime-gpu`

## USAGE
```python

import cv2
from mtcnn_ort import MTCNN

detector = MTCNN()
test_pic = "t.jpg"

image = cv2.cvtColor(cv2.imread(test_pic), cv2.COLOR_BGR2RGB)
result = detector.detect_faces(image)

# Result is an array with all the bounding boxes detected. Show the first.
print(result)
"""
[{'box': [60, 0, 314, 356],
  'confidence': 0.9993509650230408,
  'keypoints': {'left_eye': (136, 71),
   'right_eye': (289, 58),
   'nose': (218, 148),
   'mouth_left': (162, 243),
   'mouth_right': (290, 228)}}]
"""

detector.detect_faces_raw(image)
"""
(array([[ 60.58798278, -66.81823712, 374.15868253, 356.04121107,
           0.99935097]]),
 array([[136.35648 ],
        [289.0994  ],
        [218.10023 ],
        [162.28156 ],
        [290.98242 ],
        [ 71.76702 ],
        [ 58.487453],
        [148.75732 ],
        [243.27672 ],
        [228.3274  ]], dtype=float32))
"""

```

Illustration:

```python

import cv2

if len(result) > 0:
    bounding_box = result[0]["box"]
    keypoints = result[0]['keypoints']
    
    cv2.rectangle(image,
                  (bounding_box[0], bounding_box[1]),
                  (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                  (0,155,255),
                  2)
    
    cv2.circle(image,(keypoints['left_eye']), 2, (0,155,255), 2)
    cv2.circle(image,(keypoints['right_eye']), 2, (0,155,255), 2)
    cv2.circle(image,(keypoints['nose']), 2, (0,155,255), 2)
    cv2.circle(image,(keypoints['mouth_left']), 2, (0,155,255), 2)
    cv2.circle(image,(keypoints['mouth_right']), 2, (0,155,255), 2)
    
    cv2.imwrite("result.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

# Generate labeled images
with open(test_pic, "rb") as fp:
    marked_data = detector.mark_faces(fp.read())
with open("marked.jpg", "wb") as fp:
    fp.write(marked_data)

```

Warped patch (then face recognition SOTA [ArcFace](https://github.com/deepinsight/insightface)) can consume it (otherwise, if one just use bounding box, what some models such as UltraNet can only make, the performance will significantly compromised.).

```python

from skimage import transform as trans
import numpy as np

image = cv2.cvtColor(cv2.imread(test_pic), cv2.COLOR_BGR2RGB)

src = np.array([
            [30.2946, 51.6963],
            [65.5318, 51.5014],
            [48.0252, 71.7366],
            [33.5493, 92.3655],
            [62.7299, 92.2041]], dtype=np.float32)
src[:, 0] += 8.0

landmark5 = detector.detect_faces_raw(image)[1].reshape(2, 5).T
tform = trans.SimilarityTransform()
tform.estimate(landmark5, src)
M = tform.params[0:2, :]
img = cv2.warpAffine(image, M, (112, 112),
                        borderValue=0.0)
cv2.imwrite("warped.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

```