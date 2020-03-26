KNOWN_WIDTH = 19

BASIC_DISTANCE = 55
BASIC_PIXEL = 153


def find_first_distance(face):
    rat = BASIC_PIXEL * BASIC_DISTANCE
    dis = rat / face[2]
    return dis


def distance_to_camera(focal_length, per_width):
    # compute and return the distance from the maker to the camera
    return (KNOWN_WIDTH * focal_length) / per_width


