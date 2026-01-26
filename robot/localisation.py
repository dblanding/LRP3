import json
import numpy as np
import time

from common import arena
from common.mqtt_behavior import connect, publish_json
from common.poses import Poses

population_size = 200

class Localisation:
    def __init__(self):
        self.poses = Poses.generate(population_size, (arena.left, arena.right),
                                    (arena.bottom, arena.top), (0, 2 * np.pi))
        self.wheel_distance = 159
        self.previous_left_distance = 0
        self.previous_right_distance = 0

    def convert_encoders_to_motion(self, left_distance_delta, right_distance_delta):
        # Special case, straight line
        if left_distance_delta == right_distance_delta:
            return left_distance_delta, 0

        mid_distance = (left_distance_delta + right_distance_delta) / 2
        theta = (right_distance_delta - left_distance_delta) / self.wheel_distance

        return mid_distance, theta

    def on_encoders_data(self, client, userdata, msg):
        # Sense
        distance_data = json.loads(msg.payload)
        left_distance_delta = (distance_data['left_distance'] -
                               self.previous_left_distance)
        right_distance_delta = (distance_data['right_distance'] -
                                self.previous_right_distance)
        self.previous_left_distance = distance_data['left_distance']
        self.previous_right_distance = distance_data['right_distance']

        # Think
        translation, theta = self.convert_encoders_to_motion(
            left_distance_delta, right_distance_delta)
        rotation = theta / 2
        self.poses = self.poses.move(rotation, translation)

        # Act
        self.publish_poses(client, self.poses)

    def publish_poses(self, client, poses):
        publish_json(client, "localisation/poses", poses.tolist())
    
    def start(self):
        client = connect()
        arena.publish_map(client)
        client.subscribe("sensors/encoders/data")
        client.publish("sensors/encoders/control/reset")
        client.message_callback_add("sensors/encoders/data",
                                    self.on_encoders_data)
        while True:
            time.sleep(0.1)


service = Localisation()
service.start()
