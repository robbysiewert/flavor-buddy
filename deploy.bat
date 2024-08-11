@echo off
REM Build the React app
cd aws-site-frontend
npm run build
if %ERRORLEVEL% NEQ 0 (
  echo "Build failed, aborting deployment."
  exit /b %ERRORLEVEL%
)
echo "building"

REM Go back to the CDK stack directory and deploy
cd ../cdk-stack
cdk deploy
echo "deploying"

REM Deploying will write the API Gateway endpoint to a file for the React app

REM Build the React app with the updated API Gateway endpoint
cd ../aws-site-frontend
npm run build
echo "building"

REM Go back to the CDK stack directory and deploy
cd ../cdk-stack
cdk deploy
echo "deploying"

