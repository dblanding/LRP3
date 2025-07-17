# This script needs to reside here so it can find & import common.
# It was used for debugging and is no longer needed.

import time

from common.mqtt_behavior import connect, publish_json

client = connect()
publish_json(client, "wheel_control/enabled", True)
publish_json(client, "wheel_control/wheel_speed_mm", [100, 100])

time.sleep(1)

publish_json(client, "wheel_control/wheel_speed_mm", [0, 0])
publish_json(client, "wheel_control/enabled", False)
publish_json(client, "all/stop", "")
