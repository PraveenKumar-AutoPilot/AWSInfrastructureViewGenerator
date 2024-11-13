from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

import boto3
from botocore.exceptions import ClientError

class InfrastructureViewGenerator:
    def GenerateDiagram(self, session):
        with Diagram("Grouped Workers", show=True, direction="LR"):
            # Create load balancer node
            lb = ELB("Load Balancer")

            # Create a cluster for the instances
            with Cluster("EC2 Instances"):
                instances = []
                ec2 = session.client('ec2')
                response = ec2.describe_instances()
                for item in response["Reservations"]:
                    for instance in item['Instances']:
                        instanceId = instance['InstanceId']
                        # Add each instance to the list and create EC2 node
                        ec2_node = EC2(instanceId)
                        instances.append(ec2_node)

                # Connect load balancer to each instance
                lb >> instances

# Example usage
if __name__ == "__main__":
    environment = 'test-environment'
    session = boto3.Session(profile_name=environment)
    generator = InfrastructureViewGenerator()
    generator.GenerateDiagram(session)
