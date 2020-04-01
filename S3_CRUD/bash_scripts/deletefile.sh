#!/bin/bash

# deletefile will have there command line parameters:
# user-name password file-key
# For example: deletefile MrCat NiceCat Bird01
# For example: deletefile <myName> <myPassword> <'myPhotoOnS3.jpg'>

##################

numargs=$#

if [ $numargs -ne 3 ]; then
    echo "usage: user-name password file-key"
    exit
fi

username="${1}"
userpsw="$2"
filekey="$3"
filekey=${filekey// /-} # replacing sapces with -

BUCKET_USER_LOGIN="chw-user-login-03282020"
BUCKET_USER_DATA="chw-user-data-03282020"
##################

#authenticating
S3_CHECK_LOGIN_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_LOGIN}" 2>&1)
if [ $? != 0 ]; then
    echo "The users bucket ${BUCKET_USER_LOGIN} does not exist. Please run createuser.sh first."
    exit 1
fi

S3_CHECK_USER=$(aws s3 ls s3://${BUCKET_USER_LOGIN}/"${username}" 2>&1)
if [ $? != 0 ] ; then
    echo "The users ${username} does not exist. Please run createuser.sh first."
    exit 1
fi

PASSWORD=$(aws s3 cp s3://${BUCKET_USER_LOGIN}/${username} - | awk -F '|' '{print $1}')

if [ $? != 0 ]; then
    echo "The user ${username} does not exist. Please run createuser.sh to creat a new user."
    exit 1
fi

if [ "$PASSWORD" != "$userpsw" ]; then
    echo "Invalid password."
    exit 1
fi

#################

# file-key checking

S3_CHECK_DATA_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_DATA}" 2>&1)
if [ $? != 0 ]; then
    echo "The users bucket ${BUCKET_USER_DATA} does not exist. Please run uploadfile.sh first."
    exit 1
fi

S3_CHECK_FILEKEY=$(aws s3 ls s3://${BUCKET_USER_DATA}/"${username}"/"${filekey}" | grep "\s${filekey}$" 2>&1)

if [ $? != 0 ]; then
    echo "The file-key ${filekey} does not exist."
    exit 1
fi

###################
# deleting

S3_CHECK_DELETE=$(aws s3 rm s3://${BUCKET_USER_DATA}/"${username}"/"${filekey}" 2>&1)

if [ $? == 0 ]; then
    echo "${filekey} is successfully deleted."
else
    echo "Deleting failed."
    exit 1
fi
