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

        # Create an API Gateway REST API resource for the Lambda function
        api = apigateway.LambdaRestApi(
            self, 'MyApiGateway',
            handler=storage_function,
            proxy=False
        )

        # Define a resource and method for the API
        storage_resource = api.root.add_resource("storage") # /storage
        storage_resource.add_method("GET")
        storage_resource.add_method("PUT")
        storage_resource.add_method("DELETE")
        # storage_resource.add_method("POST")
        storage_resource.add_method(
            "POST",
            integration=apigateway.LambdaIntegration(storage_function),
            method_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": True,
                    },
                }
            ],
        )
        # Add CORS preflight OPTIONS method
        storage_resource.add_cors_preflight(
            allow_origins=["http://localhost:3000"],  # Allow requests from your React app
            allow_methods=["POST", "OPTIONS"],        # Allow POST and OPTIONS methods
            allow_headers=["Content-Type"],           # Allow necessary headers
        )

       # S3 bucket to host React app
        site_bucket = s3.Bucket(self, "ReactAppBucket",
            website_index_document="index.html",
            # public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Create the CloudFront distribution
        distribution = cloudfront.Distribution(self, "ReactAppDistribution",
            default_behavior={
                "origin": origins.S3Origin(site_bucket),
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

        # Deploy the React app to the S3 bucket
        deployment = s3_deployment.BucketDeployment(self, "DeployReactApp",
            sources=[s3_deployment.Source.asset("../aws-site-frontend/build")],
            destination_bucket=site_bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )


        # Output the URLs
        CfnOutput(self, "S3BucketURL", value=site_bucket.bucket_website_url)
        CfnOutput(self, "CloudFrontURL", value=distribution.domain_name)

        # gateway_response_2xx = apigateway.GatewayResponse(
        #     self, "GatewayResponse200",
        #     rest_api=api,
        #     response_type=apigateway.ResponseType.DEFAULT_2_XX,
        #     response_headers={
        #         "Access-Control-Allow-Origin": "'http://localhost:3000'"
        #     }
        # )

        # gateway_response_4xx = apigateway.GatewayResponse(
        #     self, "GatewayResponse4XX",
        #     rest_api=api,
        #     response_type=apigateway.ResponseType.DEFAULT_4_XX,
        #     response_headers={
        #         "Access-Control-Allow-Origin": "'http://localhost:3000'"
        #     }
        # )

        # gateway_response_5xx = apigateway.GatewayResponse(
        #     self, "GatewayResponse5XX",
        #     rest_api=api,
        #     response_type=apigateway.ResponseType.DEFAULT_5_XX,
        #     response_headers={
        #         "Access-Control-Allow-Origin": "'http://localhost:3000'"
        #     }
        # )
