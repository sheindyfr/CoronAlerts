import math

# basic sizes of the factors
# this sizes I got from average of a few trials
KNOWN_WIDTH = 19
BASIC_DISTANCE = 45
BASIC_PIXEL = 153

'''
find the first distance from face to camera
according to a ratio between the basic sizes
'''
def find_first_distance(face):
    rat = BASIC_PIXEL * BASIC_DISTANCE
    dis = rat / face[2]
    return dis

'''
find the distance from face to camera
according to the focal length and the face width
'''
def distance_to_camera(focal_length, face_width):
    # compute and return the distance from the maker to the camera
    return (KNOWN_WIDTH * focal_length) / face_width

'''
find the vectors of the distances between the people and the camera
the vectors x coordinate is the x coordinate of the face
the vectors y coordinate is the vertical distance between the face to the camera
'''
def find_vectors(pnt1, pnt2, dis1, dis2, screen):
    centerX = screen[0]
    # find the y coordinates of the vectors by Pythagorean theorem
    y1 = math.sqrt(abs(cm_to_pixel(dis1) ** 2 - (pnt1[0] - centerX) ** 2))
    y2 = math.sqrt(abs(cm_to_pixel(dis2) ** 2 - (pnt2[0] - centerX) ** 2))
    # build the vectors
    vector1 = [pnt1[0] - centerX, y1]
    vector2 = [pnt2[0] - centerX, y2]
    # calc the angle between the vectors
    return angle(vector1, vector2)

'''
find the angle between 2 vectors with Scalar multiplication
'''
def angle(vector1, vector2):
    length1 = math.sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
    length2 = math.sqrt(vector2[0] * vector2[0] + vector2[1] * vector2[1])
    return math.acos((vector1[0] * vector2[0] + vector1[1] * vector2[1])/ (length1 * length2))

'''
find the distance between two faces by find the vectors, 
find the angle and the Law of cosines.
'''
def distance_between_obj(pnt1, pnt2, dis1, dis2, screen):
    # find the mid point of the screen
    mid_screen = (screen[0] / 2, screen[1] / 2)
    # find the angle by the vectors
    angle = find_vectors(pnt1, pnt2, dis1, dis2, mid_screen)
    # use the Law of cosines to find the distance
    dis3 = math.sqrt(abs(dis1 ** 2 + dis2 ** 2 - 2 * dis1 * dis2 * math.cos(angle)))
    return dis3

'''
convert from cm to pixel (all the sizes need to use the same units)
'''
def cm_to_pixel(dis):
    rat = BASIC_PIXEL / KNOWN_WIDTH
    return dis * rat
