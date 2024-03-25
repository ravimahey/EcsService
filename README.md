# ECS Infrastructure Scaling using Lambda function

This Python utility is designed to upscale or downscale ECS (Amazon Elastic Container Service) services, providing functionality to manage containerized applications efficiently. It utilizes Boto3, the AWS SDK for Python, along with AWS Lambda functions.

## Key Features

1. **Upscale and Downscale ECS Services**: Automatically adjust the desired task count for ECS services based on specified criteria such as CPU or memory utilization.

2. **Retrieve ECS Service Information**: Obtain detailed information about ECS services including the number of tasks pending and running, aiding in monitoring and management.

3. **Production Environment Protection**: Implements safeguards to restrict updates to ECS services in production environments, minimizing risks and ensuring stability.

## Benefits

1. **Cost Optimization**: Efficiently manage ECS resources to optimize costs by scaling up or down based on demand, avoiding unnecessary expenses.

2. **On-Demand Development and Staging Environments**: Enable on-demand scaling for development and staging environments, allowing flexibility and agility in testing and development workflows.

## Usage

There are two way to use this use this utility

    1. Clone the repository and execute the utility as a standard Python project, allowing for customization and direct usage.
    2. Configuration with AWS Lambda Function:
     


### Prerequisites for Lambda functoin

- AWS account with appropriate permissions to access ECS services.
- Lambda function with the appropriate IAM role.
- Postman for testing API endpoints. 

### Configuration with Lambda function

- Set up a Lambda function with the provided IAM role.
```commandline
{
    "Effect": "Allow",
    "Action": [
        "ecs:ListServices",
        "ecs:ListTasks",
        "ecs:ListContainerInstances",
        "ecs:ListTaskDefinitions",
        "ecs:ListClusters",
        "ecs:DescribeClusters",
        "ecs:DescribeServices",
        "ecs:DescribeTaskDefinition",
        "ecs:DescribeTasks",
        "ecs:UpdateService"
    ],
    "Resource": "*"
}
```

- Attach an API Gateway to the Lambda function for external access. Consider implementing additional security measures such as API keys or IAM access.
- Utilize HTTP POST/GET requests to interact with the API Gateway endpoint.
- Provide the request body with parameters such as desired task count, cluster names, and environment details.

Example Request Body for Postman:
```commandline
Use body object in case of Post man
{
    "desired_tasks": "0",
    "cluster_names": "all",
    "environment" : "dev,stage"
}


```

## Production Resources Safty:
To ensure safety and prevent unintended actions, the Prefix class has been implemented with specific keywords designated for different access levels.

**ALLOWED**: This includes a list containing only the wildcard '*', which essentially allows unrestricted access to all resources.

**RESTRICTED**: This list contains 'prod', indicating restricted access specifically to production resources.
```commandline
to change the  Constants.py you can chage safeguard

class Prefix(Enum):
    ALLOWED = ['*']
    RESTRICTED = ['prod']
```
## Summary
The ECS Infrastructure Scaling Utility is a Python tool for automating ECS service scaling based on resource utilization. It offers monitoring features and safeguards for production environments, optimizing costs and enhancing flexibility.

