from deploy import virtual_env
from pyinfra.operations import apt, pip, server

apt.packages(
    name = "pulseaudio",
    packages = ["pulseaudio"],
    _sudo = True
)

piper = pip.packages(
    name="Install piper TTS Python packages",
    packages=[
        "piper-tts",
        "sounddevice",
    ],
    virtualenv=virtual_env.robot_venv,
    extra_install_args="--no-cache-dir -vvv",
)

if piper.changed:
    server.shell("robotpython -m piper.download_voices en_US-ryan-low")
