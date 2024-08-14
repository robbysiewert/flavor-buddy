import boto3

# Initialize the Boto3 CloudFormation client
client = boto3.client('cloudformation')

response = client.describe_stacks(StackName='CdkStackStack')

# Initialize variables to hold the outputs
api_gateway_url = None
api_resource_path = None

# Extract the URL and resource path from the stack outputs
for output in response['Stacks'][0]['Outputs']:
    if output['OutputKey'] == 'ApiUrl':
        api_gateway_url = output['OutputValue']
    elif output['OutputKey'] == 'ApiResourcePath':
        api_resource_path = output['OutputValue']

if api_gateway_url and api_resource_path:
    # Write the API Gateway URL and Resource Path to the .env file
    with open("../aws-site-frontend/.env", "w") as env_file:
        env_file.write(f"REACT_APP_API_GATEWAY_URL={api_gateway_url}{api_resource_path.lstrip('/')}\n") # strip the / to avoid duplicate /
else:
    print("API Gateway URL or Resource Path not found in stack outputs.")
