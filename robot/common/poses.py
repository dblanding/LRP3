import numpy as np

class Poses(np.ndarray):
    Pose = np.dtype([('x', np.float32), ('y', np.float32), ('theta', np.float32)])

    def __new__(cls, input_array):
        return np.asarray(input_array, dtype=cls.Pose).view(cls)
