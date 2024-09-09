#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_stack.cdk_stack_stack import CdkStackStack
from cdk_stack.pipeline_stack import CicdPipelineStack

app = cdk.App()

# # CI/CD pipeline stack
# CicdPipelineStack(app, "CicdPipelineStack",
#     code_star_id="8e417a13-4164-4ce4-b1bf-deb77c7c6018", # TODO
#     )

# Application PreProd stack
CdkStackStack(app, "PreProdApplicationStack",
    environment="PreProd",
    env=cdk.Environment(account='021891619017', region='us-west-2')
    )

# Application Prod stack
CdkStackStack(app, "ProApplicationStack",
    environment="Prod",
    env=cdk.Environment(account='021891619017', region='us-west-2')
    )

app.synth()
