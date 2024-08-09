from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3_deployment,
)
from constructs import Construct

class S3BucketPolicyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Retrieve bucket name and OAI ID from the first stack's outputs
        bucket_name = self.node.try_get_context("bucketName")
        oai_id = self.node.try_get_context("oaiId")

        # Reference the existing bucket
        site_bucket = s3.Bucket.from_bucket_name(self, "ReactAppBucket", bucket_name)

        # Allow CloudFront (with the OAI) to access the S3 bucket
        bucket_policy = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{site_bucket.bucket_arn}/*"],
            effect=iam.Effect.ALLOW,
            principals=[iam.ArnPrincipal(f"arn:aws:iam::cloudfront.amazonaws.com:{oai_id}")]
        )

        site_bucket.add_to_resource_policy(bucket_policy)

        # Deploy the React app to the S3 bucket
        deployment = s3_deployment.BucketDeployment(self, "DeployReactApp",
            sources=[s3_deployment.Source.asset("../aws-site-frontend/build")],
            destination_bucket=site_bucket,
            distribution=None,  # Distribution is already set up in the first stack
            distribution_paths=["/*"]
        )
