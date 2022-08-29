from flask import request


def update_source(data: dict):  # sourcery skip: dict-assign-update-to-union
    source = {
        "code": 0,
        "msg": None
    }
    source.update(data)
    return source


def post_params(param):
    return request.json.get(param)


def get_params(param):
    return request.args.get(param)


def to_format(param):
    return f'mpt_{param.replace(":", "_")}'
