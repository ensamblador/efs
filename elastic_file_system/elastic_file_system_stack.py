import boto3
from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    Stack,
    aws_iam as iam,
    aws_efs as efs,
    aws_ssm as ssm,
)

from aws_cdk.aws_ec2 import SecurityGroup, Port, Peer

from constructs import Construct


class ElasticFileSystemStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = self.get_vpc()
        security_group = self.get_security_group()

        #https://ahmadreza.com/2023/02/how-to-construct-ecs-service-with-efs-volume/
        filesystem = efs.FileSystem(self, "efs", vpc=vpc, security_group=security_group)
        
        # https://github.com/aws-samples/aws-cdk-examples/blob/master/typescript/ecs/fargate-service-with-efs/index.ts
        filesystem.add_to_resource_policy(
            iam.PolicyStatement(
                actions=['elasticfilesystem:ClientMount'], 
                principals=[iam.AnyPrincipal()], 
                conditions= {"Bool": {'elasticfilesystem:AccessedViaMountTarget': 'true'}}
            )
        )

        access_point = efs.AccessPoint(
            self,
            "volume-accesspoint",
            file_system=filesystem,
            path="/data",
            posix_user=efs.PosixUser(gid="1000", uid="1000"),
            create_acl=efs.Acl(owner_gid="1000", owner_uid="1000", permissions="755"),
        )
        self.create_ssm_param("access-point-id", access_point.access_point_id)
        self.create_ssm_param("file-system-id", filesystem.file_system_id)


    def get_vpc(self):
        vpc_id = self.get_ssm_parameter("vpc-id")
        vpc = ec2.Vpc.from_lookup(self, "V", vpc_id=vpc_id)

        return vpc

    def get_security_group(self):
        task_sg_id = self.get_ssm_parameter("task-sg-id")
        security_group = SecurityGroup.from_security_group_id(
            self, "SG", security_group_id=task_sg_id
        )
        security_group.add_ingress_rule(
            security_group, connection=Port.tcp(2049), description="Allow NFS"
        )

        return security_group

    def get_ssm_parameter(self, parameter_name):
        return boto3.client("ssm").get_parameter(Name=f"/gen-ai-apps/{parameter_name}")[
            "Parameter"
        ]["Value"]

    def create_ssm_param(self, name, value):
        ssm.StringParameter(
            self,
            f"ssm-{name}",
            parameter_name=f"/gen-ai-apps/{name}",
            string_value=value,
        )
