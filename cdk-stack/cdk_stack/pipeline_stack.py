from aws_cdk import (
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam,
    RemovalPolicy,
    Stack,
    StackProps,
)
from constructs import Construct

class CicdPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, props: StackProps, code_star_id: str) -> None:
        super().__init__(scope, id, props)

        # CodeBuild project for unit tests
        unittest_code_build = codebuild.PipelineProject(
            self,
            "CodeBuildUnittest",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "commands": [
                            "echo $CODE_COMMIT_ID",
                            "pip install -r requirements.txt",
                        ],
                    },
                    "build": {
                        "commands": [
                            "python -m pytest -s -v unittests/test_lambda_logic.py",
                        ],
                    },
                },
                "artifacts": {},
            }),
        )

        # IAM Role for integration tests
        role = iam.Role(
            self,
            "RoleForIntegrationTest",
            role_name="RoleForIntegrationTestDev",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
        )

        role.attach_inline_policy(
            iam.Policy(
                self,
                "CodeBuildReadCloudFormation",
                policy_name="CodeBuildReadCloudFormation",
                statements=[
                    iam.PolicyStatement(
                        actions=["cloudformation:*"],
                        resources=["*"],
                    ),
                ],
            )
        )

        # CodeBuild project for integration tests
        integtest_code_build = codebuild.PipelineProject(
            self,
            "CodeBuildIntegTest",
            role=role,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "commands": [
                            "SERVICE_URL=$(aws cloudformation describe-stacks --stack-name PreProdApplicationStack --query \"Stacks[0].Outputs[?OutputKey=='UrlPreProd'].OutputValue\" --output text)",
                            "echo $SERVICE_URL",
                            "pip install -r requirements.txt",
                        ],
                    },
                    "build": {
                        "commands": ["python -m pytest -s -v integtests/test_service.py"],
                    },
                },
                "artifacts": {},
            }),
        )

        # CodeBuild project for CDK template
        cdk_code_build = codebuild.PipelineProject(
            self,
            "CodeBuildCdk",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "commands": ["npm install"],
                    },
                    "build": {
                        "commands": ["npm run cdk synth -- -o dist"],
                    },
                },
                "artifacts": {
                    "base-directory": "dist",
                    "files": ["*.template.json"],
                },
            }),
        )

        # Artifacts
        source_output = codepipeline.Artifact("SourceCode")
        cdk_build_output = codepipeline.Artifact("CdkBuildOutput")
        unittest_code_build_output = codepipeline.Artifact("UnittestBuildOutput")
        pre_prod_output = codepipeline.Artifact("PreProductOutput")

        # Source Action (GitHub)
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub",
            owner="cdk-entest",
            connection_arn=f"arn:aws:codestar-connections:{self.region}:{self.account}:connection/{code_star_id}",
            repo="cicd-integration-test",
            branch="master",
            output=source_output,
        )

        # Build Actions
        unittest_build_action = codepipeline_actions.CodeBuildAction(
            environment_variables={
                "CODE_COMMIT_ID": {
                    "value": source_action.variables.commit_id,
                },
            },
            action_name="DoUnitest",
            project=unittest_code_build,
            input=source_output,
            outputs=[unittest_code_build_output],
        )

        cdk_build = codepipeline_actions.CodeBuildAction(
            action_name="BuildCfnTemplate",
            project=cdk_code_build,
            input=source_output,
            outputs=[cdk_build_output],
        )

        # Deploy PreProd
        deploy_pre_prod = codepipeline_actions.CloudFormationCreateUpdateStackAction(
            action_name="DeployPreProdApplication",
            template_path=cdk_build_output.at_path("PreProdApplicationStack.template.json"),
            stack_name="PreProdApplicationStack",
            admin_permissions=True,
        )

        # Integration Test Action
        integtest_build_action = codepipeline_actions.CodeBuildAction(
            action_name="IntegTest",
            project=integtest_code_build,
            input=source_output,
        )

        # Deploy Prod
        deploy_prod = codepipeline_actions.CloudFormationCreateUpdateStackAction(
            action_name="DeployProd",
            template_path=cdk_build_output.at_path("ProApplicationStack.template.json"),
            stack_name="ProApplicationStack",
            admin_permissions=True,
        )

        # Pipeline definition
        pipeline = codepipeline.Pipeline(
            self,
            "CicdPipelineDemo",
            pipeline_name="CicdPipelineDemo",
            cross_account_keys=False,
            stages=[
                {
                    "stageName": "Source",
                    "actions": [source_action],
                },
                {
                    "stageName": "Unittest",
                    "actions": [unittest_build_action],
                },
                {
                    "stageName": "BuildTemplate",
                    "actions": [cdk_build],
                },
                {
                    "stageName": "DeployPreProd",
                    "actions": [deploy_pre_prod],
                },
                {
                    "stageName": "IntegTest",
                    "actions": [integtest_build_action],
                },
                {
                    "stageName": "DeployProd",
                    "actions": [deploy_prod],
                },
            ],
        )

        # Destroy artifact bucket when deleting pipeline
        pipeline.artifact_bucket.apply_removal_policy(RemovalPolicy.DESTROY)
