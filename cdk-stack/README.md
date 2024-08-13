# Technical Setup Instructions

The following contains technical information regarding replicating the AWS CDK repository (interacts with the React app but does not contain setup instructions regarding the frontend)  on your system. Some of this information is courtesy of AWS and not written by the owner of the project.

```
$ aws configure
```

Enter your access ID, secret, region

```
$ mkdir [directory-name]
$ cd [directory-name]
$ cdk init app --language python
```

```
$ pip install aws-cdk-lib
```

# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```
Or
```
% .venv\Scripts\activate
```
If using Git Bash on windows platform

```
% .venv/Scripts/activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

To add libraries or modules for the Lambda functions, add the package and version to lambda_dependencies.txt and run the following command. Zip the python directory, rename it lambda_layer, and place the zip file .

```
$ pip install -r lambda-dependencies.txt -t lambda_layer/python
```

Zip the "python" folder and place in the folder cdk-stack, name the zip file lambda_layer.zip

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Build the React app and deploy the stack (Git Bash)
```
$ ./deploy.sh
```


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
