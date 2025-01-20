from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ecr_assets as ecr_assets,
    CfnOutput
)

from constructs import Construct
import os

class CdkEc2StreamlitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(
            self, "StreamlitVPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ]
        )

        # Create security group
        security_group = ec2.SecurityGroup(
            self, "StreamlitSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for Streamlit Docker EC2 instance"
        )

        # Allow inbound HTTP traffic on port 8080
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            # ec2.Peer.ipv4("10.36.XX.XXX/32"), #Restrict to a sepcific IP access
            ec2.Port.tcp(8501),
            "Allow Streamlit application access"
        )

        # Allow SSH access (optional, for troubleshooting)
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            # ec2.Peer.ipv4("10.36.XX.XXX/32"), #Restrict to a sepcific IP access
            ec2.Port.tcp(22),
            "Allow SSH access"
        )

        # Create IAM role for EC2
        role = iam.Role(
            self, "StreamlitEC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # Add required policies
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly")
        )

        # Build Docker image
        docker_image = ecr_assets.DockerImageAsset(
            self, "StreamlitDockerImage",
            directory=os.path.join(os.path.dirname(__file__), "..", "streamlit_app")
        )

        # Create user data script
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            # Update and install Docker
            "yum update -y",
            "yum install -y docker",
            "systemctl start docker",
            "systemctl enable docker",
            "usermod -a -G docker ec2-user",
            
            # Install AWS CLI
            "yum install -y aws-cli",
            
            # Configure AWS CLI and login to ECR
            f"aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin {self.account}.dkr.ecr.{self.region}.amazonaws.com",
            
            # Pull and run the Docker image
            f"docker pull {docker_image.image_uri}",
            f"docker run -d -p 8501:8501 {docker_image.image_uri}"
        )

        # Create EC2 instance
        instance = ec2.Instance(
            self, "StreamlitInstance",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            
            instance_type=ec2.InstanceType("t4g.micro"),
                        
            machine_image=ec2.MachineImage.latest_amazon_linux2023(
                cpu_type=ec2.AmazonLinuxCpuType.ARM_64
            ),
            
            security_group=security_group,
            role=role,
            user_data=user_data
        )

        # Output the instance public IP
        CfnOutput(
            self, "InstancePublicIP",
            value=f"http://{instance.instance_public_ip}:8501",
            description="URL for Streamlit application"
        )