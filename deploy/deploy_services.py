from pyinfra.operations import files, systemd
from pyinfra import host
import os


def deploy_service(service_name, command, auto_start, changed):
    if auto_start:
        restart = "always"
    else:
        restart = "no"

    unit_file = files.template(
        name=f"Create {service_name} service",
        src="deploy/service_template.j2",
        dest=f"/etc/systemd/system/{service_name}.service",
        pi_user=host.data.get('ssh_user'),
        service_name=service_name,
        command=command,
        restart=restart,
        _sudo=True
    )

    if changed or code.changed or unit_file.changed:
        systemd.service(
            name=f"Restart {service_name} service",
            service=service_name,
            running=auto_start,
            enabled=auto_start,
            restarted=auto_start,
            daemon_reload=unit_file.changed,
            _sudo=True,
        )


common = files.sync(
    name="Update common code",
    src="robot/common", dest="robot/common")

code = files.put(
    name="Update inventor hat code",
    src="robot/inventor_hat_service.py", dest="robot/inventor_hat_service.py")

deploy_service("inventor_hat_service", "robot/inventor_hat_service.py",
               True, common.changed or code.changed)

code = files.put(
    name="Update wheel control code",
    src="robot/wheel_control_service.py",
    dest="robot/wheel_control_service.py")
deploy_service("wheel_control_service", "robot/wheel_control_service.py",
               True, common.changed or code.changed)

code = files.put(
    name="Update launcher code",
    src="robot/launcher_service.py",
    dest="robot/launcher_service.py")
deploy_service("launcher_service", "robot/launcher_service.py",
               True, common.changed or code.changed)

code = files.put(
    name="Update config store code",
    src="robot/config_store.py",
    dest="robot/config_store.py")
deploy_service("config_store", "robot/config_store.py",
               True, common.changed or code.changed)

code = files.put(
    name="Update behavior_path code",
    src="robot/behavior_path.py",
    dest="robot/behavior_path.py")
deploy_service("behavior_path", "robot/behavior_path.py",
               False, common.changed or code.changed)

code = files.put(
    name="Update drive_known_distance code",
    src="robot/drive_known_distance.py",
    dest="robot/drive_known_distance.py")
deploy_service("drive_known_distance", "robot/drive_known_distance.py",
               False, common.changed or code.changed)

code = files.put(
    name="Update circle_head code",
    src="robot/circle_head_behavior.py",
    dest="robot/circle_head_behavior.py")
deploy_service("circle_head", "robot/circle_head_behavior.py",
               False, common.changed or code.changed)

code = files.put(
    name="Update distance sensor service",
    src="robot/distance_sensor_service.py",
    dest="robot/distance_sensor_service.py")
deploy_service("distance_sensor_service",
               "robot/distance_sensor_service.py",
               True, common.changed or code.changed)

code = files.put(
    name="Update IMU service",
    src="robot/imu_service.py",
    dest="robot/imu_service.py")
deploy_service("imu_service", "robot/imu_service.py",
                False, common.changed or code.changed)

code = files.put(
    name="Update face direction code",
    src="robot/face_direction.py",
    dest="robot/face_direction.py")
deploy_service("face_direction", "robot/face_direction.py",
                False, common.changed or code.changed)

code = files.put(
    name="Update fixed distance avoider",
    src="robot/fixed_distance_avoider.py",
    dest="robot/fixed_distance_avoider.py")
deploy_service("fixed_distance_avoider",
               "robot/fixed_distance_avoider.py",
               False, common.changed or code.changed)

code = files.put(
    name="Update smooth distance avoider",
    src="robot/smooth_distance_avoider.py",
    dest="robot/smooth_distance_avoider.py")
deploy_service("smooth_distance_avoider",
               "robot/smooth_distance_avoider.py",
               False, common.changed or code.changed)

code = files.put(
    name="Update localisation",
    src="robot/localisation.py",
    dest="robot/localisation.py")
deploy_service("localisation",
               "robot/localisation.py",
               False, common.changed or code.changed)

code = files.put(
    name="Update camera view code",
    src="robot/camera_view.py",
    dest="robot/camera_view.py")
deploy_service("camera_view", "robot/camera_view.py",
                False, common.changed or code.changed)

code = files.put(
    name="Update face detector code",
    src="robot/face_detector.py",
    dest="robot/face_detector.py")
deploy_service("face_detector", "robot/face_detector.py",
                False, common.changed or code.changed)

files.directory(
    name="Create robot_control/libs",
    path="robot_control/libs"
)
files.download(
    name="Download joystick widget",
    src="https://github.com/bobboteck/JoyStick/raw/master/joy.js",
    dest="robot_control/libs/joy.js"
)
files.download(
    name="Download mqtt js",
    src="https://unpkg.com/mqtt@5.7.0/dist/mqtt.esm.js",
    dest="robot_control/libs/mqtt.js"
)
files.download(
    name="Download chart js",
    src="https://cdn.jsdelivr.net/npm/chart.js",
    dest="robot_control/libs/chart.js"
)
files.download(
    name="Download chartjs datalabels plugin",
    src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2",
    dest="robot_control/libs/chartjs-plugin-datalabels"
) # https://v2_2_0--chartjs-plugin-datalabels.netlify.app/guide/

# Loop over all the files in the robot_control directory
pages_folder = files.directory(
    name="Create robot_control folder",
    path="robot_control"
)
pages = [
    files.template(
        name=f"Deploy {file_name}",
        src=f"robot_control/{file_name}",
        dest=f"robot_control/{file_name}",
    )
    for file_name in os.listdir("robot_control")
]

pages_changed = pages_folder.changed or any(page.changed for page in pages)

deploy_service("web_server", "-m http.server --directory robot_control 80",
               True, pages_changed)
