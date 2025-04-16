from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_cloudwatch as cloudwatch,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_apigateway as apigateway,
)


class SampleApp1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "UrlShortenerVpc",
            max_azs=2,
            nat_gateways=1
        )
        # Optional: Add VPC Endpoint for DynamoDB
        vpc.add_gateway_endpoint("DynamoDbEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.DYNAMODB
        )

        #  Create a DynamoDB table to store short codes and original URLs
        dynamodb_table = dynamodb.Table(
            self, "UrlTable",
            partition_key=dynamodb.Attribute(
                name="sht_url_table",  # Partition key name
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST  # Cost-efficient pay-per-request mode
        )
        
        # Define least privilege IAM role for Lambda (optional advanced control)
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        # Give the role permission to write to DynamoDB
        dynamodb_table.grant_read_write_data(lambda_role)


        #  Define Lambda function for shortening URLs
        shorten_lambda = _lambda.Function(
            self, "ShortenFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,  # Python 3.9 runtime
            handler="shorten.handler",  # Path to the function's handler
            code=_lambda.Code.from_asset("lambda"),  # Directory containing your lambda/shorten.py
            environment={
                "TABLE_NAME": dynamodb_table.table_name  # Pass table name to Lambda via environment variable
            },
            vpc=vpc,
            role=lambda_role
        )

        # 🔧 Define Lambda function for redirecting to original URL
        redirect_lambda = _lambda.Function(
            self, "RedirectFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="redirect.handler",  # Path to lambda/redirect.py
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": dynamodb_table.table_name
            },
            vpc=vpc,
            role=lambda_role
        )

        dynamodb_table.grant_read_data(redirect_lambda)       # Redirect function only needs read access

        #  Grant appropriate permissions to the Lambda functions
        dynamodb_table.grant_read_write_data(shorten_lambda)  # Shorten function needs full access
        

        #  API Gateway setup
        api = apigateway.RestApi(
            self, "UrlShortenerApi",
            rest_api_name="URL Shortener Service",
            deploy_options=apigateway.StageOptions(
                throttling_rate_limit=10,
                throttling_burst_limit=2
            )
        )
        
        #  CloudWatch Alarm for monitoring shorten Lambda
        shorten_lambda_error_alarm = cloudwatch.Alarm(
            self, "ShortenLambdaErrors",
            metric=shorten_lambda.metric(metric_name="Errors",period=Duration.minutes(1),statistic="Sum"),
            threshold=1,
            evaluation_periods=1,
            alarm_description="Alarm if shorten lambda has more than 1 error in 1 minute"
        )

        
        
        #  POST /shorten endpoint
        shorten_resource = api.root.add_resource("shorten")
        shorten_integration = apigateway.LambdaIntegration(shorten_lambda)
        shorten_resource.add_method("POST", shorten_integration)

        # GET /{short_code} endpoint
        redirect_resource = api.root.add_resource("{short_code}")
        redirect_integration = apigateway.LambdaIntegration(redirect_lambda)
        redirect_resource.add_method("GET", redirect_integration)


