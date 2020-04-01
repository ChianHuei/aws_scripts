#!/bin/bash

# uploadfile will have these command line arguments:
# user-name password file-key path-to-file-to-upload
# For example: uploadfile <my_name> <my_password> <"My Favorite Dog Picture"> <.\dog1.jpg>

###################################
#basic error handling
numargs=$#

if [ $numargs -ne 4 ]; then
    echo "usage: uploadfile.sh user password filekey filepath"
    exit
fi

# checking validity
if [[ $1 =~ [[:space:]] ]]; then
    echo "Ivalid username, cannot contain whitespaces."
    exit 1
fi

if [[ $2 =~ [[:space:]] ]]; then
    echo "Ivalid password, cannot contain whitespaces."
    exit 1
fi

if [[ $2 =~ ['\|'] ]]; then
    echo "Ivalid password, cannot contain '|'."
    exit 1
fi

#check to see if file being uploaded exists
if [ ! -f "$4" ]; then
    echo "cannot find upload file $4"
    exit 1
fi
####################
username=${1}
userpsw=$2
filekey=$3
fileToUpload=$4

filekey=${filekey// /-} # replacing sapces with -

BUCKET_USER_LOGIN="chw-user-login-03282020"
BUCKET_USER_DATA="chw-user-data-03282020"

#########################
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

PASSWORD=$(aws s3 cp s3://${BUCKET_USER_LOGIN}/${username} -|awk -F '|' '{print $1}')

if [ $? != 0 ] ; then
    echo "The user ${username} does not exist. Please run createuser.sh to creat a new user."
    exit 1
fi

if [ "$PASSWORD" != "$userpsw" ] ; then
    echo "Invalid password."
    exit 1
fi

####################
# checking to see if the data bucket exists
S3_CHECK_DATA_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_DATA}" 2>&1)
if [ $? != 0 ] ; then
    echo "Creating bucket $BUCKET_USER_DATA..."
    aws s3 mb "s3://$BUCKET_USER_DATA"
    S3_CHECK_DATA_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_DATA}" 2>&1)
    if [ $? != 0 ] ; then
        echo "Bucket $BUCKET_USER_DATA cannot be created. Please check AWS S3 Bucket Naming Requirements."
        exit 1
    fi
fi

S3_CHECK_FILEKEY=$(aws s3 ls s3://${BUCKET_USER_DATA}/"${username}"/"${filekey}" | grep "\s${filekey}$" 2>&1)

if [ $? == 0 ]; then
    read -p "The file-key ${filekey} exists. Do you want to replace it? (y or n): " rpl
    if [ "$rpl" != "y" ] ; then
        echo "uploading canceled"
        exit 0
    fi
fi

####################

#uploading file
S3_UPLOAD_MSG=$(aws s3 cp "${fileToUpload}" "s3://${BUCKET_USER_DATA}/${username}/${filekey}")
if [ $? != 0 ]; then
    echo "error uploading $fileToUpload"
else
    echo "$fileToUpload uploaded into S3"
fi
