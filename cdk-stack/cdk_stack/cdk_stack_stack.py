"""Module providing resources for defining AWS infrastructure to deploy as code"""
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3_deployment,
    RemovalPolicy,
    Duration,
    CfnOutput
)
from constructs import Construct

class CdkStackStack(Stack):
    """
    This AWS CDK stack defines the infrastructure resources required for a serverless application.

    The resources created include:
    - A DynamoDB table named 'Metadata' for storing application metadata
    - A Lambda layer containing dependencies for the Lambda function
    - An IAM role and policy for the Lambda function to access DynamoDB
    - A Lambda function named 'StorageFunction' to interact with the DynamoDB table
    - An API Gateway REST API with resources and methods to invoke the Lambda function

    The stack is configured to remove all resources when deleted (for testing purposes).
    This removal policy should be removed for production deployments.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a table for metadata storage
        metadata = dynamodb.Table(
            self, 'Metadata',
            table_name='Metadata',
            partition_key=dynamodb.Attribute(
                name='identifier',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,  # for testing purposes, remove for production
        )

        # Create Lambda Layer to house dependencies
        dependency = _lambda.LayerVersion(
            self, 'LambdaLayer',
            code=_lambda.Code.from_asset('lambda_layer.zip'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description='A Lambda layer containing dependencies'
        )

        # Create IAM role for Lambda function
        storage_function_role = iam.Role(
            self, "StorageFunctionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # Create a custom IAM policy for the Lambda
        storage_function_policy = iam.Policy(
            self, 'StorageFunctionPolicy',
            policy_name='StorageFunctionPolicy',
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem",
                        "dynamodb:Scan",
                        "dynamodb:Query"
                    ],
                    resources=[
                        f"arn:aws:dynamodb:{self.region}:{self.account}:table/Metadata"
                    ]
                )
            ]
        )

        # Attach the policy to the Lambda function's role
        storage_function_role.attach_inline_policy(storage_function_policy)

        # Lambda function to interact with DynamoDB
        storage_function = _lambda.Function(
            self, 'StorageFunction',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='storage_interactions.handler',
            code=_lambda.Code.from_asset('lambda_functions'),
            layers=[dependency],
            role=storage_function_role
        )

        # Create the API Gateway with CORS enabled
        api = apigateway.LambdaRestApi(
            self, 'MyApiGateway',
            handler=storage_function,
            proxy=False,
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
                "allow_headers": apigateway.Cors.DEFAULT_HEADERS
            }
        )

        # Define a resource and method for the API
        storage_resource = api.root.add_resource("storage") # /storage
        storage_resource.add_method("GET")
        storage_resource.add_method("PUT")
        storage_resource.add_method("DELETE")
        storage_resource.add_method("POST")

        # Create the S3 bucket
        site_bucket = s3.Bucket(self, "ReactAppBucket",
            website_index_document="index.html",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Create an Origin Access Identity for CloudFront
        oai = cloudfront.OriginAccessIdentity(self, "OriginAccessIdentity")

        # Create the CloudFront distribution
        distribution = cloudfront.Distribution(self, "ReactAppDistribution",
            default_behavior={
                "origin": origins.S3Origin(site_bucket, origin_access_identity=oai),
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            },
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30)
                )
            ]
        )

        # Allow CloudFront (with the OAI) to access the S3 bucket
        bucket_policy = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{site_bucket.bucket_arn}/*"],
            effect=iam.Effect.ALLOW,
            principals=[iam.ArnPrincipal(f"arn:aws:iam::cloudfront.amazonaws.com::{oai.origin_access_identity_id}")]
        )
        site_bucket.add_to_resource_policy(bucket_policy)

        # Deploy the React app to the S3 bucket
        deployment = s3_deployment.BucketDeployment(self, "DeployReactApp",
            sources=[s3_deployment.Source.asset("../aws-site-frontend/build")],
            destination_bucket=site_bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )

        # Output the URLs
        CfnOutput(self, "BucketName", value=site_bucket.bucket_name)
        CfnOutput(self, "DistributionId", value=distribution.distribution_id)
        CfnOutput(self, "OAIId", value=oai.origin_access_identity_id)
        CfnOutput(self, "S3BucketURL", value=site_bucket.bucket_website_url)
        CfnOutput(self, "CloudFrontURL", value=distribution.domain_name)



    #    # S3 bucket to host React app
    #     site_bucket = s3.Bucket(self, "ReactAppBucket",
    #         website_index_document="index.html",
    #         # public_read_access=True,
    #         removal_policy=RemovalPolicy.DESTROY,
    #         auto_delete_objects=True
    #     )

    #     # Create an Origin Access Identity for CloudFront
    #     oai = cloudfront.OriginAccessIdentity(self, "OriginAccessIdentity")

    #     # Allow CloudFront (with the OAI) to access the S3 bucket
    #     bucket_policy = iam.PolicyStatement(
    #         actions=["s3:GetObject"],
    #         resources=[f"{site_bucket.bucket_arn}/*"],
    #         effect=iam.Effect.ALLOW,
    #         principals=[
    #             iam.ServicePrincipal("cloudfront.amazonaws.com"),
    #             iam.ArnPrincipal(oai.cloud_front_origin_access_identity_s3_canonical_user_id)
    #         ]
    #     )

    #     site_bucket.add_to_resource_policy(bucket_policy)
    #     # Create the CloudFront distribution
    #     distribution = cloudfront.Distribution(self, "ReactAppDistribution",
    #         default_behavior={
    #             "origin": origins.S3Origin(site_bucket),
    #             "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
    #         },
    #         error_responses=[
    #             cloudfront.ErrorResponse(
    #                 http_status=404,
    #                 response_http_status=200,
    #                 response_page_path="/index.html",
    #                 ttl=Duration.minutes(30)
    #             )
    #         ]
    #     )

    #     # Deploy the React app to the S3 bucket
    #     deployment = s3_deployment.BucketDeployment(self, "DeployReactApp",
    #         sources=[s3_deployment.Source.asset("../aws-site-frontend/build")],
    #         destination_bucket=site_bucket,
    #         distribution=distribution,
    #         distribution_paths=["/*"]
    #     )
