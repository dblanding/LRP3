from deploy import virtual_env
from pyinfra.operations import apt, files, pip

apt.packages(
    name="Install AI packages",
    packages=["python3-picamera2", "python3-opencv", "opencv-data",
              "python3-flask"],
    no_recommends=True,
    _sudo=True,
)

pip.packages(
    name="Install OpenCV contrib",
    packages=["opencv-contrib-python"],
    virtualenv=virtual_env.robot_venv,
    )

files.download(
    name="Download Face detection model",
    src="https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_detection_yunet/face_detection_yunet_2023mar_int8.onnx",
    dest="face_detection_yunet_2023mar_int8.onnx"
)
