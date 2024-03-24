from utils import build_response
from Constants import (StatusCodes,Operations)
from EcsManage import ECSManager
import json
from EcsClusterProcessor import ClusterProcessor


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
            return self.event["body"]

    @staticmethod
    def extract_clusters(body):
        """Extract cluster names from the request body."""
        return body.get("cluster_names", "").split(',')

    @staticmethod
    def extract_environments( body):
        """Extract environments from the request body."""
        return body.get("environment", "").split(',')

    @staticmethod
    def extract_desired_tasks( body):
        """Extract desired tasks from the request body."""
        return body.get("desired_tasks", "")

    def handle_request(self,operation:Operations = Operations.GET_STATUS):
        """Handle Lambda request."""
        try:
            body = self._parse_request_body()
            environments = self.extract_environments(body)
            cluster_names = self.extract_clusters(body)
            desired_tasks = self.extract_desired_tasks(body)
            process = self.cluster_processor.process_clusters(
                cluster_names=cluster_names,
                environments=environments,
                desired_tasks= desired_tasks,
                operation=operation
            )

            return process
        except Exception as e:
            print(e)
            return build_response(StatusCodes.ERROR_STATUS_CODE, "Internal Server Error", e)