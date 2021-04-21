

from cv2 import cv2  # opencv is alway imported since other logic still depend on it.
import numpy as np

use_onnxruntime = False
try:
    import onnxruntime as ort
    print(f"Use onnxruntime backend: {ort.get_device()}, Available Providers: {ort.get_available_providers()}")
    use_onnxruntime = True
except:
    print("onnxruntime is not detected, use fallback OpenCV backend. Try `pip install onnxruntime` or `pip install onnxruntime-gpu` according to hardware specification.")


class ONNXModel:
    def __init__(self, path):
        raise NotImplementedError

    def __call__(self):
        raise NotImplementedError


class ONNXModelOpenCV(ONNXModel):
    def __init__(self, path):
        self.model = cv2.dnn.readNetFromONNX(path)
        self.out_names = self.model.getUnconnectedOutLayersNames()
    
    def __call__(self, input):
        self.model.setInput(input)
        out = self.model.forward(self.out_names)
        return out


class ONNXModelONNXRuntime(ONNXModel):
    def __init__(self, path):
        self.session = ort.InferenceSession(path)
        assert len(self.session.get_inputs()) == 1  # support only one input argument
        self.input_name = self.session.get_inputs()[0].name

    def __call__(self, input):
        if input.dtype == np.float32:
            pass
        elif input.dtype == np.float64:
            input = input.astype(np.float32)
        else:
            raise ValueError(f"Unexpected input type {input.dtype}")
        
        return self.session.run(None, {self.input_name: input})


def load_model(path, cls=None):
    if cls is None:
        cls =  ONNXModelONNXRuntime if use_onnxruntime else ONNXModelOpenCV
    return cls(path)
