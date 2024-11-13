# Infrastructure View Generator

The Infrastructure View Generator is a Python-based tool that helps you audit, documentation and visualize your AWS infrastructure. Using Boto3, it retrieves details on various AWS resources such as VPCs, subnets, EC2 instances, security groups, load balancers, and S3 buckets. This is useful for AWS environment documentation and auditing.

## Features

The tool provides detailed information about the following AWS resources:
- **VPCs**: Lists VPC IDs, names, CIDR blocks, default status, and states.
- **Regions and Availability Zones**: Shows available AWS regions and availability zones.
- **Subnets**: Details subnets within VPCs, including CIDR blocks and available IPs.
- **EC2 Instances**: Provides instance details including type, architecture, attached EBS volumes, and security groups.
- **Security Groups**: Displays inbound and outbound rules for security groups.
- **Load Balancers**: Details for load balancers, including types, DNS names, security groups, and associated target groups.
- **Target Groups and Instances**: Health check status for instances within target groups.
- **EBS Volumes**: Information about volume types, sizes, and attachment details.
- **S3 Buckets**: Lists all S3 buckets in the environment.

## Prerequisites

- Python 3.x
- AWS credentials configured with appropriate permissions to describe infrastructure components
- Boto3 library (`pip install boto3`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/infrastructure-view-generator.git
   cd infrastructure-view-generator
   ```
2. **Install Dependencies**:
   ```bash
   pip install boto3
   ```

## Usage

1. **Configure AWS CLI Profile**:
   Ensure you have an AWS CLI profile with the necessary permissions to describe infrastructure resources:
   ```bash
   aws configure --profile your-environment-name
   ```

2. **Set the Environment Name in the Script**:
   Open `main.py` and set your environment name:
   ```python
   environment = 'your-environment-name'
   ```

3. **Run the Script**:
   Execute the script to output AWS infrastructure details:
   ```bash
   python main.py
   ```

### Example Output

The tool prints infrastructure details in a structured format, grouped by resource type.

**VPC List**
```
## VPC List
Environment, VpcId, VpcName, CidrBlock, IsDefault, State
my-profile, vpc-123abc, MyVPC, 10.0.0.0/16, False, available
```

**Subnets Details**
```
## Subnets Details
Environment, VpcName, AvailabilityZone, SubnetName, CidrBlock, AvailableIpAddressCount, State
my-profile, MyVPC, us-east-1a, MySubnet, 10.0.1.0/24, 251, available
```

**EC2 Instances**
```
## EC2 Instances
Environment, RegionName, VpcName, AvailabilityZone, SubnetName, ImageId, InstanceId, InstanceType, MonitoringState, Platform, Architecture, EbsOptimized, cpuCores, cpuThreadsPerCore, RootDeviceType, RootDeviceName
my-profile, us-east-1, MyVPC, us-east-1a, MySubnet, ami-123456, i-12345abc, t2.micro, disabled, Linux/UNIX, x86_64, True, 2, 1, ebs, /dev/sda1
```

### Customization

You can modify the script to include additional resource details or remove specific sections:

1. **Add/Remove AWS Resources**: 
   - Edit methods within the `InfrastructureViewGenerator` class in `main.py` to customize resource outputs. For example, to exclude S3 details, comment out or remove the `Print_S3_Details` method.
   
2. **Formatting and Output**:
   - Customize print statements to match your preferred output format or redirect outputs to a file for structured documentation.

### Code Overview

The script contains several methods in the `InfrastructureViewGenerator` class:
- `Print_VPC_Details(session)`: Retrieves and prints details of all VPCs.
- `Print_Availability_Zones_Details(session)`: Lists availability zones.
- `Print_Subnets_Details(session)`: Displays subnet details within each VPC.
- `Print_EC2_Instance_Details(session)`: Provides instance information.
- `Print_EBS_Details(session)`: Prints details about EBS volumes.
- `Print_S3_Details(session)`: Lists S3 buckets.
- And additional methods for security groups, load balancers, and target groups.

### Sample Run

Here's how to initiate a sample run for an AWS environment profile:
```python
# Example usage
if __name__ == "__main__":
    environment = 'your-environment-name'
    generator = InfrastructureViewGenerator()
    generator.PrintInfra(environment)
```