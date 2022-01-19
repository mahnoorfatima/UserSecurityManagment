# Third party imports
import ujson
from loguru import logger

# User based imports
from utils import generate_response
from routes import routes_policy as routes
from utils import logger_config

# init logger
__log__ = logger_config.Logger(logger)


def lambda_handler(event, context):
    """[lambda handler which is main entry point for execution]

    Args:
        event ([dict]): [incoming event by AWS]
        context ([dicr]): [lambda execution context]

    Returns:
        [proxy]: [proxified resopnse to API gateway]
    """
    event_context = __log__.__event__(event)
    body = ujson.loads(event['body']) if event['body'] else {}
    logger.debug(f'BODY_PAYLOAD {ujson.dumps(body)}')
    body.update(event_context)
    response, status_code = routes.handle_request(event, body)
    logger.info(f'SERVICE_EXIT {ujson.dumps(response)}')
    return generate_response.built_response(body=response, status_code=status_code)
