"""Module providing resources for defining AWS infrastructure to deploy as code"""
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_iam as iam,
    RemovalPolicy
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
        items = api.root.add_resource("storage") # /storage
        items.add_method("GET")
        items.add_method("POST")
        items.add_method("PUT")
        items.add_method("DELETE")