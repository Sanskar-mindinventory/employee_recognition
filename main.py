import time
import cv2
import pandas as pd
import face_recognition
from src.utils.custom_exception import NoFaceDetectedException, NoFaceMatchedException

class RecognizeEmployee:

    def __init__(self):
        self.face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.faces_dict = self.create_face_encoding_dict(pd.read_csv('faces_dict.csv').drop(['Unnamed: 0'], axis=1))

    def create_face_encoding_dict(self,dataframe):
        employee_cols  = dataframe.columns
        return {employee_name: dataframe[employee_name].to_numpy() for employee_name in employee_cols}

    def capImage(self, frame):
        """"
        Capture image if face detected
        """
        face = self.face_classifier.detectMultiScale(
            frame, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        if len(face)>0:
            return frame, True
        raise NoFaceDetectedException("There is no face detected")


    def getName(self, frame):
        encoded_face_list = face_recognition.face_encodings(frame)
        if encoded_face_list:
            imgEncodingFrame = encoded_face_list[0]
            for name, encoding in self.faces_dict.items():
                faceComparison = face_recognition.compare_faces([encoding], imgEncodingFrame, tolerance=0.42)
                if len(faceComparison)>0 and faceComparison[0] == True:
                    return name
        raise NoFaceMatchedException("There is no macthing for this face.")    
        
    def face_detection(self, camUrl=0):
        try:
            vid = cv2.VideoCapture(index=camUrl)
            while vid.isOpened():
                ret, frame = vid.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face, ret = self.capImage(frame=frame)
                value = self.getName(frame=frame)
                if value is not None:
                    break
                return (value)
        except NoFaceDetectedException as error:
            print(error)
            self.face_detection()
        except NoFaceMatchedException as face_error:
            print(face_error)    
            self.face_detection()
        finally:
            vid.release()


# for i in 



recogemp = RecognizeEmployee()

if __name__=="__main__":
    start = time.time()
    val = recogemp.face_detection()
    end = time.time()
    total_time = end-start
    print(total_time)
    print(val)