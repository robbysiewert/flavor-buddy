from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

class CdkStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Example bucket to confirm successful deployment
        bucket = s3.Bucket(self, "MyBucket",
            removal_policy=RemovalPolicy.DESTROY)
