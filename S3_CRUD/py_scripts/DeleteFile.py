# -*- coding: utf-8 -*-

"""
command line parameters:
user-name password file-key

For example:

python DeleteFile.py MrCat NiceCat Bird01
where MrCat is a user-name and NiceCat is the password from a previous running of the CreateUser.py script
"""


import boto3
import sys
from UploadFile import authenticateUser
from CreateUser import isBucketCreated
from CreateUser import isFilekeyCreated



BUCKET_USERLOGIN = "chw-user-login-02152020"
BUCKET_USERDATA = "chw-user-data-02152020"
REGION = 'us-west-1'

def deleteFiles(s3,bucket, key):
    """
    :param bucket: String
    :param prefix: String
    :param region: String
    """
    oBucket = s3.Bucket(bucket)
    oBucket.delete_objects(Delete={'Objects': [{'Key': key}]})



def main():

    if len(sys.argv) < 4:
        print("Usage: Three arguments: user-name, password and file-key, are required.")
        return

    userName, psw, fileName = sys.argv[1], sys.argv[2], sys.argv[3]
    s3 = boto3.resource('s3', region_name=REGION)

    # errors handling
    if not isBucketCreated(BUCKET_USERLOGIN, REGION):  # if the Bucket for login files doesn't exist.
        print(f'Bucket {BUCKET_USERLOGIN} does not exist. '
              f'Please check the bucket name or run CreateUser.py to create a new user.')
        return
    # check if the bucket exists
    if not isBucketCreated(BUCKET_USERDATA, REGION):
        print(f'Bucket {BUCKET_USERDATA} does not exist. ')
        return

    if not authenticateUser(s3, userName, psw, BUCKET_USERLOGIN, REGION):
        print(f'Invalid user-name or password.')
        return

    # check if the file exists
    fileToDelete = userName + "/" + fileName
    if not isFilekeyCreated(BUCKET_USERDATA, fileToDelete, REGION):
        print(f'Invalid file-key.')
        return

    # delete it
    deleteFiles(s3,BUCKET_USERDATA,fileToDelete)
    print(f'{fileName} is deleted.')




if __name__ == '__main__':
    main()