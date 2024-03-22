import json
import os
import boto3

def build_response(status_code, message, exception=None):
    """Build response object."""
    response_body = {"message": message}
    if exception:
        response_body["error"] = str(exception)

    return {"statusCode": status_code, "body": json.dumps(response_body)}

class ECSManager:
    def __init__(self):
        self.ecs_client = self._get_ecs_client()

    def _get_ecs_client(self):
        region = os.environ.get("AWS_REGION")
        return boto3.client("ecs", region_name=region)

    def _contains_prod(self, arn):
        return "prod" in arn.lower()

    def remove_prod_arns(self, arn_list):
        return [arn for arn in arn_list if not self._contains_prod(arn)]

    def get_all_clusters_arns(self):
        try:
            response = self.ecs_client.list_clusters()
            return self.remove_prod_arns(response["clusterArns"])
        except Exception as e:
            print(e)
            return self._error_response(str(e))

    def get_all_services_arns(self, cluster):
        try:
            response = self.ecs_client.list_services(cluster=cluster)
            return response["serviceArns"]
        except Exception as e:
            print(e)
            return self._error_response(str(e))

    def update_ecs_service(self, desired_task, cluster, service):
        if "prod" in cluster.lower():
            raise Exception("Operation on production clusters is restricted")
        self.ecs_client.update_service(cluster=cluster, service=service, desiredCount=int(desired_task))
        print("Service updated successfully:", {"cluster": cluster, "service": service})

    def _error_response(self, message):
        return build_response(500, message)

class LambdaHandler:
    def __init__(self, event):
        self.event = event
        self.ecs_manager = ECSManager()
        self.cluster_processor = ClusterProcessor(self.ecs_manager)

    def _parse_request_body(self):
        """Parse the request body."""
        try:
            body = json.loads(self.event["body"])
            return body
        except Exception as e:
            print(e)
            return self.event

    def extract_clusters(self, body):
        """Extract cluster names from the request body."""
        return body.get("cluster_names", "").split(',')

    def extract_environments(self, body):
        """Extract environments from the request body."""
        return body.get("environment", "").split(',')

    def extract_desired_tasks(self, body):
        """Extract desired tasks from the request body."""
        return body.get("desired_tasks", "")

    def handle_request(self):
        """Handle Lambda request."""
        try:
            body = self._parse_request_body()
            environments = self.extract_environments(body)
            cluster_names = self.extract_clusters(body)
            desired_tasks = self.extract_desired_tasks(body)

            self.cluster_processor.process_clusters(cluster_names, environments, desired_tasks)

            return build_response(200, "Successfully updated your ECS clusters")
        except Exception as e:
            print(e)
            return build_response(500, "Internal Server Error", e)

def lambda_handler(event, context):
    """Lambda handler function."""
    handler = LambdaHandler(event)
    return handler.handle_request()
