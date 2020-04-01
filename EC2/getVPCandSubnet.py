####
#http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#client

#get the 1st vpc and 1st subnet

import boto3
def getVPC(ec2c):
    resp = ec2c.describe_vpcs()
    vpcidtouse = resp['Vpcs'][0]['VpcId']
    return vpcidtouse

def getSubnet(ec2c, vpcidtouse):
    subnetlist = ec2c.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpcidtouse]}])
    subnetid = subnetlist['Subnets'][0]['SubnetId']
    return subnetid

#uncomment this to see format of response from describe_subnets
#print(json.dumps(subnetlist,indent=2,separators=(',',':')))

