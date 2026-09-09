# AWS Inventory & Asset Management

A serverless inventory system built with AWS and Terraform.

The API accepts inventory records, stores them in DynamoDB, and sends an SNS notification when an item's stock reaches its minimum level.

## Architecture

![AWS Inventory Architecture](architecture.png)

```text
API Gateway → Lambda → DynamoDB
                  ↓
                 SNS
                  ↓
                Email
```

Terraform manages the AWS infrastructure.
CloudWatch is used for logging and troubleshooting.

## AWS Services

- Amazon API Gateway
- AWS Lambda
- Amazon DynamoDB
- Amazon SNS
- Amazon CloudWatch
- AWS IAM

Infrastructure is defined and deployed with Terraform.

## How It Works

1. An inventory record is sent to the API.
2. API Gateway receives the request and requires AWS IAM authorization.
3. Lambda validates the inventory data.
4. Lambda stores the record in DynamoDB.
5. Lambda checks the quantity against the minimum stock level.
6. If stock is low, Lambda publishes a notification to SNS.
7. SNS sends an email alert.
8. CloudWatch records Lambda activity for monitoring and troubleshooting.

## Infrastructure

Terraform is used to define and manage the AWS resources.

The infrastructure includes:

- DynamoDB table for inventory records
- IAM role and policies for Lambda
- Lambda function
- SNS topic and email subscription
- API Gateway HTTP API
- API Gateway IAM authorization
- Lambda permission for API Gateway
- CloudWatch logging

## Testing

The API was tested with both successful and invalid requests.

Tested scenarios include:

- Valid authenticated inventory submission
- Missing required fields
- Negative quantity validation
- Stock above the minimum level
- Stock at or below the minimum level
- IAM authorization
- Unauthorized API requests
- SNS low-stock email notifications
- CloudWatch logging

## Project Structure

```text
.
├ ─main.tf
├ ─lambda_function.py
├ ─test_api.py
└ ─README.md
```

main.tf contains the Terraform infrastructure.
lambda_function.py contains the Lambda application logic.
test_api.py is used to send authenticated requests to the API.

## Security

- API requests require AWS IAM authorization.
- Lambda uses an IAM role with permissions limited to the resources it needs.
- DynamoDB access is limited to the inventory table.
- SNS publishing is limited to the low-stock notification topic.
- Unauthorized API requests were tested and returned `403 Forbidden`.
- Invalid inventory data is rejected by Lambda validation.

## Cleanup

To remove the AWS resources created by Terraform:

```bash
terraform destroy
```

Review the plan before confirming the deletion.

## Lessons Learned

This project gave me hands-on experience with:

- Building and connecting serverless AWS services
- Managing AWS infrastructure with Terraform
- Using IAM to control access between AWS services
- Designing and testing an API
- Implementing input validation and error handling
- Using CloudWatch for troubleshooting
- Automating low-stock notifications with SNS
- Testing both successful and unauthorized requests

