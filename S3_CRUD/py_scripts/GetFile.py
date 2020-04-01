# -*- coding: utf-8 -*-

"""
command line arguments:
user-name password file-key path-to-save-file-to

For example:

python GetFile MrCat NiceCat 'Picture of my favorite dog' .\MyFavoriteDog
"""
import boto3
import sys
import os
from UploadFile import authenticateUser
from CreateUser import isFilekeyCreated
from CreateUser import isBucketCreated

BUCKET_USERLOGIN = "chw-user-login-02152020"
BUCKET_USERDATA = "chw-user-data-02152020"
REGION = 'us-west-1'


def getFile(bucket, userName,fileName, pathToSave):

    fileToGet = userName+"/"+fileName
    try:
        bucket.download_file(fileToGet, pathToSave)
    except Exception as err:
        print(err)




def main():

    #  make sure there are four arguments
    if len(sys.argv) < 5:
        print("Argument Error: Four arguments, user-name password file-key, and path-to-save-file-to, are required.")
        return
    s3 = boto3.resource('s3', region_name=REGION)
    userName, userPsw, fileName, pathToSave = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    # errors handling
    if not isBucketCreated(BUCKET_USERLOGIN, REGION):
        print(f'Bucket {BUCKET_USERLOGIN} does not exist.')
        return
    if not isFilekeyCreated(BUCKET_USERLOGIN, userName, REGION):
        print(f'Invalid UserName! Please try again.')
        return
    if not authenticateUser(s3, userName, userPsw, BUCKET_USERLOGIN, REGION):
        print(f'Invalid Password! Please try again.')
        return
    if not isBucketCreated(BUCKET_USERDATA, REGION):
        print(f'Bucket {BUCKET_USERDATA} does not exist.')
        return

    try:
        obucket = s3.Bucket(BUCKET_USERDATA)
    except Exception as err:
        print(err)

    getFile(obucket, userName, fileName, pathToSave)


if __name__ == '__main__':
    main()