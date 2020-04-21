import math

KNOWN_WIDTH = 19
BASIC_DISTANCE = 45
BASIC_PIXEL = 153


def find_first_distance(face):
    rat = BASIC_PIXEL * BASIC_DISTANCE
    dis = rat / face[2]
    return dis


def distance_to_camera(focal_length, per_width):
    # compute and return the distance from the maker to the camera
    return (KNOWN_WIDTH * focal_length) / per_width


def angle(vector1, vector2):
    length1 = math.sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
    length2 = math.sqrt(vector2[0] * vector2[0] + vector2[1] * vector2[1])
    return math.acos((vector1[0] * vector2[0] + vector1[1] * vector2[1])/ (length1 * length2))


def find_vectors(pnt1, pnt2, dis1, dis2, screen):
    print("pnt1", pnt1)
    print("pnt2", pnt2)
    centerX = screen[0]
    centerY = screen[1]
    print("center", centerX, centerY)
    y1 = math.sqrt(cm_to_pixel(dis1) ** 2 - (pnt1[0] - centerX) ** 2)
    y2 = math.sqrt(cm_to_pixel(dis2) ** 2 - (pnt2[0] - centerX) ** 2)
    vector1 = [pnt1[0] - centerX, y1]
    vector2 = [pnt2[0] - centerX, y2]
    print("v1", vector1)
    print("v2", vector2)
    return angle(vector1, vector2)


def distance_between_obj(pnt1, pnt2, dis1, dis2, screen):
    mid_screen = (screen[0] / 2, screen[1] / 2)
    angle = find_vectors(pnt1, pnt2, dis1, dis2, mid_screen)
    print("ang", angle)
    print("cos", math.cos(angle))
    dis3 = math.sqrt(dis1 ** 2 + dis2 ** 2 - 2 * dis1 * dis2 * math.cos(angle))
    print("dis", dis3)
    return dis3

def cm_to_pixel(dis):
    rat = BASIC_PIXEL / KNOWN_WIDTH
    return dis * rat
