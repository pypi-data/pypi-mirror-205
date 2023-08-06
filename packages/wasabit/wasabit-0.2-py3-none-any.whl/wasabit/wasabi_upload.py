# import json
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import NoCredentialsError, ClientError
from wasabit.wasabi_auth import wasabi_auth
import os
from botocore.exceptions import NoCredentialsError

import os
from pathlib import Path
from typing import Optional
import boto3



def upload_to_wasabi(folder_path: str, bucket_name: str, wasabi_path: str, access_key = None, secret_key = None) -> None:
    """
    Uploads all files present in a specific folder to a specified Wasabi bucket and subfolder or prefix.
    :param folder_path: The path of the folder containing the files to be uploaded.
    :param bucket_name: The name of the Wasabi bucket where the files will be uploaded.
    :param wasabi_path: The prefix or subfolder within the bucket where the files will be uploaded.
    :param access_key: The Wasabi access key.
    :param secret_key: The Wasabi secret key.
    """
    transfer_config = TransferConfig(
    multipart_threshold=1024 * 25,  # 25MB
    max_concurrency=10,
    num_download_attempts=10,
)
    try:
        # create an S3 client
        s3 = wasabi_auth(access_key,secret_key)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                remote_file = file_path.split('/')[-1]
                remote_file = wasabi_path + remote_file
                # upload the file
                s3.upload_file(file_path, bucket_name,remote_file,Config=transfer_config)
                print(f'{file_path} is uploaded to {remote_file}')
    except NoCredentialsError as e:
        print("Credentials not found, please check your access key and secret key.")
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidAccessKeyId":
            print("Invalid access key, please check your access key.")
        elif e.response['Error']['Code'] == "SignatureDoesNotMatch":
            print("Invalid secret key, please check your secret key.")
        else:
            print(f'An error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

        

def file_upload_to_wasabi(csv_file_path: str, bucket_name: str, wasabi_path: str, access_key, secret_key) -> None:
    """
    Uploads a specific CSV file to a specified Wasabi bucket and subfolder or prefix.
    :param csv_file_path: The full path of the CSV file to be uploaded.
    :param bucket_name: The name of the Wasabi bucket where the file will be uploaded.
    :param wasabi_path: The prefix or subfolder within the bucket where the file will be uploaded.
    :param access_key: The Wasabi access key.
    :param secret_key: The Wasabi secret key.
    """
    transfer_config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        num_download_attempts=10,
    )
    try:
        # create an S3 client
        s3 = wasabi_auth(access_key,secret_key)
        # get the file name from the full path
        file_name = os.path.basename(csv_file_path)
        remote_file = wasabi_path + file_name
        # upload the file
        s3.upload_file(csv_file_path, bucket_name, remote_file, Config=transfer_config)
        print(f'{csv_file_path} is uploaded to {remote_file}')
    except NoCredentialsError as e:
        print("Credentials not found, please check your access key and secret key.")
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidAccessKeyId":
            print("Invalid access key, please check your access key.")
        elif e.response['Error']['Code'] == "SignatureDoesNotMatch":
            print("Invalid secret key, please check your secret key.")
        else:
            print(f'An error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')


def upload_folder_to_wasabi(local_folder_path: str, bucket_name: str, wasabi_path: str, access_key: str, secret_key: str) -> None:
    """
    Recursively uploads all files present in a specific folder to a specified Wasabi bucket and subfolder or prefix.
    :param local_folder_path: The path of the local folder containing the files to be uploaded.
    :param bucket_name: The name of the Wasabi bucket where the files will be uploaded.
    :param wasabi_path: The prefix or subfolder within the bucket where the files will be uploaded. Optional.
    :param access_key: The Wasabi access key.
    :param secret_key: The Wasabi secret key.
    """
    transfer_config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        num_download_attempts=10,
    )
    try:
        # create an S3 client
        s3 = boto3.client('s3',
                          endpoint_url='https://s3.ap-southeast-1.wasabisys.com',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)

        # convert folder path to platform-independent path
        local_folder_path = Path(local_folder_path).resolve()
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                # get local file path and remote file path
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_folder_path)
                remote_file_path = os.path.join(wasabi_path, relative_path).replace(os.sep, '/')
                
                # upload the file
                s3.upload_file(local_file_path, bucket_name, remote_file_path, Config=transfer_config)
                print(f'{local_file_path} is uploaded to {remote_file_path}')
    except NoCredentialsError as e:
        print("Credentials not found, please check your access key and secret key.")
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidAccessKeyId":
            print("Invalid access key, please check your access key.")
        elif e.response['Error']['Code'] == "SignatureDoesNotMatch":
            print("Invalid secret key, please check your secret key.")
        else:
            print(f'An error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
