import cv2
import distance


class FaceDetect:

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_TRIPLEX

    # init the variables
    def __init__(self):
        self.rec = []
        self.x_points = []
        self.colors = []

    def run(self, file_name=0):

        # start capture the video
        cap = cv2.VideoCapture(file_name)

        # read frame from the video
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # get the detected faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        while len(faces) == 0:
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        # in this 3 lines I receive the basic sizes of: distance, focal_length
        # this sizes are the markers of all the faces.
        # I get the Known distance of this face after calculate according to basic known about faces size
        # then I find the focal length
        marker = faces[0]
        known_dis = distance.find_first_distance(marker)
        focal_length = (marker[2] * known_dis) / distance.KNOWN_WIDTH


        while True:
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            # sort the faces by x coordinate
            faces = sorted(faces, key=lambda tup: tup[0])
            i = 1   # i --> the current face

            # pass on the faces
            for (x, y, w, h) in faces:

                # draw rectangle around the face, and write the number
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, str(i), (int(x), y), self.font, 0.5, (255, 0, 0), 0)
                i += 1

            # if there is a crowded --> alert
            if len(faces) > 10:
                cv2.putText(img, 'WARNING! More than 10 people', (10, 50), self.font, 0.8, (0, 0, 255), 2)

            # calc the distance between 2 people, and draw this distance
            img = self.calc_dis(img, faces, focal_length)
            # show the image
            cv2.imshow('img', img)

            # Stop if escape key is pressed
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        # Release the VideoCapture object
        cap.release()


    '''
    the function get the img, the faces and the focal length in order to calculate 
    the distance between 2 people
    return: the update image with the lines of distance
    '''
    def calc_dis(self, img, faces, focal_length):

        # pass on the faces
        for i in range(len(faces) - 1):
            x = faces[i][0]
            y = faces[i][1]
            w = faces[i][2]
            h = faces[i][3]

            # the horizontal distance between 2 people
            dis0 = faces[i+1][0] - (x + h)

            height, width = img.shape[:2] # the screen sizes

            # calc distance from camera to the 2 near faces
            dis1 = distance.distance_to_camera(focal_length, faces[i][2])
            dis2 = distance.distance_to_camera(focal_length, faces[i + 1][2])
            # calc the distance between the faces
            dis3 = distance.distance_between_obj(faces[i], faces[i + 1], dis1, dis2, (height, width))

            # if the distance is less than 2 meter --> alert
            if dis3 < 200:
                cv2.putText(img, 'WARNING! Keep 2 meters...', (10, 50), self.font, 0.8, (0, 0, 255), 2)

            # draw the line of distance and write the distance above the line
            cv2.line(img, (x + w, int(y + h/2)), (x + w + dis0, int(faces[i+1][1] + h/2)), (0, 255, 0), 2)
            cv2.putText(img, str(round((dis3 / 100), 2)) + "m", (int(x + w + dis0/2), int(y + h/2)), self.font, 0.5, (0, 0, 255), 2)
        return img
