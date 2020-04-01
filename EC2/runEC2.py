
import boto3
def runInstance(ec2c,amiid,insttype,sshkeypair, secgrpid,subnetid, numinstances):
	if not secgrpid:
		print(f'security id is not valid.')
		return

	#amiid = 'ami-021bb9f371690f97a'
	#insttype = 't2.micro'
	#sshkeypair = 'cloudcomputing'
	#numinstances = 1
	secgrpidlist = [secgrpid]


	resp = ec2c.run_instances(
		ImageId=amiid,
		InstanceType=insttype,
		KeyName=sshkeypair,
		SecurityGroupIds=secgrpidlist,
		SubnetId=subnetid,
		MaxCount=numinstances,
		MinCount=numinstances)

	#uncomment this to see format of response from run_instances
	#print json.dumps(resp,indent=2,separators=(',',':'))

	inst = resp["Instances"][0]
	instid = inst["InstanceId"]
	print('Waiting for instance to enter running state')

	bIsRunning = False
	while bIsRunning == False:
		rz = ec2c.describe_instance_status(InstanceIds=[instid])

		#call can return before all data is available
		if not bool(rz):
			continue
		if len(rz["InstanceStatuses"]) == 0:
			continue

		# print(json.dumps(rz,indent=2,separators=(',',':')))
		#rz["InstanceStatuses"][0]["InstanceState"]["Name"]

		inststate = rz["InstanceStatuses"][0]["InstanceState"]
		#print(json.dumps(inststate,indent=2,separators=(',',':')))
		state = inststate["Name"]
		if state == 'running':
			bIsRunning = True
		else:
			print('.')

	print(' ')

	bGotIp = False
	while bGotIp == False:
		outp = ec2c.describe_instances(InstanceIds=[instid])
		inst = outp["Reservations"][0]["Instances"][0]
		instid = inst["InstanceId"]
		# publicip=inst["PublicIpAddress"]
		publicip = inst.get('PublicIpAddress')
		if not publicip:
			print('do not have ip address yet')
			continue
		else:
			bGotIp = True

	print('ip=' + publicip)
	return instid, publicip
