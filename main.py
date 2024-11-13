import boto3
from botocore.exceptions import ClientError

class InfrastructureViewGenerator:
    def __init__(self):
        self.vpcNameList = {}
        self.subnetNameList = {}
        self.securityGroupNameList = {}

    def Print_VPC_Details(self, session):
        self.vpcNameList = {}
        ec2 = session.client('ec2')
        response = ec2.describe_vpcs()
        print('## VPC List')
        print('Environment, VpcId, VpcName, CidrBlock, IsDefault, State')
        for vpc in response["Vpcs"]:
            VpcId = vpc['VpcId']
            CidrBlock = vpc['CidrBlock']
            IsDefault = str(vpc['IsDefault'])
            State = vpc['State']

            Tags = vpc['Tags']
            vpcName = ''
            for tag in Tags:
                if tag['Key'] == 'Name':
                    vpcName = tag['Value']
                    break
            self.vpcNameList[VpcId] = vpcName
            print(session.profile_name + ", " + VpcId + ", " + vpcName + ", " + CidrBlock + ", " + IsDefault+ ", " + State)

    def Print_Regions_Details(self, session):
        ec2 = session.client('ec2')
        response = ec2.describe_regions()
        print('Environment, RegionName, Endpoint')
        for region in response["Regions"]:
            RegionName = region['RegionName']
            Endpoint = region['Endpoint']
            print(session.profile_name + ", " + RegionName + ", " + Endpoint )

    def Print_Availability_Zones_Details(self, session):
        ec2 = session.client('ec2')
        response = ec2.describe_availability_zones()
        print('\n## Availability Zones List')
        print('Environment, RegionName, AvailabilityZoneName, State')
        for availabilityZone in response["AvailabilityZones"]:
            RegionName = availabilityZone['RegionName']
            ZoneName = availabilityZone['ZoneName']
            State = availabilityZone['State']
            print(session.profile_name + ", " + RegionName + ", " + ZoneName+ ", " + State)

    def Print_Subnets_Details(self, session):
        self.subnetNameList = {}
        ec2 = session.client('ec2')
        response = ec2.describe_subnets()
        print('\n## Subnets Details')
        print('Environment, VpcName, AvailabilityZone, SubnetName, CidrBlock, AvailableIpAddressCount, State')
        for subnet in response['Subnets']:
            VpcId = subnet['VpcId']
            AvailabilityZone = subnet['AvailabilityZone']
            SubnetId = subnet['SubnetId']
            CidrBlock = subnet['CidrBlock']
            AvailableIpAddressCount = str(subnet['AvailableIpAddressCount'])
            State = subnet['State']
            Tags = subnet['Tags']

            subnetName = ''
            for tag in Tags:
                if tag['Key'] == 'Name':
                    subnetName = tag['Value']
                    break
            #if 'Name' in Tags:
            #    subnetName = Tags['Key']['Name']

            self.subnetNameList[SubnetId] = subnetName
            vpcName = self.GetVpcName(VpcId)
            if vpcName == '':
                vpcName = VpcId

            if subnetName == '':
                print(
                    session.profile_name + ", " + vpcName + ", " + AvailabilityZone + ", " + SubnetId + ", " + CidrBlock + ", " + AvailableIpAddressCount + ", " + State)
            else:
                print(
                    session.profile_name + ", " + vpcName + ", " + AvailabilityZone + ", " + subnetName + ", " + CidrBlock + ", " + AvailableIpAddressCount + ", " + State)

    def Print_EC2_SecurityGroups_Details(self, session):
        self.securityGroupNameList = {}
        # Initialize a session using Amazon EC2
        ec2 = session.client('ec2')
        response = ec2.describe_security_groups()

        print('\n## SecurityGroups')
        print('Environment, VpcName, SecurityGroupId, SecurityGroupName, Description')
        for securityGroup in response['SecurityGroups']:
            VpcId = str(securityGroup['VpcId'])
            GroupId = securityGroup['GroupId']
            GroupName = securityGroup['GroupName']
            Description = securityGroup['Description']

            self.securityGroupNameList[GroupId] = GroupName
            vpcName = self.GetVpcName(VpcId)
            if vpcName == '':
                vpcName = VpcId

            print(session.profile_name + ", " + vpcName + ", " + GroupId + ", " + GroupName + ", " + Description)

    def Print_EC2_Security_GroupRules_Details(self, session):
        # Initialize a session using Amazon EC2
        ec2 = session.client('ec2')
        response = ec2.describe_security_groups()

        print('\n## SecurityGroups Rules')
        print('Environment, SecurityGroupName, VpcName, Inbound, IpProtocol, FromPort, CidrIp, Description')
        for securityGroup in response['SecurityGroups']:
            VpcId = str(securityGroup['VpcId'])
            GroupName = securityGroup['GroupName']
            Description = securityGroup['Description']
            IpPermissions = securityGroup['IpPermissions']

            vpcName = self.GetVpcName(VpcId)
            if vpcName == '':
                vpcName = VpcId

            for ipPermission in IpPermissions:
                IpProtocol = ipPermission['IpProtocol']
                FromPort = ''
                if IpProtocol != '-1':
                    FromPort = str(ipPermission['FromPort'])

                IpRanges = ipPermission['IpRanges']
                for ipRange in IpRanges:
                    #print(ipRange)
                    CidrIp = str(ipRange['CidrIp'])
                    if 'Description' in ipRange:
                        Description2 = ipRange['Description']
                    else:
                        Description2 = ''
                    print(session.profile_name + ", " +  GroupName + ", " + vpcName + ", Inbound, "+IpProtocol+ ", "+FromPort + ", "+ CidrIp+ ", "+ Description2)

            IpPermissionsEgress = securityGroup['IpPermissionsEgress']
            for ipPermissionsEgres in IpPermissionsEgress:
                IpProtocol = ipPermissionsEgres['IpProtocol']
                FromPort = ''
                if IpProtocol == '-1':
                    IpProtocol = ''
                else:
                    FromPort = str(ipPermissionsEgres['FromPort'])

                IpRanges = ipPermissionsEgres['IpRanges']
                for ipRange in IpRanges:
                    CidrIp = str(ipRange['CidrIp'])
                    if 'Description' in ipRange:
                        Description2 = ipRange['Description']
                    else:
                        Description2 = ''
                    print(session.profile_name + ", " + GroupName + ", " + vpcName + ", Outbound, "+IpProtocol+ ", "+FromPort + ", "+ CidrIp+ ", "+ Description2)

    def Print_LoadBalancer_Details(self, session):
        elbv2 = session.client('elbv2')
        response = elbv2.describe_load_balancers()
        print("\n## LoadBalancers")
        print('Environment, LoadBalancerName, Type, DNSName, VpcName, ZoneName/SubnetId List, SecurityGroup List, IpAddressType, State')
        for loadBalancer in response['LoadBalancers']:
            LoadBalancerName = loadBalancer['LoadBalancerName']
            DNSName = loadBalancer['DNSName']
            VpcId = loadBalancer['VpcId']
            State = loadBalancer['State']['Code']
            Type = loadBalancer['Type']
            IpAddressType = loadBalancer['IpAddressType']
            SecurityGroups = loadBalancer['SecurityGroups']

            ZoneName_SubnetIdList = ''
            for availabilityZone in loadBalancer['AvailabilityZones']:
                ZoneName = availabilityZone['ZoneName']
                SubnetId = availabilityZone['SubnetId']

                subnetName = self.GetSubnetName(SubnetId)
                if subnetName == '':
                    subnetName = SubnetId

                ZoneName_SubnetIdList = ZoneName_SubnetIdList + ZoneName + '/' + subnetName + "#"

            SecurityGroupList = ''
            for securityGroup in SecurityGroups:
                securityGroupName = self.GetSecurityGroupName(securityGroup)
                if securityGroupName == '':
                    securityGroupName = securityGroup
                SecurityGroupList = SecurityGroupList + securityGroupName + '#'

            vpcName = self.GetVpcName(VpcId)
            if vpcName == '':
                vpcName = VpcId

            print(session.profile_name + ", " + LoadBalancerName + ", " + Type + ", " + DNSName + ", " + vpcName + ", " + ZoneName_SubnetIdList + ", " + SecurityGroupList + ", " + IpAddressType + ", " + State)

    def Print_LoadBalancer_TargetGroup_Details(self, session):
        elbv2 = session.client('elbv2')
        response = elbv2.describe_target_groups()
        print("\n## LoadBalancer TargetGroups")
        print('Environment, TargetGroupName, Protocol, Port, VpcName, TargetType, LoadBalancerArns, HealthCheckProtocol, HealthCheckPort, HealthCheckEnabled, HealthCheckIntervalSeconds, HealthCheckTimeoutSeconds, HealthyThresholdCount, UnhealthyThresholdCount, HealthCheckPath ')
        for targetGroup in response['TargetGroups']:
            TargetGroupName = targetGroup['TargetGroupName']
            Protocol = targetGroup['Protocol']
            Port = str(targetGroup['Port'])
            VpcId = targetGroup['VpcId']
            TargetType = targetGroup['TargetType']
            HealthCheckProtocol = targetGroup['HealthCheckProtocol']
            HealthCheckPort = str(targetGroup['HealthCheckPort'])
            HealthCheckEnabled = str(targetGroup['HealthCheckEnabled'])
            HealthCheckIntervalSeconds = str(targetGroup['HealthCheckIntervalSeconds'])
            HealthCheckTimeoutSeconds = str(targetGroup['HealthCheckTimeoutSeconds'])
            HealthyThresholdCount = str(targetGroup['HealthyThresholdCount'])
            UnhealthyThresholdCount = str(targetGroup['UnhealthyThresholdCount'])

            HealthCheckPath =  ''
            if 'HealthCheckPath' in targetGroup:
                HealthCheckPath = targetGroup['HealthCheckPath']

            vpcName = self.GetVpcName(VpcId)
            if vpcName == '':
                vpcName = VpcId

            LoadBalancerArns = targetGroup['LoadBalancerArns']
            if len(LoadBalancerArns) > 0:
                for loadBalancerArn in LoadBalancerArns:
                    print(session.profile_name + ", " + TargetGroupName + ", " + Protocol + ", " + Port + ", " + vpcName + ", " + TargetType + ", " + loadBalancerArn + ", " + HealthCheckProtocol + ", " + HealthCheckPort + ", " + HealthCheckEnabled + ", " +  HealthCheckIntervalSeconds + ", " + HealthCheckTimeoutSeconds + ", " + HealthyThresholdCount + ", " + UnhealthyThresholdCount + ", " + HealthCheckPath )
            else:
                print(session.profile_name + ", " + TargetGroupName + ", " + Protocol + ", " + Port + ", " + vpcName + ", " + TargetType + ", " + 'None Associated' + ", " + HealthCheckProtocol + ", " + HealthCheckPort + ", " + HealthCheckEnabled + ", " + HealthCheckIntervalSeconds + ", " + HealthCheckTimeoutSeconds + ", " + HealthyThresholdCount + ", " + UnhealthyThresholdCount + ", " + HealthCheckPath)

    def Print_TargetGroup_TargetInstance_Details(self, session):
        elbv2 = session.client('elbv2')
        response = elbv2.describe_load_balancers()
        print("\n## LoadBalancer TargetGroup TargetInstances")
        print('Environment, LoadBalancerName, TargetGroupName, instanceid, instanceName, HealthCheckPort, TargetHealthState')

        for loadBalancer in response['LoadBalancers']:
            LoadBalancerArn = loadBalancer["LoadBalancerArn"]
            LoadBalancerName = loadBalancer['LoadBalancerName']

            response2 = elbv2.describe_target_groups(LoadBalancerArn=LoadBalancerArn)
            for targetGroup in response2["TargetGroups"]:
                TargetGroupArn = targetGroup["TargetGroupArn"]
                TargetGroupName = targetGroup['TargetGroupName']
                response3 = elbv2.describe_target_health(TargetGroupArn=TargetGroupArn)

                for targetHealthDescription in response3["TargetHealthDescriptions"]:
                    instanceid = targetHealthDescription['Target']['Id']
                    instanceName = self._GetInstanceName(session, instanceid)
                    HealthCheckPort = targetHealthDescription['HealthCheckPort']
                    TargetHealthState = targetHealthDescription['TargetHealth']['State']

                    print(session.profile_name + ", " + LoadBalancerName + ", " + TargetGroupName + ", " + instanceid + ", " + instanceName + ", " + HealthCheckPort +", " + TargetHealthState)

    def _GetTargetGroups(self, session, arn):
        tgs = session.describe_target_groups(LoadBalancerArn=arn)
        tgstring = []
        for tg in tgs["TargetGroups"]:
            tgstring.append(tg["TargetGroupName"])
        return tgstring

    def _GetTargetGroupArns(self, session, arn):
        elbv2 = session.client('elbv2')
        tgs = elbv2.describe_target_groups(LoadBalancerArn=arn)
        tgarns = []
        for tg in tgs["TargetGroups"]:
            tgarns.append(tg["TargetGroupArn"])
        return tgarns

    def _GetTargetHealth(self, session, arn):
        elbv2 = session.client('elbv2')
        response = elbv2.describe_target_health(TargetGroupArn=arn)
        instanceids = []
        for targetHealthDescription in response["TargetHealthDescriptions"]:
            instanceid = targetHealthDescription['Target']['Id']
            targetHealthDescription["Name"] = self._GetInstanceName(session, instanceid)
            instanceids.append(targetHealthDescription['Target']['Id'])
            print(targetHealthDescription)

    def _GetInstanceName(self, session, instanceid):
        ec2 = session.client('ec2')
        instances = ec2.describe_instances(Filters=[
            {
                'Name': 'instance-id',
                'Values': [
                    instanceid
                ]
            },
        ], )
        for instance in instances["Reservations"]:
            for inst in instance["Instances"]:
                for tag in inst["Tags"]:
                    if tag['Key'] == 'Name':
                        return (tag['Value'])

    def Print_EC2_Instance_Details(self, session):
        environment = session.profile_name
        # Initialize a session using Amazon EC2
        ec2 = session.client('ec2')
        response = ec2.describe_instances()
        print('\n## EC2 Instances')
        print('Environment, RegionName, VpcName, AvailabilityZone, SubnetName, ImageId, InstanceId, InstanceType, MonitoringState, Platform, Architecture, EbsOptimized, cpuCores, cpuThreadsPerCore, RootDeviceType, RootDeviceName')
        for item in response["Reservations"]:
            for instance in item['Instances']:
                imageId = instance['ImageId']
                instanceId = instance['InstanceId']
                instanceType = instance['InstanceType']
                monitoringState = instance['Monitoring']['State']
                availabilityZone = instance['Placement']['AvailabilityZone']
                platform = instance['Platform']
                subnetId = instance['SubnetId']
                vpcId = instance['VpcId']
                architecture = instance['Architecture']
                ebsOptimized = str(instance['EbsOptimized'])
                iamInstanceProfile = instance['IamInstanceProfile']['Arn']
                networkInterfaces = instance['NetworkInterfaces']
                rootDeviceName = instance['RootDeviceName']
                rootDeviceType = instance['RootDeviceType']
                tags = instance['Tags']
                cpuCores = str(instance['CpuOptions']['CoreCount'])
                cpuThreadsPerCore = str(instance['CpuOptions']['ThreadsPerCore'])

                for tag in tags:
                    key = tag['Key']
                    value = tag['Value']
                    #print(key + ":" + value)

                vpcName = self.GetVpcName(vpcId)
                if vpcName == '':
                    vpcName = vpcId

                subnetName = self.GetSubnetName(subnetId)
                if subnetName == '':
                    subnetName = subnetId

                print(environment + ", " + session.region_name + ", " + vpcName + ", " +  availabilityZone + ", " + subnetName + ", " + imageId + ", " + instanceId + ", " + instanceType + ", " + monitoringState +", "+   platform +", "+ architecture +","+ ebsOptimized +", "+  cpuCores+", "+ cpuThreadsPerCore+", "+ rootDeviceType+", "+rootDeviceName)

        print("\n## EC2 SecurityGroups")
        print("Environment, EC2 InstanceId, SecurityGroupName")
        for item in response["Reservations"]:
            for instance in item['Instances']:
                # print(instance)
                instanceId = instance['InstanceId']
                securityGroups = instance['SecurityGroups']
                for securityGroup in securityGroups:
                    securityGroupName = securityGroup['GroupName']
                    print(environment + ", "+instanceId + ", " + securityGroupName)
    def Print_EBS_Details(self, session):
        ec2 = session.client('ec2')
        # Describes the specified EBS volumes or all of your EBS volumes.
        response = ec2.describe_volumes()
        print('\n## EBS Details')
        print('Environment, AvailabilityZone, VolumeId, VolumeType, Size, Iops, Throughput, Encrypted, MultiAttachEnabled, State, Device, AttachedWithInstanceIde, AttachedWithInstanceState, DeleteOnTermination')
        #print(response)
        for volume in response['Volumes']:
            AvailabilityZone = volume['AvailabilityZone']
            VolumeId = volume['VolumeId']
            VolumeType = volume['VolumeType']
            Size = str(volume['Size']) + ' GiB'
            Iops = str(volume['Iops'])
            Throughput = ''
            #for item in volume:
            #    if item['Key'] == 'Throughput':
            #        Throughput = str(item['Value'])
            #        break

            if 'Throughput' in volume:
                Throughput = str(volume['Throughput'])
            Encrypted = str(volume['Encrypted'])
            MultiAttachEnabled = str(volume['MultiAttachEnabled'])
            State = volume['State']

            for attachment in volume['Attachments']:
                Device = attachment['Device']
                AttachedWithInstanceId = attachment['InstanceId']
                AttachedWithInstanceState = attachment['State']
                DeleteOnTermination = str(attachment['DeleteOnTermination'])

                print(session.profile_name + ", " + AvailabilityZone + ", " + VolumeId + ", " + VolumeType + ", " + Size + ", " + Iops + ", " + Throughput+ ", " + Encrypted+ ", " + MultiAttachEnabled+ ", " + State+ ", " + Device + ", " +AttachedWithInstanceId+ ", " + AttachedWithInstanceState+ ", " + DeleteOnTermination)
    def Print_S3_Details(self, session):
        environment = session.profile_name

        # Let's use Amazon S3
        s3 = session.resource('s3')
        print("\n## S3")
        print("Environment, BucketName")
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(session.profile_name + ", " + bucket.name)

    def GetVpcName(self, id:str):
        name = ''
        if id in self.vpcNameList.keys():
            name = self.vpcNameList[id]
        return name

    def GetSubnetName(self, id:str):
        name = ''
        if id in self.subnetNameList.keys():
            name = self.subnetNameList[id]
        return name

    def GetSecurityGroupName(self, id: str):
        name = ''
        if id in self.securityGroupNameList.keys():
            name = self.securityGroupNameList[id]
        return name

    def PrintInfra(self, environment):
        print('\n-------------------------------- '+environment+'-------------------------------- ')
        session = boto3.Session(profile_name=environment)
        generator.Print_VPC_Details(session)
        generator.Print_Availability_Zones_Details(session)
        generator.Print_Subnets_Details(session)
        generator.Print_EC2_SecurityGroups_Details(session)
        generator.Print_EC2_Security_GroupRules_Details(session)
        generator.Print_LoadBalancer_Details(session)
        generator.Print_LoadBalancer_TargetGroup_Details(session)
        generator.Print_TargetGroup_TargetInstance_Details(session)
        generator.Print_EC2_Instance_Details(session)
        generator.Print_EBS_Details(session)
        generator.Print_S3_Details(session)

# Example usage
if __name__ == "__main__":
    environment = 'your-environment-name' # for example 'ej-commercial-vt100-preprod1'
    generator = InfrastructureViewGenerator()
    generator.PrintInfra(environment)

