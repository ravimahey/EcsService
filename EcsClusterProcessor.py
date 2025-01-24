from EcsManage import ECSManager
from Constants import Operations
from utils import build_response
from Constants import StatusCodes


class ClusterProcessor:
    def __init__(self, ecs_manager):
        self.ecs_manager:ECSManager = ECSManager()

    def process_clusters(self, cluster_names, environments, desired_tasks,operation:Operations=Operations.GET_STATUS):
        """Process ECS clusters."""
        cluster_arns = self.ecs_manager.get_all_clusters_arns()
        response = []
        for cluster_name in cluster_names:
            for cluster_arn in cluster_arns:
                if self.should_process_cluster(cluster_name, cluster_arn, environments):
                    if operation == Operations.UPDATE_SERVICE:
                        self.ecs_manager.update_cluster_services(cluster_arn, desired_tasks)
                        response = build_response(StatusCodes.SUCCESS_STATUS_CODE,f"Successfully update {cluster_name}")
                    elif operation == Operations.GET_STATUS:
                        response.append(self.ecs_manager.check_status(cluster_arn))
        return response

    @staticmethod
    def should_process_cluster(cluster_name, cluster_arn, environments):
        """Check if the cluster should be processed."""
        return (cluster_name == "all" or cluster_name in cluster_arn) and any(env in cluster_arn for env in environments) and cluster_name and cluster_arn

