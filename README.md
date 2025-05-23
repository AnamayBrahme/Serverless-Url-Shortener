# Serverless URL Shortener with AWS CDK and LocalStack

This project deploys a serverless URL shortener locally using AWS CDK and LocalStack. It includes Lambda functions, API Gateway, and DynamoDB for a complete URL shortening and redirection service.

## Features

- **Shorten URLs:** Creates short URLs for long URLs.
- **Redirect URLs:** Redirects short URLs to their original long URLs.
- **Local Development:** Uses LocalStack for local development and testing.
- **Serverless Architecture:** Leverages AWS Lambda, API Gateway, and DynamoDB.

![ChatGPT Image Apr 16, 2025, 10_10_18 PM](https://github.com/user-attachments/assets/19d39308-47e2-4c28-878b-655badc4f70a)



## Prerequisites

- Python 3.7+
- AWS CDK (`npm install -g aws-cdk`)
- LocalStack (running locally via Docker or `localstack-cli`)
- AWS CLI configured for LocalStack:
```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566
```

## 📁 Project Structure

```
.
├── app.py                  # CDK App Entry Point
├── cdk.json                # CDK Configuration
├── lambda/
│   ├── shorten.py          # Lambda function to create short URLs
│   └── redirect.py         # Lambda function to handle redirection
├── sample_app1/
│   └── sample_app1_stack.py # CDK Stack logic
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .venv/                  # Python virtual environment (created after setup)
```

## 🔗 API Endpoints

### POST /shorten
Creates a short URL.

**Request Body:**
```json
{
  "long_url": "https://example.com"
}
```

**Response:**
```json
{
  "short_url": "https://<api>.amazonaws.com/prod/abc123"
}
```

### GET /{short_code}
Redirects to the original long URL.

**Example:**
```bash
curl -L https://<api>.amazonaws.com/prod/abc123
```

## 🚀 Getting Started

### 1. Set up virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate.bat  # On Windows
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Bootstrap your CDK environment (only once per account/region):
```bash
cdk bootstrap
```

### 4. Synthesize the CloudFormation template:
```bash
cdk synth
```

### 5. Deploy the stack:
```bash
cdk deploy
```

Once deployed, you'll get the API Gateway endpoint URL to test your service.

## 📚 Useful CDK Commands

| Command       | Description                                           |
|---------------|-------------------------------------------------------|
| `cdk ls`      | List all stacks in the app                            |
| `cdk synth`   | Emit the synthesized CloudFormation template          |
| `cdk deploy`  | Deploy the stack to your AWS account (or LocalStack)  |
| `cdk diff`    | Compare deployed stack with current state             |
| `cdk destroy` | Destroy the deployed stack                            |


##  TODO
- Add support for custom short codes
- Add TTL (Time to Live) support to DynamoDB items
- Add a frontend/CLI client
- Add monitoring (e.g., CloudWatch Alarms, Dashboards)

##  Security Measures Implemented
- 1. **DynamoDB Encryption at Rest:**
     DynamoDB is encrypted using AWS-managed KMS keys (AES-256).
     Encryption is enabled by default to protect data stored in the table.
- 2. **Least Privilege IAM Roles:**
    - Custom IAM roles are used for Lambda functions.
    - Roles have limited permissions to perform only necessary actions.
    - Access limited to the specific DynamoDB table ARN.
    - AWSLambdaBasicExecutionRole used for CloudWatch logging only
- 3. **VPC & Endpoint Isolation:**
    - Lambda functions are deployed inside a dedicated VPC.
    - DynamoDB Gateway VPC Endpoint is used for private access (no public internet traffic for D B operations).
- 4. **Future Enhancements (Planned)**
    - Implement Dead Letter Queues (DLQs) for failed Lambda invocations.
    - Add input validation & sanitation in Lambda code.
    - Enable CORS policy & custom error responses for API Gateway.

## Local Development with LocalStack

Ensure LocalStack is running before you run `cdk deploy`. You can start LocalStack with Docker:

```bash
docker run --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack
```

⚠️ Make sure to point AWS CLI and SDKs to http://localhost:4566.
