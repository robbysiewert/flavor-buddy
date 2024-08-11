#!/bin/bash
# Build the React app
cd aws-site-frontend
npm run build
echo "building"

# Go back to the CDK stack directory and deploy
cd ../cdk-stack
cdk deploy
echo "deploying"

# Deploying will write the API Gateway endpoint to a file for the React app

# Build the React app with the updated API Gateway endpoint
cd ../aws-site-frontend
npm run build
echo "building"

# Go back to the CDK stack directory and deploy
cd ../cdk-stack
cdk deploy
echo "deploying"

