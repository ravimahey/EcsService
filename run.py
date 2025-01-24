from lambda_function import lambda_handler

Event = {
  "httpMethod": "GET",
  "body": {
    "desired_tasks": "0",
    "cluster_names": "all",
    "environment" : "dev,stage"
  }
}
lambda_handler(event=Event,context="Hello World")