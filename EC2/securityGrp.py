
import boto3

def setSecurityGrp(ec2c,secgrpname, vpcidtouse):

	try:
		secgrpfilter = [{'Name':'group-name', 'Values':[secgrpname]}]
		secgroups = ec2c.describe_security_groups(Filters=secgrpfilter)
		secgrptouse = secgroups["SecurityGroups"][0]
		secgrpid = secgrptouse['GroupId']
	except:
		print('no security group, will create security group' + secgrpname)
		secgrptouse = ec2c.create_security_group(
			GroupName=secgrpname,Description='aws class open ssh,http,https',
			VpcId=vpcidtouse)
		#print("created security group:" + secgrpid)

		secgrpid = secgrptouse['GroupId']
		portlist = [22, 80, 443]
		for port in portlist:
			try:
				ec2c.authorize_security_group_ingress(
					CidrIp='0.0.0.0/0',
					FromPort=port,
					GroupId=secgrpid,
					IpProtocol='tcp',
					ToPort=port)
			except:
				print("error opening port:" + str(port))
				return
	return secgrpid