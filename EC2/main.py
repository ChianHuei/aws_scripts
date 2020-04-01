#!/usr/bin/env python3
"""
this file is to create AWS EC2 instance and open an file "records.txt" to record instance id.
"""
import boto3
from getVPCandSubnet import getVPC
from getVPCandSubnet import getSubnet
from securityGrp import setSecurityGrp
from runEC2 import runInstance
from terminateInstance import terminateEC2



def main():

    # connect with AWS
    region = 'us-west-1'
    ec2Client = boto3.client('ec2', region_name=region)

    #get VPC and subnet info
    vpcId = getVPC(ec2Client)
    subnetId = getSubnet(ec2Client,vpcId)
    secgrpName = 'awsTesting'
    secgrpId = setSecurityGrp(ec2Client, secgrpName,vpcId)
    if not secgrpId:
        print(f'security id is not valid.')
        return

    # configuration
    amiId = 'ami-01c94064639c71719'  # Amazon Linux 2 AMI (HVM), SSD Volume Type
    instanceType = 't2.micro'
    sshKeyPair = 'cloudcomputing'
    num_of_instances = 1

    # run a instance
    instanceId, ip = runInstance(ec2Client, amiId,instanceType, sshKeyPair, secgrpId,subnetId,num_of_instances)
    # if more than one instance has been launched, this line of code should be revised
    outputFile = open("records.txt","a+")
    outputFile.write(f"instance id: {instanceId}, ip: {ip}\n")
    outputFile.close()

    # prompt to terminate the instance
    ans = input(f'terminate the instance now? (y or n) ')
    if ans == "y":
        print(f'terminating...')
        terminateEC2(ec2Client, instanceId)
    else:
        print(f'the instance remains running.')



if __name__ == '__main__':
    main()