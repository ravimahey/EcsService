from LambdaHandler import LambdaHandler
from utils import build_response
from Constants import Operations


def lambda_handler(event, context):
    if 'httpMethod' in event:
        http_method = event['httpMethod']
        lambda_handler_ecs: LambdaHandler = LambdaHandler(event)
        if http_method == 'GET':
            print("______________________get request__________________________")
            response = lambda_handler_ecs.handle_request(
                operation=Operations.GET_STATUS
            )
            print("Cluster_status: ", response )
            return response
        # Handle GET request
        elif http_method == 'POST':
            print("_______________________post request________________________")
            request = lambda_handler_ecs.handle_request(
                operation=Operations.UPDATE_SERVICE
            )
            # Handle POST request
            return request
        else:
            # Handle other HTTP methods
            return build_response(405, 'Unsupported HTTP method')
    else:
        # Handle case where HTTP method is not provided
        return build_response(400, 'No HTTP method provided')
    
