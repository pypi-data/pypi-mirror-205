import json

from aws_lambda_mess.framework.failures import bad_request


def get_handler(routes):
    def lambda_handler(event, context):
        path = event.get("path", "/")
        method = event.get("httpMethod", "GET")
        body = json.loads(event.get("body", None) or "{}")

        for route in routes:
            match, params = route.match(method, path)
            if match:
                return route.run(params, body)

        return bad_request()
    return lambda_handler