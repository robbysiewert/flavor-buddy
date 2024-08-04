from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    RemovalPolicy
)
from constructs import Construct

class CdkStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Example bucket to confirm successful deployment
        # bucket = s3.Bucket(self, "MyBucket",
        #     removal_policy=RemovalPolicy.DESTROY) # For testing purposes, remove for production   


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
        
        # Lambda function to interact with DynamoDB
        storage_function = _lambda.Function(
            self, 'MyFunction',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='storage_interactions.handler',
            code=_lambda.Code.from_asset('lambda_functions'),
            layers=[dependency]
        )

        # TODO grantReadWrite permissions and policies for dynamodb:GetItem etc

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