#!/bin/bash

#createuser will have these command line arguments:
#user-name password email
#for example, in a console/terminal:
#createuser <my_name> <my_password> <mymail@gmail.com>

##################
#basic error handling
numargs=$#

if [ $numargs -ne 3 ]; then
    echo "usage: createuser.sh username password email"
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

if [[ $3 =~ [[:space:]] ]]; then
    echo "Ivalid email, cannot contain whitespaces."
    exit 1
fi

if [[ $3 =~ ['\|'] ]]; then
    echo "Ivalid password, cannot contain '|'."
    exit 1
fi

##################
# arguments
USERNAME=${1}
PASSWORD=$2
EMAIL=$3

BUCKET_USER_LOGIN="chw-user-login-03282020"
BUCKET_USER_DATA="chw-user-data-03282020"
##################
# making a bucket for user credentials files

S3_CHECK_LOGIN_BUCKET=$(aws s3 ls "s3://${BUCKET_USER_LOGIN}" 2>&1)
if [ $? != 0 ]; then
    echo "creating users-login bucket..."
    aws s3 mb "s3://${BUCKET_USER_LOGIN}"
else
    echo "Bucket $BUCKET_USER_LOGIN exists."
fi

######################################
# creating a user credentials file

S3_CHECK_USER_LOGIN_FILE=$(aws s3 ls s3://${BUCKET_USER_LOGIN}/${USERNAME} | grep ${USERNAME}$ 2>&1)
if [ $? == 0 ]; then
    echo "$USERNAME credentials file exists. Will update password and email."
else
    echo "$USERNAME credentials file does not exist, will create it."
fi

echo "$PASSWORD|$EMAIL" | aws s3 cp - s3://${BUCKET_USER_LOGIN}/${USERNAME}

# ckecking whether the credentials file is created
S3_CHECK_USER_LOGIN_FILE=$(aws s3 ls s3://${BUCKET_USER_LOGIN}/${USERNAME} | grep ${USERNAME}$ 2>&1)
if [ $? == 0 ]; then
    echo "Done."
else
    echo "It failed to create $USERNAME credentials file."
    exit 1
fi
######################################
# making a bucket for users to upload files

S3_CHECK_DATA_BUCKET=$(aws s3 ls "s3://$BUCKET_USER_DATA" 2>&1)
if [ $? != 0 ] ; then
  echo "Creating bucket $BUCKET_USER_DATA..."
  aws s3 mb "s3://$BUCKET_USER_DATA"
  echo "Bucket $BUCKET_USER_DATA is created"
fi
