# -*- coding: utf-8 -*-

"""
command line arguments:
user-name password file-key path-to-file-to-upload

user-name = the user-name from CreateUser.py
password = the user's password from CreateUser
file-key = is a tag/string that the user can associate with an uploaded file
path-to-file-to-upload = the path to a file on your machine to save in S3
"""
import boto3
import sys
import os
import CreateUser

BUCKET_USERLOGIN = "chw-user-login-02152020"
BUCKET_USERDATA = "chw-user-data-02152020"
REGION = 'us-west-1'

def authenticateUser(s3, userName:str, pswToCheck:str, bucketName:str, region:str) -> bool:

    try:
        pswAndEmail = CreateUser.readDataFromObject(s3, bucketName, userName, region)
    except Exception as err:
        print(err)
        return False
    if not pswAndEmail:
        print(f'Authentication Error: no data inside \'{userName}\' login file')
        return False
    psw = pswAndEmail.split("|")[0]
    #print(psw)
    if pswToCheck == psw:
        return True
    return False




def uploadFile(s3,userName, userPsw, fileKey, fileToUpload):

    # errors handling
    if not os.path.isfile(fileToUpload):
        print(f'cannot find file: \'{fileToUpload}\'')
        return
    if not CreateUser.isBucketCreated(BUCKET_USERLOGIN, REGION):  # if the Bucket for login files doesn't exist.
        print(f'Bucket {BUCKET_USERLOGIN} does not exist. '
              f'Please check the bucket name or run CreateUser.py to create a new user.')
        return
    if not CreateUser.isFilekeyCreated(BUCKET_USERLOGIN, userName, REGION):
        print(f'Invalid UserName! Please try again.')
        return
    if not authenticateUser(s3, userName, userPsw, BUCKET_USERLOGIN, REGION):
        print(f'Invalid Password! Please try again.')
        return

    # if the bucket to store user data is not there, create it.
    if not CreateUser.isBucketCreated(BUCKET_USERDATA, REGION):
        try:
            CreateUser.createBucket(s3, BUCKET_USERDATA, REGION)
        except Exception as err:
            print(err)
            return

    oBucketForDataUpload = s3.Bucket(BUCKET_USERDATA)

    # if file is there, update it.
    folder = userName
    fileKey = folder + "/" + fileKey
    if CreateUser.isFilekeyCreated(BUCKET_USERDATA, fileKey, REGION):
        print(f'Updating {fileKey}')

    try:
        oBucketForDataUpload.upload_file(fileToUpload, fileKey)
        print(f'file is uploaded.')
    except Exception as err:
        print(err)


def main():
    #  make sure there are four arguments
    if len(sys.argv) < 5:
        print("Usage: Four arguments, user-name password file-key, and path-to-file-to-upload, are required.")
        return
    s3 = boto3.resource('s3', region_name=REGION)
    uploadFile(s3, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == '__main__':
    main()