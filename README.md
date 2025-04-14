Markdown

# Serverless URL Shortener with AWS CDK and LocalStack

This project deploys a serverless URL shortener locally using AWS CDK and LocalStack. It includes Lambda functions, API Gateway, and DynamoDB for a complete URL shortening and redirection service.

## Features

-   **Shorten URLs:** Creates short URLs for long URLs.
-   **Redirect URLs:** Redirects short URLs to their original long URLs.
-   **Local Development:** Uses LocalStack for local development and testing.
-   **Serverless Architecture:** Leverages AWS Lambda, API Gateway, and DynamoDB.

## Prerequisites

-   Python 3.7+
-   AWS CDK (`npm install -g aws-cdk`)
-   LocalStack (running locally, e.g., via Docker or `localstack-cli`)
-   AWS CLI configured for LocalStack:

    ```bash
    export AWS_ACCESS_KEY_ID=test
    export AWS_SECRET_ACCESS_KEY=test
    export AWS_DEFAULT_REGION=us-east-1
    export AWS_ENDPOINT_URL=http://localhost:4566
    ```

## Project Structure

.
├── app.py                  # CDK App Entry Point
├── cdk.json                # CDK Configuration
├── lambda/
│   ├── shorten.py          # Lambda function to create short URLs
│   └── redirect.py         # Lambda function to handle redirection
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .venv/                  # Python virtual environment (created after setup)
## API Endpoints

### POST /shorten

Creates a short URL.

**Request Body:**

```json
{
  "long_url": "[https://example.com](https://example.com)"
}
Response:

JSON

{
  "short_url": "https://<api>[.amazonaws.com/prod/abc123](https://.amazonaws.com/prod/abc123)"
}
GET /{short_code}
Redirects to the original long URL.

Example:

Bash

curl -L https://<api>[.amazonaws.com/prod/abc123](https://.amazonaws.com/prod/abc123)
Getting Started
Set up virtual environment:

Bash

python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate.bat # On Windows
Install dependencies:

Bash

pip install -r requirements.txt
Bootstrap your environment (one-time setup per account/region):

Bash

cdk bootstrap
Deploy the stack:

Bash

cdk deploy
This will deploy your Lambda functions, API Gateway, and DynamoDB table.

Development & Testing
Synthesize CloudFormation template:

Bash

cdk synth
Destroy the stack:

Bash

cdk destroy
Useful CDK Commands
cdk ls – List all stacks
cdk synth – Emits the synthesized CloudFormation template
cdk deploy – Deploys the stack
cdk diff – Compares deployed stack with current state
cdk docs – Opens CDK documentation
TODO
Add support for custom short codes.
Add TTL (Time to Live) support to DynamoDB items.
Add a frontend/CLI client.
Add monitoring (e.g., CloudWatch Alarms, Dashboards).
