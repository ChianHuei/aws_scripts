
import boto3
import time

def terminateEC2(ec2c, instid):
    resp = ec2c.stop_instances(InstanceIds=[instid])
    #json.dumps(resp,indent=2,separators=(',',':')))

    resp = ec2c.terminate_instances(InstanceIds=[instid])
    time.sleep(5)
    print(f'EC2 instance id:{instid} is {resp["TerminatingInstances"][0]["CurrentState"]["Name"]}.')
    time.sleep(10)
    print(f'EC2 instance id:{instid} is {resp["TerminatingInstances"][0]["CurrentState"]["Name"]}.')

