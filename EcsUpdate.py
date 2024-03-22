import json
import os
import boto3

# Constants
SUCCESS_STATUS_CODE = 200
ERROR_STATUS_CODE = 500

# AWS ECS Client
def get_ecs_client():
    region = os.environ.get("AWS_REGION")
    return boto3.client("ecs", region_name=region)

# Response helpers
def create_response(status, message):
    return {"statusCode": status, "body": json.dumps({"message": message})}

def success_response(message):
    return create_response(SUCCESS_STATUS_CODE, message)

def error_response(message):
    return create_response(ERROR_STATUS_CODE, message)

# ECS Functions
def contains_prod(arn):
    return "prod" in arn.lower()

def remove_prod_arns(arn_list):
    return [arn for arn in arn_list if not contains_prod(arn)]

def get_all_clusters_arns():
    try:
        ecs = get_ecs_client()
        response = ecs.list_clusters()
        return remove_prod_arns(response["clusterArns"])
    except Exception as e:
        print(e)
        return error_response(str(e))

def get_all_services_arns(cluster):
    try:
        ecs = get_ecs_client()
        response = ecs.list_services(cluster=cluster)
        return response["serviceArns"]
    except Exception as e:
        print(e)
        return error_response(str(e))

def update_ecs_service(desired_task, cluster, service):
    if "prod" in cluster.lower():
        raise Exception("Operation on production clusters is restricted")
    ecs = get_ecs_client()
    ecs.update_service(cluster=cluster, service=service, desiredCount=int(desired_task))
    print("Service updated successfully:", {"cluster": cluster, "service": service})

# Request processing functions
def parse_request_body(event):
    try:
        body = json.loads(event["body"])
        return body
    except:
        return event

def extract_clusters(body):
    return body["cluster_names"].split(',')

def extract_environments(body):
    return body['environment'].split(',')

def extract_desired_tasks(body):
    return body['desired_tasks']

# Lambda Handler
def lambda_handler(event, context):
    try:
        body = parse_request_body(event)
        environments = extract_environments(body)
        cluster_names = extract_clusters(body)
        desired_tasks = extract_desired_tasks(body)
        
        cluster_arns = get_all_clusters_arns()

        for cluster_name in cluster_names:
            for cluster_arn in cluster_arns:
                if (cluster_name == "all" or cluster_name in cluster_arn) and any(env in cluster_arn for env in environments):
                    service_arns = get_all_services_arns(cluster=cluster_arn)
                    for service_arn in service_arns:
                        update_ecs_service(desired_task=desired_tasks, cluster=cluster_arn, service=service_arn)
        
        return success_response("Successfully updated your ECS clusters")
    except Exception as e:
        print(e)
        return error_response(str(e))
