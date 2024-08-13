#!/bin/bash

# Initial deployment: the React app will not have the API Gateway URL
# If this is the initial deployment, pass argument "2" to deploy twice

DEPLOYMENTS=1
if [ "$1" == "2" ]; then
    DEPLOYMENTS=2
fi

for ((i = 1; i <= DEPLOYMENTS; i++)); do

    # Navigate to the React frontend directory
    cd aws-site-frontend

    # Build the React application
    echo "Building..."
    npm run build > /dev/null 2>&1

    # Navigate to the CDK stack directory
    cd ../cdk-stack

    # Deploy the CDK stack
    echo "Deploying..."
    cdk deploy

    # Run the script to propagate the API URL
    echo "Propagating API URL..."
    python propagate_api_url.py

    cd .. # return to the root directory
done

echo "Deployment Complete"

