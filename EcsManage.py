import json
import os
import boto3
from Constants import (Prefix)
from utils import (build_response,
                   get_name_from_arn,
                   build_service_status)


class ECSManager:
    def __init__(self):
        self.ecs_client = self._get_ecs_client()

    @staticmethod
    def _get_ecs_client():
        region = os.environ.get("AWS_REGION")
        return boto3.client('ecs', region_name=region)

    @staticmethod
    def _contains_restricted(arn):
        for restricted in Prefix.RESTRICTED.value:
            return restricted.lower() in arn.lower()

    def remove_restricted_arns(self, arn_list):
        return [arn for arn in arn_list if not self._contains_restricted(arn)]

    def get_all_clusters_arns(self):
        try:
            response = self.ecs_client.list_clusters()
            return self.remove_restricted_arns(response["clusterArns"])
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
        if self._contains_restricted(cluster):
            raise Exception("Operation on this clusters is restricted")
        self.ecs_client.update_service(cluster=cluster, service=service, desiredCount=int(desired_task))
        cluster_name = get_name_from_arn(cluster)
        service_name = get_name_from_arn(service)
        print("Service updated successfully:", {"cluster": cluster_name, "service": service_name})

    def update_cluster_services(self, cluster_arn, desired_tasks):
        """Update services in the cluster."""
        service_arns = self.get_all_services_arns(cluster=cluster_arn)
        for service_arn in service_arns:
            self.update_ecs_service(desired_task=desired_tasks, cluster=cluster_arn, service=service_arn)

    def check_status(self,cluster):
        services = self.get_all_services_arns(cluster)
        response = self.ecs_client.describe_services(
            cluster=cluster,
            services=services
        )
        cluster_name = get_name_from_arn(cluster)
        cluster_status = {"cluster": cluster_name, "services":[]}
        if 'services' in response and len(response['services']) > 0:
            for service in response['services']:
                service_name = service.get('serviceName','')
                running_count = service.get('runningCount', 0)
                pending_count = service.get('pendingCount', 0)
                cluster_status['services'].append(build_service_status(
                    service=service_name,
                    running=running_count,
                    pending=pending_count
                ))
        return cluster_status

    @staticmethod
    def _error_response(message):
        return build_response(500, message)