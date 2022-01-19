# Standard library imports
from logging import log
import traceback

# Third party imports
import ujson
from pydash import py_
from loguru import logger

# User based imports
from engine import dynamodb
from utils import utils

# Constants
GLOBAL = 'routes_policy'
POLICY_NAME = 'PubSubPolicy'


def handle_request(event, body):
    """[it handle request based on routes]

    Args:
        event ([dict]): [incoming event from api gateway]
        body ([dict]): [incoming body payload from api gateway]

    Returns:
        [dict, status_code]: [return response and status code]
    """

    response = None
    status_code = 404
    logger.debug(f'ROUTE {event["resource"]}')

    try:
        if event['resource'] == '/security/attach-iot-policy':
            idenity_id = event['queryStringParameters']['identityId']
            policy_status = utils.attach_iot_policy(policy_name=POLICY_NAME, identity_id=idenity_id)
            logger.success(ujson.dumps(policy_status))
            response = {
                'message': policy_status
            }
            status_code = 200

    except Exception as error:
        response = {
            'status': 'failure',
            'component': f'{GLOBAL}.py',
            'exception': str(error),
            'traceback': traceback.format_exc()
        }
        status_code = 500
        logger.opt(exception=True).error('API_FAILURE')

    return {"message": "invalid route"} if not response else response, status_code
