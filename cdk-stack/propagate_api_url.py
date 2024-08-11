import subprocess

# Get API Gateway URL endpoint
stack_name = "CdkStackStack"
result = subprocess.run(
    ["aws", "cloudformation", "describe-stacks",
    "--stack-name", stack_name,
    "--query", "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue",
    "--output", "text"],
    capture_output=True,
    text=True
)
api_gateway_url = result.stdout.strip()

# Write the API Gateway URL to a .env file for the React app to read
with open("../aws-site-frontend/.env", "w") as env_file:
    env_file.write(f"REACT_APP_API_GATEWAY_URL={api_gateway_url}\n")