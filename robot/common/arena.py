from common.mqtt_behavior import publish_json

width = 2100
height = 1800
cutout = 760

# The dimensions in this section are defined so other code will work
left = 0
bottom = 0
right = width
top = height
cutout_left = width - cutout
cutout_top = cutout
# end of dimensions section

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
