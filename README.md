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
from mtcnn_cv2 import MTCNN

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
