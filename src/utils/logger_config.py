# Standard library imports
import os
import sys
from distutils.util import strtobool

# Third party imports
import ujson
from pydash import py_


class Logger:
    """[Logger]
    """

    def __init__(self, logger) -> None:
        """[init]

        Args:
            logger ([logger]): [logging]
        """
        self.logger = logger
        logger.remove()
        logger.configure(
            handlers=[
                dict(sink=sys.stderr,
                    format='{time:X!UTC} | {level} | {extra[is_client_admin]} | {extra[is_customer_admin]} | {extra[client_id]} | {extra[customer_id]} | {extra[user_name]} | {module} | {function} | {message}')
            ],
            levels=[dict(name="DEBUG")],
        )

    def __event__(self, event):
        """[Perform parsing and logging event]

        Args:
            event ([dict]): [API Gateway event]

        Returns:
            [dict]: [body of the event for further use]
        """
        context = 'requestContext.authorizer.claims'

        is_client_admin = strtobool(
            py_.get(event, f'{context}.custom:isClientAdmin', 'False'))
        is_customer_admin = strtobool(
            py_.get(event, f'{context}.custom:isCustomerAdmin', 'False'))
        client_id = py_.get(event, f'{context}.custom:clientId', 'UNKNOWN')
        customer_id = py_.get(event, f'{context}.custom:customerId', 'UNKNOWN')
        user_name = py_.get(event, f'{context}.custom:userName', 'UNKNOWN')

        body = {'is_client_admin': is_client_admin,
                'is_customer_admin': is_customer_admin,
                'client_id': client_id,
                'customer_id': customer_id,
                'user_name': user_name}

        self.logger.configure(extra=body)
        self.logger.info(f'SERVICE_ENTER {ujson.dumps(event)}')

        body.update({'user_id': py_.get(event, f'{context}.sub', 'UNKNOWN')})

        return body
