import cv2
import random
import distance


class FaceDetect:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def __init__(self):
        self.rec = []
        self.x_points = []
        self.colors = []
        self.rand_color()

    def run(self, file_name=None):

        if file_name is None:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(file_name)

        font = cv2.FONT_HERSHEY_TRIPLEX
        cnt = 0
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        while len(faces) == 0:
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        marker = faces[0]
        known_dis = distance.find_first_distance(marker)
        focal_length = (marker[2] * known_dis) / distance.KNOWN_WIDTH
        print("known_dis:", known_dis, marker)

        while True:
            _, img = cap.read()
            cnt += 1
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            faces = sorted(faces, key=lambda tup: tup[0])
            i = 1
            for (x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), self.colors[i-1], 4)
                cv2.putText(img, str(i), (int(x), y), font, 1, (0, 0, 255), 2)
                dis = distance.distance_to_camera(focal_length, w)
                print(dis)
                i += 1
                color = (0, 0, 255)
                cv2.rectangle(img, (10, 400), (620, 450), color, 4)
                cv2.rectangle(img, (9+i, 401), (9+i + (60*(i-1)), 449), color, -1)

            if len(faces) > 10:
                cv2.putText(img, 'WARNING! The police is coming...', (10, 50), font, 1, (0, 0, 255), 2)

            img = self.draw_dis(img, faces)
            cv2.imshow('img', img)

            # Stop if escape key is pressed
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        # Release the VideoCapture object
        cap.release()

    def rand_color(self):
        for i in range(12):
            a = random.randint(0, 255)
            b = random.randint(0, 255)
            c = random.randint(0, 255)
            self.colors.append((a, b, c))

    @staticmethod
    def draw_dis(img, faces):
        for i in range(len(faces) - 1):
            x = faces[i][0]
            y = faces[i][1]
            w = faces[i][2]
            h = faces[i][3]
            dis = faces[i+1][0] - (x + h)
            cv2.line(img, (x + w, int(y + h/2)), (x + w + dis, int(y + h/2)), (0, 255, 0), 2)
        return img

