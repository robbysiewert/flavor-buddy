import boto3

# Initialize the Boto3 CloudFormation client
client = boto3.client('cloudformation')

response = client.describe_stacks(StackName='CdkStackStack')

# Extract the URL from the stack outputs
api_gateway_url = None
for output in response['Stacks'][0]['Outputs']:
    if output['OutputKey'] == 'ApiUrl':
        api_gateway_url = output['OutputValue']
        break

if api_gateway_url:
    # Write the API Gateway URL to the .env file for the React app to read
    with open("../aws-site-frontend/.env", "w") as env_file:
        env_file.write(f"REACT_APP_API_GATEWAY_URL={api_gateway_url}\n")
else:
    print("API Gateway URL not found in stack outputs.")
