import json
import boto3

class S3Utils:
    def __init__(self):
        s3_secret = SecretManagerUtils.get_secret(secret_name='employee-recognition-s3-secrets',region_name='us-east-2')
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        self.bucket = s3_secret.get('bucket_name')

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


class SecretManagerUtils:
    def get_secret(secret_name, region_name):
        secret_client = boto3.client(service_name='secretsmanager', region_name=region_name)
        get_secret_value_response = secret_client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(get_secret_value_response.get('SecretString'))