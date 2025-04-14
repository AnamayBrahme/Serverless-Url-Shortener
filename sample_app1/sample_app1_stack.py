from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3 as s3,  # Unused in current code, can remove if not needed
    aws_lambda as _lambda,
    aws_iam as iam,  # Unused in current code, can remove if not needed
    aws_sqs as sqs,  # Unused in current code, can remove if not needed
    aws_sns as sns,  # Unused in current code, can remove if not needed
    aws_dynamodb as dynamodb,
    aws_sns_subscriptions as subs,  # Unused in current code, can remove if not needed
    aws_apigateway as apigateway,
)


class SampleApp1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #  Create a DynamoDB table to store short codes and original URLs
        dynamodb_table = dynamodb.Table(
            self, "UrlTable",
            partition_key=dynamodb.Attribute(
                name="sht_url_table",  # Partition key name
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST  # Cost-efficient pay-per-request mode
        )
        
        #  Define Lambda function for shortening URLs
        shorten_lambda = _lambda.Function(
            self, "ShortenFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,  # Python 3.9 runtime
            handler="shorten.handler",  # Path to the function's handler
            code=_lambda.Code.from_asset("lambda"),  # Directory containing your lambda/shorten.py
            environment={
                "TABLE_NAME": dynamodb_table.table_name  # Pass table name to Lambda via environment variable
            }
        )

        # 🔧 Define Lambda function for redirecting to original URL
        redirect_lambda = _lambda.Function(
            self, "RedirectFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="redirect.handler",  # Path to lambda/redirect.py
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": dynamodb_table.table_name
            }
        )

        #  Grant appropriate permissions to the Lambda functions
        dynamodb_table.grant_read_write_data(shorten_lambda)  # Shorten function needs full access
        dynamodb_table.grant_read_data(redirect_lambda)       # Redirect function only needs read access

        #  Set up the REST API using Amazon API Gateway
        api = apigateway.RestApi(
            self, "UrlShortenerApi",
            rest_api_name="URL Shortener Service"  # Friendly name
        )

        # ➕ Create the POST /shorten endpoint
        shorten_resource = api.root.add_resource("shorten")  # Add /shorten path
        shorten_integration = apigateway.LambdaIntegration(shorten_lambda)  # Connect to shorten Lambda
        shorten_resource.add_method("POST", shorten_integration)  # Allow POST requests

        # 🔁 Create the GET /{short_code} redirect endpoint
        redirect_resource = api.root.add_resource("{short_code}")  # Path parameter for short code
        redirect_integration = apigateway.LambdaIntegration(redirect_lambda)  # Connect to redirect Lambda
        redirect_resource.add_method("GET", redirect_integration)  # Allow GET requests
