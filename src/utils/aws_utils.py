import boto3
from config.config import S3Settings

class S3Utils:
    def __init__(self):
        self.s3_resource = boto3.resource('s3', aws_access_key_id=S3Settings().ACCESS_KEY,
    aws_secret_access_key=S3Settings().SECRET_KEY)
        self.s3_client = boto3.client('s3', aws_access_key_id=S3Settings().ACCESS_KEY,
    aws_secret_access_key=S3Settings().SECRET_KEY)
        self.bucket = S3Settings().bucket_name

    def upload_file_obj(self,folder_name, emp_name, image_string):
        file_path = f'{folder_name}/{emp_name.lower()}.jpg'
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=file_path,
            Body=image_string
        )

    def delete_uploaded_object(self, folder_name, deleted_folder_name, emp_name):
        file_path = f'{folder_name}/{emp_name}.jpg'
        new_file_path = f'{deleted_folder_name}/{emp_name}.jpg'
        copy_source = {'Bucket': self.bucket, 'Key': file_path}
        self.s3_client.copy_object(CopySource=copy_source, Bucket=self.bucket, Key=new_file_path)
        self.s3_client.delete_object(Bucket=self.bucket, Key=file_path)
