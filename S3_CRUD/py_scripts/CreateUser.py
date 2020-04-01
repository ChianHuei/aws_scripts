# -*- coding: utf-8 -*-
"""
command line arguments: user-name password email

for example:
python CreateUser.py MrCat NiceCat cats@cats.com
"""
import boto3
import sys


def isBucketCreated(bucketName, region) -> bool:
    """
    if bucketName already exists, returns True, else False.
    """
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()
    for element in response['Buckets']:
        if element['Name'] == bucketName:
            return True
    return False

def isFilekeyCreated(bucketName, obKey, region) -> bool:
    """
     if the file name or the object name, which means the key,
     already exists in the bucket, returns True, else False.
    """
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_objects_v2(Bucket=bucketName)
    for element in response['Contents']:
        if element['Key'] == obKey:
            return True
    return False


def createBucket(s3, bucketName: str, region: str) -> None:
    """
    This function creates bucket.
    If the bucket can not been successfully created, it raises errors.
    """
    print('Creating bucket: ' + bucketName + " in region: " + region)
    try:
        resp = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': region})
        if resp is not None:
            print(f"Bucket: {bucketName} is ready.")
    except:
        raise Exception(f'Bucket-Creating Error: bucket \'{bucketName}\' can not be created.')



def createObjectInBucket(s3, bucketName: str, keyName: str, data: str, region) -> None:
    """
    This function either creates a object (keyName) in an assigned bucket(bucketName),
    writing data into the object, or updates an old object.
    It returns True when succeeds, otherwise False.
    """
    bucket = s3.Bucket(bucketName)
    binaryData = data.encode()
    try:
        bucket.put_object(Key=keyName, Body=binaryData)
    except:
        raise Exception(f'Data-Writing Error: object \'{keyName}\' can not be written.')


def readDataFromObject(s3, bucketName: str,keyName: str, region) -> str:
    """
    read from an existing objcet
    :return string
    """
    if not isBucketCreated(bucketName, region):
        raise Exception(f'Data-Reading Error: bucket \'{bucketName}\' is not there.')

    bucket = s3.Bucket(bucketName)
    if not isFilekeyCreated(bucketName, keyName, region):
        raise Exception(f'Data-Reading Error: objcet \'{keyName}\' is not there.')

    try:
        key = bucket.Object(keyName)
        resp = key.get()
        bData = resp["Body"].read()
    except:
        raise Exception(f"Data-Reading Error: objcet \'{keyName}\' can not be read.")
    return bData.decode()




def createUser():

    # user login data, and 1 bucket to store all user data
    BUCKET_USERLOGIN = "chw-user-login-02152020"
    BUCKET_USERDATA = "chw-user-data-02152020"
    REGION = 'us-west-1'

    #  make sure there are three arguments
    if len(sys.argv) < 4:
        raise Exception("Usage: Three arguments user-name password and email, are required.")

    s3 = boto3.resource('s3', region_name=REGION)
    userName, userPsw, userEmail = sys.argv[1], sys.argv[2], sys.argv[3]
    # if the user-login bucket doesn't exist, create it.
    if not isBucketCreated(BUCKET_USERLOGIN, REGION):
        try:
            createBucket(BUCKET_USERLOGIN, REGION)
        except Exception as err:
            raise err

    # check user-name
    stringToWriting = userPsw.replace("|","") + "|" + userEmail.replace("|","")
    fileExists = updateIsRequired = False  # set two flags

    if isFilekeyCreated(BUCKET_USERLOGIN, userName,REGION):  # if the userName is already there as a filekey
        print(f'The user-login file: {userName} has been created.')
        fileExists = True
        try:  # read old data
            oldString = readDataFromObject(s3, BUCKET_USERLOGIN, userName, REGION)
        except Exception as err:
            raise err
        if stringToWriting != oldString:
            updateIsRequired = True

    if fileExists and not updateIsRequired:
        print(f'The user-login file: {userName} does not need update.')
    else:
        if updateIsRequired:
            print(f'Updating {userName} login file: ...')
        try:
            createObjectInBucket(s3, BUCKET_USERLOGIN, userName, stringToWriting, REGION)
        except Exception as err:
            raise err







def main():
    try:
        createUser()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()


