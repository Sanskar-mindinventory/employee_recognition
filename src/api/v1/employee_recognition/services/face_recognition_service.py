from email.mime import image
from re import S
import cv2
import numpy
import pandas as pd
import face_recognition
from config.config import PathSettings
from src.utils.aws_utils import S3Utils

class RecogEmployee:

    def __init__(self):
        self.folder_name = PathSettings().train_folder_path
        self.deleted_folder = PathSettings().delete_folder_path
        self.face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        try:
           self.faces_dict = self.create_face_encoding_dict(pd.read_csv('faces_dict.csv').drop(['Unnamed: 0'], axis=1))
        except Exception as e:
            self.faces_dict = {}

    def create_face_encoding_dict(self,dataframe):
        employee_cols  = dataframe.columns
        return {employee_name: dataframe[employee_name].to_numpy() for employee_name in employee_cols}
 
    def batch_record_faces(self, files):
        for file in files:
            emp_name = file.filename.split(".")[0].lower()
            file_body = file.file.read()
            original_img = cv2.imdecode(numpy.fromstring(file_body, numpy.uint8), cv2.IMREAD_UNCHANGED)
            S3Utils().upload_file_obj(folder_name=self.folder_name,emp_name=emp_name, image_string=file_body)
            self.create_face_encoding_from_the_image(image=original_img,employee_name=emp_name)
        self.create_csv()
        return self.faces_dict
    
    def single_record_faces(self, file, empName):
        file_body = file.file.read()
        original_img = cv2.imdecode(numpy.fromstring(file_body, numpy.uint8), cv2.IMREAD_UNCHANGED)
        S3Utils().upload_file_obj(folder_name=self.folder_name,emp_name=empName, image_string=file_body)
        self.create_face_encoding_from_the_image(image=original_img,employee_name=empName)
        self.create_csv()
        return self.faces_dict.keys()
                
    def create_face_encoding_from_the_image(self, image, employee_name):
        trainImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.faces_dict[employee_name] = face_recognition.face_encodings(trainImg)[0]

    def create_csv(self):
        df = pd.DataFrame(self.faces_dict)
        df.to_csv("faces_dict.csv")    

    def delete_employee(self, employee_name):
        deleted_employee = self.faces_dict.pop(employee_name)
        self.create_csv()
        S3Utils().delete_uploaded_object(emp_name= employee_name, folder_name=self.folder_name, deleted_folder_name=self.deleted_folder)
        return deleted_employee