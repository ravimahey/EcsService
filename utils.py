import json


def build_response(status_code, message, exception=None):
    """Build response object."""
    response_body = {"message": message}
    if exception:
        response_body["error"] = str(exception)
    return {"statusCode": status_code, "body": json.dumps(response_body)}


def build_cluster_status(cluster,services:[]):
    return {"cluster": cluster, services:services}


def build_service_status(service,running,pending):
    return {"service":service,"running":running,"pending":pending}


def get_name_from_arn(arn):
    name = arn.split('/')[-1]
    return name