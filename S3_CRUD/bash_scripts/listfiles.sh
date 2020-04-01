#!/bin/bash

# listfiles will have these command line arguments:
# user-name password
# For example:
# listfiles.sh MtCat NiceCat

##################

numargs=$#

if [ $numargs -ne 2 ]; then
    echo "usage: listfiles user-name password"
exit
fi

##################


username=${1}
userpsw=$2

BUCKET_USER_LOGIN="chw-user-login-03282020"
BUCKET_USER_DATA="chw-user-data-03282020"
##################

#authenticating
S3_CHECK_LOGIN_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_LOGIN}" 2>&1)
if [ $? != 0 ] ; then
    echo "The users bucket ${BUCKET_USER_LOGIN} does not exist. Please run createuser.sh first."
    exit 1
fi

S3_CHECK_USER=$(aws s3 ls s3://${BUCKET_USER_LOGIN}/"${username}" 2>&1)
if [ $? != 0 ] ; then
    echo "The users ${username} does not exist. Please run createuser.sh first."
    exit 1
fi

PASSWORD=$(aws s3 cp s3://${BUCKET_USER_LOGIN}/"${username}" -|awk -F '|' '{print $1}')

if [ $? != 0 ] ; then
    echo "The user ${username} does not exist. Please run createuser.sh to creat a new user."
    exit 1
fi

if [ "$PASSWORD" != "$userpsw" ] ; then
    echo "Invalid password."
    exit 1
fi

#################

S3_CHECK_DATA_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_DATA}" 2>&1)
if [ $? != 0 ] ; then
    echo "The data bucket ${BUCKET_USER_DATA} does not exist. Please run uploadfile.sh first."
    exit 1
fi

aws s3 ls s3://${BUCKET_USER_DATA}/"${username}"/ | awk '{print $4}'