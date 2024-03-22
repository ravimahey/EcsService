import json
import os
import boto3
def response_object(status, message):
    return {"statusCode": status, "body": json.dumps({"message": message})}

def response(status, message):
    if status == 200:
        return response_object(status, message)
    else:
        return response_object(status, message)

def get_client():
    region = os.environ.get("AWS_REGION")
    print(region)
    ecs = boto3.client(
        "ecs",
        region_name=region,
    )
    return ecs

def contains_prod(arn):
    return "prod" in arn.lower()

def remove_prod_arns(arn_list):
    new_arn_list = [arn for arn in arn_list if not contains_prod(arn)]
    return new_arn_list

def get_arn_by_environment_tag(arn_list, environment):
    new_arn_list = set()
    for arn in arn_list:
        if environment in arn:
            new_arn_list.add(arn)
    return new_arn_list
    
def get_all_clusters_arn():
    ecs = get_client()
    try:
        cluster = ecs.list_clusters()
        clusters_arns = cluster["clusterArns"]
        return remove_prod_arns(clusters_arns)
    except Exception as e:
        print(e)
        return response(500, str(e))
    
def get_all_services_arn(cluster):
    ecs = get_client()
    try:
        response = ecs.list_services(cluster=cluster)
        services = response["serviceArns"]
        return services
    except Exception as e:
        print(e)
        return response(500, str(e))
    
def update_ecs_service(desired_task, cluster, service):
    if "prod" in cluster.lower():
        raise Exception("Operation on production clusters is restricted")
    print("Updating ECS Service")
    # Create ECS client
    ecs = get_client()
    # Update service with desired task count
    updated = ecs.update_service(
        cluster=cluster, service=service, desiredCount=int(desired_task)
    )
    print("Service updated successfully:", {"cluster":cluster, "service": service})
def request_object(event):
    try:
        body = json.loads(event["body"])
        return body
    except:
        return event
def get_deisred_tasks(body):
    return body['desired_tasks']
def extract_clusters(body):
    clusters = body["cluster_names"].split(',')
    return clusters
def get_environment(body):
    env = body['environment'].split(',')
    return env

def lambda_handler(event, context):
    try:
        body = request_object(event)
        environments = get_environment(body)
        cluster_names = extract_clusters(body)
        desired_tasks = get_deisred_tasks(body)            
                
        cluster_arns = get_all_clusters_arn()

        for cluster_name in cluster_names:
            if cluster_name == "all":
                for cluster_arn in cluster_arns:
                    if "dev" in environments and "dev" in cluster_arn:
                        services_arns = get_all_services_arn(cluster_arn)
                        for service_arn in services_arns:
                            update_ecs_service(desired_task=desired_tasks,cluster=cluster_arn,service=service_arn)
                    elif "stage" in environments and "stage" in cluster_arn:
                        services_arns = get_all_services_arn(cluster_arn)
                        for service_arn in services_arns:
                            update_ecs_service(desired_task=desired_tasks,cluster=cluster_arn,service=service_arn)
            else:
                for cluster_arn in cluster_arns:
                    if cluster_name in cluster_arn and (("dev" in environments and "dev" in cluster_arn) or ('stage' in environments and 'stage' in cluster_arn) ):
                        service_arns = get_all_services_arn(cluster=cluster_arn)
                        for service_arn in service_arns:
                            update_ecs_service(desired_task=desired_tasks,cluster=cluster_arn,service=service_arn)         
        return response(200, "Successfully Update your ECS clusters")
    except Exception as e:
        print(e)
        return response(500, str(e))


