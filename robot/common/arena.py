from common.mqtt_behavior import publish_json

width = 2100
height = 1800
cutout = 760
# define the dimensions used by the book so final example will work
cutout_left = width - cutout
cutout_top = cutout

walls = [
    (0, height),
    (width, height),
    (width, cutout),
    (width - cutout, cutout),
    (width - cutout, 0),
    (0, 0)
]

def publish_map(client):
    publish_json(client, "localisation/map", {
        "walls": walls
    })
