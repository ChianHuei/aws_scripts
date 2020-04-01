# -*- coding: utf-8 -*-

"""
ListFiles.py will have these command line arguments:
user-name password

For example: python ListFiles.py MtCat NiceCat
For each user file stored, this Python script prints one line to the console:
"""

import boto3
import sys
from UploadFile import authenticateUser
import CreateUser

BUCKET_USERLOGIN = "chw-user-login-02152020"
BUCKET_USERDATA = "chw-user-data-02152020"
REGION = 'us-west-1'

def listFiles(bucket, prefix, region):
    """
    :param bucket: String
    :param prefix: String
    :return: List (a list containing file names)
    """

    client = boto3.client('s3', region)
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for ob in response['Contents']:
        fileName = ob['Key'].replace(prefix,"")
        print(fileName)



def main():

    if len(sys.argv) < 3:
        print("Argument Error: two arguments, user-name and password, are required.")
        return

    userName, psw = sys.argv[1], sys.argv[2]
    s3 = boto3.resource('s3', region_name=REGION)

    # errors handling
    if not CreateUser.isBucketCreated(BUCKET_USERLOGIN, REGION):  # if the Bucket for login files doesn't exist.
        print(f'Bucket {BUCKET_USERLOGIN} does not exist. '
              f'Please check the bucket name or run CreateUser.py to create a new user.')
        return
    if not authenticateUser(s3, userName, psw, BUCKET_USERLOGIN, REGION):
        print(f'Invalid password.')
        return

    listFiles(BUCKET_USERDATA, userName+"/", REGION)


if __name__ == '__main__':
    main()