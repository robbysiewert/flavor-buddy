#!/bin/bash
# Build the React app
cd aws-site-frontend
npm run build

# Go back to the CDK stack directory and deploy
cd ../cdk-stack
cdk deploy