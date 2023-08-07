def error(code):
    return {
        "isBase64Encoded": False,
        "statusCode": code,
    }


def not_found():
    return error(404)

def bad_request():
    return error(400)